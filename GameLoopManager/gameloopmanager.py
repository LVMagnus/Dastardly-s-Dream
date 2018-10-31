"""This module defines the GameLoopManager. Do not instantiate directly (inherit and customize your class, then instantiate it)."""


__author__="Luiz de Mello"
__date__ ="$Jan 22, 2010 6:04:50 AM$"

if __name__ != "__main__":

    #imports
    import pygame
    from datetime import *
    from time import *
    from sys import exit
    from pygame.locals import *
    #-------------------------


    class GameLoopManager:
        """The main objective of this class is to manage the main game flow. It provides methods
        for automatic updates and drawing. Should not be instantiated directly. Rather, derive
        your own class from it, override its Update and Draw methods, customize any properties
        that you wish on its constructor (do not forget to call this class' __init__ method),
        instantiate your class and call the instance's Run() method.

        Attributes:
        targetFPS ->> value must be greater than 0, and indicates the desired Frames Per Second
            that the game will achieve. The game won't run faster than this value, but is not
            guaranteed how slower it will be (depends on how much time Draw() and Update() are
            taking to be processed).
            Default value: 30.

        frameSlowDownTolerance ->> express, in percents, a tolerance value for the time consumed
            by the Update() method before it is considered to have taken to long and skip a
            Draw() call. For example, for the default FPS each frame takes about 16.7 ms or less
            to process on an ideal situation. If this value is 1.1 (the default, which means
            110%) then if it takes up to 18.37 (16.7 * 110%) the GameLoopManager will consider
            that it is running on an accetable time and shouldn't be skipping a call toDraw().
            Default value: 1.1.

        drawSkipLimit ->> also in percents, but the value should be such that 0 <= value <= 1
            is true. It determines how many calls to Draw() can be skipped due to a slow
            running game before enforcing an obrigatory call. For example, for the default FPS
            of 60 and the default drawSkipLimit of 0.1 it would skip up to 6 Draw() calls in a
            row, but the seventh time it attempted to skip would enforce a compulsory call,
            then the cycle would restart.
            Default value: 0.1.

        perecentageConsideredSlow ->> another perecentage. The values are recommended to be
            greater than 0.5 and smaller or equal to 1. The GameLoopManager uses this value to
            determine if the game is running slow and set the isSlow property (see bellow).
            When the game has completed a number of calls to Update() equal to its targetFPS
            it will compare with the number of calls to Draw. If Draw() was called a number of
            times greater or equal to targetFPS * percentageConsideredSlow it will consider
            that the speed is okay and set isSlow to False, but true if it is smaller than
            that. Therefore, 0 or less means that it will never consider the game slow, and 1
            will consider it slow if the Draw() calls are not on par with the calls to
            Update(), and anything greater means it is always considered slow.
            Default value: 0.8.

        isSlow ->> Should be used as read only (the class does not use it on its internal
            routines, it is only informative). It points if the game is been considered to be
            running slow or not. See the above property to understand how the game calculates
            it. By consulting this property you can use it to enforce optmization routines.
            Default value: False.


        Notice that due to performance optmization there is no routine to enforce valid values.
        Those attributes are not meant to be altered often (usually only at your own class
        initialization, if altered at all), so there the required attention to them will hardly
        impact development time.
        """


        def __init__(self):
            self.targetFPS = 60
            self.frameSlowDownTolerance = 1.1 
            self.drawSkipLimit = 0.1
            self.perecentageConsideredSlow = 0.8
            self.isSlow = False


            self.__updateTimeCounter = 0
            self.__updatesCounter = 0
            self.__drawsCounter = 0
            self.__skippedDrawsCounter = 0


        #-------------------def __init__()-------------------------

        def Update(self, updateTimeDifference):
            """Updates the game.
            updateTimeDifference = time between the current and the previous call to this
            method, in milliseconds."""
            pass



        def Draw(self, updateTimeDifference):
            """Draws the game. If the game is having problems reaching the targetFPS it will
            skip some calls to this method to atempt to keep at least the desired update rate.
            All the inner game logic should be present at the Update method, use this exclusively
            to draw whenever possible.
            updateTimeDifference = time between the two last calls of the Update method."""
            pass



        def OnExit(self):
            """Override this methond and implement here any logic you may wish to run just before leaving the game (such as saving a file).
            Your logic must return two values. The first must be either True or False that will control if the application
            will indeed quite (True) or not (False). The second should be 0 or an error message/code that will be used when
            calling sys.exit(). Observe that this will only be called if you call the instance method Exit()."""
            return True, 0



        def Exit(self):
            """Executes the OnExit() function and quits if that function returns True as it first return value, but does nothing if it
            returns False."""
            notTooLegit, ErrorC = self.OnExit()
            if notTooLegit: #then you quit!
                exit(ErrorC)


        def Run(self):
            """Call it once from your instance to run your game. Do not override."""
            self.Update(0) #initial calls to update and draw before anything else
            self.Draw(0)
            
            clockTower = pygame.time.Clock()
            elapsedTime = 0

            while True:
                elapsedTime = clockTower.tick(self.targetFPS) #time is given in millis. See pygame's reference for more info

                self.Update(elapsedTime)
                self.__updatesCounter += 1

                targetAverageFrameTime = 1000/self.targetFPS
                #skips the call to Draw if update took too long and if it didn't skip too many calls already
                if elapsedTime-targetAverageFrameTime <= targetAverageFrameTime * self.frameSlowDownTolerance or self.__skippedDrawsCounter >= self.targetFPS * self.drawSkipLimit:
                    self.Draw(elapsedTime)
                    self.__drawsCounter +=1
                    self.__skippedDrawsCounter = 0
                else:
                    self.__skippedDrawsCounter += 1


                if self.__updatesCounter >= self.targetFPS:
                    if self.__drawsCounter >= self.targetFPS * self.perecentageConsideredSlow:
                        self.isSlow = False
                    else:
                        self.isSlow = True

                    self.__updatesCounter = 0
                    self.__drawsCounter = 0

            #-----------------while True----------------------------

        #---------------------def Run(self)------------------------

    #-------------------------GameManager-------------------------

