from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token, get_password_hash
from app.schemas.user import Token, TokenRefresh, LoginRequest, UserCreate, User as UserSchema
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
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
    try:
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
    except SQLAlchemyError as e:
        logger.error(f"Database error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error",
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


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
