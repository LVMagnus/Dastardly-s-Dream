

__author__="Luiz de Mello"
__date__ ="$Jan 30, 2010$"

PLAYING = 0
PAUSE = 1
STAGE_END = 2
GAME_OVER = 3
CONGRATULATIONS = 4

#imports
from gameelement import GameElement
from pigeon import Pigeon
import random
import pygame
from pygame.locals import *
#--------------------

class GameStage(GameElement):
    #Unlike the other GameElements, the metrics on this are on pixesl rather than
    #percents. Since the image files are the same for all resolution, everything
    #is just scaled down or up to match the 1024x800 resolution (the same used on
    #the image files) when dealing with logic, then scaled back to the active
    #resolution when drawing.
    def __init__(self, maingame, level):
        GameElement.__init__(self, maingame)

        #General-------------------------
        self.level = level
        self.state = PLAYING        
        self.scale = (1024/maingame.resVal[0], 768/maingame.resVal[1]  )
        self.previousMouseState =(0,0,0)
        self.cursorX = 0
        self.cursorX, self.cursorY = pygame.mouse.get_pos()
        self.shotCooldown = 1000
        self.shotCountdown = 0
        self.timeWithNoSound = 0


        #Pigeon related--------------------------
        self.releasedPigeons = 0
        self.totalWaves = 10 + 5 * (level//2)
        self.pigeonsHit = 0
        self.pigeonsPerWave = 2 - (level % 2) #1 piegon on odd levels, 2 on even levels.
        self.totalPigeons = self.pigeonsPerWave * self.totalWaves
        self.pigeons = []
        self.goalKills = self.totalPigeons//2

        #Important
        self.maingame.totalPigeon += self.totalPigeons

        #Renderables (Images and Font)-----------------
        #pause screen
        self.pauseScreenBG = pygame.Surface((1024,768))
        self.pauseScreenBG.fill( (0x14, 0x3D, 0x3D))
        self.pauseScreenBG.set_alpha(204) #80% opaque

        self.pauseFont = pygame.font.Font(r"Font\maturasc.ttf",50)
        self.pauseFontColor = (0xFF, 0x59, 0x59)
        
        #hud
        self.hudBG = pygame.Surface((1024,68))
        self.hudBG.fill( (0, 0, 0))
        self.hudBG.set_alpha(int(255*0.7))
        self.hudFont = pygame.font.Font(r"Font\harngton.ttf", 35)

        #general
        self.background = pygame.image.load(r"Image\gamescreen_bg.png").convert()
        self.cursor = pygame.image.load(r"Image\1024x768_cursor.png").convert_alpha() #it will also be scaled
        self.crosshair = pygame.image.load(r"Image\crosshair.png").convert_alpha()
        self.selectionMark = pygame.image.load(r"Image\gamescreen_selected.png").convert_alpha()

        #game over
        self.gameoverBG = pygame.Surface((1024,768))
        self.gameoverBG.fill( (0, 0, 0))
        self.gameoverBG.set_alpha(0)

        self.gameoverImg = pygame.image.load(r"Image\gamescreen_gameover.png").convert_alpha()

        #Congratulations
        self.congratsImg = pygame.image.load(r"Image\gamescreen_gameend.png").convert_alpha()
        self.congratsMedal = pygame.image.load(r"Image\gamescreen_medal.png").convert_alpha()
        
        #Sounds---------------------------------
        self.bgm = (
            pygame.mixer.Sound(r"SoundFX\bird_tweet.ogg"),
            pygame.mixer.Sound(r"SoundFX\bird_tweet_2.ogg"),
            pygame.mixer.Sound(r"SoundFX\bird_tweet_3.ogg"),
            pygame.mixer.Sound(r"SoundFX\bird_tweet_4.ogg"),
            pygame.mixer.Sound(r"SoundFX\pigeon_wings.ogg"))
        
        #That is not a 'real' bgm, but will work as one built
        #randomly and dynamically. The pieces are on the SoundFX instead of the
        #Music folder since individually they're sound effects.

        self.gunfire = pygame.mixer.Sound(r"SoundFX\shot.wav")
        self.gameoverSound = pygame.mixer.Sound(r"SoundFX\that_dog_laughing.wav")#using music volume for consistency

        self.gameendSound = pygame.mixer.Sound(r"Music\stageend.ogg")#


        #Pause menu-------------------------
        #buttons (center X, Y), (width, height), label = Button text
        self.pauseBts = {
            'Return'   : ((512, 291), self.pauseFont.size('Return')),
            'Options'  : ((512, 378), self.pauseFont.size('Options')),
            'End Game' : ((512, 462), self.pauseFont.size('End Game')),
            'Yes'      : ((765, 425), self.pauseFont.size('Yes')),
            'No'       : ((765, 505), self.pauseFont.size('No'))}
        
        self.confirmEndGame = False
        self.pauseBtSel = []

        #Game Over----------------
        self.gameoverCountdown = 0
        self.gameoverFullimg = False
        

    #--------------------__init__()------------s
    def Update(self, updateTimeDifference):
        currentMouseState = pygame.mouse.get_pressed()
        self.cursorX, self.cursorY = pygame.mouse.get_pos()
        self.cursorX *= self.scale[0]
        self.cursorY *= self.scale[1]
        hasClicked = self.previousMouseState[0] == 0 and currentMouseState[0] == 1
        hasRightClicked = self.previousMouseState[2] == 0 and currentMouseState[2] == 1
        pigLen = len(self.pigeons)

        if self.state == PLAYING:
            if hasRightClicked:
                self.state = PAUSE
            else:                
                if self.shotCountdown <= 0:
                    hasShot = hasClicked and self.state == PLAYING and pigLen > 0
                    if hasShot:
                        self.shotCountdown = self.shotCooldown
                        self.gunfire.stop()
                        self.gunfire.set_volume(self.maingame.audioVolume * self.maingame.effectsVolume)
                        self.gunfire.play()
                else:
                    hasClicked = False #somehow this makes the sound work regularly
                    hasShot = False
                    self.shotCountdown -= updateTimeDifference

                
                if pigLen != 0: #regular game
                    for i in range(0, pigLen):
                        hit = self.pigeons[i].Update(updateTimeDifference, self.cursorX, self.cursorY, hasClicked)
                        if hit:
                            self.pigeonsHit += 1
                        if self.pigeons[i].mustBeRemoved:
                            del self.pigeons[i]
                            break
                else: #Stage end, congratulations, Game over and pigeon spaw
                    if self.releasedPigeons == self.totalPigeons:
                        if self.pigeonsHit >= self.goalKills:
                            if self.level != 6:
                                pygame.mixer.stop()
                                self.state = STAGE_END
                                self.maingame.score += self.pigeonsHit
                            else:
                                pygame.mixer.stop()
                                self.state = CONGRATULATIONS
                                self.maingame.score += self.pigeonsHit
                        else:
                            pygame.mixer.stop()
                            self.state = GAME_OVER
                            self.maingame.score += self.pigeonsHit
                    elif (self.totalPigeons - self.releasedPigeons) + self.pigeonsHit < self.goalKills:
                        pygame.mixer.stop()
                        self.state = GAME_OVER
                        self.maingame.score += self.pigeonsHit
                    elif self.releasedPigeons < self.totalPigeons: #check if all pigeons are dead, but game still runs
                        self.UnleashPigeons()
                    
                #-------if PigLen, else-------------------
                #Playing sound
                self.timeWithNoSound += updateTimeDifference
                if self.timeWithNoSound >= 2000:
                    self.timeWithNoSound -= 2000
                    i = random.randint(0, len(self.bgm)-1)
                    self.bgm[i].set_volume(self.maingame.audioVolume * self.maingame.musicVolume)
                    self.bgm[i].play()
            #--------------if hasRightClicked----------------
        #------------------if self.state == PLAYING--------------
        elif self.state == PAUSE:
            if hasRightClicked:
                self.state = PLAYING
            else:
                self.pauseBtSel = []
                if not self.confirmEndGame:                    
                    for name, metrics in self.pauseBts.items():
                        bbox = Rect(
                            (metrics[0][0] - metrics[1][0]//2, metrics[0][1] - metrics[1][1]//2),
                            (metrics[1][0], metrics[1][1]))
                        if bbox.collidepoint(self.cursorX//1, self.cursorY//1) and name not in ['Yes','No']:
                            self.pauseBtSel = metrics                            
                            break

                    if self.pauseBtSel != [] and hasClicked:
                        if self.pauseBtSel == self.pauseBts['Return']:
                            self.state = PLAYING
                        elif self.pauseBtSel == self.pauseBts['Options']:
                            self.maingame.ToggleOptionsScreen()
                        elif self.pauseBtSel == self.pauseBts['End Game']:
                            self.confirmEndGame = True
                else:
                    for name, metrics in self.pauseBts.items():
                        bbox = Rect(
                            (metrics[0][0] - metrics[1][0]//2, metrics[0][1] - metrics[1][1]//2),
                            (metrics[1][0], metrics[1][1]))
                        if bbox.collidepoint(self.cursorX//1, self.cursorY//1) and name in ['Yes','No']:
                            self.pauseBtSel = metrics
                            break

                    if self.pauseBtSel != [] and hasClicked:
                        if self.pauseBtSel == self.pauseBts['Yes']:
                            self.maingame.ShowTitle()                            
                        elif self.pauseBtSel == self.pauseBts['No']:
                            self.confirmEndGame = False
                #---------------if not confirmExit,else-------------------------
            #--------------------if hasRightClicked,else------------------------
        #-------------------------elif state == Pause---------------------------
        elif self.state == GAME_OVER:
            self.gameoverCountdown += updateTimeDifference
            if self.gameoverCountdown-updateTimeDifference == 0:
                pass #used to play the sound here
            elif 200 < self.gameoverCountdown  <= 3000:
                self.gameoverBG.set_alpha( int( 255 *((self.gameoverCountdown-200)/2800) ) )
                if self.gameoverCountdown> 500 and self.gameoverCountdown - updateTimeDifference < 500:#if it is the first update after reaching or passing 500
                    self.gameoverSound.set_volume(self.maingame.audioVolume * self.maingame.musicVolume)
                    self.gameoverSound.play()
            elif self.gameoverCountdown > 3000:
                if hasClicked:
                    self.maingame.ShowTitle()                    
                elif self.gameoverCountdown >= 3500: #loop counting
                    self.gameoverCountdown = 3001
                    self.gameoverFullimg = not self.gameoverFullimg                    

        elif self.state == STAGE_END:
            self.maingame.StartGame(self.level+1)
        
        else: #then it is congratulations            
            self.gameoverCountdown += updateTimeDifference
            if self.gameoverCountdown-updateTimeDifference == 0:
                self.gameendSound.set_volume(self.maingame.audioVolume * self.maingame.musicVolume)
                self.gameendSound.play()
            elif self.gameoverCountdown > 11000:
                self.gameoverFullimg = True
                if hasClicked:
                    self.maingame.ShowTitle()
                    



        self.previousMouseState = currentMouseState
        
    #----------------Update()-------------------
    def Draw(self, updateTimeDifference):
        tempScreen = pygame.Surface((1024,768)).convert()
        #BG
        tempScreen.blit(self.background, (0,0))

        #pigeons
        for P in self.pigeons:
            P.Draw(tempScreen)

        #HUD
        if self.state != CONGRATULATIONS:
            tempScreen.blit(self.hudBG,(0,700))

            height = [40, 0]
            width = []
            width.append(self.hudFont.size("Level: 20"))
            height[0] += width[0][0] #1
            height[1] = width[0][1] #same value for all, so won't collect it again

            width.append(self.hudFont.size("Pigeons: 40 / 40"))
            height[0] += width[1][0] #2

            width.append(self.hudFont.size("Killed: 40"))
            height[0] += width[2][0] #3

            width.append(self.hudFont.size("Goal: 20"))
            height[0] += width[3][0] #4

            height[0] = 1024 - height[0] #total width - unspaced total text width
            height[0] /= 3 #Text_Text_Text_Text = 3 spaces in between (total -1)

            #discarding duplicated values while getting the final metrics
            width[0] = width[0][0] + height[0]
            for i in range(1, len(width)):
                width[i] = width[i-1] + width[i][0]+height[0]

            height = (height[1]/2) * 0.6 #measured size includes some extra pixesl for
                                         #line spacing, but that is not needed here

            #finally blitting text on the hud
            text = "Level: {}".format(self.level)
            textImg = self.hudFont.render(text, True, (255,255,255))
            tempScreen.blit(textImg, (20, 700 + height))

            text = "Pigeons: {} / {}".format(self.releasedPigeons, self.totalPigeons)
            textImg = self.hudFont.render(text, True, (255,255,255))
            tempScreen.blit(textImg, (20 + width[0], 700 + height))

            text = "Killed: {}".format(self.pigeonsHit)
            textImg = self.hudFont.render(text, True, (255,255,255))
            tempScreen.blit(textImg, (20 + width[1], 700 + height))

            text = "Goal: {}".format(self.goalKills)
            textImg = self.hudFont.render(text, True, (255,255,255))
            tempScreen.blit(textImg, (20 + width[2], 700 + height))

        #pause Game Drawing
        if self.state == PAUSE:
            tempScreen.blit(self.pauseScreenBG, (0,0))

            if self.pauseBtSel != []:
                tempScreen.blit(self.selectionMark,
                (self.pauseBtSel[0][0] - self.selectionMark.get_width()//2,
                self.pauseBtSel[0][1] - self.selectionMark.get_height()//2))

            for name, metrics in self.pauseBts.items():
                if self.confirmEndGame:
                    tempScreen.blit(self.pauseFont.render(name, True, self.pauseFontColor),
                        (metrics[0][0] - metrics[1][0]//2, metrics[0][1] - metrics[1][1]//2))
                elif name not in ['Yes', 'No']:
                    tempScreen.blit(self.pauseFont.render(name, True, self.pauseFontColor),
                        (metrics[0][0] - metrics[1][0]//2, metrics[0][1] - metrics[1][1]//2))

        elif self.state == GAME_OVER:
            #bg
            tempScreen.blit(self.gameoverBG, (0,0))
            #Score
            text = 'Score: {}'.format(self.maingame.score)
            metrics = self.pauseFont.size(text)
            tempScreen.blit(self.pauseFont.render(text, True, (255,255,255)),
            (512 - metrics[0]//2, 327 - metrics[1]//2-60))

            #Game over /Click anywhere img
            if self.gameoverFullimg:
                tempScreen.blit(self.gameoverImg, (0, 327))
            else:
                tempScreen.blit(self.gameoverImg.subsurface( (0,0),(1024, 115)),
                (0, 327))

        elif self.state == CONGRATULATIONS:
            tempScreen.blit(self.congratsImg, (0,65))
            if self.maingame.score/self.maingame.totalPigeon < 0.75:
                medal = 0
            elif self.maingame.score/self.maingame.totalPigeon < 0.95:
                medal = 1
            else:
                medal = 2

            tempScreen.blit(self.congratsMedal.subsurface((206*medal,0), (206, 306)),
                (409,333)) #measured when creating the layout
            size = self.pauseFont.size('{}'.format(self.maingame.score))
            size = size[0]
            text = self.pauseFont.render('{}'.format(self.maingame.score),True, (0, 0, 0), (1,1,1)).convert()
            text.set_colorkey( (1,1,1) )
            text.set_alpha(int(255*0.4))
            tempScreen.blit(text,
                ( 512 - size/2, 542))#half measured when creating the layout

            if self.gameoverFullimg: #read as: gameendShowClickMSG
                size = self.pauseFont.size('Click Anywhere')
                size = size[0]
                tempScreen.blit(self.pauseFont.render('Click Anywhere',True, (255, 255, 255)),
                    ( 512 - size/2, 669))#half measured when creating the layout
        
        #Aim or Cursor
        if self.state in (PLAYING, STAGE_END):
            if self.shotCountdown <= 0:
                subsurfaceCrosshair = self.crosshair.subsurface( (0, 0), (self.crosshair.get_width(),self.crosshair.get_height()/2) )
            else:
                subsurfaceCrosshair = self.crosshair.subsurface( (0, self.crosshair.get_height()/2), (self.crosshair.get_width(), self.crosshair.get_height()/2) )

            tempScreen.blit(subsurfaceCrosshair, (self.cursorX-subsurfaceCrosshair.get_width()/2, self.cursorY-subsurfaceCrosshair.get_height()/2 ))
        else:
            tempScreen.blit(self.cursor, ( self.cursorX - (0.018 * 1024), self.cursorY) )


        #transfering from tempScreen to the real screen.
        if self.maingame.screen.get_bitsize() >= 24:
            tempScreen = pygame.transform.smoothscale(tempScreen, self.maingame.resVal)
        else:
            tempScreen = pygame.transform.scale(tempScreen, self.maingame.resVal)

        self.maingame.screen.blit(tempScreen, (0,0))
    
    #----------------------Draw()-----------------------------------------------
    def AlterResolution(self, newResolution):
        pass #since everything is always rescaled, this function has no purpose other than
            #compatibility

    def UnleashPigeons(self):
        self.pigeons = []
        self.shotCountdown = 0
        if self.level % 2 == 1:
            self.pigeons = [ Pigeon(self.level)]

        else:
            self.pigeons = [ Pigeon(self.level), Pigeon(self.level)]

        self.releasedPigeons += len(self.pigeons)
            #pigeons are more likely not the same, their init method randoms somethings.

#----------------------class Pigeon-----------------------------------------------------

