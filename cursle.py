import argparse, curses, json, hashlib, random, time

class Cursle:
	def __init__(self):
		try:
			words = open(f"lang/{args.length}/{args.lang}", "r").read()
		except FileNotFoundError:
			words = open(f"lang/5/en", "r").read()
			args.length = 5

		with open("lang.json", "r") as langdict:
			langdict = json.loads(langdict.read())["languages"][f"{args.lang[:2]}"]
		if args.daily:
			args.wordcode = round(time.time())
			args.tries = 6
		elif args.wordcode == -1:
			args.wordcode = random.randint(0, 999999999)
		word = hashlib.sha512()
		word.update(bytes(args.wordcode // 86400))
		try:
			args.difficulty = {"easy": len(words.split("\n")) // 8, "medium": len(words.split("\n")) // 4, "hard": len(words.split("\n")) // 2, "obscure": len(words.split("\n"))}[args.difficulty]
		except:
			if type(args.difficulty) == "int" and args.difficulty > len(words).split("\n"):
				args.diffculty = len(words)

		word = [words.split("\n")[:args.difficulty][int(word.hexdigest(), 16) % len(words.split("\n")[:args.difficulty]) - 1]]

		alphab = langdict["writingsystem"]
		if langdict["direction"] == "l":
			offset = 0
		elif langdict["direction"] == "r":
			offset = 16

		if args.tries == -1:
			args.tries = len(alphab) // args.length + 1

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
		render.renderinit(screen, game, screen.getmaxyx()[1] // 2)
	except curses.error:
		screen.refresh()
		screen.clear()
		if args.length * 4 >= len(game.alphab): minx = args.length
		else: minx = len(game.alphab)
		screen.addstr(f"terminal too small\n must be >= {minx}x{args.tries * 3 + 2}")
	while True:
		if len(game.guesses) > 0 and game.guesses[-1] == game.word[0] or len(game.guesses) == args.tries:
			end(screen, game)

		key = str(screen.get_wch())
		halfx = screen.getmaxyx()[1] // 2

		if key == "409":
			try:
				_, x, y, _, _ = curses.getmouse()
			except curses.error:
				x, y = 0, 0
			if len(game.guess) < args.length and y == 3 * args.tries + 1:
				try:
					game.guess += game.alphab[x - halfx - len(game.alphab) // 2]
					render.guessing(screen, game, halfx)
				except IndexError:
					pass
			elif y == 3 * args.tries:
				if x > halfx - 9 and x < halfx - 3:
					key = "\n"
				elif x > halfx - 3 and x < halfx + 7:
					key = "263"

		if key == "1":
			end(screen, game)
		elif key == "[":
			key = ""
		elif key == "410":
			try: 
				render.renderinit(screen, game, halfx)
				if len(game.guesses) != 0:
					render.guessed(screen, game, halfx)
				render.guessing(screen, game, halfx)
			except curses.error: 
				screen.refresh()
				if args.length * 4 >= len(game.alphab): minx = args.length
				else: minx = len(game.alphab)
				screen.addstr(f"terminal too small\n must be >= {minx}x{args.tries * 3 + 2}")
		elif key == "\n" and game.guess in game.words != None and len(game.guess) == args.length:
			game.guesses.append(game.guess)
			game.guess = ""
			render.guessed(screen, game, halfx)
		elif key == "263":
			game.guess = game.guess[:-1]
			render.guessing(screen, game, halfx)
		elif len(game.guess) != args.length and len(key) == 1 and key.lower() in game.alphab:
			game.guess += key.lower()
			render.guessing(screen, game, halfx)

def end(screen, game):
	if not args.daily:
		mode = "free"
	if args.daily:
		mode = "daily"
	stats = json.load(open("stats.json", "r"))

	while len(stats[mode]["winsbyattempts"]) < args.tries:
		stats[mode]["winsbyattempts"].append(0)

	if game.guesses == [] or game.guesses[-1] != game.word[0]:
		stats[mode]["losses"] += 1
	elif game.guesses[-1] == game.word[0]:
		stats[mode]["winsbyattempts"][len(game.guesses) - 1] += 1
		stats[mode]["wins"] += 1
	
	render.end(screen, game, stats[mode])

	with open(f"stats.json", "w") as f:
		f.write(json.dumps(stats))
	
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
	def renderinit(screen, game, halfx):
		screen.refresh()
		screen.clear()
		for i in range(args.tries):
			screen.addstr(i * 3, halfx - (args.length * 2 - 1), "╭─╮ "*args.length)
			screen.addstr(i * 3 + 2, halfx - (args.length * 2 - 1), "╰─╯ "*args.length)
		screen.addstr(3 * args.tries, halfx - 7, "ENTER BACKSPACE")
		screen.addstr(3 * args.tries + 1, halfx - len(game.alphab) // 2, game.alphab.upper())

	def guessed(screen, game, halfx):
		for i in range(len(game.guesses)):
			for j in range(args.length):
				if game.word[0][j] == game.guesses[i][j]:
					colour = curses.color_pair(2)
					screen.addstr(i * 3 + 2, halfx - (args.length * 2 - 1) + (j * 4), "╰v╯", colour)
				elif game.word[0][j] != game.guesses[i][j] and game.guesses[i][j] in game.word[0]:
					colour = curses.color_pair(3)
					screen.addstr(i * 3 + 2, halfx - (args.length * 2 - 1) + (j * 4), "╰-╯", colour)
				elif game.word[0][j] != game.guesses[i][j] and game.guesses[i][j] not in game.word[0]:
					colour = curses.color_pair(1)
					screen.addstr(i * 3 + 2, halfx - (args.length * 2 - 1) + (j * 4), "╰x╯", colour)
				screen.addstr(i * 3 + 1, halfx - (args.length * 2 - 1) + abs(j * 4 - game.offset), f"│{game.guesses[i][j].upper()}│", colour)
				screen.addstr(i * 3, halfx - (args.length * 2 - 1) + (j * 4), "╭─╮", colour)
	
	def guessing(screen, game, halfx):
		i = len(game.guesses)
		screen.addstr(i * 3 + 1, abs(len(game.guess) * 4 - game.offset) + halfx - (args.length * 2 - 2), " ")
		for j in range(args.length):
			try:
				screen.addstr(i * 3 + 1, abs(j * 4 - game.offset) + halfx - (args.length * 2 - 2), game.guess[j].upper())
			except:
				break
	
	def end(screen, game, stats):
		br = " ▏▎▍▌▋▊▉█"
		screen.clear()
		halfx = screen.getmaxyx()[1] // 2
		maxs = stats["winsbyattempts"][:]
		maxs.sort()
		maxs = maxs[-1]
		
		for i in range(args.tries):
			if i + 1 == len(game.guesses) and game.guesses[-1] == game.word[0]:
				colour = curses.color_pair(2)
			elif i + 1 != len(game.guesses) or game.guesses[-1] != game.word[0]:
				colour = curses.color_pair(0)	
			try:
				segments, subsegments = round(stats["winsbyattempts"][i] / maxs * (args.length * 4 - 3)), round((stats["winsbyattempts"][i] / maxs - int(stats["winsbyattempts"][i] / maxs)) * 8)
			except ZeroDivisionError:
				segments, subsegments = round(stats["winsbyattempts"][i] / 1 * (args.length * 4 - 3)), round((stats["winsbyattempts"][i] / 1 - int(stats["winsbyattempts"][i] / 1)) * 8)

			screen.addstr(i * 3, halfx - (args.length * 2 - 1), f"╭{'─'*(args.length * 4 - 3)}╮", colour)
			screen.addstr(i * 3 + 1, halfx - (args.length * 2 - 1), f"│{br[0]*(args.length * 4 - 3)}│ {stats['winsbyattempts'][i]}", colour)
			if subsegments > 0:
				screen.addstr(i * 3 + 1, halfx - (args.length * 2 - 2), f"{br[8]*segments}{br[subsegments]}", colour)
			else:
				screen.addstr(i * 3 + 1, halfx - (args.length * 2 - 2), f"{br[8]*segments}", colour)
			screen.addstr(i * 3 + 2, halfx - (args.length * 2 - 1), f"╰{'─'*(args.length * 4 - 3)}╯", colour)

		try:
			screen.addstr(3 * args.tries, halfx - 7, f"Wins: {stats['wins']}  Losses: {stats['losses']}")
		except ZeroDivisionError:
			screen.addstr(3 * args.tries, halfx - 9, f"Wins: {stats['wins']}  Losses: {stats['losses']}")

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
