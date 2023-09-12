# -*- coding: utf-8 -*-
from vosk import Model, KaldiRecognizer
import pyaudio
import socket
import sys
import select
import time



if __name__ == '__main__':
    #lineas correspondientes a TCP/IP
    
    #creamos el TCP/IP socket
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Asignamos el socket al puerto
    server_address=('localhost', 10000)
    sock.bind(server_address)

    #escuchamos las conexiones entrantes
    sock.listen(5)

    #lineas correspondientes a escuchar el microfono
    model=Model('/home/marina/Desktop/SERVICIOS/es') #leemos el modelo
    recognizer=KaldiRecognizer(model, 16000)

    #Reconocer el audio del microfono
    cap= pyaudio.PyAudio() #para capturar el microfono
    stream=cap.open(format=pyaudio.paInt16, channels=1, rate=16000,input=True, frames_per_buffer=8192)
    
    #variables
    cont = 0
    cad  = False
    msg = ''

    

    while True:
        print("Esperando a la conexión")
        
        connection, client_address=sock.accept()
        
        try:
            print("Conexión establecida con el cliente",client_address)
            while True:
                if cont == 0:
                    stream.start_stream()

                cont = 1
                data = stream.read(1024)

                if recognizer.AcceptWaveform(data):
                    message=recognizer.Result()[14:-3]

                    if cad == True:
                        print(message)
                        connection.send(message.encode('utf-8'))
                        cad = False
                    else:
                        msg = connection.recv(1024).decode('utf-8')
                        cont = 0
                        stream.stop_stream()

                    if msg == 'peticion':
                        cad = True
                        msg = ''

        finally:
            connection.close()
        
