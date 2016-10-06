# helper.py
import sublime
import os
import Walker.walker.config as config

def reset():

    config.gV['SCORE'] = 0
    config.gV['DIRECTION'] = "right"
    config.gV['INTENDED_DIRECTION'] = "right"
    config.gV['ANIMATION_SWITCH'] =False

    #reseting the keybinding by changing the Default.sublime-keymap-reset  extention back  to .sublime-keymap

    # keymap_file_reset = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '\\Default.sublime-keymap-reset'
    # print(keymap_file_reset ,  os.path.isfile(keymap_file_reset))

    # if os.path.isfile(keymap_file_reset):
    #     try:
    #         base = os.path.splitext(keymap_file_reset)[0]
    #         print(keymap_file_reset, ' ', base)
    #         os.rename(keymap_file_reset, base + ".sublime-keymap")
    #     except Exception as e:
    #         raise e

    #reset file content of Default.sublime-keymap
    keymap_file = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '\\Default.sublime-keymap'
    if os.path.isfile(keymap_file):
        print('Writting to ...:', keymap_file)
        f = open('keymap_file', 'w')
        f.write(config.keymap_maze)


