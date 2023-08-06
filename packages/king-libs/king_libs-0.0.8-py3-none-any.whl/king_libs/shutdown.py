import os
import time
from random import choice
from colorama import init
from colorama import Fore, Back, Style
init()
cmd = "init 0"
colors = [Fore.MAGENTA,Fore.GREEN,Fore.YELLOW,Fore.RED,Fore.BLUE,Fore.LIGHTCYAN_EX]
minute = int(input(Fore.MAGENTA+"~~~~~~~~~~~~~> : "))
counter = minute*60
for i in range(1800):
	color = choice(colors)
	reset = Style.RESET_ALL
	print(f"{color} ---> ({counter}) {reset} Second Left to ShutDown The System ..",end="\r")
	reset
	time.sleep(1)
	counter-=1
	if counter == 0:
		break

os.system(cmd)

