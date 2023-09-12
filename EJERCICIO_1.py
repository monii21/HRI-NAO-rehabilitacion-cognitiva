# -*- coding: utf-8 -*-
#1º EJERCICIO 

import socket
import sys
import time
import select
import argparse
import math
import time
import qi
from naoqi import ALProxy

MESSAGE='peticion'
FORMAT='utf-8'
IP_ROBOT="192.168.1.128"
PORT=9559

#Variables de los sonidos
SONIDO_PAJARO='pio pio pio pio'
SONIDO_PUERTA='toc toc toc toc'
SONIDO_PERRO='guau guau guau guau'
SONIDO_GATO='miau miau miau miau'
SONIDOS=[SONIDO_PAJARO,SONIDO_PUERTA,SONIDO_PERRO,SONIDO_GATO]

RESP_PAJARO='pájaro'
RESP_PUERTA='puerta'
RESP_PERRO='perro'
RESP_GATO='gato'
RESPUESTAS=[RESP_PAJARO,RESP_PUERTA,RESP_PERRO,RESP_GATO]

#Variables globales
acierto=False
error=0
n=0

def comp_respuesta(respuesta,tts,sock,animation_player):
    global acierto
    global error
    global n

    while (acierto==False and error<1):
        if(respuesta == RESPUESTAS[n]) : 
            acierto = True
            future = animation_player.run("animations/Stand/Gestures/Enthusiastic_5", _async=True)
            tts.say("\\emph=2\\ Muy bien!!!! Has acertado.")
        else:
            if(error <= 2): #hay tres oportunidades
                tts.say("Parece que la respuesta no es correcta. Probamos de nuevo?")
                tts.say(SONIDOS[n])
                sock.send(MESSAGE.encode(FORMAT))
                respuesta=sock.recv(1024)
                error = error + 1
        
    if(error == 1): #ya ha agotado las oportunidades
        tts.say("Parece que la respuesta no es correcta, pero has estado a punto de conseguirlo. \\pau=500\\ Vamos a por el siguiente sonido!")

    #en cualquier caso cuando sale del while debemos volver a inicializar acierto y error y aumentar la n
    acierto = False
    error = 0
    n = n + 1   


def main (RobotIP, Port,session,sock):
    global n
    tts = ALProxy("ALTextToSpeech",RobotIP,Port)
    motionProxy  = ALProxy("ALMotion", RobotIP, Port)
    postureProxy = ALProxy("ALRobotPosture", RobotIP,Port)
    animation_player = session.service("ALAnimationPlayer")
    tts.setVolume(1.2)

    motionProxy.setStiffnesses("Head", 1.0)

    fractionMaxSpeed = 0.1
	#Wake up robot
    motionProxy.wakeUp()

	# Send robot to Stand Init
    postureProxy.goToPosture("StandInit", 0.5)

    tts.say("Hola, soy Nao.")
    
    animation_player.run("animations/Stand/Gestures/Hey_3")

    future = animation_player.run("animations/Stand/Gestures/Explain_10", _async=True)
    tts.say("Vamos a empezar con la sesion de hoy. Primero me gustaria saber cual es tu nombre.")
    
    
    sock.send(MESSAGE.encode(FORMAT))
    name=sock.recv(1024)

    tts.say("Hola " + name)

    animation_player.run("animations/Stand/Gestures/BowShort_1")
    tts.say("A continuacion voy a reproducir un sonido y debes intentar reconocer a cual de las opciones pertenece.")


    while(n < len(SONIDOS)): #para hacerlo para todos los sonidos
        
        future = animation_player.run("animations/Stand/Gestures/IDontKnow_1", _async=True)
        tts.say("Estas preparado? Alla vamos!")
        
        tts.say(SONIDOS[n])
        tts.say("El sonido que acabas de escuchar es alguna de las siguientes opciones.\\pau=1000\\" + RESPUESTAS[3]+"\\pau=250\\" + RESPUESTAS[1]+"\\pau=250\\" + RESPUESTAS[0]+"\\pau=250\\" + "o" + RESPUESTAS[2])
        
        future = animation_player.run("animations/Stand/Gestures/IDontKnow_1", _async=True)
        tts.say("Podrias decirme cual es?")
        
        sock.send(MESSAGE.encode(FORMAT))
        respuesta=sock.recv(1024)
        print(respuesta)
        comp_respuesta(respuesta,tts,sock,animation_player)
    
    tts.say("Lo haz hecho muy bien.\\pause=250\\ Hasta luego")

    

if __name__ == '__main__':

    #conectamos el socket al mismo puerto donde el servidor esta escuchando
    sock=socket.socket()
    server_address=('localhost', 10000)
    sock.connect(server_address)
    session = qi.Session()
    time.sleep(2)
    
    try: 
        session.connect("tcp://" + IP_ROBOT + ":" + str(PORT))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + IP_ROBOT + "\" on port " + str(PORT) +".\n"
        "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    main(IP_ROBOT,PORT,session,sock)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

