### mindmap: Command line tool for keeping notes simple way.

use pyenv (recommended), tested python 3.8.5
- https://github.com/pyenv/pyenv


#### Installation:
```
$ pip install mindmap
$ mindmap -r

```

#### Usage
```
$ mindmap 
using default scope: general
usage: mindmap.py [-h] [--init INIT] [-s SCOPE] [-n NAME] [-ap APPEND] [-v] [-r] [-a] [-l]

Command line tool for keeping notes simple way.

optional argumemindmap:
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
$ mindmap -r # read notes
using default scope and name: general/todo
nothing here...
you can append note to default scope and name via command;
$ mindmap -ac "test" # append "test" to notes
$ mindmap -av # append vim content to notes


$ mindmap -ac "test"
using default scope and name: general/todo
note saved to /home/coronoa/mindmap/general/todo.md

$ mindmap -r # read notes
using default scope and name: general/todo

test

# you can customize scope and name with (-s, -n)
# just add below lines, doesnt matter read, list or append mode

$ mindmap -s scope_name -n filename -ac "custom scope and name test"
note saved to /home/coronoa/mindmap/scope_name/filename.md

$ mindmap -ra # read all notes
$ mindmap -la # list all notes

# combine with grep command for more flexibiility
$ mindmap -ra | grep search  # print all notes and find 'search'


```

### todo
- upload pypi
- mindmap folder can be store git or dropbox (conflict problems)