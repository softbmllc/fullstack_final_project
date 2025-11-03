# Imagen base ligera con Python 3.10
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Carpeta de la app
WORKDIR /app

# Instalar dependencias
# (requirements.txt está dentro de server/, por eso lo copiamos así desde la raíz del repo)
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copiar el código Django (carpeta server/ del repo → /app)
COPY server/ /app/

# Opcional: colectar estáticos; si falla, que no rompa la build
RUN python manage.py collectstatic --noinput || true

# Exponer puerto 8080 (Code Engine espera 8080)
EXPOSE 8080

# Ejecutar con gunicorn (producción)
CMD ["gunicorn", "djangoproj.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3"]
