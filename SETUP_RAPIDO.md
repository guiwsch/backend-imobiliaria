# Setup Rápido - Backend Imobiliária

## Passo a Passo

### 1. Instalar PostgreSQL (se não tiver)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Baixe em: https://www.postgresql.org/download/windows/
```

### 2. Configurar PostgreSQL

```bash
# Iniciar serviço
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS

# Acessar PostgreSQL
sudo -u postgres psql

# Dentro do psql, execute:
CREATE DATABASE imobiliaria_db;
CREATE USER imob_user WITH PASSWORD 'imob_senha123';
GRANT ALL PRIVILEGES ON DATABASE imobiliaria_db TO imob_user;
\q
```

### 3. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
```

### 4. Editar arquivo .env

Abra o arquivo `.env` e configure:

```env
DATABASE_URL=postgresql://imob_user:imob_senha123@localhost:5432/imobiliaria_db
SECRET_KEY=mude-esta-chave-para-algo-super-secreto-e-aleatorio-123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
UPLOAD_DIR=uploads
```

**IMPORTANTE:** Gere uma SECRET_KEY segura:

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Ou online em: https://djecrety.ir/
```

### 5. Inicializar Banco de Dados

```bash
# Criar tabelas
python init_db.py

# Criar usuário admin
python create_user.py
```

Credenciais padrão:
- **Username:** admin
- **Password:** admin123

### 6. Rodar o Servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Testar a API

Abra no navegador:
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

### 8. Testar Login

No Swagger UI (http://localhost:8000/docs):

1. Clique em `POST /api/token/`
2. Clique em "Try it out"
3. Preencha:
   - **username:** admin
   - **password:** admin123
4. Execute
5. Copie o `access` token
6. Clique em "Authorize" (cadeado no topo)
7. Cole o token e clique em "Authorize"

Agora você pode testar todas as rotas protegidas!

## Comandos Úteis

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Rodar servidor
uvicorn main:app --reload

# Rodar servidor em outra porta
uvicorn main:app --reload --port 8080

# Ver logs detalhados
uvicorn main:app --reload --log-level debug

# Resetar banco de dados
python init_db.py

# Criar novo usuário
python create_user.py
```

## Integração com Frontend

O frontend já está configurado para se conectar em `http://localhost:8000`.

Certifique-se de que o backend está rodando antes de iniciar o frontend:

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Troubleshooting

### Erro: "could not connect to server"

PostgreSQL não está rodando:
```bash
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS
```

### Erro: "password authentication failed"

Verifique as credenciais no arquivo `.env`

### Erro: "No module named 'app'"

Certifique-se de estar no diretório `backend/` e com o ambiente virtual ativado

### Erro: "Upload directory not found"

```bash
mkdir uploads
chmod 755 uploads
```

### Porta 8000 já em uso

```bash
# Encontre o processo
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Ou use outra porta
uvicorn main:app --reload --port 8001
```

## Próximos Passos

1. ✅ Backend rodando
2. ✅ Banco de dados configurado
3. ✅ Usuário admin criado
4. ⬜ Iniciar frontend
5. ⬜ Fazer login no sistema
6. ⬜ Cadastrar imóveis
7. ⬜ Testar funcionalidades

## Suporte

Documentação FastAPI: https://fastapi.tiangolo.com/
Documentação SQLAlchemy: https://docs.sqlalchemy.org/
