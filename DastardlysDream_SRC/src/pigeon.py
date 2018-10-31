

__author__="Adriano"
__date__ ="$Feb 1, 2010 7:24:01 AM$"

import random
import math
import pygame
from pygame.locals import *


class Pigeon:
    _img = None
    _frameSize = (146, 95)
    _hitAreaOffset = ((26, 10, -60, -40))
    def __init__(self, level):
        self.animationTime = 0
        self.frameTime = 1000/(10+(level-1)*2) #flaps wings faster as level gets higher
        self.alive = True
        self.deadFrame = 6
        self.mustBeRemoved = False
        self.deathCountdown = 0 #after one second the dead image is removed and the main game should delete it
        self.currentFrame = 0
        self.countdownToRemoval = (5 + random.randint(1, 16-level))*1000 #max 10s on level 6(last), max 15s on level 1
        #self.countdownToRemoval = 5 #use for test on game over
        
        #initializing in the regular places will raise an error since it is processed
        #before the call to pygame.init(), so it is initialized on the first time an
        #object is created
        if Pigeon._img is None:
            Pigeon._img = pygame.image.load(r'Image\pigeon_spritesheet.png').convert_alpha()

        if random.randint(0,1) == 0:
            X = -Pigeon._frameSize[0] 
        else:
            X = 1023 + Pigeon._frameSize[0] #keep in mind that if the first pixel is 0, the 1024th one is 1023

        Y = random.randint(0,1023)
        self.pos = [X,Y]
        
        minSpeed = 80 + level*20 #level one = 100, 6 (last) = 200
        maxSpeed = 4 * minSpeed
        X = random.randint(minSpeed, maxSpeed) #inclusive higher range
        if X > maxSpeed//2:
            Y = random.randint(minSpeed, X)
        else:
            Y = random.randint(X, maxSpeed)

        self.speed = [X,Y]
        #-----------------------init()-----------------


    def Update(self, updateTimeDifference, mouseX, mouseY, hasClicked):#returns if the pigeon was shoot or not
        returnVal = False
        self.animationTime += updateTimeDifference
        self.countdownToRemoval -= updateTimeDifference

        if self.alive:
            self.pos[0] += self.speed[0] * (updateTimeDifference/1000)#ms to seconds
            if self.pos[0] < 0 and self.speed[0] < 0:
                if self.countdownToRemoval > 0:
                    self.pos[0] = 0
                    self.speed[0] *= -1
                elif self.pos[0] <= -Pigeon._frameSize[0]: #out of the screen entirely
                    self.mustBeRemoved = True
            elif self.pos[0] > 1023-Pigeon._frameSize[0] and self.speed[0] > 0:
                if self.countdownToRemoval > 0:
                    self.pos[0] = 1023-Pigeon._frameSize[0]
                    self.speed[0] *= -1
                elif self.pos[0] >= 1023: #out of the screen entirely
                    self.mustBeRemoved = True


            self.pos[1] += self.speed[1] * (updateTimeDifference/1000) #ms to seconds
            if self.pos[1] < 0 and self.speed[1] < 0:
                if self.countdownToRemoval > 0:
                    self.pos[1] = 0
                    self.speed[1] *= -1
                elif self.pos[1] <= -Pigeon._frameSize[1]: #out of the screen entirely
                    self.mustBeRemoved = True
            elif self.pos[1] > 699 - Pigeon._frameSize[1] and self.speed[1] > 0:
                if self.countdownToRemoval > 0:
                    self.pos[1] = 699 - Pigeon._frameSize[1]
                    self.speed[1] *= -1
                elif self.pos[1] >= 699 + Pigeon._frameSize[1]: #out of the screen entirely
                    self.mustBeRemoved = True

            boundingBox = Rect(self.pos[0] + Pigeon._hitAreaOffset[0],
                self.pos[1]+ Pigeon._hitAreaOffset[1],
                Pigeon._frameSize[0] + Pigeon._hitAreaOffset[2],
                Pigeon._frameSize[1] + Pigeon._hitAreaOffset[3])
            
            if not (boundingBox.collidepoint(mouseX//1,mouseY//1) and hasClicked):
                if self.animationTime >= self.frameTime:
                    self.animationTime -= self.frameTime
                    self.currentFrame +=1
                    if self.currentFrame == self.deadFrame:
                        self.currentFrame = 0                
            else: #if collision was detected and player shoot
                self.alive = False
                returnVal = True
                self.countdownToRemoval = 1000
                self.currentFrame = self.deadFrame
                

        elif self.countdownToRemoval <= 0: #is is not alive and...
            self.mustBeRemoved = True
            #returnVal = False

        return returnVal
    #-------------------------Update()------------------------------

    def Draw(self, screen):        
        frameImage = Pigeon._img.subsurface(
            ( self.currentFrame * Pigeon._frameSize[0], 0 ),
            Pigeon._frameSize )

        if self.speed[0] < 0 and self.alive:
            frameImage = pygame.transform.flip(frameImage, True, False)

        screen.blit(frameImage, self.pos)

        