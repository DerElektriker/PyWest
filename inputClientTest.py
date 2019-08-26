import pygame
from input import InputHandler
import pprint

from itertools import chain

def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)





# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    

####### CLIENT ########
import socket , time
import input
TCP_IP = '127.0.0.1'
TCP_PORT = 5005

BUFFER_SIZE = 1024
MESSAGE = b"Mi-Vieja-Mula arg1 arg2 // Traaa arg1 arg2 //"#input().encode()

import json
def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    # binary = ' '.join(format(ord(letter), 'b') for letter in str)
    binary = str.encode()
    return binary


def binary_to_dict(the_binary):
    # jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    jsn = the_binary.decode()
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

pygame.init()

pygame.time.set_timer(USERCMD, round(1000 / cmdRate))
pygame.time.set_timer(UPDATE, round(1000 / updateRate))

 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()


playerInput = InputHandler()

message = {
    'usercmds' : []
}

# -------- Main Program Loop -----------
while done==False:

    newUserCmd = {}
    newUserCmd['mseg'] = pygame.time.get_ticks()
    message['usercmds'].append(newUserCmd)

    ##Check for updates

    #Client update

    # Sample inputs

    playerInput.update()

    if playerInput.get("escape"):
        if (playerInput.getDevice()).name == "Mouse and Keyboard":
            if "Controller (Xbox One For Windows)" in map(lambda x: x.name, playerInput.getDevicesList()):
                playerInput.setDevice("Controller (Xbox One For Windows)")
        elif (playerInput.getDevice()).name == "Controller (Xbox One For Windows":
            playerInput.setDevice("Mouse and Keyboard")

    newUserCmd['gamecontrols'] = playerInput.inGameControls
    print("sampling")

    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
        if event.type == USERCMD:
            # print("Enviando mensaje:", message)
            udpSocket.sendto(dict_to_binary(message), (UDP_IP, UDP_PORT))
            message['usercmds'] = []
            print("Mensaje enviado")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    for k,v in playerInput.inGameControls.items():
        textPrint.print(screen, "{}, {}".format(k,v))

    textPrint.print(screen, " ")

    for k,v in playerInput.currentDevice.configuration.items():
        textPrint.print(screen, "{}, {}".format(k,v))
    #textPrint.indent()
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(tickRate)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()