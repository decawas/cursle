# Cursle

cursle is a terminal-based wordle clone made in python and curses which you can play as many times as you like, challenge your friends by sending them a gamecode or sync with the wordle on New York Times

## To run:

Clone the repository with "git clone https://github.com/decawas/cursle" or you can Download ZIP<br />
Then open the directory in a terminal and type either "./cursle.py [args]" or "python ./cursle.py"<br />
__You can not enter any arguments if you use "python ./cursle.py"__

## Arguments:

--daily - gives you the same word as on New York Times, based on GMT only<br />
--tries [int] - set the number of attempts you can make<br />
--gamecode [int] - this is a number that sets what word you get in case you had a cool word that you want to do again or to send to a friend<br />
--lang - lets you enter a language code to use a language other than english, based on ISO-639-1 language codes.  __this argument can not be used with --daily and --daily will take priority__

## Languages:

- br (brezhoneg / Breton)
- ca (català / Catalan)
- cy (Cymraeg / Welsh)
- de (Deutsch / German) [old source](https://woertchen.sofacoach.de/) [other old source](https://sourceforge.net/projects/germandict/)
- el (Ελληνικά / Greek)
- en (English) [old source](https://github.com/dwyl/english-words)
- en_times (The list on New York Times) [source](https://www.nytimes.com/games/wordle/index.html)
- es (Español / Spanish) [old source](https://wordle-es.xavier.cc/)
- gl (Galego / Galician)
- fr (français / french) [old source](https://github.com/hbenbel/French-Dictionary)
- fy (Frysk / Frisian)
- it (Italiani / Italian) [old source](https://parolle.it/)
- kw (Kernowek / Cornish)
- pl (Polski / Polish)
- pt (Português / Portuguese)
- ru (Русский / Russian)
- sv (Svenska / Swedish) [old source](https://github.com/martinlindhe/wordlist_swedish)
- tr (Türkçe / Turkish)
- uk (українська / Ukrainian)

all new word lists come from [this source](https://fasttext.cc/docs/en/crawl-vectors.html)

all word lists in /lang which end in "_old" are an older and much smaller version of that word list

### Custom Word lists:
    
to add a custom word list put the file into the lang folder and to use it write the file name as the input for --lang

## --daily might be out of sync

Sometimes --daily is a few words behind New York Times, this happens because New York Times occasionally skips a word which is not accounted for automatically in cursle, I have been doing my best to make a commit each time that New York Times skips a word but if I havent adjusted for a skip then you should edit cursle.py and increment the integer at the end of line 89