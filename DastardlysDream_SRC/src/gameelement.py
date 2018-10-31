

__author__="Luiz de Mello"
__date__ ="$Jan 26, 2010 8:30:30 AM$"


class GameElement:
    def __init__(self, maingame):
        self.visible = True #Used externally
        self.enabled = True #Used externally
        self.maingame = maingame

    def Update(self, updateTimeDifference):        
        pass

    def Draw(self, updateTimeDifference):        
        pass

    def AlterResolution(self, newResolution):
        pass