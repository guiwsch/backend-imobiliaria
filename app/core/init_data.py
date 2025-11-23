"""
Módulo para inicializar dados básicos no banco de dados
Executado automaticamente na inicialização do app
"""
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)


def init_admin_user():
    """
    Cria usuário admin inicial se não existir
    """
    db = SessionLocal()
    try:
        # Verifica se já existe um usuário admin
        existing_user = db.query(User).filter(User.username == "admin").first()

        if existing_user:
            logger.info("Admin user already exists")
            return

        # Cria novo usuário admin
        admin_user = User(
            username="admin",
            email="admin@imobiliaria.com",
            hashed_password=get_password_hash("admin123")
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        logger.info("=" * 60)
        logger.info("Admin user created successfully!")
        logger.info(f"Username: admin")
        logger.info(f"Password: admin123")
        logger.info(f"Email: admin@imobiliaria.com")
        logger.info("IMPORTANT: Change password after first login!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()


def initialize_database():
    """
    Inicializa dados básicos do banco de dados
    """
    logger.info("Initializing database with basic data...")
    init_admin_user()
    logger.info("Database initialization complete")
