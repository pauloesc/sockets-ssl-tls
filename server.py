import socket
import ssl
import sys
from funciones import *


# Configuración del servidor
server_address = ('localhost', 20037)

# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al servidor
server_socket.bind(server_address)

# Escuchar conexiones entrantes
server_socket.listen(1)
print("Esperando conexiones")


# Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conexión establecida desde {client_address}")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.verify_mode = ssl.CERT_NONE

#certfile="server_cert.pem": Especifica el archivo que contiene el certificado del servidor.
#Este certificado es utilizado para autenticar al servidor ante el cliente.
#keyfile="server_key.pem": Especifica el archivo que contiene la clave privada correspondiente al certificado del servidor.
#La clave privada se utiliza para firmar los mensajes y establecer la conexión segura.
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")


#La línea de código siguente se utiliza para envolver un socket existente en un nuevo socket seguro utilizando el contexto SSL proporcionado (ssl_context).
#Aquí hay una explicación más detallada:
#ssl_context: Es un objeto que representa la configuración y las opciones de seguridad para una conexión segura utilizando SSL/TLS.
#wrap_socket: Es un método de la clase SSLContext que se utiliza para crear un nuevo objeto de socket seguro.
#client_socket: Es el socket existente que se desea asegurar. Este socket puede ser, por ejemplo, un socket creado previamente para manejar la conexión con un cliente.
#server_side=True: Indica que este socket se utilizará en el lado del servidor de la conexión segura. En otras palabras, se está estableciendo una conexión segura desde el servidor hacia el cliente.
try:
    ssl_client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
except Exception as e:
    print(f"Error 1: {e}")
    server_socket.close()
    sys.exit()


data = "".encode("utf-8")
try:
    while True:

        #lo siguiente simula un do-while
        while True:
            data = data + ssl_client_socket.recv(1024)
            mensaje_cliente, resto_mensaje = extraer_hasta_guion(data)
            if mensaje_cliente is not None:
                data = resto_mensaje
                print(f"Cliente dice: {mensaje_cliente}")
                break

        # Enviar datos al cliente
        message = input("Tú dices: ")
        enviar_mensaje(ssl_client_socket, message)

except Exception as e:
    print(f"Error 2: {e}")
finally:
    # Cerrar la conexión SSL
    ssl_client_socket.close()
    # Cerrar el socket del servidor
    server_socket.close()
    sys.exit()

