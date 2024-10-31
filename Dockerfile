# Usa una imagen base de Python
FROM python:3.9-slim

# Define directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de configuración y scripts
COPY app.py /app/
COPY requirements.txt /app/
# Copia el certificado de la CA en una ubicación estándar
COPY tls/ca_cert.pem /usr/local/share/ca-certificates/ca_cert.crt

# Instala dependencias
RUN pip install -r requirements.txt

# Añade el certificado de la CA al sistema de autoridades de confianza
#RUN apt-get update && \
#    apt-get install -y ca-certificates && \
#    update-ca-certificates


# Ejecuta el script
CMD ["python", "app.py"]
