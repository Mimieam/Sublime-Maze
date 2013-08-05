# player.py
import sublime
import sublime_plugin

import Walker.walker.config
gV = Walker.walker.config.gV


class Player(object):
    """docstring for Player"""
    def __init__(self, view):

        self.view = view
        self.pos = [2, 2]
        self.prev_pos = self.pos

    def _next_point(self,direction,curX,curY):
        
        if gV['WALKER_ON']:
            gV['SCORE'] = gV['SCORE'] + 1

            # Get position of next point
            newPosX, newPosY = (curX,curY)
            if direction == "right": newPosY = newPosY +1
            elif direction == "left": newPosY = newPosY-1
            elif direction == "up": newPosX = newPosX-1
            else: newPosX = newPosX +1

            gV['DIRECTION'] = direction
            newPoint = self.view.text_point(newPosX, newPosY)

            # if self.is_wall(newPoint):
            #     print ("Face in Wall")
            #     return self.view.text_point(curX,curY)
            # else:
            #     return newPoint

    #accept pt from .text_point(xp,yp)
    def is_wall(self, pt):

            char = self.view.substr(pt)
            print ('|',char,'|')
            if char in [']','[','\n','\t'] :
                return True 
            else :
                return False
        
        # lineOrChar - move by line or charactere - sublime way of moving cursor
        # tof - true or false
    def on_move(self,edit ,direction, head,lineOrChar, tof):
            
        cur_position = self.view.sel()[0]
        curX,curY = self.view.rowcol(cur_position.begin())

        curPos= cur_position.begin()
        nextPos = self._next_point(direction, curX, curY)

        # don't update the position if we hit a wall
        if self.is_wall(nextPos):
            print ("Face in Wall")
            return self.view.text_point(curX,curY)
        else:
            print ("dir",direction, 'cur ',curPos,' next',nextPos)

            frontCursor = sublime.Region(nextPos-1, nextPos)
            backCursor = sublime.Region(curPos-2, curPos)
            #move the head by 1
            self.view.replace(edit, frontCursor, head)

            #set active cursor at the starting position        
            pt = self.view.text_point(curX , curY)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(pt))


            # return newPoint
        #delete the trail 
        # self.view.replace(edit, backCursor, " ")

            # print ('moving ', lineOrChar, 'tof', tof)
            self.view.run_command("move", {"by": lineOrChar,"forward": tof })

    def _starting_at(self):

        return self.pos
        
