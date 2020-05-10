import uuid

class Player:
    def __init__(self, default=False):
        # Dane gry
        self.id = uuid.uuid4().int

        # Cechy
        self.imie = Noun("Karol") if default else None
        self.nazwisko = Noun("Baryła") if default else None
        self.wiek = 17

        self.ulub = "i" if default else None
        self.uslab = "m" if default else None
        self.mocny = "p" if default else None
        self.slaby = "p" if default else None

        # Statystyki
        self.inte = 0
        self.sila = 0
        self.spra = 0
        self.szcz = 0

        self.spoznienia = 0
        self.np = 0
        self.wagary = 0


class State:
    def __init__(self):
        self.level = None

        self.location = None
        self.tutorial = True

        self.time = 7 * 60 + 47
        self.week = 1
        self.weekday = 0

        self.player = Player(True)
        self.lesson = None

        self.hp = 55
        self.dp = 34

    def add_time(self, t):
        self.time += t

    def mod_hp(self, m):
        self.hp += m
        if self.hp > 100:
            self.hp = 100
        elif self.hp < 0:
            self.hp = 0

    def mod_dp(self, m):
        self.dp += m
        if self.dp > 100:
            self.dp = 100
        elif self.dp < 0:
            self.dp = 0


class Noun:
    def __init__(self, m, d=None, b=None, c=None,
                 n=None, msc=None, wol=None,
                 alias=None):
        self.mianownik = m
        self.dopelniacz = d if d else m
        self.biernik = b if b else m
        self.celownik = c if c else m
        self.narzednik = n if n else m
        self.miejscownik = msc if msc else m
        self.wolacz = wol if wol else m

        self.alias = m.split()
        if alias:
            self.alias += alias

    def __repr__(self):
        return self.mianownik
