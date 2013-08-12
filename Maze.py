import time
import sys , os
import sublime
import sublime_plugin
# 
import sys,logging
from imp import reload

from  Walker.walker.maze import makeMaze, mazeString
# import Walker.walker.player as player
import Walker.walker.config
import Walker.walker.helper as helper
from Walker.edit import Edit 


gV = Walker.walker.config.gV

# mod_prefix = 'Walker'

# for suffix in ['.walker.player','.walker.config','.walker.helper']:
#     mod = mod_prefix + suffix
#     reload(sys.modules[mod])

from .walker.directionCmd import go_right_cmd, go_left_cmd, go_up_cmd, go_down_cmd , ClientPlayer


class WalkerCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # helper.reset()
        self.edit = edit
        gV['WALKER_ON'] = True
        print('Start Walker',gV['WALKER_ON'])

        view = sublime.active_window().new_file()
        view.set_scratch(True)
        view.set_name("Walk.mzl")
        self.view = gV['View']=view

        #load the maze color syntax
        self.view.set_syntax_file("Packages/Walker/syntax/Maze.tmLanguage")

        # Make the 2D array filled with a maze of 1's and 0's
        self.maze = makeMaze(30,15)
         
        # Print that maze to the console
        mazestr =  (mazeString(self.maze, (u"[]", "  ")))

        self.walker = ClientPlayer(view)
        cur_position = view.sel()[0]

        #generate the add the maze to the view
        view.insert(edit, cur_position.a, mazestr)

        EndPt = self.view.size()
        # add the ending point 
       
        EndRegion = sublime.Region(EndPt-5, EndPt-3)
        # EndPt = EndPt - 8

        with Edit(self.view) as edit:
            edit.replace(EndRegion, "__")

        # xEnd, yEnd = self.view.rowcol(EndPt)
        # print (xEnd , yEnd)
        # self.draw_at("__",xEnd, yEnd)

        #make room for timer
        # self.view.insert(edit, 0,"\n\n")

        # add the starting point 
        xStart, yStart =self.walker.starting_at()
        print (xStart , yStart)
        self.draw_at(u"\u25BC",xStart, yStart)

        #set active cursor at the starting position        
        pt = self.view.text_point(xStart , yStart)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))
        # self.animate(view,edit,'w', 5, 3)

        #initializing timer
        self.time_start = time.time()

        gV['SELF'] = self
        
        #set position of the timer at the end of the file
        self.timerPos = self.view.size()
        
        #starting timer
        self.timer(edit,0,0)
        
        #start the rendering function - this function makes the char walk alone.
        sublime.set_timeout(lambda:self.walker.renderSteps(edit),100)
        
            

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
            self.view.run_command("replace_edit" ,{"pos":pos , "length":length, "content":'◇◯◆'})
            # view.replace(edit, )
            print ('passed')
            sublime.set_timeout(lambda: self.animate(view,edit,'w', pos, 3),2000)


    def timer(self,edit ,_sec, _min):
        if gV['WALKER_ON']:
            print('walker_on', gV['WALKER_ON'])
            seconds = _sec
            minutes = _min

            self.elasped = "{minutes} : {seconds}".format(minutes=minutes, seconds=seconds)
            print(self.elasped)
            pt = self.view.text_point(0, 0)
            # self.view.replace(edit, sublime.Region(pt, pt + 6),elasped)
            self.view.run_command("replace_edit" ,{"pos":self.timerPos , "length":10, "content":self.elasped})

            # time.sleep(1)
            seconds = int(time.time() - self.time_start) - minutes * 60
            if seconds >= 60:
                minutes += 1
                seconds = 0

            #time constraint
            if minutes == 2 and seconds > 30 :
                self.walker.gameOver()
                
            sublime.set_timeout(lambda: self.timer(edit,seconds,minutes),1000)
            # sublime.set_timeout_async(lambda: self.timer(edit,seconds,minutes),1000)

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
        
class MazeListener(sublime_plugin.EventListener):

    def on_pre_close(self, view):  

        keymap_file = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '\\Default.sublime-keymap'
        if os.path.isfile(keymap_file):
            f = open('keymap_file', 'w')
            f.write(config.keymap_default)

        gV['WALKER_ON'] = False
  

  
# quick fix for this error when using self.view.replace - use  self.view.run_command("replace_edit" ,{} ) with params
# raise ValueError("Edit objects may not be used after the TextCommand's run method has returned")
# ValueError: Edit obj  ects may not be used after the TextCommand's run method has returned
class ReplaceEditCommand(sublime_plugin.TextCommand):

    def run(self, edit, pos,length,content):
        reg = sublime.Region(pos, pos+length)
        reg2 = sublime.Region(pos+length, pos+length*2)
        view = gV['View']
        view.replace(edit, reg, content) 
        # view.insert(edit, reg2, '- ') 
        
