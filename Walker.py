import sublime
import sublime_plugin


import sys
from imp import reload
# import imp

import Walker.walker.player
import Walker.walker.config
import Walker.helper


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

    def run(self, edit):
        self.edit = edit

        if gV['WALKER_ON'] == False:
            gV['WALKER_ON'] = True

            view = sublime.active_window().new_file()
            view.set_scratch(True)
            view.set_name("Walk")
            self.view = gV['View']=view

            walker = ClientPlayer(view)
            cur_position = view.sel()[0]
            view.insert(edit, cur_position.a, 
"""[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
[]                  []                          []                              []
[]  [][][][][][][]  []  [][][][][][][][][]  [][][]  [][][]  [][][][][][][][][]  []
[]      []  []      []  []          []      []      []      []              []  []
[]  []  []  []  [][][]  []  [][][]  []  [][][]  [][][]  [][][]  [][][][][]  []  []
[]  []  []              []      []  []      []      []  []      []          []  []
[]  []  [][][][][]  [][][][][]  []  [][][][][]  [][][]  []  [][][][][][][][][]  []
[]  []      []      []          []              []      []                  []  []
[]  [][][]  []  [][][]  [][][][][][][][][][][][][]  [][][]  [][][][][][][]  []  []
[]  []      []  []  []  []      []          []      []      []      []      []  []
[][][]  [][][]  []  []  []  []  []  [][][]  []  [][][]  [][][]  [][][]  []  []  []
[]      []          []      []  []  []  []  []      []  []          []  []  []  []
[]  [][][][][][][]  [][][][][]  []  []  [][][][][]  []  [][][][][]  []  [][][]  []
[]              []  []          []  []              []              []  []      []
[]  [][][][][]  [][][]  [][][][][]  []  [][][][][][][][][][][][][][][]  []  [][][]
[]      []  []          []      []  []  []              []              []  []  []
[][][]  []  [][][][][][][][][]  []  []  []  [][][][][]  []  [][][][][][][]  []  []
[]      []                      []  []              []  []  []          []  []  []
[]  [][][]  [][][][][][][][][]  []  [][][][][][][][][]  []  []  [][][]  []  []  []
[]          []                  []                      []          []          []
[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
""")
            xStart, yStart = walker.starting_at()
            print (xStart , yStart)
            self.draw_at("S",xStart, yStart)

            #set active cursor at the starting position        
            pt = self.view.text_point(xStart , yStart)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(pt))

            # self.view.show(pt)


        else:
            gV['WALKER_ON'] = False
            gV['DIRECTION'] = "right"

    def gameOver():

        sublime.error_message("Game Over!\nYour SNAKE_SCORE was: " + str(gV['SCORE']))
        gV['WALKER_ON'] = False 


    def reset(self,edit):

        # reset stuff
        gV['SCORE'] = 0
        gV['DIRECTION'] = "right"
        gV['INTENDED_DIRECTION'] = "right"
        gV['ANIMATION_SWITCH'] =True

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

    #give credit where it is due : chat_at & draw_at where take from this repo : https://github.com/miningold/Traverse/blob/master/Traverse.py
    # Get character at position in vector or x,y form
    def char_at(self, xpos, ypos=None):
        if ypos is None:
            return self.char_at(xpos[0], xpos[1])

        return self.view.substr(self.view.text_point(ypos, xpos))

    # Draw character at position in vector or x,y form
    def draw_at(self, char, xpos, ypos=None):
        if ypos is None:
            return self.draw_at(char, xpos[0], xpos[1])

        pt = self.view.text_point(ypos, xpos)
        self.view.replace(self.edit, sublime.Region(pt, pt + 1), char)

class ReplaceEditCommand(sublime_plugin.TextCommand):

    def run(self, edit, view, pos,length,head):
        reg = sublime.Region(pos, pos+length)
        reg2 = sublime.Region(pos+length, pos+length*2)
        view = gV['View']
        view.replace(edit, reg, head) 
        # view.insert(edit, reg2, '- ') 
        
