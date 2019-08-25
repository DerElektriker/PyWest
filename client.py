
# Connect to server
import socket
import select

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

received, _, _ = select.select([sock], [], [])

while True:
    #data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    # Select consilta [socket], si hay datos,
    # los almacena en received

    received, _, _ = select.select([sock], [], [], 0)
    print "received message:", data
# Init game

# run
## loop
## sampleInput
## 