# A simple chess visualization trainer

The trainer helps to practice blind fold chess visualization, by asking for
the colour of random squares, and knight and bishop tours between random
squares.

## Requirements
- Python3

## How to use

Run `python3 cli.py` from a console. Answer the questions by typing your
answer and hitting return. You can quit any time, by answering `q` or skip
a question by answering `s`.

## Example

```
$ python3 cli.py 
Visualization trainer.
You can type the following letters at any time:
              - q to exit,
              - s to skip an answer,
              - or h to see this message.
Is c3 a light square? [y/n]
n
Correct!
List all knight jumps from c3 (e.g. c2, b3).
b1 d1 a2 e2 a4 e4 b5 d5
Correct!
Give a knight tour from c3 to c6.
b5 d4 c6
Correct!
List all transfer squares for a bishop from c3 to a1 (leave empty if on same diagonal).

Correct!
Is c4 a light square? [y/n]
y
Correct!
List all knight jumps from c4 (e.g. c2, b3).
s
The answer is:  a3, a5, b2, b6, d2, d6, e3, e5
Give a knight tour from c4 to g1.
s
List all transfer squares for a bishop from c4 to h1 (leave empty if on same diagonal).
e7
 - incorrect: e7
 - missing: d5
Is a1 a light square? [y/n]
q
Good bye.
```
