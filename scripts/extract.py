import json, sys
d = json.load(open(sys.argv[1]))
t = d.get(chr(116) + chr(101) + chr(120) + chr(116))
open(sys.argv[2], chr(119)).write(t)
print(len(t))
