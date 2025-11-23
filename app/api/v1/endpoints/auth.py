from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token, get_password_hash
from app.core.deps import get_current_user
from app.schemas.user import (
    Token,
    TokenRefresh,
    LoginRequest,
    UserCreate,
    User as UserSchema,
    UserProfile,
    UserProfileUpdate,
    ChangePassword
)
from app.models.user import User

router = APIRouter()


@router.post("/register/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    # Verificar se o username já existe
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Verificar se o email já existe
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Criar novo usuário
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/token/", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username, "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"user_id": user.id, "username": user.username}
    )

    return {"access": access_token, "refresh": refresh_token}


@router.post("/token/refresh/", response_model=Token)
def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db),
):
    payload = decode_token(token_data.refresh)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username, "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"user_id": user.id, "username": user.username}
    )

    return {"access": access_token, "refresh": refresh_token}


@router.get("/user/", response_model=UserProfile)
def get_user_profile(
    current_user: User = Depends(get_current_user),
):
    """Obtém o perfil do usuário autenticado"""
    return current_user


@router.put("/user/", response_model=UserProfile)
def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Atualiza o perfil do usuário autenticado"""

    # Verificar se o username está sendo alterado e já existe
    if profile_data.username and profile_data.username != current_user.username:
        existing_user = db.query(User).filter(User.username == profile_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        current_user.username = profile_data.username

    # Verificar se o email está sendo alterado e já existe
    if profile_data.email and profile_data.email != current_user.email:
        existing_email = db.query(User).filter(User.email == profile_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        current_user.email = profile_data.email

    # Atualizar first_name e last_name
    if profile_data.first_name is not None:
        current_user.first_name = profile_data.first_name

    if profile_data.last_name is not None:
        current_user.last_name = profile_data.last_name

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/change-password/", status_code=status.HTTP_200_OK)
def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Altera a senha do usuário autenticado"""

    # Verificar senha atual
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    # Atualizar senha
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
