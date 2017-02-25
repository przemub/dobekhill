import random
import sys
import time

import termcolor

SKIP = True


def hprint(s, col=None, a=(), delay=0):
    count = 0
    color = col
    bold = False

    delaylong = delay * 5 if delay > 0 or SKIP else 0.5

    if SKIP:
        delay = 0

    for i, c in enumerate(s):
        if c == '\n':
            try:
                if s[i + 1] == '\n':
                    time.sleep(delay * 10)
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
                count += 1
        elif c == '*':
            if not color == 'red':
                color = 'red'
            else:
                color = col
        elif c == '^':
            sys.stdout.flush()
            time.sleep(delaylong)
        else:
            text = termcolor.colored(c, color,
                                     attrs=a + ('bold',) if bold else a)
            print(text, end="")
            count += 1

        if delay != 0:
            sys.stdout.flush()
            time.sleep(delay)


def cont():
    print("[Naciśnij Enter, aby kontynuować]")
    input()


def k100(prob):
    return random.randint(0, 99) < prob
