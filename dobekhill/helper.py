import termcolor

import sys
import time

SKIP = False

def hprint(s, col=None, a=[], delay=0):
    count = 0
    color = col
    bold = False

    if SKIP:
        delay = 0

    for i, c in enumerate(s):
        if c == '\n':
            try:
                if s[i+1] == '\n':
                    time.sleep(delay*10)
            except IndexError:
                pass

            print('\n', end="")
            count = 0
        elif c == ' ':
            if count > 60:
                print('\n', end="")
                count = 0
            else:
                print(' ', end="")
                count = count + 1
        elif c == '*':
            if not color == 'red':
                color = 'red'
            else:
                color = col
        elif c == '^':
            time.sleep(delay*5)
        else:
            text = termcolor.colored(c, color,
                    attrs=a + ['bold'] if bold else [])
            print(text, end="")
            count = count + 1

        if delay != 0:
            time.sleep(delay)
            sys.stdout.flush()

def cont():
    print("[Naciśnij Enter, aby kontynuować]")
    input()

