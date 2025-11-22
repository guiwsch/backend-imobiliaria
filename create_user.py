"""
Script para criar um usuário admin inicial
Usage: python create_user.py
"""
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def create_admin_user():
    db = SessionLocal()

    # Verifica se já existe um usuário
    existing_user = db.query(User).filter(User.username == "admin").first()

    if existing_user:
        print("Usuário 'admin' já existe!")
        return

    # Cria novo usuário
    admin_user = User(
        username="admin",
        email="admin@imobiliaria.com",
        hashed_password=get_password_hash("admin123"),
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print(f"Usuário criado com sucesso!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print(f"Email: admin@imobiliaria.com")
    print("\nIMPORTANTE: Altere a senha após o primeiro login!")

    db.close()


if __name__ == "__main__":
    create_admin_user()
