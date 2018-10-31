

__author__="Adriano"
__date__ ="$Jan 27, 2010$"

from gameelement import *
from gameelement import GameElement #Appeasing netbeans
import pygame

class TitleScreen(GameElement):
    BG = "_titlescreen_bg.png"
    CURSOR = "_cursor.png"
    OPTIONS = "_titlescreen_options.png"
    SELECTION_MARK = "_titlescreen_selected.png"
    CREDITS = "_credits.png"



    def __init__(self, maingame):
        """
        Defines the Title Screen of the game (with all options). Do not
        call pygame init again, it is called on the main game.
            Params:
            maingame ->> The instance of our custom subclass of GameLoopManager
                that is controling the game.
        """
        GameElement.__init__(self, maingame)        

        #Renderables
        self.semipath = "Image\\" + maingame.resolution
        self.background = pygame.image.load(self.semipath + TitleScreen.BG).convert()
        self.cursor = pygame.image.load(self.semipath+TitleScreen.CURSOR).convert_alpha()
        self.options = pygame.image.load(self.semipath+TitleScreen.OPTIONS).convert_alpha()
        self.selectionMark = pygame.image.load(self.semipath+TitleScreen.SELECTION_MARK).convert_alpha()
        self.credits = pygame.image.load(self.semipath+TitleScreen.CREDITS).convert_alpha()
        
        #Control
        self.timeWithNoSong = 60000 #milliseconds, it restarts the song one minute after it has ended.

        self.cursorX, self.cursorY = pygame.mouse.get_pos()
        self.cursorX = self.cursorX/self.maingame.resVal[0]
        self.cursorY = self.cursorY/self.maingame.resVal[1]
        #mouse cursor and everything else are handled in percents.

        #buttons['N'] = (X, Y)
        #these were mensured from the original .png files, and
        #reflect the positions they occupy on the screen.
        self.buttons = {
            'PLAY'    : (0.648, 0.487),
            'OPTIONS' : (0.716, 0.608),
            'CREDITS' : (0.784, 0.723),
            'EXIT'    : (0.851, 0.845)}

        self.buttonDimensions = (0.117,0.111)
        self.selectedBT = None
        self.previousMouseBtStates = pygame.mouse.get_pressed()

        pygame.mouse.set_visible(False)

        self.showingCredits = False

        #Sound and music
        pygame.mixer.music.load(r"Music\Intro.ogg")
        self.startGame = pygame.mixer.Sound(r"SoundFX\zoom.ogg")
        self.selectOption = pygame.mixer.Sound(r"SoundFX\xylophone.ogg")


    def Update(self, updateTimeDifference):
        #handling bgm
        if not pygame.mixer.music.get_busy():
            self.timeWithNoSong += updateTimeDifference


        if self.timeWithNoSong >= 60000:
            self.timeWithNoSong = 0
            #self.maingame.bgmChannel.play(self.bgm)
            pygame.mixer.music.play()

        #updates Cursor and handles mouse
        tempCursorX, tempCursorY = pygame.mouse.get_pos()
        tempCursorX = tempCursorX/self.maingame.resVal[0]
        tempCursorY = tempCursorY/self.maingame.resVal[1]
        self.cursorX += (tempCursorX - self.cursorX)
        self.cursorY += (tempCursorY - self.cursorY)

        currentMouseBtState = pygame.mouse.get_pressed()

        #handling option selection
        self.selectedBT = None
        if not self.showingCredits:
            for btName, pos in self.buttons.items():
                if self.cursorX >= pos[0] and self.cursorX < pos[0]+ self.buttonDimensions[0]:
                    if self.cursorY >= pos[1] and self.cursorY < pos[1]+ self.buttonDimensions[1]:
                        self.selectedBT = pos
                        break
                

        #hanlding click
        if self.showingCredits:
            if currentMouseBtState[0] and not self.previousMouseBtStates[0]:
                self.showingCredits = False
        elif currentMouseBtState[0] and not self.previousMouseBtStates[0] and self.selectedBT:
            if self.selectedBT == self.buttons['EXIT']:
                self.maingame.Exit()
            elif self.selectedBT == self.buttons['CREDITS']:
                self.showingCredits = True
            elif self.selectedBT == self.buttons['OPTIONS']:
                self.selectedBT = None
                self.maingame.ToggleOptionsScreen()
            elif self.selectedBT == self.buttons['PLAY']:
                pygame.mixer.music.stop()
                self.maingame.StartGame(1)

        self.previousMouseBtStates = currentMouseBtState
        currentMouseBtState = None

    #------------------def Update()-------------------------------
    def Draw(self, updateTimeDifference):
        self.maingame.screen.blit(self.background, (0,0))

        if self.selectedBT:
            self.maingame.screen.blit(
            self.selectionMark,( (self.selectedBT[0]-0.028)* self.maingame.resVal[0],
            (self.selectedBT[1]-0.016) * self.maingame.resVal[1] ))

        self.maingame.screen.blit(self.options, (0.68 * self.maingame.resVal[0],0.49 * self.maingame.resVal[1] ))
        
        if self.showingCredits:
            self.maingame.screen.blit(self.credits, (0,0))

        self.maingame.screen.blit(self.cursor, ((self.cursorX - 0.018) * self.maingame.resVal[0], self.cursorY * self.maingame.resVal[1]) )


    #----------------def Draw()----------------------------
    def AlterResolution(self, newResolution):
        self.semipath = "Image\\" + newResolution
        self.background = pygame.image.load(self.semipath + TitleScreen.BG).convert()
        self.cursor = pygame.image.load(self.semipath+TitleScreen.CURSOR).convert_alpha()
        self.options = pygame.image.load(self.semipath+TitleScreen.OPTIONS).convert_alpha()
        self.selectionMark = pygame.image.load(self.semipath+TitleScreen.SELECTION_MARK).convert_alpha()
        self.credits = pygame.image.load(self.semipath+TitleScreen.CREDITS).convert_alpha()