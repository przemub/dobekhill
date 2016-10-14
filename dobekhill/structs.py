class Player:
    imie = None
    nazwisko = None

    ulub = None 
    uslab = None
    mocny = None
    slaby = None

class State:
    level = 1

    location = None
    tutorial = True

    hr = 7
    min = 47

    def addTime(self, t):
        self.min += t
        self.hr += self.min // 60
        self.min %= 60

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

    def __init__(self, m, d=None, b=None, c=None,
                    n=None, msc=None, wol=None):
        self.mianownik = m
        self.dopelniacz = d if d else m
        self.biernik = b if b else m
        self.celownik = c if c else m
        self.narzednik = n if n else m
        self.miejscownik = msc if msc else m
        self.wolacz = wol if wol else m

    def __repr__(self):
        return self.mianownik

