import socket , time
TCP_IP = '127.0.0.1'
TCP_PORT = 5005

BUFFER_SIZE = 1024
MESSAGE = b"Mi-Vieja-Mula arg1 arg2 // Traaa arg1 arg2 //"#input().encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while(1):
    time.sleep(5)
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE) #por ahora se cuelga aca porque el server no tira nada
    print ("received data:", data)
s.close()
