# -*- coding: utf-8 -*-
#2º EJERCICIO: preguntas generales

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

#Variables para las preguntas
DIA_SEMANA ='miércoles'      #que dia de la semana es hoy: LUNES
MES_ANO ='diciembre'     #en que mes del año estamos: DICIEMBRE
MANZANA = 'fruta'        #la manzana es una: FRUTA
LECHE = 'blanco'         #la leche es de color: BLANCO
INVIERNO = 'invierno'    #despues del otoño viene el: INVIERNO
FALLA = 'valencia'        #las fallas se celebran en: VALENCIA
RESPUESTAS = [DIA_SEMANA, MES_ANO, MANZANA, LECHE, INVIERNO, FALLA]


PREG_DIA = 'que dia de la semana es hoy?'
PREG_MES = 'en que mes del año estamos?'
PREG_MANZANA = 'que es la manzana?'
PREG_LECHE = 'el color de la leche es?'
PREG_INVIERNO = 'despues de la estacion del otoño viene el?'
PREG_FALLA = 'las fallas se celebran en la ciudad de?'
PREGUNTAS = [PREG_DIA, PREG_MES, PREG_MANZANA, PREG_LECHE, PREG_INVIERNO, PREG_FALLA]

#Variable global
acierto=False
error=0
n=0

def comp_respuesta(respuesta,tts,sock,animation_player):
    global acierto
    global error
    global n

    while (acierto == False and error < 1):
        if(respuesta == RESPUESTAS[n]) : 
            acierto = True
            future = animation_player.run("animations/Stand/Gestures/Enthusiastic_5", _async=True)
            tts.say("\\emph=2\\ Muy bien! Has acertado.")
        else:
            if(error <= 2): #hay dos oportunidades
                tts.say("Parece que la respuesta no es correcta. Probamos de nuevo?")
                tts.say(PREGUNTAS[n]+ "\\pause=250\\")
                sock.send(MESSAGE.encode(FORMAT))
                respuesta=sock.recv(1024)
                error = error + 1
        
    if(error == 1): #ya ha agotado las oportunidades
        tts.say("Parece que la respuesta no es correcta, pero has estado a punto de conseguirlo. \\pau=500\\ Vamos a por la siguiente pregunta!")

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
    tts.say("A continuacion voy a hacerte unas preguntas y debes intentar responderlas.")


    while(n < len(PREGUNTAS)): #para hacerlo para todos los sonidos
        
        future = animation_player.run("animations/Stand/Gestures/IDontKnow_1", _async=True)
        tts.say("Estas preparado? Alla vamos!")
        
        tts.say(PREGUNTAS[n])
        
        future = animation_player.run("animations/Stand/Gestures/IDontKnow_1", _async=True)
        tts.say("Podrias decirme cual es la respuesta?")
        
        sock.send(MESSAGE.encode(FORMAT))
        respuesta=sock.recv(1024)

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
