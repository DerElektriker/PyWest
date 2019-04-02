from _thread import *
import socket , threading

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print_lock = threading.Lock() 
control_lock = threading.Lock() 

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
            data = self.conn.recv(BUFFER_SIZE)
            if not data:
                control_lock.acquire()
                if self.threadID in hilos:
                    del hilos[self.threadID]
                control_lock.release()
                break
            print (process_data.unpack(data))
            print_lock.acquire()
            print ("received from:", self.addr)
            print_lock.release()
            for threads in list(hilos.values()):
                if (threads.addr != self.addr):
                    threads.conn.send(data)


            #self.conn.send(data)  # echo


def server():
    i = 1
    while 1:
        conn, addr = s.accept()
        thread = myThread(i,str(i),i,conn,addr)
        control_lock.acquire()
        hilos[str(i)] = thread
        control_lock.release()
        thread.start()
        i = i+1


if __name__ == '__main__':
    server()