import socket , time
import input
TCP_IP = '127.0.0.1'
TCP_PORT = 5005

BUFFER_SIZE = 1024
MESSAGE = b"Mi-Vieja-Mula arg1 arg2 // Traaa arg1 arg2 //"#input().encode()

import json
def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)  
    return d

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Iniciando conexión...")
s.connect((TCP_IP, TCP_PORT))
print("Conexión TCP iniciada")

# UDP socket
import select

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

udpSocket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
#udpSocket.bind((UDP_IP, UDP_PORT))
udpSocket.setblocking(False)
# udpSocket.settimeout(0)

import pygame
clock = pygame.time.Clock()
pygame.init()

tickRate = 33
#sample input rate, same as server tick rate

USERCMD = pygame.USEREVENT+1
cmdRate = 33
#rate in which the user send user commands at the server

UPDATE = pygame.USEREVENT+2
updateRate = 20
#rate at which client recieve snapshots

interpolationPeriod = 100

snapshotHistory = []
userCmdList = []

pygame.time.set_timer(USERCMD, round(1000 / cmdRate))
pygame.time.set_timer(UPDATE, round(1000 / updateRate))

controls = input.InputHandler()

print("Comenzando LOOP")
while(1):

    newUserCmd = {}
    newUserCmd['mseg'] = pygame.time.get_ticks()



    #Sample input
    controls.update()
    newUserCmd['gamecontrols'] = controls.inGameControls
    print("sampling")
    #Client update

    #Events
    for event in pygame.event.get():
        if (event.type == USERCMD):
            #send user command
            # print("--> usercmd")
            pass
        elif (event.type == UPDATE):
            # print("--> update")
            pass
    time.sleep(5)
    message = "Ticks: "+str(pygame.time.get_ticks())
    print("Enviando mensaje:", message)
    udpSocket.sendto(dict_to_binary(newUserCmd), (UDP_IP, UDP_PORT))
    print("Mensaje enviado")


    print("Esperando respuesta:")
    # data = udpSocket.recvfrom(BUFFER_SIZE) #por ahora se cuelga aca porque el server no tira nada

    received, _, _ = select.select([udpSocket], [], [], 0)
    if (received):
        data = udpSocket.recvfrom(BUFFER_SIZE)
        print("received data:", data, received)
        #received = []
    else:
        print("Ningún dato recibido")
    # print("Datos recibidos:", received[0] if received else None)

    clock.tick(tickRate)
s.close()

class UserCmd():
    interpolationTime
    msec
    gamecontrols
