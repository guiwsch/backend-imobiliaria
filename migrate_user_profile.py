"""
Migration script para adicionar colunas first_name e last_name na tabela users
"""
import sys
import os

# Adicionar o diretório do backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from sqlalchemy import text

def run_migration():
    print("Iniciando migration para adicionar first_name e last_name...")

    with engine.connect() as conn:
        # Verificar se as colunas já existem
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users'"))
        columns = [row[0] for row in result]
        print(f'Colunas existentes: {columns}')

        if 'first_name' not in columns:
            print('Adicionando coluna first_name...')
            conn.execute(text('ALTER TABLE users ADD COLUMN first_name VARCHAR'))
            conn.commit()
            print('✓ Coluna first_name adicionada')
        else:
            print('✓ Coluna first_name já existe')

        if 'last_name' not in columns:
            print('Adicionando coluna last_name...')
            conn.execute(text('ALTER TABLE users ADD COLUMN last_name VARCHAR'))
            conn.commit()
            print('✓ Coluna last_name adicionada')
        else:
            print('✓ Coluna last_name já existe')

        print('\n✅ Migration concluída com sucesso!')

if __name__ == "__main__":
    run_migration()
