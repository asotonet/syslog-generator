# Usa una imagen base de Python
FROM python:3.9-slim

# Define directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de configuración y scripts
COPY app.py /app/
COPY requirements.txt /app/

# Instala dependencias
RUN pip install -r requirements.txt

# Ejecuta el script
CMD ["python", "app.py"]
