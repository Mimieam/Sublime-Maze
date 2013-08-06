
import plistlib , json, sys


src= sys.argv[1]
dest = sys.argv[2]

if src.endswith('json'):
    json_text = json.load(open(src))
    plistlib.writePlist(json_text , dest)
    print('done')
else:
	print('error exiting')