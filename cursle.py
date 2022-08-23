#!/usr/bin/env python3

import math
import curses
import argparse
from re import search as res

def main(stdscr):
	global guess
	curses.init_pair(1, 7, 0)
	curses.init_pair(2, 2, 0)
	curses.init_pair(3, 3, 0) 
	curses.init_pair(4, 1, 0)

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
			_, x, y, _, _ = curses.getmouse()	
			if len(guess) < 5 and y == 4 * args.tries:
				try: guess += alphab[x]
				except IndexError: pass
			elif y == 4 * args.tries + 1:
				if x < 5 and res(f"\n{guess}\n", words) != None:
						guesses.append(guess)
						guess = ""
				elif x < 15: key = "263"
		
		if key == "1":
			curses.endwin()
			import sys
			sys.exit()
		elif key == "\n" and res(f"\n{guess}\n", words) != None:
				guesses.append(guess)
				guess = ""
		elif key == "263": guess = guess[:-1]
		elif len(guess) != 5 and len(key) == 1 and res(key, alphab) != None: guess += key

def render(stdscr):
	stdscr.refresh()
	stdscr.clear()
	for i in range(args.tries):
		try:
			if len(guesses[i]) == 5:
				for j in range(5):
					if word[j] == guesses[i][j]:
						colour = 2
						stdscr.addstr(i * 4 + 3, j * 4, "YES", curses.color_pair(colour))
					elif word[j] != guesses[i][j] and res(guesses[i][j], word) != None:
						colour = 3
						stdscr.addstr(i * 4 + 3, j * 4, "MID", curses.color_pair(colour))
					elif word[j] != guesses[i][j] and res(guesses[i][j], word) == None:
						colour = 4
						stdscr.addstr(i * 4 + 3, j * 4, "BAD", curses.color_pair(colour))
					stdscr.addstr(i * 4, j * 4, "┌─┐", curses.color_pair(colour))
					stdscr.addstr(i * 4 + 1, j * 4, f"│{guesses[i][j].upper()}│", curses.color_pair(colour))
					stdscr.addstr(i * 4 + 2, j * 4, "└─┘", curses.color_pair(colour))	
		except IndexError:
			if guess != "" and len(guesses) == i:
				for j in range(5):
					stdscr.addstr(i * 4, j * 4, "┌─┐")
					try: stdscr.addstr(i * 4 + 1, j * 4 + 1, guess[j].upper())
					except: pass
					stdscr.addstr(i * 4 + 2, j * 4, "└─┘")
			else: stdscr.addstr(i * 4, 0, "┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐\n\n└─┘ └─┘ └─┘ └─┘ └─┘")
	stdscr.addstr(4 * args.tries, 0, alphab.upper())
	stdscr.addstr(4 * args.tries + 1, 0, "ENTER")
	stdscr.addstr(4 * args.tries + 1, 6, "BACKSPACE")

parser = argparse.ArgumentParser(description="Cursle")
parser.add_argument("--daily", help="gives you the same word as on New York Times, based on GMT only", action="store_true")
parser.add_argument("--tries", help="set the number of attempts you can make", type=int, default=6)
parser.add_argument("--gamecode", help="lets you set the word based on an integer so you can send it to a friend without them knowing the word", type=int, default=-1)
parser.add_argument("--lang", help="select the language", default="en")
args = parser.parse_args()

guess = ""
guesses = []

if args.daily: f = open("lang/en_times", "r")
else: f = open(f"lang/{args.lang}", "r")
words = f.read()
f.close()

if args.daily:
	import time
	num = math.floor((time.time() - 1624060800) / 86400) + 11
elif args.gamecode == -1:
	import random
	num = random.randint(0, (len(words.split("\n"))) - 1)
	print(f"the gamecode is {(num * 86400) + 1624060800}")
else: num = math.floor((args.gamecode - 1624060800) / 86400)

word = words.split("\n")[num]
print(f"the word was {word}")
alphab = words.split("\n")[-1]

curses.wrapper(main)
