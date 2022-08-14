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
--lang - lets you enter a language code to use a language other than english, based on ISO-639 language codes.  __this argument can not be used with --daily and --daily will take priority__

## Languages:

### Current languages:

- en (English)
- enu (English but unfiltered word list)
- es (Español / Spanish)
- de (Deutsch / German)
- fr (français / french)
- it (Italiani / Italian)
- sv (Svenska / Swedish)

### Future languages:

- bn (বাংলা / Bengali)
- br (brezhoneg / Breton)
- ca (català / Catalan)
- cy (Cymraeg / Welsh)
- fy (Frysk / Frisian)
- ga (Gaeilge / Irish)
- gd (Gàidhlig / Scottish)
- gl (Galego / Galician)
- gr (Ελληνικά / Greek)
- hi (हिन्दी / Hindi)
- kw (Kernowek / Cornish)
- pt (Português / Portuguese)
- tr (Türk / Turkish)

### Custom Word lists:
    
to add a custom word list put the file into the lang folder and to use it write the file name as the input for --lang

## Credits:

[Unfiltered English words list](https://github.com/dwyl/english-words)<br />
[Italian words list](https://parolle.it/)<br />
[french words list](https://github.com/hbenbel/French-Dictionary)<br />
[German words list](https://woertchen.sofacoach.de/) and [here too](https://sourceforge.net/projects/germandict/)<br />
[Spanish words list](https://wordle-es.xavier.cc/)<br />
[Swedish words list](https://github.com/martinlindhe/wordlist_swedish)<br />

## --daily might be out of sync

Sometimes --daily is a few words behind New York Times, this happens because New York Times occasionally skips a word which is not accounted for automatically in cursle, I have been doing my best to make a commit each time that New York Times skips a word but if I havent adjusted for a skip then you should edit cursle.py and increment the integer at the end of line 104
