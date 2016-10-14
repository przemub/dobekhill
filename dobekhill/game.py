#!/usr/bin/env python3
from helper import *
from structs import *
from locations import *

import cmd
import time
import random
import threading
import sys

class HillShell():
    gracz = Player()

    commands = []
    s = None

    def do_patrz(self, arg):
        if len(arg) == 0:
            self.desc()
            return

        for item in self.s.location.items:
            if item.name.mianownik.lower().startswith(arg[0].lower()):
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

    def move(self, dir):
        if self.s.location.move(self.s, dir):
            self.desc()
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
        [ "poruszanie się", """*Poruszanie się*
Po świecie Dobek Hill można się przemieszczać aż na dziesięć stron świata! Używasz w tym celu angielskich skrótów nazw kierunków (n, s, w, e, nw, ne, sw, se) i poleceń góra i dół.
Opis pomieszczenia, w którym aktualnie się znajdujesz, można wyświetlić komendą *patrz*.
Zauważ, że czasem będziesz musiał spełnić pewne warunki, by móc znaleźć się w pomieszczeniu. Nie do pomyślenia jest, by w elitarnym liceum wbijać innym na lekcje!
""" ],
        [ "statystyki", """*Statystyki*
Jeszcze niezaimplementowane…
""" ],
        [ "lekcje", """*Lekcje*
Jeszcze niezaimplementowane…
""" ]]

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

    def do_wyjdź(self, arg):
        hprint("Do zobaczenia w świecie Dobek Hill!\n")
        self.event.takZabijSie()
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
                        self.state.addTime(ret[2])
                        self.game.desc()
                    prompt = "(%02d:%02d %d%%hp %d%%dp) " % (self.state.hr,
                            self.state.min, self.state.hp, self.state.dp)

                    hprint(prompt, 'cyan')
                    sys.stdout.flush()
                    time.sleep(1)

                time.sleep(0.5)

        def takZabijSie(self):
            self.zabijSie = True

    def start(self, state=State()):
        self.commands = [func for func in dir(self)
                if callable(getattr(self, func)) and func[:3] == "do_"]
        self.s = state

        random.seed()

        self.event = self.EventThread(self.s, self)
        self.event.start()

        if self.s.level == 1 and self.s.tutorial == 1:
            hprint('1 PAŹDZIERNIKA 2016\n\n', 'yellow', delay=0.15)
            hprint('Lament pierwszy: ', 'red', delay=0.15)
            time.sleep(1)
            hprint('WEJŚCIÓWKA', 'yellow', delay=0.1)
            time.sleep(1)

            hprint('\n\n')

            hprint("""Jesteś już w pełni uczniem Gdyńskiej Trójki i możesz się tym chwalić.^ Dostałeś miejsce w internacie Zespołu Szkół Budowlanych^. To jasne, w końcu nie będziesz dojeżdżał aż z Nowego Dworu.

Ciężko jednak powiedzieć, żebyś radził sobie całkiem dobrze…^ Koledzy z Gimnazjum nr 24 bez przerwy rozprawiają o heurach, wbijaniu olimpiadek, brutach i złożonościach, a ty zupełnie nie wiesz o co chodzi!

Co gorsza, w twoim powiatowym gimnazjum nie omawiano trygonometrii, co spowodowało marną sytuację jeśli chodzi o twoje oceny z matematyki.^ Dzięki dodatkowi do dziennika pewnego starszego mat-infa, twoja nieco nadgorliwa matka jak na dłoni widzi, że nie zdajesz i zagroziła ci, że jeśli w ciągu miesiąca się nie poprawisz, wracasz do Nowego Dworu.^ A tobie bardzo spodobało się życie w mieście.

Czy masz w sobie to coś i uda ci się zostać w Najlepszym Liceum Regionu?^ Czy udowodnisz, że wieśniak nie znaczy gorszy?^ Czy zdobędziesz przyjaciół i zostaniesz królem wbijania olimpiadek?^ Czy dasz się poznać jako dobry człowiek i zacny obywatel?

*Witaj na Wzgórzu Dobesława.*^

Wszelkie podobieństwo do osób rzeczywistych jest przypadkowe.\n\n""", delay=0.07, a=[])

            cont()

            self.s.location = Front()
            self.desc()
            self.loop()

    def desc(self):
        hprint(self.s.location.name+"\n", 'blue')
        hprint("[Wyjścia: %s]\n" % ", ".join(self.s.location.directions), 'green')
        if len(self.s.location.actions) > 0:
            hprint("[Akcje: %s]\n" % ", ".join([a.name for a in self.s.location.actions]), 'yellow')
        hprint(self.s.location.desc + "\n")

        for item in self.s.location.items:
            if item.list:
                hprint("\t" + item.desc + "\n", 'green')

        hprint("W sali nr 9 trwa lekcja matematyki.\n", 'magenta')

        print()

    class ExitException(Exception):
        pass

    def loop(self):
        cont = True
        while cont:
            prompt = "(%02d:%02d %d%%hp %d%%dp) " % (self.s.hr, self.s.min, self.s.hp, self.s.dp)
            hprint(prompt, 'cyan')

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
                    cont = False
            else:
                hprint("Nie ma takiego polecenia.\n")

if __name__ == "__main__":
    SKIP = True
    hill = HillShell()
    hill.start()

