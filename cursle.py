import argparse, curses, json, hashlib, math, random, re, time

class Cursle:
	def __init__(self):
		try:
			with open(f"lang/{args.length}/{args.lang}", "r") as f:
				words = f.read()
		except FileNotFoundError:
			with open(f"lang/5/en", "r") as f:
				words = f.read()
			args.length = 5

		with open("lang.json", "r") as langdict:
			langdict = json.loads(langdict.read())["languages"][f"{args.lang[:2]}"]
		if args.daily:
			args.wordcode = round(time.time())
			args.tries = 6
		elif args.wordcode == -1:
			args.wordcode = random.randint(0, 999999999)
		word = hashlib.sha512()
		word.update(bytes(math.floor(args.wordcode / 86400)))
		if args.difficulty == "easy":
			args.difficulty = int(len(words) / 2)
		elif args.difficulty == "medium":
			args.difficulty = int(len(words) / 2)
		elif args.difficulty == "hard":
			args.difficulty = int(len(words) / 2)
		elif args.difficulty == "obscure":
			args.difficulty = len(words)
		elif type(args.difficulty) == "int" and args.diffculty > len(words):
			args.diffculty = len(words)

		word = [words.split("\n")[:args.difficulty][int(word.hexdigest(), 16) % len(words.split("\n")[:args.difficulty]) - 1]]

		alphab = langdict["writingsystem"]
		if langdict["direction"] == "l":
			offset = 0
		elif langdict["direction"] == "r":
			offset = 16

		if args.tries == -1:
			args.tries = math.floor(len(alphab) / args.length) + 1

		self.word = word
		self.words = words
		self.alphab = alphab
		self.offset = offset
		self.guess = ""
		self.guesses = []

def main(screen):
	curses.init_pair(1, 7, 0)
	curses.init_pair(2, 2, 0)
	curses.init_pair(3, 3, 0) 

	curses.start_color()
	curses.curs_set(0)
	screen.keypad(True)
	screen.bkgd(" ", curses.color_pair(1))
	curses.mousemask(1)

	game = Cursle()
	try:
		render.renderinit(screen, game, math.floor(screen.getmaxyx()[1] / 2))
	except curses.error:
		screen.refresh()
		screen.clear()
		if args.length * 4 >= len(game.alphab): minx = args.length
		else: minx = len(game.alphab)
		screen.addstr(f"terminal too small\n must be >= {minx}x{args.tries * 3 + 2}")
	x, y = 0, 0
	while True:
		if len(game.guesses) > 0 and game.guesses[-1] == game.word[0] or len(game.guesses) == args.tries:
			end(screen, game)

		key = str(screen.get_wch())
		maxx = math.floor(screen.getmaxyx()[1] / 2)

		if key == "409":
			_, x, y, _, _ = curses.getmouse()
			if len(game.guess) < args.length and y == 3 * args.tries + 1:
				try: 
					game.guess += game.alphab[x - maxx - math.floor(len(game.alphab) / 2)]
					render.guessing(screen, game)
				except IndexError:
					pass
			elif y == 3 * args.tries:
				if x > maxx - 9 and x < maxx - 3:
					key = "\n"
				elif x > maxx - 3 and x < maxx + 7:
					key = "263"

		if key == "1":
			end(screen, game)
		elif key == "[":
			key = ""
		elif key == "410":
			try: 
				render.renderinit(screen, game, maxx)
				if len(game.guesses) != 0:
					render.guessed(screen, game, maxx)
				render.guessing(screen, game, maxx)
			except curses.error: 
				screen.refresh()
				if args.length * 4 >= len(game.alphab): minx = args.length
				else: minx = len(game.alphab)
				screen.addstr(f"terminal too small\n must be >= {minx}x{args.tries * 3 + 2}")
		elif key == "\n" and re.search(f"{game.guess}\n", game.words) != None and len(game.guess) == args.length:
			game.guesses.append(game.guess)
			game.guess = ""
			render.guessed(screen, game, maxx)
		elif key == "263":
			game.guess = game.guess[:-1]
			render.guessing(screen, game, maxx)
		elif len(game.guess) != args.length and len(key) == 1 and re.search(key, game.alphab) != None:
			game.guess += key
			render.guessing(screen, game, maxx)

def end(screen, game):
	if not args.daily:
		mode = "free"
	if args.daily:
		mode = "daily"
	with open(f"{mode}.stats", "r") as f:
		stats = f.read().split(",")

	for i in range(len(stats)):
		stats[i] = int(stats[i])
	while len(stats) - 2 < args.tries:
		stats.append(0)

	if game.guesses == [] or game.guesses[-1] != game.word[0]:
		stats[1] += 1
	elif game.guesses[-1] == game.word[0]:
		stats[len(game.guesses) + 1] += 1
		stats[0] += 1
	
	render.end(screen, game, stats)

	with open(f"{mode}.stats", "w") as f:
		f.write(str(stats)[1:-1])
	
	while True:
		key = str(screen.get_wch())
		if key == "1":
			curses.endwin()
			print(f"the word was {game.word[0].upper()}")
			print(f"the wordcode is {args.wordcode}")
			raise SystemExit
		
		if key == "410":
			try:
				render.end(screen, game, stats)
			except curses.error:
				screen.refresh()
				screen.clear()
				if args.length * 4 >= len(game.alphab): minx = args.length
				else: minx = len(game.alphab)
				screen.addstr(f"terminal too small\n must be >= {minx}x{args.tries * 3 + 2}")

class render:
	def renderinit(screen, game, maxx):
		screen.refresh()
		screen.clear()
		for i in range(args.tries):
			screen.addstr(i * 3, maxx - (args.length * 2 - 1), "╭─╮ "*args.length)
			screen.addstr(i * 3 + 2, maxx - (args.length * 2 - 1), "╰─╯ "*args.length)
		screen.addstr(3 * args.tries, maxx - 7, "ENTER BACKSPACE")
		screen.addstr(3 * args.tries + 1, maxx - math.floor(len(game.alphab) / 2), game.alphab.upper())

	def guessed(screen, game, maxx):
		for i in range(len(game.guesses)):
			for j in range(args.length):
				if game.word[0][j] == game.guesses[i][j]:
					colour = curses.color_pair(2)
					screen.addstr(i * 3 + 2, maxx - (args.length * 2 - 1) + (j * 4), "╰v╯", colour)
				elif game.word[0][j] != game.guesses[i][j] and re.search(game.guesses[i][j], game.word[0]) != None:
					colour = curses.color_pair(3)
					screen.addstr(i * 3 + 2, maxx - (args.length * 2 - 1) + (j * 4), "╰-╯", colour)
				elif game.word[0][j] != game.guesses[i][j] and re.search(game.guesses[i][j], game.word[0]) == None:
					colour = curses.color_pair(1)
					screen.addstr(i * 3 + 2, maxx - (args.length * 2 - 1) + (j * 4), "╰x╯", colour)
				screen.addstr(i * 3 + 1, maxx - (args.length * 2 - 1) + abs(j * 4 - game.offset), f"│{game.guesses[i][j].upper()}│", colour)
				screen.addstr(i * 3, maxx - (args.length * 2 - 1) + (j * 4), "╭─╮", colour)
	
	def guessing(screen, game, maxx):
		i = len(game.guesses)
		screen.addstr(i * 3 + 1, abs(len(game.guess) * 4 - game.offset) + maxx - (args.length * 2 - 2), " ")
		for j in range(args.length):
			try:
				screen.addstr(i * 3 + 1, abs(j * 4 - game.offset) + maxx - (args.length * 2 - 2), game.guess[j].upper())
			except:
				break
	
	def end(screen, game, stats):
		br = " ▏▎▍▌▋▊▉█─"
		screen.clear()
		maxx = math.floor(screen.getmaxyx()[1] / 2)
		maxs = stats[2:]
		maxs.sort()
		maxs = maxs[-1]
		
		for i in range(args.tries):
			if i + 1 == len(game.guesses) and game.guesses[-1] == game.word[0]:
				colour = curses.color_pair(2)
			elif i + 1 != len(game.guesses) or game.guesses[-1] != game.word[0]:
				colour = curses.color_pair(0)	
			try:
				segments, subsegments = round(stats[i + 2] / maxs * (args.length * 4 - 3)), round((stats[i + 2] / maxs - int(stats[i + 2] / maxs)) * 8)
			except ZeroDivisionError:
				segments, subsegments = round(stats[i + 2] / 1 * (args.length * 4 - 3)), round((stats[i + 2] / 1 - int(stats[i + 2] / 1)) * 8)

			screen.addstr(i * 3, maxx - (args.length * 2 - 1), f"╭{br[9]*(args.length * 4 - 3)}╮", colour)
			screen.addstr(i * 3 + 1, maxx - (args.length * 2 - 1), f"│{br[0]*(args.length * 4 - 3)}│ {stats[i+2]}", colour)
			if subsegments > 0:
				screen.addstr(i * 3 + 1, maxx - (args.length * 2 - 2), f"{br[8]*segments}{br[subsegments]}", colour)
			else:
				screen.addstr(i * 3 + 1, maxx - (args.length * 2 - 2), f"{br[8]*segments}", colour)
			screen.addstr(i * 3 + 2, maxx - (args.length * 2 - 1), f"╰{br[9]*(args.length * 4 - 3)}╯", colour)

		try:
			screen.addstr(3 * args.tries, maxx - 7, f"Wins: {stats[0]}  Losses: {stats[1]}")
		except ZeroDivisionError:
			screen.addstr(3 * args.tries, maxx - 9, f"Wins: {stats[0]}  Losses: {stats[1]}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Cursle")
	parser.add_argument("--daily", help="gives you a daily challenge, based on GMT", action="store_true")
	parser.add_argument("--difficulty", help="set game diffculty", default="medium")
	parser.add_argument("--lang", help="select the language", default="en")
	parser.add_argument("--length", help="set word length [experimental]", type=int, default=5)
	parser.add_argument("--tries", help="set the number of attempts you can make", type=int, default=-1)
	parser.add_argument("--wordcode", help="lets you spread the word to your friends", type=int, default=-1)
	args = parser.parse_args()

	curses.wrapper(main)
