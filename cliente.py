import socket
import ssl
from funciones import *

server_address = ('localhost', 20037)

# Crear un socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect(server_address)

# Configurar un contexto SSL en el cliente
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

ssl_context.check_hostname = True
#supuestamente la siguiente configuracion ya se hace al hacer ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
#al usar ssl.Purpose.SERVER_AUTH ya queda establecida dicha configuracion
ssl_context.verify_mode = ssl.CERT_REQUIRED

ssl_context.load_verify_locations("root.crt")  # El certificado del servidor


# si ssl_context.check_hostname = True entonces tenemos que indicar cual es la direccion del server... es este caso es localhost
ssl_client_socket = ssl_context.wrap_socket(client_socket, server_hostname="localhost")

data = "".encode("utf-8")
try:
    while True:
        # Enviar datos al servidor
        message = input("Tú dices: ")
        enviar_mensaje(ssl_client_socket, message)


        while True:
            data = data + ssl_client_socket.recv(1024)
            mensaje_server, resto_mensaje = extraer_hasta_guion(data)
            if mensaje_server is not None:
                data = resto_mensaje
                print(f"Cliente dice: {mensaje_server}")
                break


except Exception as e:
    pass
finally:
    # Cerrar la conexión SSL
    ssl_client_socket.close()

