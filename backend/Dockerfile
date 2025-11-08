# ========= Stage 1: Build =========
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

# ========= Stage 2: Runtime =========
FROM python:3.11-slim

WORKDIR /app

# Runtime dependency for some image operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy installed dependencies before code
COPY --from=builder /install /usr/local

# ✅ Copy application code once
COPY --from=builder /app /app

# ✅ Allow SQLite DB to be created
RUN chmod -R 777 /app

# Create non-root user (only once)
RUN useradd -m appuser
USER appuser

ENV PORT=8000 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
