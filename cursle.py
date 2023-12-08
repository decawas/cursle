#!/usr/bin/env python3

import argparse, curses, json, hashlib, math
from re import search as res

class Cursle:
	def __init__(self):
		try:
			with open(f"lang/{args.length}/{args.lang}", "r") as f: words = f.read()
		except FileNotFoundError:
			with open(f"lang/5/en", "r") as f: words = f.read()
			args.length = 5

		with open("lang.json", "r") as langdict:
			langdict = json.loads(langdict.read())["languages"][f"{args.lang[:2]}"]
		if args.daily:
			import time
			args.wordcode = round(time.time())
		elif args.wordcode == -1:
			import random
			args.wordcode = random.randint(0, 999999999)
		hashh = hashlib.sha512()
		hashh.update(bytes(round(args.wordcode / 86400)))
		word = [words.split("\n")[:25000][int(hashh.hexdigest(), 16) % len(words.split("\n")[:25000]) - 1]]

		alphab = langdict["writingsystem"]

		if langdict["direction"] == "l": offset = 0
		elif langdict["direction"] == "r": offset = 16

		if args.tries == -1: args.tries = math.floor(len(alphab) / args.length) + 1

		self.word = word
		self.words = words
		self.alphab = alphab
		self.offset = offset
		self.guess = ""
		self.guesses = []

def cursesinit(stdscr):
	curses.init_pair(1, 7, 0)
	curses.init_pair(2, 2, 0)
	curses.init_pair(3, 3, 0) 

	curses.start_color()
	curses.curs_set(0)
	stdscr.keypad(True)
	stdscr.bkgd(" ", curses.color_pair(1))
	curses.mousemask(1)
	
def main(stdscr):
	game = Cursle()
	cursesinit(stdscr)
	render.renderinit(stdscr, game)
	while True:
		key = str(stdscr.get_wch())

		if key == "410":
			try: 
				render.renderinit(stdscr, game)
				if len(game.guesses) != 0: render.guessed(stdscr, game)
				render.guessing(stdscr, game)
			except curses.error: 
				stdscr.refresh()
				stdscr.clear()
				stdscr.addstr("bad")

		if key == "409":
			try: _, x, y, _, _ = curses.getmouse()
			except curses.error: x, y = 0, 0
			if len(game.guess) < args.length and y == 3 * args.tries + 1:
				try: 
					game.guess += game.alphab[x - math.floor(stdscr.getmaxyx()[1] / 2) - math.floor(len(game.alphab) / 2)]
					render.guessing(stdscr, game)
				except IndexError: pass
			elif y == 3 * args.tries:
				if x > math.floor(stdscr.getmaxyx()[1] / 2) - 9 and x < math.floor(stdscr.getmaxyx()[1] / 2) - 3: key = "\n"
				elif x > math.floor(stdscr.getmaxyx()[1] / 2) - 3 and x < math.floor(stdscr.getmaxyx()[1] / 2) + 7: key = "263"

		if key == "1":
			curses.endwin()
			print(f"the word was {game.word[0].upper()}")
			print(f"the wordcode is {args.wordcode}")
			raise SystemExit
		elif key == "\n" and res(f"{game.guess}\n", game.words) != None and len(game.guess) == args.length:
				game.guesses.append(game.guess)
				game.guess = ""
				render.guessed(stdscr, game)
		elif key == "263":
			game.guess = game.guess[:-1]
			render.guessing(stdscr, game)
		elif len(game.guess) != args.length and len(key) == 1 and res(key, game.alphab) != None:
			game.guess += key
			render.guessing(stdscr, game)

class render:
	def renderinit(stdscr, game):
		stdscr.refresh()
		stdscr.clear()
		mx = math.floor(stdscr.getmaxyx()[1] / 2)
		for i in range(args.tries):
			for j in range(args.length):
				stdscr.addstr(i * 3, mx - (args.length * 2 - 1) + (j * 4), "╭─╮")
				stdscr.addstr(i * 3 + 2, mx - (args.length * 2 - 1) + (j * 4), "╰─╯")

		stdscr.addstr(3 * args.tries, mx - 7, "ENTER BACKSPACE")
		stdscr.addstr(3 * args.tries + 1, mx - math.floor(len(game.alphab) / 2), game.alphab.upper())
	def guessed(stdscr, game):
		mx = math.floor(stdscr.getmaxyx()[1] / 2)
		for i in range(len(game.guesses)):
			for j in range(args.length):
				if game.word[0][j] == game.guesses[i][j]:
					colour = 2
					stdscr.addstr(i * 3 + 2, mx - (args.length * 2 - 1) + (j * 4), "╰v╯", curses.color_pair(colour))
				elif game.word[0][j] != game.guesses[i][j] and res(game.guesses[i][j], game.word[0]) != None:
					colour = 3
					stdscr.addstr(i * 3 + 2, mx - (args.length * 2 - 1) + (j * 4), "╰-╯", curses.color_pair(colour))
				elif game.word[0][j] != game.guesses[i][j] and res(game.guesses[i][j], game.word[0]) == None:
					colour = 1
					stdscr.addstr(i * 3 + 2, mx - (args.length * 2 - 1) + (j * 4), "╰x╯", curses.color_pair(colour))
				stdscr.addstr(i * 3, mx - (args.length * 2 - 1) + (j * 4), "╭─╮", curses.color_pair(colour))
				stdscr.addstr(i * 3 + 1, mx - (args.length * 2 - 1) + abs(j * 4 - game.offset), f"│{game.guesses[i][j].upper()}│", curses.color_pair(colour))
	
	def guessing(stdscr, game):
		mx = math.floor(stdscr.getmaxyx()[1] / 2)
		i = len(game.guesses)
		for j in range(args.length):
			stdscr.addstr(i * 3 + 1, abs(j * 4 - game.offset) + mx - (args.length * 2 - 2), " ")
			try: stdscr.addstr(i * 3 + 1, abs(j * 4 - game.offset) + mx - (args.length * 2 - 2), game.guess[j].upper())
			except: pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Cursle")
	parser.add_argument("--daily", help="gives you a daily challenge, based on GMT", action="store_true")
	parser.add_argument("--tries", help="set the number of attempts you can make", type=int, default=-1)
	parser.add_argument("--wordcode", help="lets you spread the word to your friends", type=int, default=-1)
	parser.add_argument("--lang", help="select the language", default="en")
	parser.add_argument("--length", help="set word length [experimental]", type=int, default=5)
	args = parser.parse_args()
	curses.wrapper(main)
