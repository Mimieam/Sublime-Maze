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
        return self._starting_at()

    # def gameOver(self):
    #     self.gameOver()

    def renderSteps(self,edit):
        if gV['INTENDED_DIRECTION'] == 'right':
            gV['Client'].on_move(edit,'right',gV['G_RIGHT'] ,"characters", True)
        elif gV['INTENDED_DIRECTION'] == 'left':
            gV['Client'].on_move(edit,'left',gV['G_LEFT'],"characters", False)
        elif gV['INTENDED_DIRECTION'] == 'up':
            gV['Client'].on_move(edit,'up',gV['G_UP'],"lines", False)
        else :
            gV['Client'].on_move(edit,'down',gV['G_DOWN'],"lines", True)

        sublime.set_timeout(lambda: self.renderSteps(edit),100)
   



# OVERWRITE ARROW KEYS - but pass through to old commands
class go_right_cmd(sublime_plugin.TextCommand):
    def run(self, edit):

        gV['INTENDED_DIRECTION'] = 'right'

        if 'Client' in gV and gV['WALKER_ON'] == True:
            print ('right Key pressed', gV['INTENDED_DIRECTION'])
            # gV['Client'].on_move(edit,'right',gV['G_RIGHT'] ,"characters", True)
            
        if gV['WALKER_ON'] == False:
            self.view.run_command("move", { "by": "characters",  "forward": True  })


class go_left_cmd(sublime_plugin.TextCommand):
    def run(self, edit):

        gV['INTENDED_DIRECTION'] = 'left'

        if 'Client' in gV:
            print('Client in gV')

        print('WALKER_ON ',gV['WALKER_ON'])

        if 'Client' in gV and gV['WALKER_ON'] == True:
            print ('left Key pressed', gV['INTENDED_DIRECTION'])
            # gV['Client'].on_move(edit,'left',gV['G_LEFT'],"characters", False)


        if gV['WALKER_ON'] == False:
            self.view.run_command("move", {  "by": "characters",  "forward": False  })


class go_up_cmd(sublime_plugin.TextCommand):
    def run(self, edit):

        gV['INTENDED_DIRECTION'] = 'up'

        if 'Client' in gV and gV['WALKER_ON'] == True :
            print ('up Key pressed', gV['G_UP'])
            # gV['Client'].on_move(edit,'up',gV['G_UP'],"lines", False)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", { "by": "lines",  "forward": False  })


class go_down_cmd(sublime_plugin.TextCommand):
    def run(self, edit):
        # gV['WALKER_ON']=False  # kick loop shutdown <---- REMOVE THIS ASAP

        gV['INTENDED_DIRECTION'] = 'down'

        if 'Client' in gV and gV['WALKER_ON'] == True:
            print ('down Key pressed', gV['G_DOWN'])
            # gV['Client'].on_move(edit,'down',gV['G_DOWN'],"lines", True)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", {"by": "lines", "forward": True })



       

