import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(5) # become a server socket, maximum 5 connections


def conversor_buffer(texto_coordenadas):

    coordenadas_separadas = texto_coordenadas.split(", ")

    coordenada_0 = coordenadas_separadas[0].split("[")
    coordenada_j1 = coordenada_0[1]

    coordenada_1 = coordenadas_separadas[1].split("]")
    coordenada_j2 = coordenada_1[0]

    coordenada_j1 = int(coordenada_j1)

    coordenada_j2 = int(coordenada_j2)


    return coordenada_j1, coordenada_j2


while True:

    connection, address = serversocket.accept()

    while True:
        buf = connection.recv(12)
        buf = str(buf)
        j1, j2 = conversor_buffer(buf)
        print(j1, j2)
        #print("Xa:", buf[0], "Xb:", buf[1])
        buf = 0