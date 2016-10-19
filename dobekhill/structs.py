class Player:
    def __init__(self, default=False):
        # Cechy
        self.imie = Noun("Karol") if default else None
        self.nazwisko = Noun("Baryła") if default else None

        self.ulub = "i" if default else None
        self.uslab = "m" if default else None
        self.mocny = "p" if default else None
        self.slaby = "p" if default else None

        # Statystyki
        self.spoznienia = 0


class State:
    def __init__(self):
        self.level = None

        self.location = None
        self.tutorial = True

        self.time = 7*60+47
        self.week = 1
        self.weekday = 0

        self.player = Player(True)
        self.lesson = None

        self.hp = 55
        self.dp = 34

    def addTime(self, t):
        self.time += t


class Noun:
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

