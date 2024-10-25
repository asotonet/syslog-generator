import logging
import random
import time
import os
import ssl
import socket

# Configuración de la conexión TLS
splunk_ip = os.getenv("SPLUNK_IP", "127.0.0.1")
splunk_port = int(os.getenv("SPLUNK_PORT", 6514))

# Rutas de los certificados y clave privada TLS
cert_path = os.getenv("TLS_CERT_PATH", "/app/tls/splunk_cert.pem")
key_path = os.getenv("TLS_KEY_PATH", "/app/tls/splunk_key.pem")
ca_cert_path = os.getenv("CA_CERT_PATH", "/app/tls/ca_cert.pem")

# Configuración del contexto SSL
tls_context = ssl.create_default_context(cafile=ca_cert_path)
tls_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

# Configuración del logger
logger = logging.getLogger('RandomLogGenerator')
logger.setLevel(logging.INFO)

# Configuración del socket para enviar logs de syslog sobre TLS
def send_syslog(message):
    with socket.create_connection((splunk_ip, splunk_port)) as sock:
        with tls_context.wrap_socket(sock, server_hostname=splunk_ip) as ssock:
            ssock.sendall(message.encode('utf-8'))

# Función para generar y enviar un log aleatorio
def generate_random_log():
    niveles = [logging.INFO, logging.WARNING, logging.ERROR, logging.DEBUG]
    mensajes = [
        "Proceso completado correctamente.",
        "Advertencia: recurso bajo.",
        "Error crítico en el sistema.",
        "Depuración en progreso."
    ]
    nivel = random.choice(niveles)
    mensaje = random.choice(mensajes)
    log_message = f"{nivel} - {mensaje}"
    send_syslog(log_message)

# Genera logs de forma indefinida cada pocos segundos
try:
    while True:
        generate_random_log()
        time.sleep(random.uniform(1, 5))  # Genera log en un intervalo aleatorio entre 1 y 5 segundos
except KeyboardInterrupt:
    print("Generación de logs detenida.")
