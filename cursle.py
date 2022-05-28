#!/usr/bin/env python3

import curses
import argparse
from re import search as res
import random

class globals:
    word = ""
    words = ""
    guess = ["", 0]
    guesses = ["", "", "", "", "", ""]


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
            try:
                try:
                    renderModeCurses.render(stdscr)
                except:
                    pass
                x = str(stdscr.getkey())
            
                if x == "\x0A" or x == "KEY_ENTER":
                    if len(globals.guess[0]) != 5:
                        pass
                    else:
                        globals.guesses[globals.guess[1]] = globals.guess[0].lower()
                        globals.guess[0] = ""
                        globals.guess[1] += 1
                elif x == "\x7f" or x == "KEY_BACKSPACE":
                    globals.guess[0] = globals.guess[0][:-1]
                elif len(globals.guess[0]) >= 5:
                    pass
                elif res("[a-z:]", x.lower()) != None and x != "KEY_RESIZE":
                    globals.guess[0] += x
            except KeyboardInterrupt:
                    curses.endwin()
                    print("the word was {0}".format(globals.word))
                    import sys
                    sys.exit()
        

    def render(stdscr):
        stdscr.bkgd(" ", curses.color_pair(1))
        stdscr.refresh()
        stdscr.clear()
        for i in range(6):
            if len(globals.guesses[i]) == 5:
                a = ""
                b = ""
                c = ""
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

            elif globals.guess[0] != "" and globals.guess[1] == i:
                a = ""
                b = ""
                c = ""
                for j in range(5):
                    a += "┌─┐ "
                    try:
                        b += " " + str(globals.guess[0][j]).upper() + "  "
                    except:
                        b += "    "
                    c += "└─┘ "
                stdscr.addstr("{0}\n{1}\n{2}\n".format(a, b, c), curses.color_pair(1))
            else:
                stdscr.addstr("┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐\n\n└─┘ └─┘ └─┘ └─┘ └─┘\n", curses.color_pair(1))

path = str("en")
f = open(path, "r")
globals.words = f.read()
swords = globals.words.split("\n")
f.close

num = random.randint(0, len(swords))

globals.word = swords[num]
swords = ""

curses.wrapper(renderModeCurses.main)


