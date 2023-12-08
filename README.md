# Cursle

cursle is a terminal-based wordle clone made in Python and curses which you can play as many times as you like, challenge your friends by sending them a wordcode or sync with the wordle on New York Times

## To run:

Clone the repository with "git clone https://github.com/decawas/cursle" or you can Download ZIP<br />
Then open the directory in a terminal and type either "./cursle.py [args]" or "python ./cursle.py"<br />
__You can not enter any arguments if you use "python ./cursle.py"__

## Arguments:

--daily - gives you a daily challenge, based on GMT only<br />
--tries [int] - set the number of attempts you can make<br />
--wordcode [int] - this is a number that sets what word you get in case you had a cool word that you want to do again or to send to a friend<br />
--lang - lets you enter a language code to use a language other than english, based on ISO-639-1 language codes.<br />
--length - {experimental} set how many letters are in the word, currently the only option is 6 letters for english

## Languages:

- af (Afrikaans)
- ar (العربية / Arabic)
- bg (български / Bulgarian)
- br (Brezhoneg / Breton)
- ca (Català / Catalan)
- cy (Cymraeg / Welsh)
- da (Dansk / Danish)
- de (Deutsch / German) [old source](https://woertchen.sofacoach.de/) and [other old source](https://sourceforge.net/projects/germandict/)
- el (Ελληνικά / Greek)
- en (English) [old source](https://github.com/dwyl/english-words)
- en_times (The list from New York Times) [source](https://www.nytimes.com/games/wordle/index.html)
- eo (Esperanto)
- es (Español / Spanish)
- et (eesti keel / Estonian)
- eu (Euskara / Basque)
- fi (Suomi / Finnish)
- fo (Føroyskt / Faroese)
- fr (français / french) [old source](https://github.com/hbenbel/French-Dictionary)
- fy (Frysk / Frisian)
- ga (Gaeilge / Irish)
- gd (Gàidhlig / Scottish)
- gl (Galego / Galician)
- he (עִבְרִית / Hebrew)
- hi (हिन्दी / Hindi)
- hu (Magyar / Hungarian)
- id (Bahasa Indonesia / Indonesian)
- is (Íslenska / Islandic)
- it (italiani / italian)
- kw (Kernowek / Cornish)
- la (Latin)
- lt (lietuvių / Lithuanian)
- lv (latviski / Lativan)
- mt (Malti / Maltese)
- nl (Nederlands / Dutch)
- no (Norsk / Norweigan)
- pl (Polski / Polish)
- pt (Português / Portuguese)
- ru (Русский / Russian)
- sr (бугарски / Serbian)
- sv (Svenska / Swedish) [old source](https://github.com/martinlindhe/wordlist_swedish)
- tr (Türkçe / Turkish)
- uk (українська / Ukrainian)

all word lists come from [this source](https://fasttext.cc/docs/en/crawl-vectors.html)

all word lists in /lang which end in "_old" are an older and much smaller version of that word list

### Custom Word lists:
    
create a custom word list and put it in ./lang/<br />
then create an entry in lang.json detailing the writingsystem and direction, the key for the entry must match the name of the file in ./lang/ <br/>
then use the name of the file in ./lang/ as the input for the --lang argument