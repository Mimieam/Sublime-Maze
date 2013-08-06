#!/usr/bin/env python
 # modified from https://gist.github.com/pokstad/1195723
import plistlib
import json
import tkFileDialog
import re
import sys
 
file_to_open = sys.argv[1]
file_to_write = "output"
converted = None
print (file_to_open)
if file_to_open.endswith('json'):
    converted = "plist"
    converted_dict = json.load(open(file_to_open))
    plistlib.writePlist(converted_dict, file_to_write)

elif file_to_open.endswith('plist'):
    converted = "json"
    converted_dict = plistlib.readPlist(file_to_open)
    converted_string = json.dumps(converted_dict, sort_keys=True, indent=4)
    open(file_to_write, 'w').write(converted_string)
else:
    print("WHAT THE F*** ARE YOU TRYING TO DO??????")
    sys.exit(1)