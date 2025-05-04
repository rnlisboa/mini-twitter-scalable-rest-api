# Usa imagem oficial do Python
FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app


RUN python -m venv /env
RUN /env/bin/pip install --upgrade pip && \
    /env/bin/pip install -r requirements.txt

ENV PATH="/env/bin:$PATH"

EXPOSE 8000

# Comando padrão para rodar o servidor
CMD ["sh", "-c", "python manage.py migrate && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]
