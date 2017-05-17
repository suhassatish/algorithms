<img src="https://www.Msoft.com/sites/default/files/3C_Msoft_logo.svg"
     align="right" valign="top" width="125" alt="MSoft" />

# Collaborative Programming Exercise

## Directory Structure Layout

This is the current layout of all the files included inside the repo

    /dataset: contains all tests suites and the expected results for each phase.
    /python: Python implementation of the tests suite using unittest

The validation environment for your parser uses the Python Standard Library,
no extra dependencies are required and runs on the latest Python 2.x

#### Plug your implementation

You can start the project by running
```
python test.py
```

Which will run all tests against the skeleton parser; *mml/parser.py* that
you need to implement.

Your parser receives a single input, `mml`.  `mml` is an object which has two methods:

- `next_char` returns the next character. If the end of the stream is reached, it will return ''.
- `is_eof` returns True if all characters have been read, otherwise False.


### Phases

There are 3 phases, by default only the phase1 is enabled.
You can enable phase2 and phase3 by setting the corresponding flag in ```test.py```:
```
PHASES = {
    'phase1': True,
    'phase2': False,
    'phase3': False
}
```
