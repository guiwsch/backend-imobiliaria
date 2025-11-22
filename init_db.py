"""
Script para inicializar o banco de dados
Usage: python init_db.py
"""
from app.db.session import engine, Base
from app.models import User, Imovel, ImovelImagem, Lead, Visita, Configuracao


def init_database():
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
    print("\nTabelas criadas:")
    print("- users")
    print("- imoveis")
    print("- imovel_imagens")
    print("- leads")
    print("- visitas")
    print("- configuracoes")
    print("\nAgora execute: python create_user.py para criar um usuário admin")


if __name__ == "__main__":
    init_database()
