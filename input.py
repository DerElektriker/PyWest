'''
    Modulo: InputHandler

    Interface
    ---------
        update()
            Actualiza el estado del input
        get(ACCION)
            Obtiene si el botón para realizar ACCION está apretado
        getDevicesList()
            Muestra los dispositivos (Joystick) disponibles
        getDevice()
            Obtiene el id del dispositivo utilizado por el input
        setDevice(deviceName)
            Marca como predeterminado el dispositivo seleccionado

        @TODO: Implementar:
        getConfig(device=currentDevice)
            Obtiene un diccionario con la configuración del control
        setConfig(dict, device=currentDevice)
            Actualiza el diccionario con la configuración en dict

    Uso:
    ----

        player.input = InputHandler()

        ...
        player.input.update()

        if player.input.get("jump"):
            player.y -= player.jumpspeed
        ...

'''

import pygame
from enum import Enum

class Device():
    def __init__(self, name="", type=""):
        self.name = name
        self.type = type
        self.configuration = {}

class InputHandler():
    def __init__(self):
        self.inGameControls = {
            "left"                  :   0,
            "right"                 :   0,
            "jump"                  :   0,
            "pause"                 :   0,
            "drop"                  :   0,
            "reset"                 :   0,
            "escape"                :   0,
            "chat"                  :   0,
            "slot1"                 :   0,
            "slot2"                 :   0,
            "slot3"                 :   0,
            "slot4"                 :   0,
            "prevSlot"              :   0,
            "nextSlot"              :   0,
            "primary"               :   0,
            "secondary"             :   0,

            #Pointer
            "pointer"              :   (0,0)
        }

        #Init Mouse
        self.keyboardAndMouse = MouseAndKeyboard()
        self.currentDevice = self.keyboardAndMouse

        #Joysticks
        if pygame.joystick.get_init() != True:
            #Inicializar Joysticks
            pygame.joystick.init()
            
        #Obtener la lista de joysticks disponibles
        self.joysticks = []
        for x in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(x)
            self.joysticks.append(Joystick(name=joystick.get_name(), joystick=joystick))

        self.devices = [self.keyboardAndMouse] + self.joysticks

    def get(self, accion):
        return self.inGameControls[accion]

    def getDevicesList(self):
        return self.devices

    def setDevice(self, device):
        l = list(filter(lambda x: x.name == device, self.devices))
        if len(l) == 1:
            self.currentDevice = l[0]
            if self.currentDevice.type == DEVICE_TYPE.JOYSTICK:
                self.currentDevice.joystick.init()

    def getDevice(self):
        return self.currentDevice

    def update(self):

        if self.currentDevice.type == DEVICE_TYPE.MOUSE_AND_KEYBOARD:
            mouse = pygame.mouse.get_pressed()
            keyboard = pygame.key.get_pressed()
            for k, v in self.currentDevice.configuration.items():
                if v:
                    device = v[0]
                    if device == 'keyboard':
                        self.inGameControls[k] = keyboard[v[1]]
                    elif device == 'mouse':
                        self.inGameControls[k] = mouse[v[1].value]
            self.inGameControls["pointer"] = pygame.mouse.get_pos()

        elif self.currentDevice.type == DEVICE_TYPE.JOYSTICK:
            for k, v in self.currentDevice.configuration.items():
                if v:
                    component = v[0]
                    if component == 'axis':
                        self.inGameControls[k] = (abs(v[2] - self.currentDevice.joystick.get_axis(v[1])) < 0.1)
                    elif component == 'button':
                        self.inGameControls[k] = self.currentDevice.joystick.get_button(v[1])
                    elif component == 'hat':
                        self.inGameControls[k] = (self.currentDevice.joystick.get_hat(v[1]) == v[2])
            self.inGameControls["pointer"] = (self.currentDevice.joystick.get_axis(3), self.currentDevice.joystick.get_axis(4))


class DEVICE_TYPE(Enum) :
    MOUSE_AND_KEYBOARD = "MouseAndKeyboard"
    JOYSTICK = "Joystick"

class MOUSEBUTTON(Enum):
    LEFTBUTTON = 0
    MIDDLEBUTTON = 1
    RIGHTBUTTON = 2

class MouseAndKeyboard(Device):
    '''
        clase 
    '''
    def __init__(self):
        self.name = "Mouse and Keyboard"
        self.type = DEVICE_TYPE.MOUSE_AND_KEYBOARD
        self.defaultConfiguration = {
            "left"              :   ('keyboard',pygame.K_a),
            "right"             :   ('keyboard',pygame.K_d),
            "jump"              :   ('keyboard',pygame.K_SPACE),
            "pause"             :   ('keyboard',pygame.K_RETURN),
            "drop"              :   ('keyboard',pygame.K_g),
            "reset"             :   ('keyboard',pygame.K_r),
            "escape"            :   ('keyboard',pygame.K_ESCAPE),
            "chat"              :   ('keyboard',pygame.K_t),
            "slot1"             :   ('keyboard',pygame.K_1),
            "slot2"             :   ('keyboard',pygame.K_2),
            "slot3"             :   ('keyboard',pygame.K_3),
            "slot4"             :   ('keyboard',pygame.K_4),
            "prevSlot"          :   ('keyboard',pygame.K_q),
            "nextSlot"          :   ('keyboard',pygame.K_e),
            "primary"           :   ('mouse',MOUSEBUTTON.LEFTBUTTON),
            "secondary"         :   ('mouse',MOUSEBUTTON.RIGHTBUTTON)
        }
        self.configuration = self.defaultConfiguration

class Joystick(Device):
    def __init__(self, name, joystick):
        self.name = name
        self.type = DEVICE_TYPE.JOYSTICK
        self.joystick = joystick
        self.defaultConfiguration = {
            "left"              :   ('axis',0,-1),
            "right"             :   ('axis',0, 1),
            "jump"              :   ('button',0),
            "pause"             :   ('button',7),
            "drop"              :   ('button',3),
            "reset"             :   None,
            "escape"            :   ('button',1),
            "chat"              :   ('button',6),
            "slot1"             :   None,
            "slot2"             :   None,
            "slot3"             :   None,
            "slot4"             :   None,
            "prevSlot"          :   ('hat',0, (-1,0)),
            "nextSlot"          :   ('hat',0, ( 1,0)),
            "primary"           :   ('axis',2, -1),
            "secondary"         :   None
        }
        self.configuration = self.defaultConfiguration