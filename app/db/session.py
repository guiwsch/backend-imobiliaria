from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Configuração do engine com pool de conexões otimizado para produção
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    pool_size=5,  # Número de conexões no pool
    max_overflow=10,  # Conexões extras permitidas
    pool_recycle=3600,  # Recicla conexões a cada hora
    echo=False  # Não loga SQL em produção
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()
