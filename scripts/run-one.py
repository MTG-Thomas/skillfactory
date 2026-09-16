import subprocess, sys
n = sys.argv[1]
dd = sys.argv[2]
mm = open(dd + chr(47) + n + chr(46) + chr(112) + chr(114) + chr(111) + chr(109) + chr(112) + chr(116) + chr(46) + chr(109) + chr(100)).read()
ex = sys.argv[3]
pv = sys.argv[4]
mo = sys.argv[5]
r = subprocess.run([ex, chr(114)+chr(117)+chr(110), chr(45)+chr(112), pv, chr(45)+chr(109), mo, chr(45)+chr(45)+chr(106)+chr(115)+chr(111)+chr(110), mm], capture_output=True, text=True, timeout=180)
open(dd + chr(47) + n + chr(46) + chr(106) + chr(115) + chr(111) + chr(110), chr(119)).write(r.stdout)
open(dd + chr(47) + n + chr(46) + chr(101) + chr(114) + chr(114), chr(119)).write(r.stderr[-2000:])
print(chr(114) + chr(99), r.returncode, len(r.stdout))
