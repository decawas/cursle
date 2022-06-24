#!/usr/bin/env python3

import curses
import argparse
from re import search as res

class globals:
    word = ""
    words = ""
    guess = ""
    guesses = []

class renderModeCurses:
    def main(stdscr):
        try:
            curses.init_pair(1, 7, 16) # none
            curses.init_pair(2, 2, 16) # place
            curses.init_pair(3, 3, 16) # letter 
            curses.init_pair(4, 1, 16) # bad
        except:
            curses.init_pair(1, 7, 0) # none
            curses.init_pair(2, 2, 0) # place
            curses.init_pair(3, 3, 0) # letter 
            curses.init_pair(4, 1, 0) # bad
        
        curses.start_color()
        curses.curs_set(0)
        stdscr.keypad(True)

        while True:
            renderModeCurses.render(stdscr)

            key = str(stdscr.getkey()).lower()
            
            if key == "\n" or key == "key_enter":
                if len(globals.guess) != 5 or res(globals.guess ,globals.words) == None: pass
                else:
                    globals.guesses.append(globals.guess)
                    globals.guess = ""
            elif key == "key_backspace": globals.guess = globals.guess[:-1]
            elif len(globals.guess) >= 5: pass
            elif res("[a-z]", key) != None:
                globals.guess += key
            fi = open("a.txt", "a")
            fi.write(globals.guess)
            fi.write("\n")
            fi.write(str(key))
            fi.close()
        
    def render(stdscr):
        stdscr.bkgd(" ", curses.color_pair(1))
        stdscr.refresh()
        stdscr.clear()
        fi = open("a.txt", "a")
        fi.write(globals.guess)
        fi.write("\n")
        fi.close()
        i = 0
        for i in range(args.tries):
            try:
                if len(globals.guesses[i]) == 5:
                    for j0 in range(5):
                        if globals.word[j0] == globals.guesses[i][j0]: stdscr.addstr("┌─┐ ", curses.color_pair(2))
                        elif globals.word[j0] != globals.guesses[i][j0] and res(globals.guesses[i][j0], globals.word) != None: stdscr.addstr("┌─┐ ", curses.color_pair(3))
                        elif globals.word[j0] != globals.guesses[i][j0] and res(globals.guesses[i][j0], globals.word) == None: stdscr.addstr("┌─┐ ", curses.color_pair(4))
                    stdscr.addstr("\n")
                    for j1 in range(5):
                        if globals.word[j1] == globals.guesses[i][j1]: stdscr.addstr("│" + str(globals.guesses[i][j1]).upper() + "│ ", curses.color_pair(2))
                        elif globals.word[j1] != globals.guesses[i][j1] and res(globals.guesses[i][j1], globals.word) != None: stdscr.addstr("│" + str(globals.guesses[i][j1]).upper() + "│ ", curses.color_pair(3))
                        elif globals.word[j1] != globals.guesses[i][j1] and res(globals.guesses[i][j1], globals.word) == None: stdscr.addstr("│" + str(globals.guesses[i][j1]).upper() + "│ ", curses.color_pair(4))
                    stdscr.addstr("\n")
                    for j2 in range(5):
                        if globals.word[j2] == globals.guesses[i][j2]: stdscr.addstr("└─┘ ", curses.color_pair(2))
                        elif globals.word[j2] != globals.guesses[i][j2] and res(globals.guesses[i][j2], globals.word) != None: stdscr.addstr("└─┘ ", curses.color_pair(3))
                        elif globals.word[j2] != globals.guesses[i][j2] and res(globals.guesses[i][j2], globals.word) == None: stdscr.addstr("└─┘ ", curses.color_pair(4))
                    stdscr.addstr("\n")
            except:
                if globals.guess != "" and len(globals.guesses) == i:
                    a = ""
                    b = ""
                    c = ""
                    for j in range(5):
                        a += "┌─┐ "
                        try:
                            b += " " + globals.guess[j].upper() + "  "
                        except:
                            b += "    "
                        c += "└─┘ "
                    stdscr.addstr("{0}\n{1}\n{2}\n".format(a, b, c), curses.color_pair(1))
                else:
                    stdscr.addstr("┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐\n\n└─┘ └─┘ └─┘ └─┘ └─┘\n", curses.color_pair(1))

        if globals.guesses:
            pass

parser = argparse.ArgumentParser(description="Wordle")
parser.add_argument("--daily", help="syncs with the real wordle on new york times", action="store_true")
parser.add_argument("--tries", help="number of tries", type=int, default=6)
args = parser.parse_args()

path = "en"
f = open(path, "r")
globals.words = f.read()
swords = globals.words.split("\n")
f.close

if args.daily:
    import time
    import math
    num = math.floor((time.time() - 1624060800) / 86400) + 4
else:
    import random
    num = random.randint(0, len(swords))

globals.word = swords[num]
swords = None
print("the word was {0}".format(globals.word))

curses.wrapper(renderModeCurses.main)
