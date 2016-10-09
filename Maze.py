import time
import sys
import os
import sublime
import sublime_plugin

from imp import reload

from Walker.walker.maze import makeMaze, mazeString
# import Walker.walker.player as player
import Walker.walker.config as config
from Walker.edit import Edit


gV = config.gV


# from Walker.walker.directionCmd import ClientPlayer
# mod_prefix = 'Walker'

# for suffix in ['.walker.player','.walker.config','.walker.helper', '.walker.directionCmd']:
#     mod = mod_prefix + suffix
#     reload(sys.modules[mod])


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

        if gV['AUTO_WALK']:
            sublime.set_timeout(lambda: self.renderSteps(edit),250)





class WalkerCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # helper.reset()
        self.edit = edit
        gV['WALKER_ON'] = True
        print('Start Walker', gV['WALKER_ON'])

        view = sublime.active_window().new_file()
        # view.set_scratch(True)
        view.set_name("Walk.mzl")
        self.view = gV['View'] = view

        # load the maze color syntax
        self.view.set_syntax_file("Packages/Walker/syntax/Maze.tmLanguage")

        # Make the 2D array filled with a maze of 1's and 0's
        self.maze = makeMaze(30, 15)

        # Print that maze to the console
        mazestr = (mazeString(self.maze, (u"[]", "  ")))

        self.walker = ClientPlayer(view)
        cur_position = view.sel()[0]

        # generate the add the maze to the view
        view.insert(edit, cur_position.a, mazestr)

        self.MAZE_LENGTH = EndPt = self.view.size()
        # add the ending point

        EndRegion = sublime.Region(EndPt - 5, EndPt - 3)
        # EndPt = EndPt - 8

        with Edit(self.view) as edit:
            edit.replace(EndRegion, "__")


        # self.animate(view, edit,'w', 5, 3)

        # initializing timer

        gV['SELF'] = self

        # set position of the timer at the end of the file
        self.time_start = time.time()
        self.timerPos = self.view.size()
        # pt = self.view.text_point(xStart, yStart)


        # starting timer
        self.timer(edit, 0, 0)
       # add the starting point
        print (self.walker.starting_at())
        xStart, yStart = [2,2] #self.walker.starting_at()
        print ("start ENd", xStart, yStart, dir(view))
        self.draw_at(u"\u25C4", xStart, yStart)

        # set active cursor at the starting position
        pt = 249
        print ("pt: ", pt, xStart, yStart)
        view.sel().clear()
        view.sel().add(sublime.Region(pt))
        # view.sel().add(sublime.Region(248))

        # start the rendering function - this function makes the char walk
        # alone.
        sublime.set_timeout(lambda:self.walker.renderSteps(edit),300)

    def animate(self, view, edit, head, pos, length):

        if gV['WALKER_ON']:
            on = gV['ANIMATION_SWITCH']
            pos = int(pos)
            if (on):
                pos = pos + 2
                gV['ANIMATION_SWITCH'] = on = False

            else:
                pos = pos - 2
                gV['ANIMATION_SWITCH'] = on = True
            print ('on in animatedStuff ', on)
            self.view.run_command(
                "replace_edit", {"pos": pos, "length": length, "content": '◇◯◆'})
            # view.replace(edit, )
            sublime.set_timeout(
                lambda: self.animate(view, edit, 'w', pos, 3), 2000)

    def timer(self, edit, _sec, _min):
        if gV['WALKER_ON']:
            # print('walker_on', gV['WALKER_ON'])
            seconds = _sec
            minutes = _min

            self.elasped = "{minutes} : {seconds}".format(
                minutes=minutes, seconds=seconds)
            # print(self.elasped)

            self.view.run_command(
                "replace_edit", {"pos": self.MAZE_LENGTH , "length": 10, "content": self.elasped})

            # time.sleep(1)
            seconds = int(time.time() - self.time_start) - minutes * 60
            if seconds >= 60:
                minutes += 1
                seconds = 0

            # time constraint
            if minutes == 2 and seconds > 30:
                self.walker.gameOver()

            sublime.set_timeout(
                lambda: self.timer(self.edit, seconds, minutes), 1000)
            # sublime.set_timeout_async(lambda: self.timer(self.edit,seconds,minutes),1000)

    # give credit where it is due : chat_at & draw_at where take from this repo : https://github.com/miningold/Traverse/blob/master/Traverse.py
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
    def on_query_context(selfview, key, operator, operand, match_all):
         if (view == gV['View']):
            print (key)
    def on_text_command(self, view, command_name, args):
        if (view == gV['View']):
            print( command_name, args)
            # pass
            # Oct-6-2016 - prevent cheating lol
            # this listen for any mouse click on the .mzl file
            # and send it to the void...
            if command_name == 'move_to' and args == {"to": "bol"}:
                print ("BOL PRESSED")
            if command_name == 'drag_select' or command_name == 'left_delete':
                sublime.Window.focus_view(sublime.active_window(), gV['View'])
                print("Drag SELECT, args")
                return ('Void','{"by": "lines", "forward": false}')

# quick fix for this error when using self.view.replace - use  self.view.run_command("replace_edit" ,{} ) with params
# raise ValueError("Edit objects may not be used after the TextCommand's run method has returned")
# ValueError: Edit obects may not be used after the TextCommand's run
# method has returned
class ReplaceEditCommand(sublime_plugin.TextCommand):

    def run(self, edit, pos, length, content):
        reg = sublime.Region(pos, pos + length)
        # reg2 = sublime.Region(pos + length, pos + length * 2)
        gV['View'].replace(edit, reg, content)

        # EndPt = view.size()
        # pt = view.text_point(EndPt, EndPt)
        # view.replace(self.edit, sublime.Region(pt, pt + 6), content)
        # view.insert(edit, reg2, '- ')


# # OVERWRITE ARROW KEYS - but pass through to old commands
class GoRightCmdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        gV['INTENDED_DIRECTION'] = 'right'
        print ('Client' in gV ,gV['WALKER_ON'], 'right Key pressed', gV['INTENDED_DIRECTION'])
        if 'Client' in gV and gV['WALKER_ON'] == True:
            gV['Client'].on_move(edit,'right',gV['G_RIGHT'] ,"characters", True)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", { "by": "characters",  "forward": True  })


class GoLeftCmdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        gV['INTENDED_DIRECTION'] = 'left'
        print ('Client' in gV ,gV['WALKER_ON'], 'left Key pressed', gV['INTENDED_DIRECTION'])
        if 'Client' in gV and gV['WALKER_ON'] == True:
            gV['Client'].on_move(edit,'left',gV['G_LEFT'],"characters", False)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", {  "by": "characters",  "forward": False  })


class GoUpCmdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        gV['INTENDED_DIRECTION'] = 'up'
        print ('Client' in gV ,gV['WALKER_ON'], 'up Key pressed', gV['G_UP'])
        if 'Client' in gV and gV['WALKER_ON'] == True :
            gV['Client'].on_move(edit,'up',gV['G_UP'],"lines", False)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", { "by": "lines",  "forward": False  })


class GoDownCmdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # gV['WALKER_ON']=False  # kick loop shutdown <---- REMOVE THIS ASAP
        gV['INTENDED_DIRECTION'] = 'down'
        print ('Client' in gV ,gV['WALKER_ON'], 'down Key pressed', gV['G_DOWN'])

        if 'Client' in gV and gV['WALKER_ON'] == True:
            gV['Client'].on_move(edit,'down',gV['G_DOWN'],"lines", True)

        if gV['WALKER_ON'] == False:
            self.view.run_command("move", {"by": "lines", "forward": True })

# void command - redirect here any native sublime command we dont want to be triggered while playing
class VoidCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('You are in the void for clicking..')




