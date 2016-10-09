# gV = global variable object
# http://www.fileformat.info/info/unicode/block/geometric_shapes/list.htm
gV = {
    'View': '',
    'DIRECTION' : 'right',
    'INTENDED_DIRECTION' : 'down',
    'WALKER_ON' : False,
    'SCORE': 0,
    'AUTO_WALK': True,
    'ANIMATION_SWITCH':False,
    'G_LEFT'    : u"\u25C0",
    'G_RIGHT'   : u"\u25B6",
    'G_UP'      : u"\u25B2",
    'G_DOWN'    : u"\u25BC",
    'PP'        : [1,1],
}

keymap_default = "[\
    { \"keys\": [\"shift+alt+m\"], \"command\": \"walker\" }\
]"

keymap_maze ="[\
    { \"keys\": [\"shift+alt+m\"], \"command\": \"walker\" },\
    { \"keys\": [\"left\"], \"command\": \"moveleft\" },\
    { \"keys\": [\"right\"], \"command\": \"moveright\" },\
    { \"keys\": [\"up\"], \"command\": \"moveup\" },\
    { \"keys\": [\"down\"], \"command\": \"movedown\" }\
]\
"
