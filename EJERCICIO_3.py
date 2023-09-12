# -*- coding: utf-8 -*-

#3º EJERCICIO: recordar el máximo de palabras

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
GRUPO1 =['arena' , 'pollo' , 'azul', 'pueblo']
GRUPO2 =['libro' , 'silla' , 'plaza', 'receta']
GRUPO3 =['precio' , 'lazo' , 'teatro', 'fresa']
RESPUESTAS = [GRUPO1,GRUPO2,GRUPO3]

#Variable global
acierto=False
n=0         #contador para movernos por RESPUESTAS
cont=0      #contador para ver cuantas palabras ha dicho el usuario

def comp_respuesta(respuesta,tts,animation_player):
    global acierto
    for i in range(len(RESPUESTAS[n])): #recorremos el grupo 1 para comprobar si la palabra que ha dicho esta ahi dentro
        if(respuesta == RESPUESTAS[n][i]) : #si está ponemos a true acierto
            if i == len(RESPUESTAS[n]):
                future = animation_player.run("animations/Stand/Gestures/Enthusiastic_5", _async=True)
                tts.say("\\emph=2\\ Muy bien! Has acertado.")
            else:
                future = animation_player.run("animations/Stand/Gestures/Enthusiastic_5", _async=True)
                tts.say("\\emph=2\\Muy bien! Has acertado.Recuerdas alguna otra palabra?")
            acierto=True
    
    if(acierto==False): #no ha acertado, esa palabra no está dentro del grupo RESPUESTAS[n]
        tts.say("Parece que esa respuesta no es ninguna de las palabras anteriores! Probamos con otra palabra?")

    
    

def main (RobotIP, Port,session,sock):
    global n
    global cont
    global acierto
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
    tts.say("A continuacion voy a decir un conjunto de palabras seguidas y debes intentar recordar el maximo numero de palabras.")


    while( n < len(RESPUESTAS)): #para hacerlo para todos los sonidos
        
        future = animation_player.run("animations/Stand/Gestures/IDontKnow_1", _async=True)
        tts.say("Estas preparado? Alla vamos!")
        
        for i in range(len(RESPUESTAS[n])): 
            tts.say(RESPUESTAS[n][i]+ "\\pau=250\\")
        
        future = animation_player.run("animations/Stand/Gestures/IDontKnow_1", _async=True)
        tts.say("Podrias decirme que palabra recuerdas")
        
        while (cont < len(RESPUESTAS[n])): #se le dan tantas oportunidades al usuario como palabras tenga el grupo RESPUESTAS[n]
            sock.send(MESSAGE.encode(FORMAT))
            respuesta=sock.recv(1024)

            cont = cont + 1
            acierto = False
            comp_respuesta(respuesta,tts,animation_player)
        
        #ya ha dicho 4 palabras el usuario 
        tts.say("Ya has probado con todas las palabras, vamos a probar ahora con otro conjunto nuevo de palabras!")
        n = n + 1  #aumentamos el contador de los grupos  
        cont = 0   #reestablecemos el contador de las palabras

    #ya ha finalizado el numero de grupos de palabras, por lo que nos despedimos

    tts.say("Ya has realizado el ejercicio con todos los grupos de palabras!\\pause=500\\ Lo has hecho genial!")


    

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
