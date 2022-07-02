# Cursle

cursle is a terminal-based wordle clone made in python and curses which you can play as many times as you like, challenge your friends by sending them a gamecode or sync with the wordle on New York Times

## To run:

Clone the repository with "git clone https://github.com/decawas/cursle" or you can Download ZIP<br />
Then open the directory in a terminal and type either "./cursle.py [args]" or "python ./cursle.py"<br />
__You can not enter any arguments if you use "python ./cursle.py"__

## Arguments:

--daily - gives you the same word as on New York Times, based on GMT only<br />
--tries [int] - set the number of attempts you can make<br />
--gamecode [int] - this is a number that sets what word you get in case you had a cool word that you want to do again or to send to a friend<br / >
--unfiltered - sets the word list to a much longer list of words, this list is unfiltered unlike so you might not have heard of the word you get __argument can not be used with --daily and --daily will take priority__

## Credits

unfiltered word list comes from: https://github.com/dwyl/english-words