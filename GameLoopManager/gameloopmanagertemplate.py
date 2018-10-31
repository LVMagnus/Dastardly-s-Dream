#This is a template. Do not alter this document unless you desire to redefine it.

__author__="Luiz de Mello"
__date__ ="$Jan 25, 2010 8:33:58 AM$"

#imports
from gameloopmanager import *
#from pygame.locals import *
#import pygame
#-------------------------

class MainGame(GameLoopManager):
    def __init__(self):
        GameLoopManager.__init__(self)

        #self.targetFPS = 60
        #Video Settings
        self.screenWidth = 800
        self.screenHeight = 600
        self.videoModes = 0
        self.colorDepth = 0        
        #self.screen = None #Is intializaded bellow

        #Sound Settings
        self.soundFrequency = 44100
        self.soundSize=-16
        self.soundChannels=2
        self.soundBuffer=4096 #MUST BE a power of 2

        #Miscelaneous and other properties
        self.caption = "Game"
        
        
        #Initialization and configuration of Pygame
        pygame.mixer.pre_init(self.soundFrequency, self.soundSize, self.soundChannels, self.soundBuffer)
        pygame.init()

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), self.videoModes, self.colorDepth)

        pygame.display.set_caption(self.caption)
    #--------------------------__init__(self)--------------------------------

    def Update(self, updateTimeDifference):
        """Updates the game.
            updateTimeDifference = time between the current and the previous call to this
            method, in milliseconds."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.Exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN and event.mod & KMOD_ALT:
                    self.videoModes = self.videoModes ^ FULLSCREEN
                    self.ResetDisplayMode()
                elif event.key == K_ESCAPE:
                    self.Exit()
                    
        #TODO: Implement your update logic here



    #----------------------Update(self, updateTimeDifference)-------------------------------

    def Draw(self, updateTimeDifference):
        """Draws the game. If the game is having problems reaching the targetFPS it will
            skip some calls to this method to atempt to keep at least the desired update rate.
            All the inner game logic should be present at the Update method, use this exclusively
            to draw whenever possible.
            updateTimeDifference = time between the two last calls of the Update method."""

        #TODO: Implement your drawing logic here and remove the sample code
        font = pygame.font.SysFont("arial", 30)
        text = "Ni!"
        font_size = font.size(text)
        self.screen.fill((0,0,0))
        self.screen.blit( font.render(text, True, (200, 100, 0)),
        ((self.screenWidth-font_size[0])/2, (self.screenHeight-font_size[1])/2) )
        pygame.display.update()

        
    #------------------------Draw(self, updateTimeDifference)-------------------------------

    def OnExit(self):
        """Implement here any logic you may wish to run just before leaving the game (such as saving a file).
           Your logic must return two values. The first must be either True or False that will control if the application
           will indeed quite (True) or not (False). The second should be 0 or an error message/code that will be used when
           calling sys.exit()."""
        return True, 0


    #-------------------_--------OnExit(self)-------------------------------------
    def ResetDisplayMode(self):
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), self.videoModes, self.colorDepth)


    def ResetSoundSettings(self):
        pygame.mixer.quit()
        pygame.mixer.init(self.soundFrequency, self.soundSize, self.soundChannels, self.soundBuffer)

#--------------------------------------MainGame(GameLoopManager)-----------------------------------------

Game = MainGame()
Game.Run()