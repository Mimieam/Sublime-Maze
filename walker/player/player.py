# player.py
import sublime
import sublime_plugin

import Walker.walker.config
gV = Walker.walker.config.gV


class Player(object):
    """docstring for Player"""
    def __init__(self, view):
        # super(Player, self).__init__()
        # self.arg = arg
        self.view = view

    def _next_point(self,direction,curX,CurY):
        
        if gV['WALKER_ON']:
            gV['SCORE'] = gV['SCORE'] + 1

            # Get position of next point
            newPosX, newPosY = (curX,CurY)
            if direction == "right": newPosY = newPosY +1
            elif direction == "left": newPosY = newPosY-1
            elif direction == "up": newPosX = newPosX-1
            else: newPosX = newPosX +1

            gV['DIRECTION'] = direction
            newPoint = self.view.text_point(newPosX, newPosY)

            return newPoint
        # snakeView.show_at_center(newPoint)
        # eatenChar = snakeView.substr(newPoint)
        
        # lineOrChar - move by line or charactere - sublime way of moving cursor
        # tof - true or false
    def on_move(self,edit ,direction, head,lineOrChar, tof):
            
        # for x in self:
        cur_position = self.view.sel()[0]
        # current_line = self.view.line(cur_position)
        curX,curY = self.view.rowcol(cur_position.begin())

        curPos= cur_position.begin()
        nextPos = self._next_point(direction, curX, curY)
        print ("dir",direction, 'cur ',curPos,' next',nextPos)
        # c_row, c_col = self.view.rowcol(cur_position.begin())

        frontCursor = sublime.Region(nextPos-1, nextPos)
        backCursor = sublime.Region(curPos-2, curPos)
        #move the head by 1
        self.view.replace(edit, frontCursor, head)
        #delete the trail 
        # self.view.replace(edit, backCursor, " ")

        print ('moving ', lineOrChar, 'tof', tof)
        self.view.run_command("move", {"by": lineOrChar,"forward": tof })

