FROM python:3.11-slim

WORKDIR /app

# Instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo tu código al contenedor
COPY . .

# Expone el puerto (por si Fly lo necesita)
EXPOSE 8080

# Usa Gunicorn para servir Flask en producción
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
