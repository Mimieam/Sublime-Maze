# clientPlayer
import sublime
import sublime_plugin
  
import Walker.walker.config
from  Walker.walker.player.player import Player
# from  Walker.walker.player.player import Player

gV = Walker.walker.config.gV

class ClientPlayer(Player):
    """docstring for ClientPlayer"""
    def __init__(self, view):
        super(ClientPlayer, self).__init__(view)
        gV['Client'] = self
        self.score = gV['SCORE']

    def starting_at(self):
        return self._starting_at()


# OVERWRITE ARROW KEYS - but pass through to old commands
class go_right_cmd(sublime_plugin.TextCommand):
    def run(self, edit):

        gV['INTENDED_DIRECTION'] = 'right'
        print ('right Key pressed', gV['INTENDED_DIRECTION'])

        if 'Client' in gV and gV['WALKER_ON'] == True:
            gV['Client'].on_move(edit,'right',gV['G_RIGHT'] ,"characters", True)
            
        if gV['WALKER_ON'] == False:
            self.view.run_command("move", { "by": "characters",  "forward": True  })


class go_left_cmd(sublime_plugin.TextCommand):
    def run(self, edit):

        gV['INTENDED_DIRECTION'] = 'left'
        print ('left Key pressed', gV['INTENDED_DIRECTION'])

        if 'Client' in gV and gV['WALKER_ON'] == True:
            gV['Client'].on_move(edit,'left',gV['G_LEFT'],"characters", False)


        if gV['WALKER_ON'] == False:
            self.view.run_command("move", {  "by": "characters",  "forward": False  })


class go_up_cmd(sublime_plugin.TextCommand):
    def run(self, edit):

        gV['INTENDED_DIRECTION'] = 'up'
        print ('up Key pressed', gV['G_UP'])

        if 'Client' in gV and gV['WALKER_ON'] == True :
            gV['Client'].on_move(edit,'up',gV['G_UP'],"lines", False)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", { "by": "lines",  "forward": False  })


class go_down_cmd(sublime_plugin.TextCommand):
    def run(self, edit):
        # gV['WALKER_ON']=False  # kick loop shutdown <---- REMOVE THIS ASAP

        gV['INTENDED_DIRECTION'] = 'down'
        print ('down Key pressed', gV['G_DOWN'])

        if 'Client' in gV and gV['WALKER_ON'] == True:
            gV['Client'].on_move(edit,'down',gV['G_DOWN'],"lines", True)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", {"by": "lines", "forward": True })
