# clientPlayer
import sublime
import sublime_plugin

import Walker.walker.config
from  Walker.walker.player.player import Player

gV = Walker.walker.config.gV

class ClientPlayer(Player):
    """docstring for ClientPlayer"""
    def __init__(self, view):
        super(ClientPlayer, self).__init__(view)
        gV['Client'] = self
        self.score = gV['SCORE']

    def starting_at(self):
        print ("STARTING AT: ",self._starting_at())
        return self._starting_at()

    # def gameOver(self):
    #     self.gameOver()

    def renderSteps(self,edit):

        print("INTENDED_DIRECTION = ", gV['INTENDED_DIRECTION'])
        if gV['INTENDED_DIRECTION'] == 'right':
            gV['Client'].on_move(edit,'right',gV['G_RIGHT'] ,"characters", True)
        elif gV['INTENDED_DIRECTION'] == 'left':
            gV['Client'].on_move(edit,'left',gV['G_LEFT'],"characters", False)
        elif gV['INTENDED_DIRECTION'] == 'up':
            gV['Client'].on_move(edit,'up',gV['G_UP'],"lines", False)
        else :
            gV['Client'].on_move(edit,'down',gV['G_DOWN'],"lines", True)

        sublime.set_timeout(lambda: self.renderSteps(edit),500)



