# Cursle

cursle is a terminal-based wordle clone made in Python and ncurses which you can play as many times as you like, challenge your friends by sending them a wordcode or do a daily challeng

## To run:

Clone the repository with "git clone https://github.com/decawas/cursle" or you can Download ZIP<br />
Then open the directory in a terminal and type "python ./cursle.py [args]"<br />

## Arguments:

--daily - gives you a daily challenge, based on GMT only<br />
--difficulty - set game diffculty, can be 'easy', 'medium', 'hard', 'obscure' or any integer<br />
difficulty will be unpredictable when using en_times or [any list]_old 
--lang - lets you enter a language code to use a language other than english, based on ISO-639-1 language codes.<br />
--length - {experimental} set how many letters are in the word, currently the only option is 6 letters for english<br />
--tries [int] - set the number of attempts you can make<br />
--wordcode [int] - this is a number that sets what word you get in case you had a cool word that you want to do again or to send to a friend

## Languages:

all word lists come from [this source](https://fasttext.cc/docs/en/crawl-vectors.html)<br />
included word lists are:

- de (Deutsch / German)
- en (English)
- es (Español / Spanish)

more word lists can be found at decawas/cursle-lang

### Custom Word lists:
    
create a custom word list and put it in ./lang/<br />
then create an entry in lang.json detailing the writingsystem and direction, the key for the entry must match the name of the file in ./lang/ <br/>
then use the name of the file in ./lang/ as the input for the --lang argument