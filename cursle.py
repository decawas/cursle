#!/usr/bin/env python3

import math
import curses
import argparse
from re import search as res

class globals:
	word = ""
	words = ""
	swords = ""
	guess = ""
	guesses = []

def main(stdscr):
	curses.init_pair(1, 7, 0)
	curses.init_pair(2, 2, 0)
	curses.init_pair(3, 3, 0) 
	curses.init_pair(4, 1, 0)

	curses.start_color()
	curses.curs_set(0)
	stdscr.keypad(True)
	curses.mousemask(1)

	while True:
		try:
			render(stdscr)
		except:
			pass

		key = str(stdscr.get_wch()).lower()

		if key == "409":
			_, x, y, _, _ = curses.getmouse()
			if len(globals.guess) < 5 and y == 4 * args.tries:
				try: globals.guess += globals.swords[x]
				except IndexError: pass
			elif y == 4 * args.tries + 1:
				if x < 5:
					if len(globals.guess) != 5 or res(globals.guess, globals.words) is None: pass
					else:
						globals.guesses.append(globals.guess)
						globals.guess = ""
				elif x < 15: key = "263"

		if key == "\n":
			if len(globals.guess) != 5 or res(globals.guess, globals.words) is None: pass
			else:
				globals.guesses.append(globals.guess)
				globals.guess = ""
		elif key == "263": globals.guess = globals.guess[:-1] 
		elif len(globals.guess) != 5 and len(key) == 1 and res("[{0}]".format(globals.swords), key) != None: globals.guess += key

def render(stdscr):
	stdscr.bkgd(" ", curses.color_pair(1))
	stdscr.refresh()
	stdscr.clear()
	for i in range(args.tries):
		try:
			if len(globals.guesses[i]) == 5:
				for j in range(5):
					if globals.word[j] == globals.guesses[i][j]: 
						stdscr.addstr(i * 4, j * 4,"┌─┐", curses.color_pair(2))
						stdscr.addstr(i * 4 + 1, j * 4,"│" + str(globals.guesses[i][j]).upper() + "│", curses.color_pair(2))
						stdscr.addstr(i * 4 + 2, j * 4,"└─┘", curses.color_pair(2))
						stdscr.addstr(i * 4 + 3, j * 4,"YES", curses.color_pair(2))
					elif globals.word[j] != globals.guesses[i][j] and res(globals.guesses[i][j], globals.word) != None: 
						stdscr.addstr(i * 4, j * 4,"┌─┐", curses.color_pair(3))
						stdscr.addstr(i * 4 + 1, j * 4,"│" + str(globals.guesses[i][j]).upper() + "│", curses.color_pair(3))
						stdscr.addstr(i * 4 + 2, j * 4,"└─┘", curses.color_pair(3))
						stdscr.addstr(i * 4 + 3, j * 4,"MID", curses.color_pair(3))
					elif globals.word[j] != globals.guesses[i][j] and res(globals.guesses[i][j], globals.word) == None: 
						stdscr.addstr(i * 4, j * 4,"┌─┐", curses.color_pair(4))
						stdscr.addstr(i * 4 + 1, j * 4,"│" + str(globals.guesses[i][j]).upper() + "│", curses.color_pair(4))
						stdscr.addstr(i * 4 + 2, j * 4,"└─┘", curses.color_pair(4))
						stdscr.addstr(i * 4 + 3, j * 4,"BAD", curses.color_pair(4))
		except IndexError:
			if globals.guess != "" and len(globals.guesses) == i:
				for j in range(5):
					stdscr.addstr(i * 4, j * 4, "┌─┐")
					try:
						stdscr.addstr(i * 4 + 1, j * 4 + 1, globals.guess[j].upper())
					except IndexError:
						pass
					stdscr.addstr(i * 4 + 2, j * 4, "└─┘")
			else:
				stdscr.addstr(i * 4, 0, "┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐\n\n└─┘ └─┘ └─┘ └─┘ └─┘", curses.color_pair(1))
	stdscr.addstr(4 * args.tries, 0, str(globals.swords).upper())
	stdscr.addstr(4 * args.tries + 1, 0, "ENTER")
	stdscr.addstr(4 * args.tries + 1, 6, "BACKSPACE")

parser = argparse.ArgumentParser(description="Wordle")
parser.add_argument("--daily", help="gives you the same word as on New York Times, based on GMT only", action="store_true")
parser.add_argument("--tries", help="set the number of attempts you can make", type=int, default=6)
parser.add_argument("--gamecode", help="lets you set the word based on an integer so you can send it to a friend without them knowing the word", type=int, default=-1)
parser.add_argument("--lang", help="select the language", default="en")
args = parser.parse_args()

if not args.daily:
	f = open("lang/" + args.lang, "r")
else:
	f = open("lang/en", "r")
globals.words = f.read()
globals.swords = globals.words.split("\n")
f.close()

if args.daily:
	import time
	num = math.floor((time.time() - 1624060800) / 86400) + 10
elif args.gamecode == -1:
	import random
	num = random.randint(0, (len(globals.swords)) - 1)
	print("the gamecode is {0}".format((num * 86400) + 1624060800))
else:
	num = math.floor((args.gamecode - 1624060800) / 86400)

globals.word = globals.swords[num]
print("the word was {0}".format(globals.word))
globals.swords = globals.swords[-1]

curses.wrapper(main)
