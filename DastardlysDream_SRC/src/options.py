

__author__="Adriano"
__date__ ="$Jan 28, 2010$"

#imports
from pygame.locals import *
from gameelement import *
import pygame
import math
#--------------------------

class Options(GameElement):
    BG = "_options_bg.png"
    CURSOR = "_cursor.png"
    OPTIONS = "_options_options.png"
    SELECTION_MARK = "_options_selected.png"
    SELECTION_MARK_B = "_titlescreen_selected.png" #same image, no need for storing 2 files.



    def __init__(self, maingame):
        """
        Defines the Options screen.        
            Params:
            maingame ->> The instance of our custom subclass of GameLoopManager
                that is controling the game.
        """
        GameElement.__init__(self, maingame)

        self.semipath = "Image\\" + maingame.resolution
        self.background = pygame.image.load(self.semipath + Options.BG).convert()
        self.cursor = pygame.image.load(self.semipath+Options.CURSOR).convert_alpha()
        self.options = pygame.image.load(self.semipath+Options.OPTIONS).convert_alpha()
        self.selectionMark = pygame.image.load(self.semipath+Options.SELECTION_MARK).convert_alpha()
        self.selectionMarkB = pygame.image.load(self.semipath+Options.SELECTION_MARK_B).convert_alpha()

        self.fontSize = 0.04036458333333
        self.font = pygame.font.Font("Font\\maturasc.ttf", int(math.ceil(self.fontSize * maingame.resVal[1])))


        self.cursorX, self.cursorY = pygame.mouse.get_pos()
        self.cursorX = self.cursorX/self.maingame.resVal[0]
        self.cursorY = self.cursorY/self.maingame.resVal[1]
        #mouse cursor and everything else are handled in percents.

        #(x,y, width, height)
        self.buttons = {
            'RES_MINUS'   : (0.445, 0.297, 0.038, 0.055),
            'RES_PLUS'    : (0.706, 0.297, 0.038, 0.055),
            'AUDIO_MINUS' : (0.543, 0.487, 0.038, 0.055),
            'AUDIO_PLUS'  : (0.674, 0.487, 0.038, 0.055),
            'MUSIC_MINUS' : (0.469, 0.586, 0.038, 0.055),
            'MUSIC_PLUS'  : (0.609, 0.586, 0.038, 0.055),
            'FX_MINUS'    : (0.474, 0.684, 0.038, 0.055),
            'FX_PLUS'     : (0.605, 0.684, 0.038, 0.055),
            'FULLSCREEN'  : (0.21 , 0.375, 0.578, 0.087),
            'APPLY'       : (0.125, 0.845, 0.18 , 0.145),
            'OK'          : (0.429, 0.845, 0.18 , 0.145),
            'CANCEL'      : (0.732, 0.845, 0.18 , 0.145)}

 

        self.highlightAreas = {
            'RESOLUTION' : (0.21 , 0.279, 0.578, 0.087),
            'FULLSCREEN' : (0.21 , 0.375, 0.578, 0.087),
            'AUDIO'      : (0.21 , 0.473, 0.578, 0.087),
            'MUSIC'      : (0.21 , 0.570, 0.578, 0.087),
            'EFFECTS'    : (0.21 , 0.668, 0.578, 0.087),
            'APPLY'      : (0.125, 0.845, 0.18, 0.145),
            'OK'         : (0.429, 0.845, 0.18, 0.145),
            'CANCEL'     : (0.732, 0.845, 0.18, 0.145)}
        
        self.selectedArea = None
        self.previousMouseBtStates = (False, False, False)

        
                
        
        #temp settings
        self.audioVol = 0
        self.musicVol = 0
        self.effectsVol = 0
        self.modes = 0
        self.resolution = ''
        self.resVal = None

        #bkp settings
        self._audioVol = 0
        self._musicVol = 0
        self._effectsVol = 0
        self._modes = 0
        self._resolution = ''
        self._resVal = None

        self.clickRepeatTimer = 0
        self.lastClickedButton = None
        
        pygame.mouse.set_visible(False)

    #--------------------init()--------------------------------
    def Update(self,updateTimeDifference):
        #updates Cursor and handles mouse
        tempCursorX, tempCursorY = pygame.mouse.get_pos()
        tempCursorX = tempCursorX/self.maingame.resVal[0]
        tempCursorY = tempCursorY/self.maingame.resVal[1]
        self.cursorX += (tempCursorX - self.cursorX)
        self.cursorY += (tempCursorY - self.cursorY)

        currentMouseBtState = pygame.mouse.get_pressed()



        #handling option selection
        self.selectedArea = None
        
        for _, area in self.highlightAreas.items():
            if self.cursorX >= area[0] and self.cursorX < area[0]+ area[2]:
                if self.cursorY >= area[1] and self.cursorY < area[1]+ area[3]:
                    self.selectedArea = area
                    break

        #self.modes = self.maingame.videoModes #it can be altered externally

        #hanlding click
        if currentMouseBtState[0] and not self.previousMouseBtStates[0] and self.selectedArea:
            if self.selectedArea == self.highlightAreas['CANCEL']:
                self.Cancel()                    
            elif self.selectedArea == self.highlightAreas['OK']:
                self.Ok()
            elif self.selectedArea == self.highlightAreas['APPLY']:
                self.Apply()
            elif self.selectedArea == self.highlightAreas['FULLSCREEN']:
                self.modes = self.modes ^ FULLSCREEN
            else:
                for _, area in self.buttons.items():
                    if self.cursorX >= area[0] and self.cursorX < area[0]+ area[2]:
                        if self.cursorY >= area[1] and self.cursorY < area[1]+ area[3]:
                            self.lastClickedButton = area
                            break
                
        elif currentMouseBtState[0]: #if left button is been held down
            if self.lastClickedButton: 
                self.clickRepeatTimer -= updateTimeDifference
                if self.clickRepeatTimer <= 0:
                    self.clickRepeatTimer = 200
                    if self.lastClickedButton == self.buttons['AUDIO_MINUS']:
                        self.audioVol = max( (self.audioVol - 0.050, 0.0) )
                    elif self.lastClickedButton == self.buttons['AUDIO_PLUS']:
                        self.audioVol = min( (self.audioVol + 0.050, 1.0) )
                    elif self.lastClickedButton == self.buttons['MUSIC_MINUS']:
                        self.musicVol = max( (self.musicVol - 0.050, 0.0) )                        
                    elif self.lastClickedButton == self.buttons['MUSIC_PLUS']:
                        self.musicVol = min( (self.musicVol + 0.050, 1.0) )
                    elif self.lastClickedButton == self.buttons['FX_MINUS']:
                        self.effectsVol = max( (self.effectsVol - 0.050, 0.0) )
                    elif self.lastClickedButton == self.buttons['FX_PLUS']:
                        self.effectsVol = min( (self.effectsVol + 0.050, 1.0) )
                    elif self.lastClickedButton == self.buttons['RES_MINUS']:
                        self.clickRepeatTimer = 1000 #regular click echo didn't work well for this option
                        prev = None                        
                        for res in self.maingame.Resolutions.items():
                            if res[1] == self.resVal:
                                break
                            else:
                                prev = res
                                
                        if prev:
                            self.resolution = prev[0]
                            self.resVal = prev[1]
                    elif self.lastClickedButton == self.buttons['RES_PLUS']:
                        self.clickRepeatTimer = 1000 #regular click echo didn't work well for this option
                        next = None
                        for res in self.maingame.Resolutions.items():
                            if next is not None:
                                next = res
                                break
                            elif res[1] == self.resVal:
                                next = res #flagging that current value was found                                

                        if next[1] != self.resVal: #if not the last
                            self.resolution = next[0]
                            self.resVal = next[1]

        else:
            self.lastClickedButton = None
            self.clickRepeatTimer = 0       

        self.previousMouseBtStates = currentMouseBtState
        currentMouseBtState = None

        self.maingame.audioVolume = self.audioVol
        self.maingame.musicVolume = self.musicVol
        self.maingame.effectsVolume = self.effectsVol
        

    #------------------def Update()-------------------------------
    def Draw(self, updateTimeDifference):
        #bg
        self.maingame.screen.blit(self.background, (0,0))

        if self.selectedArea in (self.highlightAreas['OK'], self.highlightAreas['APPLY'], self.highlightAreas['CANCEL']):
            self.maingame.screen.blit(self.selectionMarkB, (self.selectedArea[0]* self.maingame.resVal[0],self.selectedArea[1]*self.maingame.resVal[1]))
        elif self.selectedArea: # != None
            self.maingame.screen.blit(self.selectionMark, (self.selectedArea[0]* self.maingame.resVal[0],self.selectedArea[1]*self.maingame.resVal[1]))

        #resolution
        text = self.resolution
        textDimension = self.font.size(text)
        fontPos = ((0.5957 - (textDimension[0]*0.5/self.maingame.resVal[0] ))*self.maingame.resVal[0],
            math.ceil(0.305 * self.maingame.resVal[1]))
        self.maingame.screen.blit(self.font.render(text, True, (0xFF,0x59,0x59)), fontPos)

        #fullscreen
        if self.modes & FULLSCREEN:
            text = " [+]"
        else:
            text=" [  ]"
        fontPos = (0.5547*self.maingame.resVal[0],
            math.ceil(0.40 * self.maingame.resVal[1]))
        self.maingame.screen.blit(self.font.render(text, True, (0xFF,0x59,0x59)), fontPos)


        #audio volume
        text = str(int(math.ceil(self.audioVol*100)))
        textDimension = self.font.size(text)
        fontPos = ((0.6274 - (textDimension[0]*0.5/self.maingame.resVal[0] ))*self.maingame.resVal[0],
            math.ceil(0.49 * self.maingame.resVal[1]))
        #the line above horizontally centers the text in a specific position and sets its proper height
        #the following two fields work likewise
        self.maingame.screen.blit(self.font.render(text, True, (0xFF,0x59,0x59)), fontPos)

        #music volume
        text = str(int(math.ceil(self.musicVol*100)))
        textDimension = self.font.size(text)
        fontPos = ((0.5649 - (textDimension[0]*0.5/self.maingame.resVal[0] ))*self.maingame.resVal[0],
            math.ceil(0.59 * self.maingame.resVal[1]))
        self.maingame.screen.blit(self.font.render(text, True, (0xFF,0x59,0x59)), fontPos)

        #FX volume
        text = str(int(math.ceil(self.effectsVol*100)))
        textDimension = self.font.size(text)
        fontPos = ((0.5601 - (textDimension[0]*0.5/self.maingame.resVal[0] ))*self.maingame.resVal[0],
            math.ceil(0.69 * self.maingame.resVal[1]))
        self.maingame.screen.blit(self.font.render(text, True, (0xFF,0x59,0x59)), fontPos)

        self.maingame.screen.blit(self.options, (0, 0))
        self.maingame.screen.blit(self.cursor, ((self.cursorX - 0.018) * self.maingame.resVal[0], self.cursorY * self.maingame.resVal[1]) )
        


    #----------------def Draw()----------------------------
    def AlterResolution(self, newResolution):
        self.semipath = "Image\\" + newResolution
        self.background = pygame.image.load(self.semipath + Options.BG).convert()
        self.cursor = pygame.image.load(self.semipath+Options.CURSOR).convert_alpha()
        self.options = pygame.image.load(self.semipath+Options.OPTIONS).convert_alpha()
        self.selectionMark = pygame.image.load(self.semipath+Options.SELECTION_MARK).convert_alpha()
        self.selectionMarkB = pygame.image.load(self.semipath+Options.SELECTION_MARK_B).convert_alpha()
        self.font = pygame.font.Font("Font\\maturasc.ttf", int(math.ceil(self.fontSize * self.maingame.resVal[1])))


    def PrepareToShow(self):
        self.audioVol = self.maingame.audioVolume
        self.musicVol = self.maingame.musicVolume
        self.effectsVol = self.maingame.effectsVolume
        self.modes = self.maingame.videoModes
        self.resolution = self.maingame.resolution
        self.resVal = self.maingame.resVal

        self._audioVol = self.maingame.audioVolume
        self._musicVol = self.maingame.musicVolume
        self._effectsVol = self.maingame.effectsVolume
        self._modes = self.maingame.videoModes
        self._resolution = self.maingame.resolution
        self._resVal = self.maingame.resVal

        self.clickRepeatTimer = 0
        self.lastClickedButton = None

    def Cancel(self):
        self.audioVol = self._audioVol
        self.musicVol = self._musicVol
        self.effectsVol = self._effectsVol
        self.modes = self._modes
        self.selectedArea = None
        self.maingame.ToggleOptionsScreen()
        

    def Apply(self):
        self._audioVol = self.audioVol
        self._musicVol = self.musicVol
        self._effectsVol = self.effectsVol
        self._modes = self.modes

        self.maingame.resolution = self.resolution
        self.maingame.resVal = self.maingame.Resolutions[self.resolution]
        self.maingame.videoModes = self.modes
        self.maingame.ResetDisplayMode()

    def Ok(self):
        self.Apply()
        self.selectedArea = None
        self.maingame.ToggleOptionsScreen()