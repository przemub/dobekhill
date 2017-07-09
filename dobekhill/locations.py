from structs import Noun
from helper import hprint

import time
import random


class Location:
    items = []
    directions = {}
    actions = []

    def event(self):
        return False, False

    def closed(self, state):
        return False

    def entered(self, state):
        pass

    def dyn_items(self):
        return []

    def get_items(self):
        return self.items + self.dyn_items()

    def move(self, state, e):
        entry = self.directions.get(e)
        if entry is None:
            return False

        loc = entry[0]
        delay = entry[1]
        available = entry[2] if len(entry) >= 3 else True
        args = entry[3] if len(entry) >= 4 else None

        if args is None:
            instance = loc()
        else:
            instance = loc(args)

        if not available and instance.closed(state):
            return False

        state.location = instance
        state.add_time(delay)
        return True

    def id(self):
        return type(self).__name__


class Item:
    name = Noun("przedmiot")
    desc = ""
    look = None
    list = True
    alias = []

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
    "UP": "góra",
    "DOWN": "dół",
}


class Front(Location):
    name = "Przed bramą szkoły"

    desc = """Stoisz przed bramą III LO w Gdyni. Rozpiera cię duma, gdy widzisz łopoczące flagi i napis: \
„VIR HONESTUS ET BONUS CIVIS”.
Możesz podejść pod główne wejście do szkoły (północ), wejść przez wejście boczne (północny wschód), pójść do sklepu \
(zachód) lub wrócić do internatu (wschód)."""

    def __init__(self):
        self.directions = {
            dirs["N"]: (PrzedWejściem, 1),
            dirs["NE"]: (Wejście, 1, True, False),
            dirs["W"]: (Sklep, 1),
            dirs["E"]: (Internat, 10)
        }

    class Tabliczka(Item):
        name = Noun("tabliczka")
        desc = "Na płocie wisi tabliczka z napisem „patrz tabliczka”."
        look = """Przyglądasz się baczniej tabliczce. W końcu nie powinna tu ona wisieć. Dostrzegasz taki oto napis…
Dotarłeś na Dobek Hill! Wprawdzie nieco spóźniony, ale przecież wysiłek się liczy… W tej grze czas mija tylko wtedy, \
gdy poruszasz się lub wykonujesz jakieś czynności, także możesz spokojnie przejrzeć opis poszczególnych zasad gry \
dostępny pod komendą *tutorial*, a także opis poszczególnych komend dostępny pod komendą *pomoc*.
Powodzenia! No i pamiętaj, że zamiast pisać np. *patrz tabliczka*, równie dobrze mógłbyś napisać *p t*!"""

    items = [Tabliczka]

    show_time = True


class Sklep(Location):
    name = "Sklep"

    desc = """Znajdujesz się w sklepie spożywczym, którego większość obrotów pochodzi od uczniów III LO, takich jak \
    ty. Możesz tu zakupić różnego rodzaju napoje, drogie pizzerki, i tak dalej. Półki ze słodyczami wypełniają \
    malinki, których ponoć od jakiegoś czasu nie ma kto kupować.
Stąd możesz wyjść pod główną bramę."""

    def __init__(self):
        self.directions = {
            dirs["E"]: (Front, 1),
        }


class Wejście(Location):
    name = "Za wejściem głównym"
    desc = "Znajdujesz się w holu za wejściem do liceum. Na południu znajduje się aula, w której co tydzień rozgrywane \
są wielkie mecze matematyczne. Po schodach możesz wejść do głównego holu. Ze szkoły możesz wyjść wejściem głównym \
(zachód) lub bocznym (południowy wschód). Na tym piętrze znajdują się także szatnia, toalety, stróżówka i punkt ksero."

    def __init__(self, glownym=False):
        self.glownym = glownym

        self.directions = {
            dirs["SE"]: (Front, 1),
            dirs["W"]: (PrzedWejściem, 0),
            dirs["UP"]: (SekretariatHol, 0),
        }

    class PanKsero(Item):
        name = Noun("pan Ksero")
        desc = "Pan Ksero liczy pieniądze w swoim pokoiku."
        look = "Patrzysz na tabelki przetwarzane przez pana Ksero. Od wczoraj dług twojej klasy urósł tylko o \
80 złotych."

    class Straznik(Item):
        name = Noun("Strażnik Teksasu")
        desc = "Strażnik Teksasu przechadza się przed głównym wejściem."

    def event(self):
        if self.glownym and random.randint(1, 3) == random.randint(1, 3):
            hprint("\nStrażnik Teksasu mówi: Na mocy nadanej mi władzy, masz wchodzić bocznym wejściem!\n",
                   'yellow')
            hprint("Zostajesz wyciągnięty za fraki na zewnątrz.\n")
            return True, PrzedWejściem(), 5

        if random.randint(1, 40) == random.randint(1, 40):
            hprint("\nWchodzi uczeń.\n")
            hprint("Strażnik Teksasu mówi: Na mocy nadanej mi władzy, masz wchodzić bocznym wejściem!\n",
                   'yellow')
            hprint("Uczeń zostaje wyciągnięty za fraki na zewnątrz.\n")
            return True, False
        return False, False

    def move(self, state, e):
        if e == dirs["SE"]:
            state.location = Front()
            state.add_time(1)
            return True
        elif e == dirs["W"]:
            state.location = PrzedWejściem()
            return True
        elif e == dirs["UP"]:
            state.location = SekretariatHol()
            return True
        return False

    items = [PanKsero, Straznik]
    directions = [dirs["UP"], dirs["S"], dirs["W"], dirs["SE"]]


class SekretariatHol(Location):
    name = "Hol przy sekretariacie"
    desc = """Nad swoją głową możesz podziwiać listy miast i wsi, z których przyjechali uczniowie, a także krajów, do \
których rozjechali się po ukończeniu szkoły. W gablotach znajdują się informacje o najnowszych osiągnięciach twoich \
kolegów. Może ty też się kiedyś znajdziesz pośród nich…
Na północy znajduje się główny hol, na południu sekretariat, a na górze gniazdo biol-chemu. Możesz też zejść po\
schodach do głównego wejścia."""

    directions = [dirs["N"], dirs["S"], dirs["UP"], dirs["DOWN"]]

    def __init__(self):
        self.directions = {
            dirs["N"]: (HolG1, 1),
            dirs["DOWN"]: (Wejście, 0)
        }


class HolG(Location):
    name = "Hol główny"
    desc = """Znajdujesz się w korytarzu szerokim na 10 metrów, gdzie uczniowie w spokoju siedzą i wymieniają się \
poglądami… Haha, nie. Przez wielkie okna możesz pogardzać ludźmi, którym się chce biegać po boisku.
"""


class HolG1(HolG):
    desc = HolG.desc + """Stąd możesz wejść do sali 8, 9 i po schodach do 10-11."""

    directions = [dirs["N"], dirs["S"], dirs["NE"], dirs["E"], dirs["UP"]]

    def __init__(self):
        self.directions = {
            dirs["N"]: (HolG2, 0),
            dirs["S"]: (SekretariatHol, 0),
            dirs["E"]: [Sala, 0, False, [8, {dirs["W"]: (HolG1, 0)}, None]],
            dirs["NE"]: [Sala, 0, False, [9, {dirs["W"]: (HolG1, 0)}, None]]
        }


class HolG2(HolG):
    desc = HolG.desc + """Stąd możesz wejść do sali 12, 13 i po schodach do 14-15."""

    def __init__(self):
        self.directions = {
            dirs["N"]: (HolWF, 0),
            dirs["S"]: (HolG1, 0),
            dirs["E"]: [Sala, 0, False, [12, {dirs["W"]: (HolG2, 0)}, None]],
            dirs["NE"]: [Sala, 0, False, [13, {dirs["W"]: (HolG2, 0)}, None]]
        }


class HolWF(Location):
    name = "Hol wuefistów"
    desc = """Znajdujesz się na środkowym piętrze w samym środku szkoły, zaraz przy sali gimnastycznej na południu. \
W gablotach widoczne są dyplomy za osiągnięcia sportowe twoich rówieśników. No nic, w konkurencji pt. \
„szybkość pisania na klawiaturze to byś wygrał”…
Po schodach na górę jest gniazdo mat-infu, a na dół jest biblioteka."""

    def __init__(self):
        self.directions = {
            dirs["S"]: (HolG2, 0),
            dirs["UP"]: (GniazdoMI, 0),
        }

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
    desc = """Zawędrowałeś w miejsce, które prawdziwie można zwać gniazdem mat-infu - znajduje się na piętrze i jako \
prawdziwy mat-inf czujesz się tu jak w domu. Gabloty wypełniają zadanka z OI-a i plakaty przedstawiające ludzi, którym \
się powiodło.
Sale informatyczne znajdują się na południu i wschodzie. Sala F2 znajduje się na zachodzie, a czytelnia na północy."""

    def __init__(self):
        self.directions = {
            dirs["DOWN"]: (HolWF, 0),
            dirs["S"]: [Sala, 0, False, [23, {dirs["N"]: (GniazdoMI, 0)}, None]],
            dirs["E"]: [Sala, 0, False, [24, {dirs["W"]: (GniazdoMI, 0)}, None]],
            dirs["W"]: [Sala, 0, False, [101, {dirs["E"]: (GniazdoMI, 0)}, None]]
        }


class Sala(Location):
    name = "Sala nr "
    desc = """Znajdujesz się w sali nr %d. Właśnie trwa lekcja %s z panem profesorem %s. Jak zamierzasz ją spędzić?"""

    def __init__(self, args):
        nr, direction, lesson = args
        self.nr = nr
        self.name += str(nr)
        self.lesson = None
        if lesson:
            self.lesson = lesson
            self._set(lesson)
        self.directions = direction

    def _set(self, lesson):
        print(lesson, lesson.name, lesson.name.dopelniacz, lesson.teacher)
        self.desc = self.desc % (self.nr, lesson.name.dopelniacz,
                                 lesson.teacher.narzednik)

        teacher = Item()
        teacher.name = lesson.teacher
        teacher.desc = lesson.teacher_desc()
        teacher.look = lesson.teacher_look()
        self.ex_items = [teacher]
        self.quote = lesson.quote
        self.actions = lesson.actions()

    def dyn_items(self):
        return self.ex_items

    def closed(self, state):
        if not state.lesson or state.lesson.classroom != self.nr:
            hprint("Drzwi są zamknięte. To oczywiste, w końcu nie masz tu lekcji!\n")
            return True

        hprint("Pukasz lekko i otwierasz drzwi.\n")
        self._set(state.lesson)
        state.lesson.state = state

        return False

    def entered(self, state):
        hprint("Zamykasz drzwi.\n")
        state.lesson.enter(state)

    def move(self, state, e):
        if not self.directions.get(e):
            # hprint("Wyjście z sali jest gdzie indziej.\n")
            return False

        if state.lesson.exit(state):
            return Location.move(self, state, e)
        else:
            return False

    def event(self):
        if random.randint(1, 20) == random.randint(1, 20):
            ret = self.quote()
            return ret, False

        return False, False


class PrzedWejściem(Location):
    name = "Przed wejściem głównym"
    desc = """Znajdujesz się przed wejściem głównym. Wchodząc tędy do szkoły możesz wprawdzie zaoszczędzić trochę \
czasu, ale za to narażasz się na gniew straszliwego Strażnika Teksasu!
Przed sobą widzisz cudowną postmodernistyczną bryłę gmachu III LO. Słyszysz odgłosy uczniów biegających po bieżni na \
północy."""

    def __init__(self):
        self.directions = {
            dirs["S"]: (Front, 1),
            dirs["E"]: (Wejście, 0, False, True)
        }


class Internat(Location):
    name = "Internat"
    desc = """Znajdujesz się w swoim pokoju w internacie, w swoim drugim domu. Przejście przez cały bajzel rozwalony \
po podłodze zajęło ci trochę czasu. W powietrzu unosi się słodki zapach zioła, a tobie nie chce się nawet myśleć o \
tym, że powinieneś teraz zajmować się szkołą…"""

    def __init__(self):
        self.directions = {
            dirs["W"]: (Front, 10),
        }

    class Diler(Item):
        name = Noun("diler")
        desc = "Na korytarzu stoi diler."

    items = [Diler]

    class BobEnd(Exception):
        pass

    def śpij(self):
        hprint("\nZasypiasz. Nieważne, że właśnie trwają lekcje…\n")
        time.sleep(1)

        hprint("\nNON VIR HONESTUS ET BONUS CIVIS\n", 'red', delay=0.15)
        hprint("BAD END\b\b\b\b\b\bOB END\n\n", 'yellow', delay=0.2)

        hprint(
            """Urządziłeś sobie wagary. Przy twojej pięknej średniej jest to niedopuszczalne i zostałeś skazany na " +
            "banicję z Najlepszego Liceum Regionu.\n""",
            delay=0.07)

        raise self.BobEnd("Przegrałeś frajerze.")

    śpij.name = "śpij"

    actions = [śpij]
