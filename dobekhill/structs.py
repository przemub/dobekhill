class Player:
    imie = None
    nazwisko = None

    ulub = None 
    uslab = None
    mocny = None
    slaby = None

class State:
    level = None

    location = None
    tutorial = True

    time = 7*60+47
    week = 1
    weekday = 0

    lesson = None

    def addTime(self, t):
        self.time += t

    hp = 55
    dp = 34

class Noun:
    mianownik = None
    dopelniacz = None
    biernik = None
    celownik = None
    narzednik = None
    miejscownik = None
    wolacz = None

    alias = None

    def __init__(self, m, d=None, b=None, c=None,
                    n=None, msc=None, wol=None,
                    alias=[]):
        self.mianownik = m
        self.dopelniacz = d if d else m
        self.biernik = b if b else m
        self.celownik = c if c else m
        self.narzednik = n if n else m
        self.miejscownik = msc if msc else m
        self.wolacz = wol if wol else m

        self.alias = m.split() + alias

    def __repr__(self):
        return self.mianownik

