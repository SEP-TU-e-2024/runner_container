import subprocess
import time

p = subprocess.Popen("python3 cheese.py", shell=True, stdin=subprocess.PIPE)

print(p.pid)

p.stdin.write(b'hey\n')
p.stdin.flush()
print('asdf')
time.sleep(8)
print('wtf')
p.stdin.write(b'hadfadf\n')

#for i in range(10):
#    print('hey')
#    if p.poll() == None:
#        p.stdin.write(b'test\n')