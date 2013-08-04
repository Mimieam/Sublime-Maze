import sublime
import sublime_plugin


import sys
from imp import reload
# import imp

import Walker.walker.player
import Walker.walker.config


gV = Walker.walker.config.gV

mod_prefix = 'Walker'

for suffix in ['.walker','.walker.player']:
    mod = mod_prefix + suffix
    reload(sys.modules[mod])

from .walker.directionCmd import go_right_cmd, go_left_cmd, go_up_cmd, go_down_cmd , ClientPlayer

#used to search thru the open windows to find 'Walk'
class WalkerWindow(sublime_plugin.WindowCommand):

    def run(self):
        
        return sublime.Window.open_file(self,'Walk')
    def getFiles(self):
        for x in self:
            print('WindowCommand', x)# return sublime.Window.open_file(self,'Walk')
        pass
        

class WalkerCommand(sublime_plugin.TextCommand):
    # def __init__(self):

    def run(self, edit):
        self.edit = edit

        if gV['WALKER_ON'] == False:
            gV['WALKER_ON'] = True
            # print('Test gV')            
            # view = sublime.Window.open_file(self,'Walk')
            # views =  sublime.active_window().open_file(self,'Walk.txt')
            # view = WalkerWindow(self)
            # print(view.getFiles())
            # for v in view:
            # views =  sublime.active_window().views()
            # view = None
            # for x in views:
            #     print (x.id(), " name ", x.name())
            #     if x.name() == "Walk":
            #        view = x 

            # print('view', view)       
            # if view is None:
            view = sublime.active_window().new_file()
            view.set_scratch(True)
            view.set_name("Walk")
            gV['View']=view
            # else:
                # self.focus_view(view)
                

            # view = self.view
            walker = ClientPlayer(view)
            # walker.on_move(edit,'left',SNAKE_HEAD)
            # print(gV['Client'])
            # selections = self.view.sel()
            # for selection in selections:
            cur_position = view.sel()[0]
            # current_line = view.line(cur_position)
            # c_row,c_col = view.rowcol(cur_position.begin())

            view.insert(edit, cur_position.a, """
I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I 
I               I           I       I               I       I   I               I 
I   I I I   I I I   I I I   I   I   I I I I I   I   I   I   I   I   I   I I I   I 
I       I               I   I   I               I       I   I       I   I       I 
I   I I I I I I I I I I I   I   I I I I I I I I I I I I I   I   I I I   I I I   I 
I   I       I               I       I           I   I       I   I   I       I   I 
I   I   I   I   I I I   I I I I I   I   I   I   I   I   I I I   I   I I I   I   I 
I   I   I   I       I   I           I   I   I       I   I   I           I   I   I 
I   I   I   I I I   I   I   I   I I I I I   I I I I I   I   I   I I I I I   I   I 
I   I   I           I   I   I   I       I               I       I       I   I   I 
I   I   I I I I I I I I I   I   I   I   I I I   I I I I I   I I I   I   I   I   I 
I   I   I               I   I   I   I   I   I           I   I       I   I   I   I 
I   I   I   I I I I I   I   I   I   I   I   I I I I I   I I I   I I I   I   I I I 
I   I       I       I   I   I   I   I       I       I           I   I   I       I 
I   I I I I I   I I I   I   I I I   I I I I I   I   I I I I I I I   I   I I I   I 
I       I       I       I           I           I   I               I           I 
I I I   I   I   I   I I I I I I I I I   I I I I I   I   I I I I I   I I I I I   I 
I   I   I   I   I           I           I       I       I       I   I       I   I 
I   I   I   I   I I I   I I I   I   I I I   I   I I I I I   I   I I I   I   I   I 
I           I       I           I           I               I           I       I 
I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I 
""")
            # print ('cur_p ',cur_position, 'current_line', current_line, 'col ',c_col+1,'row ',c_row+1, 'edit ',edit)
 
            # view.run_command("move", {"by": "characters","forward": False })

            # region = sublime.Region(cur_position.a+1, cur_position.b + 2)
            # view.replace(edit, region, u"\u25CF")

            # start snake update timeout loop
            # sublime.set_timeout(lambda: self.animatedStuff(view,edit,
            #                                         'w',
            #                                         0,
            #                                         5), 500)
            # stuff = animatedStuff(view)
            # sublime.set_timeout(lambda: self.animate(view,edit,'w', 0, 5),1000)
            self.animate(view,edit,'w', 10, 5)
        else:
            gV['WALKER_ON'] = False
            gV['DIRECTION'] = "right"

    # def gameOver():

    #     sublime.error_message("Game Over!\nYour SNAKE_SCORE was: " +
    #                           str(gV['SCORE']))
    #     gV['WALKER_ON'] = False 


    # def reset(self,edit):

    #     # reset stuff
    #     gV['SCORE'] = 0
    #     gV['DIRECTION'] = "right"
    #     gV['INTENDED_DIRECTION'] = "right"
    #     gV['ANIMATION_SWITCH'] =True

    def animate (self, view,edit,head,pos,length):
        if gV['WALKER_ON']:
            on = gV['ANIMATION_SWITCH']
            pos = int(pos)
            if (on):
                pos = pos +2
                gV['ANIMATION_SWITCH'] = on=False
                
            else:
                pos = pos -2
                gV['ANIMATION_SWITCH'] = on=True
            print ('on in animatedStuff ',on)
            self.view.run_command("replace_edit" ,{"view":43, "pos":pos , "length":length, "head":'◇◯◆'})
            # view.replace(edit, )
            print ('passed')
            sublime.set_timeout(lambda: self.animate(view,edit,'w', pos, 3),2000)

class ReplaceEditCommand(sublime_plugin.TextCommand):

    def run(self, edit, view, pos,length,head):
        reg = sublime.Region(pos, pos+length)
        reg2 = sublime.Region(pos+length, pos+length*2)
        view = gV['View']
        view.replace(edit, reg, head) 
        view.insert(edit, reg2, '- ') 
        
