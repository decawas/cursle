#!/usr/bin/env python3

import math
import curses
import argparse
from re import search as res
import json

def main(stdscr):
	global guess
	curses.init_pair(1, 7, 0)
	curses.init_pair(2, 2, 0)
	curses.init_pair(3, 3, 0) 

	curses.start_color()
	curses.curs_set(0)
	stdscr.keypad(True)
	stdscr.bkgd(" ", curses.color_pair(1))
	curses.mousemask(1)
	while True:
		try: render(stdscr)
		except curses.error: pass

		key = str(stdscr.get_wch())

		if key == "409":
			try: _, x, y, _, _ = curses.getmouse()
			except: x, y = 0, 0
			if len(guess) < 5 and y == 3 * args.tries + 1:
				try: guess += alphab[x - math.floor(stdscr.getmaxyx()[1] / 2) - math.floor(len(alphab) / 2)]
				except IndexError: pass
			elif y == 3 * args.tries:
				if x > math.floor(stdscr.getmaxyx()[1] / 2) - 9 and x < math.floor(stdscr.getmaxyx()[1] / 2) - 3: key = "\n"
				elif x > math.floor(stdscr.getmaxyx()[1] / 2) - 3 and x < math.floor(stdscr.getmaxyx()[1] / 2) + 7: key = "263"

		if key == "1":
			curses.endwin()
			import sys
			sys.exit()
		elif key == "\n" and res(f"{guess}\n", words) != None:
				guesses.append(guess)
				guess = ""
		elif key == "263": guess = guess[:-1]
		elif len(guess) != 5 and len(key) == 1 and res(key, alphab) != None: guess += key

def render(stdscr):
	mx = math.floor(stdscr.getmaxyx()[1] / 2)
	stdscr.refresh()
	stdscr.clear()
	for i in range(args.tries):
		try:
			if len(guesses[i]) == 5:
				for j in range(5):
					if word[j] == guesses[i][j]:
						colour = 2
						stdscr.addstr(i * 3 + 2, j * 4 + mx - 9, "╰v╯", curses.color_pair(colour))
					elif word[j] != guesses[i][j] and res(guesses[i][j], word) != None:
						colour = 3
						stdscr.addstr(i * 3 + 2, j * 4 + mx - 9, "╰-╯", curses.color_pair(colour))
					elif word[j] != guesses[i][j] and res(guesses[i][j], word) == None:
						colour = 1
						stdscr.addstr(i * 3 + 2, j * 4 + mx - 9, "╰x╯", curses.color_pair(colour))
					stdscr.addstr(i * 3, j * 4 + mx - 9, "╭─╮", curses.color_pair(colour))
					stdscr.addstr(i * 3 + 1, abs(j * 4 - o) + mx - 9, f"│{guesses[i][j].upper()}│", curses.color_pair(colour))
		except IndexError:
			if guess != "" and len(guesses) == i:
				for j in range(5):
					stdscr.addstr(i * 3, j * 4 + mx - 9, "╭─╮")
					try: stdscr.addstr(i * 3 + 1, abs(j * 4 - o) + mx - 8, guess[j].upper())
					except: pass
					stdscr.addstr(i * 3 + 2, j * 4 + mx - 9, "╰─╯")
			else: 
				stdscr.addstr(i * 3, mx - 9, "╭─╮ ╭─╮ ╭─╮ ╭─╮ ╭─╮")
				stdscr.addstr(i * 3 + 2, mx - 9, "╰─╯ ╰─╯ ╰─╯ ╰─╯ ╰─╯")
	stdscr.addstr(3 * args.tries, mx - 7, "ENTER BACKSPACE")
	stdscr.addstr(3 * args.tries + 1, mx - math.floor(len(alphab) / 2), alphab.upper())

parser = argparse.ArgumentParser(description="Cursle")
parser.add_argument("--daily", help="gives you the same word as on New York Times, based on GMT only", action="store_true")
parser.add_argument("--tries", help="set the number of attempts you can make", type=int, default=6)
parser.add_argument("--gamecode", help="lets you set the word based on an integer so you can send it to a friend without them knowing the word", type=int, default=-1)
parser.add_argument("--lang", help="select the language", default="en")
args = parser.parse_args()

guess = ""
guesses = []

with open ("lang.json", "r") as langdict:
	langdict = json.loads(langdict.read())["languages"][0][f"{args.lang[:2]}"]

if args.daily: 
	with open(f"lang/en_times", "r") as f:
		words = f.read()
	import time
	num = math.floor((time.time() - 1624060800) / 86400) + langdict["languages"][0]["en"]["offset"]
	args.lang = ["languages"][0]["en"]
else:
	with open(f"lang/{args.lang}", "r") as f:
		words = f.read()
	if args.gamecode == -1:
		import random
		num = random.randint(0, (len(words.split("\n"))) - 1)
		print(f"the gamecode is {(num * 86400) + 1624060800}")
	else: num = math.floor((args.gamecode - 1624060800) / 86400)

word = words.split("\n")[num]
print(f"the word was {word.upper()}")
alphab = langdict["writingsystem"]

if langdict["direction"] == "l": o = 0
elif langdict["direction"] == "r": o = 16

curses.wrapper(main)
