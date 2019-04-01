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

path = os.path.dirname(os.path.abspath(__file__))
print (path)
'''
Objects
'''


class Map:
    def __init__(self,display):
        self.display = display
        self.objects_list = pygame.sprite.Group()

        for i in range(5):
             self.objects_list.add(Crate(self,50+50*i,300))
        for i in range(5):
             self.objects_list.add(Crate(self,250+50*i,500))
        for i in range(4):
             self.objects_list.add(Crate(self,750+50*i,100))
        for i in range(5):
             self.objects_list.add(Crate(self,300+50*i,200))
        for i in range(30):
             self.objects_list.add(Crate(self,0+50*i,700))
        for i in range(4):
             self.objects_list.add(Crate(self,750+50*i,500))

    def draw(self):
        self.objects_list.draw(self.display) #refresh player position


class Crate(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self,scene,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.x = x  
        self.y = y 
        self.scene = scene

        img = pygame.image.load(os.path.join(path,'desert','Objects','Crate.png')).convert()
        img_size = img.get_size()
        img = pygame.transform.scale(img, (int(img_size[0]/2), int(img_size[1]/2)))
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        # img = pygame.transform.scale(img, (int(img_size[0]/4), int(img_size[1]/4)))
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.y = self.y
        self.rect.x = self.x



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
        


        self.lookingAtRight = True

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

    def checkCol(self):

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


        objs = pygame.sprite.spritecollide(self, self.scene.objects_list, False)

        for obj in objs:
            if obj.rect.collidepoint(floor_bottomleft)  or obj.rect.collidepoint(floor_bottomright):
                isNotFalling.append(obj)

            if obj.rect.collidepoint(top_topleft)  or obj.rect.collidepoint(top_topright):
                isStuckTop.append(obj)
        
            if obj.rect.collidepoint(bottomleft)  or obj.rect.collidepoint(topleft)  or obj.rect.collidepoint(midleft):
                isStuckLeft.append(obj)
                # print('StuckLeft ->   self: ',midleft,'  Crate: ',obj.rect.right)

            if obj.rect.collidepoint(bottomright)  or obj.rect.collidepoint(topright)  or obj.rect.collidepoint(midright):
                isStuckRight.append(obj)



        if isNotFalling:
            if not 'notFalling' in self.states:
                self.states['notFalling']=isNotFalling
        else:
            if 'notFalling' in self.states:
                self.states.pop('notFalling')

        if isStuckTop:
            if not 'stuckTop' in self.states:
                self.states['stuckTop']=isStuckTop
        else:
            if 'stuckTop' in self.states:
                self.states.pop('stuckTop')

        if isStuckLeft:
            if not 'stuckLeft' in self.states:
                self.states['stuckLeft']=isStuckLeft
        else:
            if 'stuckLeft' in self.states:
                self.states.pop('stuckLeft')

        if isStuckRight:
            if not 'stuckRight' in self.states:
                self.states['stuckRight']=isStuckRight
        else:
            if 'stuckRight' in self.states:
                self.states.pop('stuckRight')


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
            self.lookingAtRight = False
            if not 'stuckLeft' in self.states:  
                self.control(-steps,0)
                
        if keyboard[pygame.K_RIGHT] or keyboard[ord('d')]:
            self.lookingAtRight = True
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
            self.image = pygame.transform.flip(self.image,not self.lookingAtRight,False)


        if 'jumping' in self.states:
            if self.lastMov != 'jump':
                self.lastMov = 'jump'
                self.frame = 0

            if not ((self.frame//self.animSpeed) >= len(self.imgJumping)):
                print(self.frame//self.animSpeed)
                self.image = self.imgJumping[self.frame//self.animSpeed]
                self.image = pygame.transform.flip(self.image,not self.lookingAtRight,False)
                self.frame += 1

        elif   not 'notFalling' in self.states:
            self.image = self.imgJumping[-1]
            self.image = pygame.transform.flip(self.image,not self.lookingAtRight,False)


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

    world.fill(BLACK)
    # world.blit(backdrop, backdropbox)
    player.update()
    desierto.draw()
    player_list.draw(world) #refresh player position
    pygame.display.flip()
    clock.tick(fps)