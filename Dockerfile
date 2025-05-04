# Usa imagem oficial do Python
FROM python:3.11

# Define diretório padrão dentro do container
WORKDIR /app

# Instale dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie o código do backend para o contêiner
COPY . /app

# Configure o ambiente virtual e instale dependências
RUN python -m venv /env
RUN /env/bin/pip install --upgrade pip && \
    /env/bin/pip install -r requirements.txt

# Configure o PATH para usar o ambiente virtual por padrão
ENV PATH="/env/bin:$PATH"

# Exponha a porta do servidor
EXPOSE 8000

# Comando padrão para rodar o servidor
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]