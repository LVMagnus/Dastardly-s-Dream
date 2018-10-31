"""Dastardly's dream come true!"""
from titlescreen import TitleScreen
from gamestage import pygame
import pygame

__author__="Luiz de Mello"
__date__ ="$Jan 26, 2010$"



#imports
from gameloopmanager import *
from gameelement import *
from titlescreen import *
from options import *
from gamestage import *
from collections import OrderedDict
#from pygame.locals import *
#import pygame
#-------------------------







class MainGame(GameLoopManager):

        
    def __init__(self):
        GameLoopManager.__init__(self)

        #Useful consts
        self.r800x600  = '800x600'
        self.r640x480  = '640x480'
        self.r1024x768 = '1024x768'
        self.r1280x960 = '1280x960'

        self.Resolutions = OrderedDict()
        self.Resolutions[self.r640x480] =  (640, 480)
        self.Resolutions[self.r800x600] =  (800, 600)
        self.Resolutions[self.r1024x768] =   (1024, 768)
        self.Resolutions[self.r1280x960] =   (1280, 960)

        #Video Settings
        self.resolution = self.r800x600
        self.resVal = self.Resolutions[self.resolution]
        self.videoModes = DOUBLEBUF
        self.colorDepth = 0
        #self.screen = None #It is intializaded bellow


        #Sound Settings
        self.soundFrequency = 44100
        self.soundSize=-16
        self.soundChannels=2
        self.soundBuffer=4096 #MUST BE a power of 2 as defined by pygame's documentation
        self.audioVolume = 1.0 # 0 --> 1
        self.effectsVolume = 1.0 # same
        self.musicVolume = 1.0 # same


        #Initialization and configuration of Pygame
        self.screen = pygame.display.set_mode(self.resVal, self.videoModes, self.colorDepth)
        pygame.mixer.pre_init(self.soundFrequency, self.soundSize, self.soundChannels, self.soundBuffer)
        pygame.init()
        pygame.display.set_caption("Dastardly's Dream")

        
        #Other properties properties
        self.currentGameElement = TitleScreen(self)        

        self.audioVolume = 1.0 # 0 --> 1
        self.effectsVolume = 1.0 # same
        self.musicVolume = 1.0 # same
        self.muteMusic = False
        self.muteEffects = False

        #self.Fullscreen = False #use self.videoModes & FULLSCREEN to test if is fullscreen instead.
        #self.targetFPS = 60
        self.totalPigeon = 0
        self.score = 0
        
        self.optionsScreen = Options(self)
        self.optionsScreen.visible = False
        self.optionsScreen.enabled = False
    #--------------------------__init__(self)--------------------------------

    def Update(self, updateTimeDifference):
        """Updates the game.
            updateTimeDifference = time between the current and the previous call to this
            method, in milliseconds."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.Exit()
            elif event.type == KEYDOWN or event.type == KEYUP:
                self.HandleInput(event)

        if self.currentGameElement.enabled:
            self.currentGameElement.Update(updateTimeDifference)
        else:
            self.optionsScreen.Update(updateTimeDifference)

        if pygame.mixer.music.get_busy():
            bgmVol = self.audioVolume * self.musicVolume
            pygame.mixer.music.set_volume(bgmVol)
                
        #TODO: Implement your update logic here
    #----------------------Update(self, updateTimeDifference)-------------------------------

    def Draw(self, updateTimeDifference):
        """Draws the game. If the game is having problems reaching the targetFPS it will
            skip some calls to this method in a atempt to guarantee at least the update rate.
            All the inner game logic should be present at the Update method, use this exclusively
            to draw whenever possible.
            updateTimeDifference = time between the two last calls of the Update method."""
        self.screen.fill( (255, 255, 255) )

        if self.currentGameElement.visible:
            self.currentGameElement.Draw(updateTimeDifference)
        else:
            self.optionsScreen.Draw(updateTimeDifference)
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
        self.screen = pygame.display.set_mode(self.resVal, self.videoModes, self.colorDepth)
        self.currentGameElement.AlterResolution(self.resolution)
        self.optionsScreen.AlterResolution(self.resolution)


    def ResetSoundSettings(self):
        pygame.mixer.quit()
        pygame.mixer.init(self.soundFrequency, self.soundSize, self.soundChannels, self.soundBuffer)


    def HandleInput(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN and event.mod & KMOD_ALT:
                self.ToggleFullscreen()
            elif event.key == K_F4 and event.mod & KMOD_ALT:
                pygame.event.post(pygame.event.Event(QUIT))
            elif isinstance(self.currentGameElement, TitleScreen):
                if event.key == K_1:
                    self.StartGame(1)
                elif event.key == K_2:
                    self.StartGame(2)
                elif event.key == K_3:
                    self.StartGame(3)
                elif event.key == K_4:
                    self.StartGame(4)
                elif event.key == K_5:
                    self.StartGame(5)
                elif event.key == K_6:
                    self.StartGame(6)

    def ToggleFullscreen(self):
        self.videoModes = self.videoModes ^ FULLSCREEN
        self.ResetDisplayMode()

    def ToggleOptionsScreen(self):
        self.optionsScreen.visible = not self.optionsScreen.visible
        self.optionsScreen.enabled = not self.optionsScreen.enabled
        self.currentGameElement.visible = not self.optionsScreen.visible
        self.currentGameElement.enabled = not self.optionsScreen.enabled
        if self.optionsScreen.enabled:
            self.optionsScreen.PrepareToShow()

    def StartGame(self, level):
        pygame.mixer.music.stop()
        if level == 1:
            self.score = 0
        self.currentGameElement = None
        #self.currentGameElement = GameStage(self, level)
        self.currentGameElement = GameStage(self, level)
        self.currentGameElement.Update(0)#this avoid a call to draw before at least one update has happened


    def ShowTitle(self):
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        self.score = 0
        self.totalPigeon = 0
        self.currentGameElement = None
        self.currentGameElement = TitleScreen(self)
        self.currentGameElement.Update(0)
#--------------------------------------MainGame(GameLoopManager)-----------------------------------------


Game = MainGame()
Game.Run()



