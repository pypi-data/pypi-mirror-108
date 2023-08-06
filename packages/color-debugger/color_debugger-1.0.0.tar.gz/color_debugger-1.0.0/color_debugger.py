from termcolor import colored, cprint
from datetime import datetime
import sys
import emoji
global set_time
set_time = False
def set_settings(show_time):
	set_time = show_time
def error(arg):
	if set_time == True:
		time = '[{}]'.format(datetime.now())
	elif set_time == False:
		time = ''
	errMsg = colored('[ERROR]', 'grey', 'on_red')
	timeMsg = colored(time, 'grey', 'on_white')
	message = f"{timeMsg} {errMsg} {arg}"
	print(message)
def warn(arg):
	if set_time == True:
		time = '[{}]'.format(datetime.now())
	elif set_time == False:
		time = ''
	errMsg = colored('[WARN]', 'grey', 'on_yellow')
	timeMsg = colored(time, 'grey', 'on_white')
	message = f"{timeMsg} {errMsg} {arg}"
	print(message)

def debug(arg):
	if set_time == True:
		time = '[{}]'.format(datetime.now())
	elif set_time == False:
		time = ''
	errMsg = colored('[DEBUG]', 'grey', 'on_green')
	timeMsg = colored(time, 'grey', 'on_white')
	message = f"{timeMsg} {errMsg} {arg}"
	print(message)

def fatal(arg):
	if set_time == True:
		time = '[{}]'.format(datetime.now())
	elif set_time == False:
		time = ''
	errMsg = '[FATAL]'
	timeMsg = time
	end = '[APP CLOSED]'
	message = colored(f"{timeMsg} {errMsg} {arg} {end}", "grey", "on_red")
	print(message)
	sys.exit()

print("""
	IN THIS PROJECT USED DebuggerLib BY ALEX.NET

	THANKS FOR WORKING WITH THIS LIBRARY! bye😊
	""")

