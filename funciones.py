def enviar_mensaje(socket, message):
    bytes_enviados = 0
    mensaje_codificado = message.encode('utf-8')
    while bytes_enviados < len(mensaje_codificado):
        parte_del_mensaje_a_enviar = mensaje_codificado[bytes_enviados:]
        bytes_enviados += socket.send(parte_del_mensaje_a_enviar)


def extraer_hasta_guion(cadena):

    #
    # es importante saber que len( '-'.encode("utf-8") ) es 1
    #

    indice = cadena.find('-'.encode("utf-8"))
    if indice != -1:
        try:
            caracteres_hasta_guion = cadena[:indice].decode("utf-8")
            cadena = cadena[indice + 1:]
        except Exception as e:
            print(f"Error: {e}")
            caracteres_hasta_guion = ""
            cadena = "".encode("utf-8")
    else:
        # Si no se encuentra un '-'
        caracteres_hasta_guion = None

    return caracteres_hasta_guion, cadena
