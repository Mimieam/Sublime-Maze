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

           
            newPoint = self.view.text_point(newPosX, newPosY)

            if self.is_wall(newPoint):
                print ("Face in Wall")
                return self.view.text_point(curX,curY)
            else:
                return newPoint

    #accept pt from .text_point(xp,yp)
    def is_wall(self, pt):
            print ('pt ',pt)
            char = self.view.substr(pt)
            print ('|',char,'|')
            if char in [']','[','\n','\t','\r']:
                return True 
            else :
                return False
        
        # lineOrChar - move by line or charactere - sublime way of moving cursor
        # tof - true or false
    def on_move(self,edit ,direction, head,lineOrChar, tof):
         
        #get current position   
        cur_position = self.view.sel()[0]
        curX,curY = self.view.rowcol(cur_position.begin())
        curPos= cur_position.begin()

        #get next position from direction
        nextPos = self._next_point(direction, curX, curY)
        # don't update the position if we hit a wall
        if self.is_wall(nextPos):
            print ("Face in Wall")
            # keep cursor at same position and don't update anything         
            # oldPt = self.view.text_point(curX , curY)
            # self.view.sel().clear()
            self.view.sel().add(sublime.Region(curPos))

        else:
            
            print ("direction: ",direction, ' prev= ',gV['PP'],' cur= ',curPos,' next= ',nextPos)
            
            # frontCursor = sublime.Region(nextPos-1, nextPos)
            frontCursor = sublime.Region(curPos, curPos+1)
            #backCursor = sublime.Region(curPos-2, curPos)
            #move the head by 1
            self.view.replace(edit, frontCursor, head)

            # return newPoint
            #delete the tail 
            # self.view.replace(edit, backCursor, " ")

            #if we are going left, the cursor need to be adjusted
            # if direction == "left":
            #     cursorPos = self.view.text_point(curX , curY-1)
            #     self.view.sel().clear()
            #     self.view.sel().add(sublime.Region(cursorPos))
            self._move_to(nextPos)
            # self.view.run_command("move", {"by": lineOrChar,"forward": tof })
            
            # set the current position as previous one since we didn't hit a wall
            gV['PP'] = curPos
            gV['DIRECTION'] = direction

    def _starting_at(self):

        return self.pos

    def _move_to (self,to=None,X=None,Y=None):
        if X is not None:
            pt = self.view.text_point(X , Y)
        else:
            pt = to

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        
