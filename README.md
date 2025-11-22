# Imobiliária API - Backend

Backend desenvolvido em Python com FastAPI para sistema de gerenciamento imobiliário.

## Tecnologias

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Pydantic

## Estrutura do Projeto

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # Autenticação JWT
│   │       │   ├── imoveis.py       # CRUD de imóveis
│   │       │   ├── leads.py         # Gerenciamento de leads
│   │       │   └── admin.py         # Endpoints admin
│   │       └── router.py
│   ├── core/
│   │   ├── config.py                # Configurações
│   │   ├── security.py              # JWT e hash de senha
│   │   └── deps.py                  # Dependências (auth)
│   ├── db/
│   │   └── session.py               # Sessão do banco
│   ├── models/                      # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── imovel.py
│   │   ├── lead.py
│   │   ├── visita.py
│   │   └── configuracao.py
│   └── schemas/                     # Schemas Pydantic
│       ├── user.py
│       ├── imovel.py
│       ├── lead.py
│       ├── visita.py
│       └── configuracao.py
├── main.py                          # Aplicação principal
├── init_db.py                       # Script de inicialização
├── create_user.py                   # Script para criar usuário
└── requirements.txt
```

## Configuração

### 1. Criar ambiente virtual

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as configurações:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/imobiliaria_db
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
UPLOAD_DIR=uploads
```

### 4. Criar banco de dados PostgreSQL

```bash
# Entre no PostgreSQL
psql -U postgres

# Crie o banco de dados
CREATE DATABASE imobiliaria_db;

# Crie um usuário (opcional)
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE imobiliaria_db TO seu_usuario;
```

### 5. Inicializar banco de dados

```bash
python init_db.py
```

### 6. Criar usuário admin

```bash
python create_user.py
```

Credenciais padrão:
- Username: `admin`
- Password: `admin123`
- Email: `admin@imobiliaria.com`

**IMPORTANTE:** Altere a senha após o primeiro login!

## Executar o servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## Endpoints da API

### Autenticação

- `POST /api/token/` - Login (retorna access e refresh tokens)
- `POST /api/token/refresh/` - Refresh token

### Imóveis (Públicos)

- `GET /api/imoveis/` - Listar imóveis (com filtros e paginação)
- `GET /api/imoveis/destaques/` - Listar imóveis em destaque
- `GET /api/imoveis/{id}/` - Detalhes de um imóvel

### Imóveis (Protegidos - requer autenticação)

- `POST /api/imoveis/` - Criar imóvel
- `PUT /api/imoveis/{id}/` - Atualizar imóvel
- `DELETE /api/imoveis/{id}/` - Deletar imóvel
- `POST /api/imoveis/{id}/upload_imagem/` - Upload de imagem

### Leads

- `POST /api/leads/contatos/` - Criar lead/contato (público)
- `GET /api/leads/` - Listar leads (protegido)
- `GET /api/leads/{id}/` - Detalhes do lead (protegido)
- `PUT /api/leads/{id}/` - Atualizar lead (protegido)
- `DELETE /api/leads/{id}/` - Deletar lead (protegido)

### Admin (todos protegidos)

- `GET /api/admin/stats/` - Estatísticas do dashboard
- `GET /api/admin/visitas/` - Listar visitas
- `POST /api/admin/visitas/` - Criar visita
- `PUT /api/admin/visitas/{id}/` - Atualizar visita
- `DELETE /api/admin/visitas/{id}/` - Deletar visita
- `GET /api/admin/configuracoes/` - Obter configurações
- `PUT /api/admin/configuracoes/` - Atualizar configurações

## Filtros de Imóveis

A API suporta os seguintes filtros na rota `GET /api/imoveis/`:

- `tipo_negocio` - venda ou aluguel
- `tipo_imovel` - casa, apartamento, terreno, comercial
- `cidade` - nome da cidade
- `bairro` - nome do bairro
- `preco_venda__gte` - preço mínimo
- `preco_venda__lte` - preço máximo
- `area_total__gte` - área mínima
- `area_total__lte` - área máxima
- `quartos` - quantidade mínima de quartos
- `banheiros` - quantidade mínima de banheiros
- `vagas_garagem` - quantidade mínima de vagas
- `piscina` - true/false
- `aceita_pets` - true/false
- `mobiliado` - true/false
- `search` - busca textual (título, descrição, cidade, bairro)
- `ordering` - campo para ordenação (ex: -criado_em)
- `page` - número da página
- `limit` - itens por página

## Autenticação

A API usa JWT (JSON Web Tokens) para autenticação. Para acessar rotas protegidas:

1. Faça login em `/api/token/` com username e password
2. Receba `access` e `refresh` tokens
3. Inclua o token de acesso no header: `Authorization: Bearer {access_token}`
4. Quando o token expirar, use `/api/token/refresh/` com o refresh token

## Integração com Frontend

O frontend React (localhost:5173) está pré-configurado no CORS. A API aceita requisições de:

- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Create React App)

## Desenvolvimento

Para desenvolvimento, recomenda-se:

1. Manter o servidor rodando com `--reload` para auto-reload
2. Acessar `/docs` para testar endpoints
3. Verificar logs no terminal
4. Usar ferramentas como Postman ou Insomnia para testes

## Troubleshooting

### Erro de conexão com o banco

- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Teste a conexão: `psql -U seu_usuario -d imobiliaria_db`

### Erro de importação

- Certifique-se de estar no ambiente virtual ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### Erro de permissão em uploads

- Crie o diretório: `mkdir uploads`
- Ajuste permissões: `chmod 755 uploads`

## Próximos Passos

- [ ] Implementar testes unitários
- [ ] Adicionar validação de CEP
- [ ] Integrar envio de emails
- [ ] Adicionar log de auditoria
- [ ] Implementar soft delete
- [ ] Adicionar compressão de imagens
- [ ] Criar endpoints para relatórios

## Suporte

Para dúvidas ou problemas, consulte a documentação do FastAPI: https://fastapi.tiangolo.com/
