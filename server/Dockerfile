# Imagen base ligera con Python 3.10
FROM python:3.10-slim

# Evitar archivos .pyc y usar stdout sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Carpeta de trabajo dentro de la imagen
WORKDIR /app

# Instalar dependencias (el requirements.txt está dentro de server/)
COPY server/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copiar el código Django (carpeta server/ → /app)
COPY server/ /app/

# Colectar estáticos (si falla, no romper la build)
RUN python manage.py collectstatic --noinput || true

# Exponer puerto (Code Engine escucha 8080)
EXPOSE 8080

# Arranque: ejecutar migraciones y luego Gunicorn
CMD ["sh","-c","python manage.py migrate --noinput && gunicorn djangoproj.wsgi:application --bind 0.0.0.0:${PORT} --workers 3"]
