# Dockerfile para Backend FastAPI
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . .

# Cria diretório de uploads
RUN mkdir -p uploads

# Expõe a porta (Railway usa a variável PORT)
EXPOSE 8080

# Comando para iniciar a aplicação
# Railway fornece a variável PORT automaticamente
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
