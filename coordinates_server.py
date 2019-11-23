#https://towardsdatascience.com/automatic-vision-object-tracking-347af1cc8a3b

from __future__ import print_function
from imutils.video import VideoStream
import imutils
import time
import cv2
import os
import numpy as np
import socket


######################################################################
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))
######################################################################

#Coletos os limites hsv da cor que for clicada com o mouse
def retorna_hsv():

    lista_rgb = []
    hsv_superior = []
    hsv_inferior = []

    def mouseRGB(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition

            colorsB = frame[y,x,0]
            colorsG = frame[y,x,1]
            colorsR = frame[y,x,2]

            lista_rgb.append(colorsR)
            lista_rgb.append(colorsG)
            lista_rgb.append(colorsB)

    def rgb_2_hsv(lista_rgb):
        blue = lista_rgb[0]
        green = lista_rgb[1]
        red = lista_rgb[2]

        color = np.uint8([[[red, green, blue]]])
        hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

        hue = hsv_color[0][0][0]

        return hue

    cv2.namedWindow('mouseRGB')
    cv2.setMouseCallback('mouseRGB',mouseRGB)

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while(True):

        ret, frame = capture.read()
        frame = imutils.resize(frame, width=1150) 
        cv2.imshow('mouseRGB', frame)

        if cv2.waitKey(1) == 27:
            break

        if len(lista_rgb)>2:

            hsv_inferior.append(int((rgb_2_hsv(lista_rgb)-5))) #sensibilidade da detecção da cor
            hsv_inferior.append((100))
            hsv_inferior.append((100))

            hsv_superior.append(int((rgb_2_hsv(lista_rgb)+5))) #sensibilidade da detecção da cor
            hsv_superior.append(255)
            hsv_superior.append(255)

            hsv_inferior = tuple(hsv_inferior)
            hsv_superior = tuple(hsv_superior)

            return hsv_inferior, hsv_superior

#coleta os limites hsv para duas cores
m1Lower, m1Upper = retorna_hsv()
m2Lower, m2Upper = retorna_hsv()

cv2.destroyAllWindows()

# initialize the video stream and allow the camera sensor to warmup
print("Acessando a webcam...")
vs = VideoStream(0).start()
time.sleep(2.0)

frame = vs.read()

#informa as coordenadas x e y, bem como o raio de um circulo de cores com limites hsv informados
def info_marcador(vs, frame, colorLower, colorUpper, raio):

     #frame = imutils.rotate(frame, angle=180)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the object color, then perform a series of dilations and erosions to remove any small blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    #cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if (radius > raio):

            return int(x), int(y), int(radius), center

    return 0, 0, 0, (0,0)

def desenha_circulos(frame, x, y, radius, center):
    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    cv2.circle(frame, center, 5, (0, 0, 255), -1)


def captura_raio():

    lista_r = []
    ultimos_r = []
    #retém a média do raio do primeriro circulo marcado
    while True:

        frame = vs.read()
        frame = imutils.resize(frame, width=1150)
        key = cv2.waitKey(1) & 0xFF

        xA, yA, rA, cA = info_marcador(vs, frame, m1Lower, m1Upper, 0)
        lista_r.append(rA)

        desenha_circulos(frame, xA, yA, rA, cA)

        cv2.imshow("Frame", frame)

        if key == 27:
            print(lista_r)
            ultimos_r = lista_r[-9:]
            raio_marcador = int(np.mean(ultimos_r))
            break

    return raio_marcador

raio_marcador = captura_raio()

def rastreia_circulo(m1Lower, m1Upper, m2Lower, m2Upper, raio_marcador):
    #rastreia dois círculos com cores e raios definidos
    while True:

        # grab the next frame from the video stream, Invert 180o, resize the frame, and convert it to the HSV color space
        frame = vs.read()
        frame = imutils.resize(frame, width=1150)

        key = cv2.waitKey(1) & 0xFF

        xA, yA, rA, cA = info_marcador(vs, frame, m1Lower, m1Upper, (raio_marcador-10))
        xZ, yZ, rZ, zA = info_marcador(vs, frame, m2Lower, m2Upper, (raio_marcador-10))

        desenha_circulos(frame, xA, yA, rA, cA)
        desenha_circulos(frame, xZ, yZ, rZ, zA)

        print("X1:", xA, " X2:", xZ)

        cv2.imshow("Frame", frame)

        return xA, xZ

        if key == 27:
            break

        cv2.destroyAllWindows()


while True:

    xa, xz= rastreia_circulo(m1Lower, m1Upper, m2Lower, m2Upper, raio_marcador)

    xa = int(xa)
    xz = int(xz)

    lista_coordenadas =[xa, xz]

    coordenadas_texto = str(lista_coordenadas)

    clientsocket.send(coordenadas_texto.encode())
