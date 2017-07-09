#!/usr/bin/env python3

import time
import random
import threading
import sys
import pickle
import os
import redis

import locations
from helper import cont, hprint
from lessons import ttm, Lament1
from locations import dirs
from structs import State, Player
from server.client import Client


# noinspection PyUnusedLocal
class HillShell:
    gracz = Player(True)

    commands = []
    s = None
    c = None

    def do_patrz(self, arg):
        if len(arg) == 0:
            self.desc()
            return

        for item in self.s.location.get_items():
            names = [alias for alias in item.alias] + item.name.mianownik.split()
            for name in names:
                if name.lower().startswith(arg[0].lower()):
                    if item.look:
                        hprint(item.look + "\n")
                    else:
                        hprint(item.desc + "\n")
                    return
        hprint("Nie ma takiego przedmiotu.\n")

    do_patrz.help = """Składnia: patrz
Składnia: patrz <przedmiot>
Wyświetla opis pomieszczenia lub podanego przedmiotu.
"""

    # Kierunki
    def move(self, direction):
        if self.s.location.move(self.s, direction):
            if self.multi:
                self.c.update(self.s)
            self.desc()
            self.s.location.entered(self.s)
        else:
            hprint("Nie ma wyjścia w tym kierunku.\n")

    def do_n(self, arg):
        self.move(dirs["N"])

    def do_s(self, arg):
        self.move(dirs["S"])

    def do_w(self, arg):
        self.move(dirs["W"])

    def do_e(self, arg):
        self.move(dirs["E"])

    def do_nw(self, arg):
        self.move(dirs["NW"])

    def do_ne(self, arg):
        self.move(dirs["NE"])

    def do_sw(self, arg):
        self.move(dirs["SW"])

    def do_se(self, arg):
        self.move(dirs["SE"])

    def do_góra(self, arg):
        self.move(dirs["UP"])

    def do_dół(self, arg):
        self.move(dirs["DOWN"])

    # Komunikacja

    def do_mów(self, arg):
        wiad = " ".join(arg)
        self.c.thread.submit(self.s.location.id(), "%s %s mówi: „%s”.\n" % (self.gracz.imie, self.gracz.nazwisko, wiad),
                             'yellow')
        hprint("Mówisz: „%s”.\n" % (wiad,), 'yellow')

    def do_krzycz(self, arg):
        wiad = " ".join(arg)
        self.c.thread.submit("all", "%s %s krzyczy: „%s”!\n" % (self.gracz.imie, self.gracz.nazwisko, wiad), 'yellow')
        hprint("Krzyczysz: „%s”!\n" % (wiad,), 'yellow')

    def do_beknij(self, arg):
        jak = arg[0] if len(arg) > 0 else "transcendentalnie"

        self.c.thread.submit("all", "%s %s beka %s.\n" % (self.gracz.imie, self.gracz.nazwisko, jak), 'yellow')
        hprint("Bekasz %s.\n" % (jak,))

    def do_legitymacja(self, arg):
        karta = """
%s, lat %d
  ----------------------------
 /         LEGITYMACJA SZKOLNA \\
|  HP:   %3d%%   DP:     %3d%%   |
|                              |
|  INTE: %2d    spóźn.: %2d      |
|  SIŁA: %2d    np.:    %2d      |
|  SPRA: %2d    wagary: %2d      |
 \ SZCZ: %2d                   /
  ----------------------------
""" % (self.gracz.imie.mianownik + " " + self.gracz.nazwisko.mianownik, self.gracz.wiek,
       self.s.hp, self.s.dp, self.gracz.inte, self.gracz.spoznienia, self.gracz.sila, self.gracz.np,
       self.gracz.spra, self.gracz.wagary, self.gracz.szcz)

        hprint("Oglądasz swoją legitymację, dowód, że należysz do społeczności Gdyńskiej Trójki.\n")
        hprint(karta)

    def do_tutorial(self, arg):
        if len(arg) == 0:
            hprint("""Witaj w tutorialu! Aby przeczytać rozdział tutoriala, wpisz tą komendę z nazwą rozdziału.
Rozdziały:
- poruszanie się
- statystyki
- lekcje
""")
            return

        rozdzialy = [
            ["poruszanie się", """*Poruszanie się*
Po świecie Dobek Hill można się przemieszczać aż na dziesięć stron świata! Używasz w tym celu angielskich skrótów\
nazw kierunków (n, s, w, e, nw, ne, sw, se) i poleceń góra i dół.
Opis pomieszczenia, w którym aktualnie się znajdujesz, można wyświetlić komendą *patrz*.
Zauważ, że czasem będziesz musiał spełnić pewne warunki, by móc znaleźć się w pomieszczeniu. Nie do pomyślenia jest, \
by w elitarnym liceum wbijać innym na lekcje!
"""],
            ["statystyki", """*Statystyki*
Jeszcze niezaimplementowane…
"""],
            ["lekcje", """*Lekcje*
Jeszcze niezaimplementowane…
"""]]

        for rozdzial in rozdzialy:
            if rozdzial[0].startswith(arg[0]):
                hprint(rozdzial[1])
                return
        hprint("Nie ma takiego rozdziału.")

    def do_pomoc(self, arg):
        if len(arg) == 0:
            hprint("Spis dostępnych komend: \n")
            comm = " ".join([func[3:] for func in self.commands])
            hprint(comm)
            print()
            return

        fun = None
        length = 999
        for func in self.commands:
            if func[3:].startswith(arg[0]) and length > len(func):
                fun = func
                length = len(func)

        if fun:
            hprint(getattr(getattr(self, fun), 'help', "Brak pomocy dla tej komendy.\n"))
        else:
            hprint("Nie ma takiej komendy.\n")

    do_pomoc.help = """Składnia: pomoc <polecenie>
Składnia: pomoc
Wyświetla pomoc powiązaną z podanym poleceniem lub listę poleceń.
"""

    def do_debug(self, arg):
        if len(arg) == 1:
            self.s.time = int(arg[0])
        elif len(arg) == 2:
            self.s.time = ttm(int(arg[0]), int(arg[1]))

    def do_zapisz(self, arg):
        dir = os.path.expanduser("~/.dobekhill")
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(dir + '/gracz', 'wb') as out:
            pickle.dump(self.gracz, out, -1)
        with open(dir + '/stan', 'wb') as out:
            pickle.dump(self.s, out, -1)

        hprint("Dodano Twe losy do scenariusza filmu „F jak wtorek”.\n")

    def do_wyjdź(self, arg):
        self.do_zapisz("")
        hprint("Do zobaczenia w świecie Dobek Hill!\n")
        self.event.tak_zabij_sie()

        if self.multi:
            self.c.logout(self.gracz)

        raise self.ExitException()

    do_wyjdź.help = """Składnia: wyjdź
Wychodzi ze świata Dobek Hill.
"""

    class EventThread(threading.Thread):
        def __init__(self, state, game):
            threading.Thread.__init__(self)

            self.state = state
            self.game = game
            self.zabijSie = False

        def run(self):
            while not self.zabijSie:
                if self.state.location:
                    ret = self.state.location.event()
                    if not ret[0]:
                        time.sleep(0.5)
                        continue
                    if ret[1]:
                        self.state.location = ret[1]
                        self.state.add_time(ret[2])
                        self.game.desc()

                    self.game.prompt()
                    sys.stdout.flush()
                    time.sleep(1)

                time.sleep(0.5)

        def tak_zabij_sie(self):
            self.zabijSie = True

    def do_kto(self, args):
        if not self.multi:
            return

        gracze = self.c.players()

        hprint("W Gdyńskiej Trójce obecnie przesiadują:\n")
        for gracz in gracze:
            hprint("%s %s\n" % (gracz.imie, gracz.nazwisko))


    def start(self, state=State()):
        self.commands = [func for func in dir(self)
                         if callable(getattr(self, func)) and func[:3] == "do_"]
        self.s = state

        self.s.player = self.gracz

        random.seed()

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        try:
            r.ping()
            self.multi = True
            self.c = Client(r, self)
            self.c.login(self.s)
        except redis.exceptions.ConnectionError as re:
            hprint("Brak połączenia z serwerem. Uruchamiam tryb jednoosobowy.")
            self.multi = False

        # noinspection PyAttributeOutsideInit
        self.event = self.EventThread(self.s, self)
        self.event.start()

        if self.s.tutorial == 1:
            hprint('1 PAŹDZIERNIKA 2016\n\n', 'yellow', delay=0.15)
            hprint('Lament pierwszy: ', 'red', delay=0.15)
            time.sleep(1)
            hprint('WEJŚCIÓWKA', 'yellow', delay=0.1)
            time.sleep(1)

            hprint('\n\n')

            hprint("""Jesteś już w pełni uczniem Gdyńskiej Trójki i możesz się tym chwalić.^ Dostałeś miejsce \
w internacie Zespołu Szkół Budowlanych^. To jasne, w końcu nie będziesz dojeżdżał aż z Nowego Dworu.

Ciężko jednak powiedzieć, żebyś radził sobie całkiem dobrze…^ Koledzy z Gimnazjum nr 24 bez przerwy rozprawiają o \
heurach, wbijaniu olimpiadek, brutach i złożonościach, a ty zupełnie nie wiesz o co chodzi!

Co gorsza, w twoim powiatowym gimnazjum nie omawiano trygonometrii, co spowodowało marną sytuację jeśli chodzi o twoje \
oceny z matematyki.^ Dzięki dodatkowi do dziennika pewnego starszego mat-infa, twoja nieco nadgorliwa matka jak na \
dłoni widzi, że nie zdajesz i zagroziła ci, że jeśli w ciągu miesiąca się nie poprawisz, wracasz do Nowego Dworu.^ \
A tobie bardzo spodobało się życie w mieście.

Czy masz w sobie to coś i uda ci się zostać w Najlepszym Liceum Regionu?^ Czy udowodnisz, że wieśniak nie znaczy \
gorszy?^ Czy zdobędziesz przyjaciół i zostaniesz królem wbijania olimpiadek?^ Czy dasz się poznać jako dobry człowiek \
i zacny obywatel?

*Witaj na Wzgórzu Dobesława.*^

Wszelkie podobieństwo do osób rzeczywistych jest przypadkowe.\n\n""", delay=0.07, a=[])

            cont()

            self.s.location = locations.Front()
            self.s.level = Lament1()
            self.s.tutorial = 0

        hprint("\n")
        self.desc()
        self.loop()
        self.c.update(self.s)

    def desc(self):
        hprint(self.s.location.name + "\n", 'blue')

        directions = ""
        for direction, location in self.s.location.directions.items():
            if len(location) >= 3 and not location[2]:
                directions += "(%s), " % direction
            else:
                directions += "%s, " % direction

        hprint("[Wyjścia: %s]\n" % directions[:-2], 'green')

        if len(self.s.location.actions) > 0:
            hprint("[Akcje: %s]\n" % ", ".join([a.name for a in self.s.location.actions]), 'yellow')
        hprint(self.s.location.desc + "\n")

        for item in self.s.location.get_items():
            if item.list:
                hprint("\t" + item.desc + "\n", 'green')
        for s in self.c.players_in(self.s.location):
            if s.player.id != self.gracz.id:
                hprint("\tStoi tu %s %s.\n" % (s.player.imie, s.player.nazwisko), 'red')

        hprint(self.s.level.status(self.s) + "\n", 'magenta')

    class ExitException(Exception):
        pass

    def prompt(self):
        prompt = "(%02d:%02d %d%%hp %d%%dp) " % (self.s.time // 60, self.s.time % 60, self.s.hp, self.s.dp)
        hprint(prompt, 'cyan')

    def loop(self):
        while True:
            self.prompt()

            comm = input()
            comm = comm.split()
            if len(comm) == 0:
                continue

            fun = None
            length = 999
            for func in self.commands:
                if func[3:].startswith(comm[0]) and length > len(func):
                    fun = getattr(self, func)
                    length = len(func)

            for func in self.s.location.actions:
                if func.name.startswith(comm[0]) and length > len(func.name):
                    fun = func
                    length = len(func.name)

            if fun:
                try:
                    fun(comm[1:])
                except self.ExitException:
                    break
            else:
                hprint("Nie ma takiego polecenia.\n")


if __name__ == "__main__":
    from main import load

    SKIP = True
    load()
