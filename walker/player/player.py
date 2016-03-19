# player.py
import sublime
import sublime_plugin
from Walker.edit import Edit

import Walker.walker.config
gV = Walker.walker.config.gV
# from Walker.Maze import on_move_wrapper

class Player(object):
    """docstring for Player"""
    def __init__(self, view):

        self.view = view
        self.pos = [1, 1]
        self.prev_pos = self.pos
        # self.lastCorrectPos

    def run(self, view):
        self.__init__(view)

    def _next_point(self,direction,curX,curY):

        if gV['WALKER_ON']:
            gV['SCORE'] = gV['SCORE'] + 1

            # Get position of next point
            newPosX, newPosY = (curX,curY)
            if direction == "right": newPosY = newPosY +1
            elif direction == "left": newPosY = newPosY-1
            elif direction == "up": newPosX = newPosX-1
            else: newPosX = newPosX +1


            newPoint = self.view.text_point(newPosX, newPosY)

            if self.is_wall(newPoint):
                return self.view.text_point(curX,curY)
            else:
                return newPoint

    # def is_cheat_jumping(self, pt):
    #     pass

    #accept pt from .text_point(xp,yp)
    def is_wall(self, pt):
            char = self.view.substr(pt)
            # print ('|',char,'|')
            if char in [']','[','\n','\t','\r','']:
                return True
            else :
                return False


    def walked_on_something(self,pt):
            char = self.view.substr(pt)
            if char in ['_']:
                self.gameOver()


    def gameOver(self):

        sublime.error_message("Your SCORE was: " + str(gV['SCORE']))
        gV['WALKER_ON'] = False


        # lineOrChar - move by line or charactere - sublime way of moving cursor
        # tof - true or false
    def on_move(self,edit ,direction, head,lineOrChar, tof):
        print (direction, head,lineOrChar, tof)
        if gV['WALKER_ON']:
            self.on_move_wrapper(self,edit ,direction, head,lineOrChar, tof)


    def _starting_at(self):
        return self.pos

    def _move_to (self,to=None,X=None,Y=None):
        if X is not None:
            pt = self.view.text_point(X , Y)
        else:
            pt = to

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))



    def on_move_wrapper(self,_self,edit ,direction, head,lineOrChar, tof):
        #get current position
        cur_position = self.view.sel()[0]
        curX,curY = self.view.rowcol(cur_position.begin())
        curPos= cur_position.begin()

        #get next position from direction
        nextPos = self._next_point(direction, curX, curY)
        # don't update the position if we hit a wall

        if self.is_wall(nextPos):
            # keep cursor at same position and don't update anything
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(curPos))

        else:

            frontCursor = sublime.Region(curPos, curPos+1)
            #move the head by 1
            # self.view.replace(edit, frontCursor, head)
            # self.view.run_command("replace_edit" ,{"pos":frontCursor, "length":10, "content":'>'})
            with Edit(self.view) as edit:
                edit.replace(frontCursor,head)
                # edit.insert(0, 'more stuff\n')
            # self.view.run_command("move", {  "by": "characters",  "forward": True  })
            # self.view.run_command("r_edit")
            #delete the tail
            # self.view.replace(edit, backCursor, " ")

            self._move_to(nextPos)
            # print('test 1',frontCursor)
            self.walked_on_something(nextPos)
            # self.view.run_command("move", {"by": lineOrChar,"forward": tof })

            # set the current position as previous one since we didn't hit a wall
            gV['PP'] = curPos
            gV['DIRECTION'] = direction
            #sublime.set_timeout(lambda:self.on_move_wrapper(self,edit ,direction, head,lineOrChar, tof) ,100)


class CursorEditCommand(sublime_plugin.TextCommand):

    def run(self, edit, pos,length,content):
        reg = sublime.Region(pos, pos+length)
        view = gV['View']
        view.replace(edit, reg, content)

class ReditCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        frontCursor = sublime.Region(3, 4)
        view = gV['View']
        view.replace(edit, frontCursor, 'T')
        print ('in redit')



