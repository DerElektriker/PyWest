#!/usr/bin/env python3
# draw a world
# add a player and player control
# add player movement

# GNU All-Permissive License
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

import pygame
import sys
import os
import math

path = os.path.dirname(os.path.abspath(__file__))
'''
Objects
'''


class Map:
    def __init__(self,display):
        self.display = display
        self.objects_list = pygame.sprite.Group()

        for i in range(5):
             self.objects_list.add(Crate(50+50*i,300))
        for i in range(5):
             self.objects_list.add(Crate(250+50*i,500))
        for i in range(4):
             self.objects_list.add(Crate(750+50*i,100))
        for i in range(5):
             self.objects_list.add(Crate(300+50*i,200))
        for i in range(30):
             self.objects_list.add(Crate(0+50*i,700))
        for i in range(4):
             self.objects_list.add(Crate(750+50*i,500))

        ## Creamos un objeto Sword
        self.sword_1 = Sword(400,100)

        self.objects_list.add(self.sword_1)

    def draw(self):
        self.objects_list.draw(self.display) #refresh player position

    def update(self):

        for i in self.objects_list.__iter__():
            i.update()
        

class Sword(pygame.sprite.Sprite):

    def __init__(self,x,y):
    ##El Init se ejecuta al momento de construirse el objeto

        ##Al ser una subclase, con la siguiente linea se inicializan todos los metodos heredados de Sprite
        pygame.sprite.Sprite.__init__(self)
        

        #Cargamos la imagen
        img = pygame.image.load("./Images/Sword.png").convert()

    #Se escala la imagen para que este de acuerdo con las dimensiones del escenario
        #Se pide las dimensiones actuales de la imagen
        size_x,size_y = img.get_size()
        #Se redimensiona la imagen a un tercio de la imagen original
        img = pygame.transform.scale(img, (int(size_x/3), int(size_y/3)))


        # Las siguientes dos lineas se utilizan para quitarle el fondo blanco a la imagen
        img.convert_alpha()
        img.set_colorkey((255,255,255))

        self.image = img

        # Se define cual va a ser el rectangulo de colision del objeto
        self.rect  = self.image.get_rect()


        self.tick = 0

        self.rect.x = x
        self.rect.y = y

        self.firstY = None

    def getConstructor(self):
        return Sword,[self.rect.x,self.rect.y]

    def update(self):



        # Si es la primera vez que se ejecuta la primera vez que se ejecuta el metodo update
        # se guarda la posición inicial de Y, para que flote al rededor de el punto inicial
        if self.firstY is None:
            self.firstY=self.rect.y
        
        # Flota siguiendo una trayectoria senoidal, utilizando la funcion "sin" (seno) y la variable 
        # PI ubicados en el modulo matematico "math"

        if self.tick>math.pi*20:
            self.tick=0
        else:
            self.tick+=0.4

        #Se actualiza la posición
        self.rect.y = self.firstY+math.sin(self.tick/10)*10
        





class Crate(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.x = x  
        self.y = y 

        img = pygame.image.load(os.path.join(path,'desert','Objects','Crate.png')).convert()
        self.img_size = img.get_size()
        img = pygame.transform.scale(img, (int(self.img_size[0]/2), int(self.img_size[1]/2)))
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        # img = pygame.transform.scale(img, (int(img_size[0]/4), int(img_size[1]/4)))
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x

    def getConstructor(self):
        return (Crate,[self.x,self.y])

    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self,scene):
        pygame.sprite.Sprite.__init__(self)

        self.scene = scene
        self.movex = 0
        self.movey = 0
        self.x = 200  
        self.y = 300 
        self.frame = 0
        self.images = []


        #Lista de estados
        self.states = {}

        #Variables auxiliares
        self.jumpSpeed = 0  #Velocidad de salto
        self.gravMovey = 0  #Gravedad inicial en Y


        for i in range(0,10):
            img = pygame.image.load(os.path.join(path,'Images','Run__00' + str(i) + '.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            img_size = img.get_size()
            img = pygame.transform.scale(img, (int(img_size[0]/4), int(img_size[1]/4)))

            self.images.append(img)
            self.image = self.images[0]
            self.rect  = self.image.get_rect()
        


        self.lookingAtRight = 1
        self.falling = 1

        ####Jumping sprites
        self.imgJumping = []
        for i in range(0,10):
            img = pygame.image.load(os.path.join(path,'Images','Jump__00' + str(i) + '.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            img_size = img.get_size()
            img = pygame.transform.scale(img, (int(img_size[0]/4), int(img_size[1]/4)))
            self.imgJumping.append(img)


        ####Idle sprites
        self.imgIdle = []
        for i in range(0,10):
            img = pygame.image.load(os.path.join(path,'Images','Idle__00' + str(i) + '.png')).convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            img_size = img.get_size()
            img = pygame.transform.scale(img, (int(img_size[0]/4), int(img_size[1]/4)))
            self.imgIdle.append(img)
        

        

        #Velocidad a la cual se mostrala la animacion
        self.animSpeed = 2

        #Variable auxiliar para saber cuando se estaba moviendo a la der o a la izq
        self.lastMov = None

    def checkCol(self,diffx=0, diffy=0, flag=True):

        ###Variable auxiliar para identificar colisiones
        isNotFalling = []
        isStuckRight = []
        isStuckLeft  = []
        isStuckTop   = []

        floor_bottomleft  = self.rect.bottomleft[0]+30 ,self.rect.bottomleft[1]   -2
        floor_bottomright = self.rect.bottomright[0]-30,self.rect.bottomright[1]  -2
        top_topleft  = self.rect.topleft[0]+30   ,self.rect.topleft[1]   -2
        top_topright = self.rect.topright[0]-30   ,self.rect.topright[1]  -2


        latOff=15

        bottomleft  = self.rect.bottomleft[0] +latOff,self.rect.bottomleft[1]   -5
        bottomright = self.rect.bottomright[0]-latOff,self.rect.bottomright[1]  -5
        topleft     = self.rect.topleft[0]    +latOff,self.rect.topleft[1]      
        topright    = self.rect.topright[0]   -latOff,self.rect.topright[1]     
        midleft     = self.rect.midleft[0]    +latOff,self.rect.midleft[1]        
        midright    = self.rect.midright[0]   -latOff,self.rect.midright[1]      

        aux = pygame.sprite.Sprite()
        if flag:
            if diffx>0:
                if diffy>0:
                    aux.rect = pygame.rect.Rect(self.rect.x,self.rect.y+diffy,self.shape_x+diffx,self.shape_y)
                else:
                    aux.rect = pygame.rect.Rect(self.rect.x,self.rect.y+diffy,self.shape_x+diffx,self.shape_y)
            else:
                if diffy>0:
                    aux.rect = pygame.rect.Rect(self.rect.x+diffx,self.rect.y+diffy,self.shape_x,self.shape_y)
                else:
                    aux.rect = pygame.rect.Rect(self.rect.x+diffx,self.rect.y,self.shape_x,self.shape_y+diffy)
        else:

            if diffx>0:
                if diffy>0:
                    aux.rect = pygame.rect.Rect(self.rect.x+diffx,self.rect.y+diffy,self.shape_x,self.shape_y)
                else:
                    aux.rect = pygame.rect.Rect(self.rect.x+diffx,self.rect.y,self.shape_x,self.shape_y+diffy)
                    # print('rect top ',aux.rect.top,',   real top ',self.rect.top)
            else:
                if diffy>0:
                    aux.rect = pygame.rect.Rect(self.rect.x,self.rect.y+diffy,self.shape_x+diffx,self.shape_y)
                    # print('rect top ',aux.rect.top,',   real top ',self.rect.top)
                else:
                    aux.rect = pygame.rect.Rect(self.rect.x,self.rect.y,self.shape_x+diffx,self.shape_y+diffy)



        objs = pygame.sprite.spritecollide(aux, self.scene.objects_list, False)

        return objs


    def control(self,x,y):
        '''
        control player movement
        '''
        self.movex += x
        self.movey += y

    def update(self):
        '''
        Update sprite position
        '''
        self.shape_x,self.shape_y = self.image.get_size()
        col_list = self.checkCol()

        tope = False

        if keyboard[pygame.K_SPACE] or keyboard[ord('w')]:
            if  not 'falling' in self.states and not  'jumping' in self.states:
                self.states['jumping']=1

        if 'jumping' in self.states:
            self.falling = -1
            if self.jumpSpeed==0:
                self.jumpSpeed = -25
            elif self.jumpSpeed<=-1:
                self.jumpSpeed -= self.jumpSpeed*0.15
            else:
                self.jumpSpeed=0
                tope = True
                self.falling = 1
                if 'jumping' in self.states:
                    self.states.pop('jumping')


        ### Procesando Caidas
        elif not 'jumping' in self.states :

            self.jumpSpeed = 0
            self.falling = 1
            if 'falling' in self.states:
                if self.gravMovey==0:
                    self.gravMovey = 3
                else:
                    if self.gravMovey < 9:
                        self.gravMovey += self.gravMovey*0.1
                        
            else:
                self.gravMovey=0
                


        if keyboard[pygame.K_LEFT] or keyboard[ord('a')]:
            self.lookingAtRight = -1
            self.movex=  -steps

        if keyboard[pygame.K_RIGHT] or keyboard[ord('d')]:
            self.lookingAtRight = 1
            self.movex=  steps

            

        diffX = totalMoveX = self.movex
        diffY = totalMoveY = self.movey +self.gravMovey+self.jumpSpeed


        self.states['falling'] = 1
        col_list=self.checkCol(-diffX-self.lookingAtRight*20,diffY+20*self.falling,False)
        for i in col_list:                     
                if diffY >= 0:
                    if not tope:
                        self.rect.bottom = i.rect.top
                        if 'falling' in self.states:
                            self.states.pop('falling')

                if diffY < 0:
                    self.jumpSpeed = -0.1
                    self.rect.top = i.rect.bottom

        self.rect.y = self.rect.y + totalMoveY
        col_list=self.checkCol(diffX+self.lookingAtRight*10,-diffY-10*self.falling)
        for i in col_list:    
                if diffX > 0:                        
                    self.rect.right = i.rect.left    
                if diffX < 0:                        
                    self.rect.left = i.rect.right

        self.rect.x = self.rect.x + totalMoveX

        ##Cantidad de animaciones es igual a la longitud del vector de animaciones
        numAnim = len(self.images)
        if not (keyboard[pygame.K_LEFT] or keyboard[ord('a')] or keyboard[pygame.K_RIGHT] or keyboard[ord('d')]) and not 'jumping' in self.states and  not 'falling' in self.states:
            self.frame += 1
            if self.frame//self.animSpeed >= len(self.imgIdle):
                self.frame = 0
            self.image = self.imgIdle[(self.frame//self.animSpeed)]
            self.image = pygame.transform.flip(self.image,not (self.lookingAtRight==1),False)


        if 'jumping' in self.states:
            if self.lastMov != 'jump':
                self.lastMov = 'jump'
                self.frame = 0

            if not ((self.frame//self.animSpeed) >= len(self.imgJumping)):
                self.image = self.imgJumping[self.frame//self.animSpeed]
                self.image = pygame.transform.flip(self.image,not (self.lookingAtRight==1),False)
                self.frame += 1

        elif   'falling' in self.states:
            self.image = self.imgJumping[-1]
            self.image = pygame.transform.flip(self.image,not (self.lookingAtRight==1),False)


        # moving left
        elif (keyboard[pygame.K_LEFT] or keyboard[ord('a')] or keyboard[pygame.K_RIGHT] or keyboard[ord('d')]) and not 'jumping' in self.states and not 'falling' in self.states:

            if self.movex < 0:
                if self.lastMov != 'left':
                    self.lastMov = 'left'
                    self.frame = 0

                self.frame += 1
                if self.frame//self.animSpeed >= numAnim:
                    self.frame = 0
                self.image = self.images[(self.frame//self.animSpeed)]
                self.image = pygame.transform.flip(self.image,True,False)

            # moving right
            elif self.movex > 0:
                if self.lastMov != 'right':
                    self.lastMov = 'right'

                    self.frame = 0
                self.frame += 1
                if self.frame//self.animSpeed >= numAnim:
                    self.frame = 0
                self.image = self.images[(self.frame//self.animSpeed)]

        self.movex = 0
        self.movey = 0

    def _update(self):
        '''
        Update sprite position
        '''

        self.checkCol()


        size_x = self.rect.right  - self.rect.left
        size_y = self.rect.bottom - self.rect.top

        if keyboard[pygame.K_SPACE] or keyboard[ord('w')]:
            if  'notFalling' in self.states and not  'jumping' in self.states:
                self.states['jumping']=1

        if 'jumping' in self.states:
            if self.jumpSpeed==0:
                self.jumpSpeed = -25
            elif self.jumpSpeed<=-1:
                self.jumpSpeed -= self.jumpSpeed*0.15
            else:
                self.jumpSpeed=0
                if 'jumping' in self.states:
                    self.states.pop('jumping')


            if not 'stuckTop' in self.states:
                oldRectY = self.rect.y
                self.rect.y += self.jumpSpeed
                self.checkCol()
                self.rect.y = oldRectY


            if  'stuckTop' in self.states:  
                maxY=self.states['stuckTop'][0].rect.bottom 
                for obj in  self.states['stuckTop']:
                    maxY = obj.rect.bottom if obj.rect.bottom<maxY else maxY
                self.rect.y = maxY
                self.jumpSpeed=0
                if 'jumping' in self.states:
                    self.states.pop('jumping')




        ### Procesando Caidas
        if not 'jumping' in self.states :
            if   not 'notFalling' in self.states:
                if self.gravMovey==0:
                    self.gravMovey = 3
                else:
                    if self.gravMovey < 9:
                        self.gravMovey += self.gravMovey*0.1
                        
                    oldRectY = self.rect.y
                    self.rect.y += self.gravMovey
                    self.checkCol()
                    self.rect.y = oldRectY

            if  'notFalling' in self.states:
                self.gravMovey=0
                
                minY=self.states['notFalling'][0].rect.top 
                for obj in  self.states['notFalling']:
                    minY = obj.rect.top if obj.rect.top<minY else minY
                self.rect.y = minY-size_y+2
        
        self.checkCol()
            # self.control(steps,0)
        # elif   not 'notFalling' in self.states and 'stuckLeft' in self.states:
            # else:

        if keyboard[pygame.K_LEFT] or keyboard[ord('a')]:
            self.lookingAtRight = -1
            if not 'stuckLeft' in self.states:  
                self.control(-steps,0)
                
        if keyboard[pygame.K_RIGHT] or keyboard[ord('d')]:
            self.lookingAtRight = 1
            if not 'stuckRight' in self.states:
                self.control(steps,0)
        # elif   not 'notFalling' in self.states and 'stuckRight' in self.states:
            # else:

        if not 'stuckLeft' in self.states: 

            auxRectX = self.movex
            auxRectY = self.movey +self.jumpSpeed
            self.rect.x+=auxRectX
            self.rect.y+=auxRectY
            self.checkCol() 
            self.rect.x-=auxRectX
            self.rect.y-=auxRectY

        if 'stuckLeft' in self.states: 
            maxX=self.states['stuckLeft'][0].rect.right 
            for obj in  self.states['stuckLeft']:
                maxX = obj.rect.right if obj.rect.right>maxX else maxX
            self.rect.x = maxX
            # self.control(steps,0)



        if not 'stuckRight' in self.states: 
            auxRectX = self.movex
            auxRectY = self.movey +self.jumpSpeed
            self.rect.x+=auxRectX
            self.rect.y+=auxRectY
            self.checkCol() 
            self.rect.x-=auxRectX
            self.rect.y-=auxRectY


        if  'stuckRight' in self.states:
            minX=self.states['stuckRight'][0].rect.left 
            for obj in  self.states['stuckRight']:
                minX = obj.rect.left if obj.rect.left<minX else minX
            self.rect.x = minX-size_x
            # self.control(-steps,0)

            


            

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey +self.gravMovey+self.jumpSpeed




        ##Cantidad de animaciones es igual a la longitud del vector de animaciones
        numAnim = len(self.images)
        if not (keyboard[pygame.K_LEFT] or keyboard[ord('a')] or keyboard[pygame.K_RIGHT] or keyboard[ord('d')]) and not 'jumping' in self.states and  'notFalling' in self.states:
            self.frame += 1
            if self.frame//self.animSpeed >= len(self.imgIdle):
                self.frame = 0
            self.image = self.imgIdle[(self.frame//self.animSpeed)]
            self.image = pygame.transform.flip(self.image,not (self.lookingAtRight==1),False)


        if 'jumping' in self.states:
            if self.lastMov != 'jump':
                self.lastMov = 'jump'
                self.frame = 0

            if not ((self.frame//self.animSpeed) >= len(self.imgJumping)):
                self.image = self.imgJumping[self.frame//self.animSpeed]
                self.image = pygame.transform.flip(self.image,not (self.lookingAtRight==1),False)
                self.frame += 1

        elif   not 'notFalling' in self.states:
            self.image = self.imgJumping[-1]
            self.image = pygame.transform.flip(self.image,not (self.lookingAtRight==1),False)


        # moving left
        elif (keyboard[pygame.K_LEFT] or keyboard[ord('a')] or keyboard[pygame.K_RIGHT] or keyboard[ord('d')]) and not 'jumping' in self.states and not 'falling' in self.states:

            if self.movex < 0:
                if self.lastMov != 'left':
                    self.lastMov = 'left'
                    self.frame = 0

                self.frame += 1
                if self.frame//self.animSpeed >= numAnim:
                    self.frame = 0
                self.image = self.images[(self.frame//self.animSpeed)]
                self.image = pygame.transform.flip(self.image,True,False)

            # moving right
            elif self.movex > 0:
                if self.lastMov != 'right':
                    self.lastMov = 'right'

                    self.frame = 0
                self.frame += 1
                if self.frame//self.animSpeed >= numAnim:
                    self.frame = 0
                self.image = self.images[(self.frame//self.animSpeed)]

        self.movex = 0
        self.movey = 0

'''
Setup
'''
worldx = 960
worldy = 720

fps = 40        # frame rate
clock = pygame.time.Clock()
pygame.init()
main = True

BLUE  = (25,25,200)
BLACK = (23,23,23 )
WHITE = (254,254,254)
ALPHA = (0,0,0)

global keyboard

global world 
world= pygame.display.set_mode([worldx,worldy])
backdrop = pygame.image.load(os.path.join(path,'desert','BG.png')).convert()
backdropbox = world.get_rect()
##MAPAAAA
desierto = Map(world)
##JUGADORR
player = Player(desierto)   # spawn player
player_list = pygame.sprite.Group()
player_list.add(player) 
steps = 10      # how fast to move

'''
Main loop
'''

while main == True:

    keyboard=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False
            if event.key == ord('r'):
                player.rect.x=0
                player.rect.y=0

            if event.key == ord('h'):
                desierto.objects_list.add(Crate(pygame.mouse.get_pos()[0]//50 *50,pygame.mouse.get_pos()[1]//50 *50))

            if event.key == ord('g'):
                for i in desierto.objects_list.__iter__():
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        desierto.objects_list.remove(i)

            if event.key == ord('k'):
                import pickle
                with open('map.pkl','wb') as wb:
                    objects = []
                    for i in desierto.objects_list.__iter__():
                        objects.append(i.getConstructor())
                        
                    pickle.dump(objects,wb)
                    

            if event.key == ord('l'):
                import pickle
                with open('map.pkl','rb') as rb:
                    objects = pickle.load(rb)
                    desierto.objects_list.empty()
                    for i in objects:
                        desierto.objects_list.add(i[0](*i[1]))




    world.fill(BLACK)
    # world.blit(backdrop, backdropbox)
    player.update()
    desierto.update()
    desierto.draw()
    player_list.draw(world) #refresh player position
    pygame.display.flip()
    clock.tick(fps)