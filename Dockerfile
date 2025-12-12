# === Imagem base ===
FROM python:3.10-slim

# === Variáveis de ambiente ===
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# === Atualiza e instala dependências do sistema ===
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libgl1 \
        libglib2.0-0 \
        ffmpeg \
        wget \
        curl \
    && rm -rf /var/lib/apt/lists/*

# === Diretório de trabalho ===
WORKDIR /app

# === Instala dependências Python ===
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# === Copia o restante da aplicação ===
COPY . .

# === Expondo porta do FastAPI ===
EXPOSE 8000

# === Comando padrão para rodar a aplicação ===
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
