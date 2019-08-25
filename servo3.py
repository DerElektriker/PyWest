from _thread import *
import socket , threading, time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print_lock = threading.Lock() 
control_lock = threading.Lock() 

import json
def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)  
    return d

#Socket UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
udpSocket.bind((UDP_IP, UDP_PORT))

hilos = {}
#Formato de los mensajes  MSJ-id1 arg1 arg2 arg3 argn // Mensaje-id2 arg1 arg2 argn  //
class process_data():
    def unpack(string):
        string = string.decode()
        string = string.split(" ")
        comandos = []
        aux = []
        for palabra in string:
            if (palabra == "//" and aux != []):
                comandos.append(aux)
                aux = []
            else :
                aux.append(palabra)
        return comandos

    def parser(id, arglist):
        if(id == "UPos"):
            pass
        elif(id == "Otracosa"):
            pass

    def command_exec(commands):
        for command in commands:
            process_data.parser(command[0],command[1:])

    def run(data):
        commands = process_data.unpack(data)
        process_data.command_exec(commands)
            


        



#    conn.close()
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter,conn,addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.conn = conn
        self.addr = addr

    def run(self):
        while 1:
            print("Listo para recibir datos")
            #data = self.conn.recv(BUFFER_SIZE)
            data, address = udpSocket.recvfrom(BUFFER_SIZE)
            if not data:
                control_lock.acquire()
                if self.threadID in hilos:
                    del hilos[self.threadID]
                control_lock.release()
                break
            print("Recibido:", binary_to_dict(data))
            # print (process_data.run(data))
            print_lock.acquire()
            print ("received from:", address)
            print_lock.release()
            
            print("Enviando múltiples respuestas")
            i = 50000
            while (i > 0):
                udpSocket.sendto(bytes("Recibido" + str(i), 'utf-8'), address)
                i -= 1
            print("Respuestas enviada")
            time.sleep(5)
            for threads in list(hilos.values()):
                if (threads.addr != self.addr):
                    threads.conn.send(data)


            #self.conn.send(data)  # echo


def server():
    i = 1
    print("Escuchando conexiones")
    while 1:
        conn, addr = s.accept()
        print("Conexión aceptada")
        thread = myThread(i,str(i),i,conn,addr)
        control_lock.acquire()
        hilos[str(i)] = thread
        control_lock.release()
        thread.start()
        i = i+1


if __name__ == '__main__':
    server()