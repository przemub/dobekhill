from structs import Noun
from helper import hprint

import time
import random

class Location:
    items = []
    directions = []
    actions = []

    def event(self):
        return (False, False)

    def move(self, state, e):
        pass

class Item:
    name = Noun("przedmiot")
    desc = ""
    look = None
    list = True

    def __repr__(self):
        return self.name.mianownik

# 7  0  1
#  \ | /
# 6- + -2
#  / | \
# 5  4  3
# góra - 8, dół - 9

dirs = {
    "N": "północ",
    "NE": "północny wschód",
    "E": "wschód",
    "SE": "południowy wschód",
    "S": "południe",
    "SW": "południowy zachód",
    "W": "zachód",
    "NW": "północny zachód",
    "N": "północ",
    "UP": "góra",
    "DOWN": "dół",
}

class Front(Location):
    name = "Przed bramą szkoły"

    desc = """Stoisz przed bramą III LO w Gdyni. Rozpiera cię duma, gdy widzisz łopoczące flagi i napis: „VIR HONESTUS ET BONUS CIVIS”.
Możesz podejść pod główne wejście do szkoły (północ), wejść przez wejście boczne (północny wschód), pójść do sklepu (zachód) lub wrócić do internatu (wschód)."""

    directions = [dirs["N"], dirs["NE"], dirs["W"], dirs["E"]]

    class Tabliczka(Item):
        name = Noun("tabliczka")
        desc = "Na płocie wisi tabliczka z napisem „patrz tabliczka”."
        look = """Przyglądasz się baczniej tabliczce. W końcu nie powinna tu ona wisieć. Dostrzegasz taki oto napis…
Dotarłeś na Dobek Hill! Wprawdzie nieco spóźniony, ale przecież wysiłek się liczy… W tej grze czas mija tylko wtedy, gdy poruszasz się lub wykonujesz jakieś czynności, także możesz spokojnie przejrzeć opis poszczególnych zasad gry dostępny pod komendą *tutorial*, a także opis poszczególnych komend dostępny pod komendą *pomoc*.
Powodzenia! No i pamiętaj, że zamiast pisać np. *patrz tabliczka*, równie dobrze mógłbyś napisać *p t*!"""

    items = [Tabliczka]

    show_time = True

    def move(self, state, e):
        if e == dirs["W"]:
            state.location = Sklep()
            state.addTime(1)
            return True
        elif e == dirs["NE"]:
            state.location = Wejście()
            state.addTime(1)
            return True
        elif e == dirs["N"]:
            state.location = PrzedWejściem()
            state.addTime(1)
            return True
        elif e == dirs["E"]:
            state.location = Internat()
            state.addTime(10)
            return True
        return False

class Sklep(Location):
    name = "Sklep"

    desc = """Znajdujesz się w sklepie spożywczym, którego większość obrotów pochodzi od uczniów III LO, takich jak ty. Możesz tu zakupić różnego rodzaju napoje, drogie pizzerki, i tak dalej. Półki ze słodyczami wypełniają malinki, których ponoć od jakiegoś czasu nie ma kto kupować.
Stąd możesz wyjść pod główną bramę."""

    directions = [ dirs["E"] ]

    def move(self, state, e):
        if e == dirs["E"]:
            state.location = Front()
            state.addTime(1)
            return True
        return False

class Wejście(Location):
    name = "Za wejściem głównym"
    desc = "Znajdujesz się w holu za wejściem do liceum. Na południu znajduje się aula, w której co tydzień rozgrywane są wielkie mecze matematyczne. Po schodach możesz wejść do głównego holu. Ze szkoły możesz wyjść wejściem głównym (zachód) lub bocznym (południowy wschód). Na tym piętrze znajdują się także szatnia, toalety, stróżówka i punkt ksero."

    def __init__(self, glownym = False):
        self.glownym = glownym

    class PanKsero(Item):
        name = Noun("pan Ksero")
        desc = "Pan Ksero liczy pieniądze w swoim pokoiku."
        look = "Patrzysz na tabelki przetwarzane przez pana Ksero. Od wczoraj dług twojej klasy urósł tylko o 80 złotych."

    class Straznik(Item):
        name = Noun("Strażnik Teksasu")
        desc = "Strażnik Teksasu przechadza się przed głównym wejściem."

    def event(self):
        if self.glownym and random.randint(1, 3) == random.randint(1, 3):
            hprint("\nStrażnik Teksasu mówi: Na mocy nadanej mi władzy, masz wchodzić bocznym wejściem!\n",
                'yellow')
            hprint("Zostajesz wyciągnięty za fraki na zewnątrz.\n")
            return (True, PrzedWejściem(), 5)

        if random.randint(1, 40) == random.randint(1, 40):
            hprint("\nWchodzi uczeń.\n")
            hprint("Strażnik Teksasu mówi: Na mocy nadanej mi władzy, masz wchodzić bocznym wejściem!\n",
                'yellow')
            hprint("Uczeń zostaje wyciągnięty za fraki na zewnątrz.\n")
            return (True, False)
        return (False, False)

    def move(self, state, e):
        if e == dirs["SE"]:
            state.location = Front()
            state.addTime(1)
            return True
        elif e == dirs["W"]:
            state.location = PrzedWejściem()
            return True
        elif e == dirs["UP"]:
            state.location = SekretariatHol()
            return True
        return False

    items = [PanKsero, Straznik]
    directions = [ dirs["UP"], dirs["S"], dirs["W"], dirs["SE"] ]

class SekretariatHol(Location):
    name = "Hol przy sekretariacie"
    desc = """Nad swoją głową możesz podziwiać listy miast i wsi, z których przyjechali uczniowie, a także krajów, do których rozjechali się po ukończeniu szkoły. W gablotach znajdują się informacje o najnowszych osiągnięciach twoich kolegów. Może ty też się kiedyś znajdziesz pośród nich…
Na północy znajduje się główny hol, na południu sekretariat, a na górze gniazdo biol-chemu. Możesz też zejść po shodach do głównego wejścia."""

    directions = [ dirs["N"], dirs["S"], dirs["UP"], dirs["DOWN"] ]
 
    def move(self, state, e):
        if e == dirs["N"]:
            state.location = HolG1()
            state.addTime(1)
            return True
        elif e == dirs["DOWN"]:
            state.location = Wejście()
            return True
        return False

class HolG(Location):
    name = "Hol główny"
    desc = """Znajdujesz się w korytarzu szerokim na 10 metrów, gdzie uczniowie w spokoju siedzą i wymieniają się poglądami… Haha, nie. Przez wielkie okna możesz pogardzać ludźmi, którym się chce biegać po boisku.
"""

class HolG1(HolG):
    desc = HolG.desc + """Stąd możesz wejść do sali 8, 9 i po schodach do 10-11."""

    directions = [ dirs["N"], dirs["S"], dirs["NE"], dirs["E"], dirs["UP"] ]

    def move(self, state, e):
        if e == dirs["N"]:
            state.location = HolG2()
            return True
        elif e == dirs["S"]:
            state.location = SekretariatHol()
            return True
        return False

class HolG2(HolG):
    desc = HolG.desc + """Stąd możesz wejść do sali 12, 13 i po schodach do 14-15."""

    directions = [ dirs["N"], dirs["S"], dirs["NE"], dirs["E"], dirs["UP"] ]

    def move(self, state, e):
        if e == dirs["N"]:
            state.location = HolWF()
            return True
        elif e == dirs["S"]:
            state.location = HolG1()
            return True
        return False

class HolWF(Location):
    name = "Hol wuefistów"
    desc = """Znajdujesz się na środkowym piętrze w samym środku szkoły, zaraz przy sali gimnastycznej na południu.W gablotach widoczne są dyplomy za osiągnięcia sportowe twoich rówieśników. No nic, w konkurencji pt. „szybkość pisania na klawiaturze to byś wygrał…
Po schodach na górę jest gniazdo mat-infu, a na dół jest biblioteka."""

    directions = [ dirs["W"], dirs["S"], dirs["UP"], dirs["DOWN"] ]

    def move(self, state, e):
        if e == dirs["S"]:
            state.location = HolG2()
            return True
        elif e == dirs["UP"]:
            state.location = GniazdoMI()
            return True
        return False

class GniazdoMI(Location):
    name = "Gniazdo mat-infu"
    desc = """Zawędrowałeś w miejsce, które prawdziwie można zwać gniazdem mat-infu - znajduje się na piętrze i jako prawdziwy mat-inf czujesz się tu jak w domu. Gabloty wypełniają zadanka z OI-a i plakaty przedstawiające ludzi, którym się powiodło.
Sale informatyczne znajdują się na południu i wschodzie. Sala F2 znajduje się na zachodzie, a czytelnia na północy."""

    directions = [ dirs["N"], dirs["S"], dirs["W"], dirs["E"], dirs["DOWN"] ]

    def move(self, state, e):
        if e == dirs["DOWN"]:
            state.location = HolWF()
            return True
        return False

class PrzedWejściem(Location):
    name = "Przed wejściem głównym"
    desc = """Znajdujesz się przed wejściem głównym. Wchodząc tędy do szkoły możesz wprawdzie zaoszczędzić trochę czasu, ale za to narażasz się na gniew straszliwego Strażnika Teksasu!
Przed sobą widzisz cudowną postmodernistyczną bryłę gmachu III LO. Słyszysz odgłosy uczniów biegających po bieżni na północy."""

    directions = [ dirs["N"], dirs["E"], dirs["S"] ]
 
    def move(self, state, e):
        if e == dirs["S"]:
            state.location = Front()
            state.addTime(1)
            return True
        elif e == dirs["E"]:
            state.location = Wejście(True)
            return True
        return False

class Internat(Location):
    name = "Internat"
    desc = """Znajdujesz się w swoim pokoju w internacie, w swoim drugim domu. Przejście przez cały bajzel rozwalony po podłodze zajęło ci trochę czasu. W powietrzu unosi się słodki zapach zioła, a tobie nie chce się nawet myśleć o tym, że powinieneś teraz zajmować się szkołą…"""

    directions = [ dirs["W"] ]

    def move(self, state, e):
        if e == dirs["W"]:
            state.location = Front()
            state.addTime(10)
            return True
        return False

    class Diler(Item):
        name = Noun("diler")
        desc = "Na korytarzu stoi diler."

    items = [ Diler ]

    class BobEnd(Exception):
        pass

    def śpij(self):
        hprint("\nZasypiasz. Nieważne, że właśnie trwają lekcje…\n")
        time.sleep(1)
        
        hprint("\nNON VIR HONESTUS ET BONUS CIVIS\n", 'red', delay=0.15)
        hprint("BAD END\b\b\b\b\b\bOB END\n\n", 'yellow', delay=0.2)

        hprint("""Urządziłeś sobie wagary. Przy twojej pięknej średniej jest to niedopuszczalne i zostałeś skazany na banicję z Najlepszego Liceum Regionu.\n""", delay=0.07)

        raise self.BobEnd("Przegrałeś frajerze.")

    śpij.name = "śpij"

    actions = [ śpij ]

