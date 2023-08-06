### snos: Command line tool for keeping notes simple way.

use pyenv (recommended), tested python 3.8.5
- https://github.com/pyenv/pyenv


#### Installation:
```
$ pip install snos
$ snos -r

```

#### Usage
```
$ python3 snos.py 
using default scope: general
usage: snos.py [-h] [--init INIT] [-s SCOPE] [-n NAME] [-ap APPEND] [-v] [-r] [-a] [-l]

Command line tool for keeping notes simple way.

optional argumesnos:
  -h, --help            show this help message and exit
  -s SCOPE, --scope SCOPE
                        scope of the note.
  -n NAME, --name NAME  name of the notes.
  -ap APPEND, --append APPEND
                        append note
  -v, --vim             append note via vim
  -r, --read            print all of the notes
  -a, --all             print all of the notes
  -l, --list            list all of the note names

```

#### Basic examples:
```
$ python snos.py -r # read notes
using default scope and name: general/todo
nothing here...
you can append note to default scope and name via command;
$ python3 snos.py -ac "test" # append "test" to notes
$ python3 snos.py -av # append vim content to notes


$ python3 snos.py -ac "test"
using default scope and name: general/todo
note saved to /home/coronoa/snos/general/todo.md

$ python snos.py -r # read notes
using default scope and name: general/todo

test

# you can customize scope and name with (-s, -n)
# just add below lines, doesnt matter read, list or append mode

$ python3 snos.py -s scope_name -n filename -ac "custom scope and name test"
note saved to /home/coronoa/snos/scope_name/filename.md

$ python snos.py -ra # read all notes
$ python snos.py -la # list all notes

# combine with grep command for more flexibiility
$ python snos.py -ra | grep search  # print all notes and find 'search'


```

### todo
- upload pypi
- snos folder can be store git or dropbox (conflict problems)