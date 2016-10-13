from helper import *
from structs import *
from locations import *

import cmd
import time

class HillShell():
    gracz = Player()

    commands = []
    s = None

    def do_wyjdź(self, arg):
        self.close()
        bye()
        return True

    def start(self, state=State()):
        commands = [func for func in dir(self)
                if callable(getattr(self, func)) and func[:3] == "do_"]
        self.s = state

        if self.s.level == 1 and self.s.tutorial == 1:
            hprint('1 PAŹDZIERNIKA 2016\n\n', 'yellow', delay=0.15)
            hprint('Lament pierwszy: ', 'red', delay=0.15)
            time.sleep(1)
            hprint('WEJŚCIÓWKA', 'yellow', delay=0.1)
            time.sleep(1)

            hprint('\n\n')

            hprint("""Jesteś już w pełni uczniem Gdyńskiej Trójki i możesz się tym chwalić.^ Dostałeś miejsce w internacie Zespołu Szkół Budowlanych (to jasne, w końcu nie będziesz dojeżdżał aż z Nowego Dworu).

Ciężko jednak powiedzieć, żebyś radził sobie całkiem dobrze…^ Koledzy z Gimnazjum nr 24 bez przerwy rozprawiają o heurach, wbijaniu olimpiadek, brutach i złożonościach, a ty zupełnie nie wiesz o co chodzi!

Co gorsza, w twoim powiatowym gimnazjum nie omawiano trygonometrii, co spowodowało marną sytuację jeśli chodzi o twoje oceny z matematyki.^ Dzięki dodatkowi do dziennika pewnego starszego mat-infa, twoja nieco nadgorliwa matka jak na dłoni widzi, że nie zdajesz i zagroziła ci, że jeśli w ciągu miesiąca się nie poprawisz, wracasz do Nowego Dworu.^ A tobie bardzo spodobało się życie w mieście.

Czy masz w sobie to coś i uda ci się zostać w Najlepszym Liceum Regionu?^ Czy udowodnisz, że wieśniak nie znaczy gorszy?^ Czy zdobędziesz przyjaciół i zostaniesz królem wbijania olimpiadek?^ Czy dasz się poznać jako dobry człowiek i zacny obywatel?

*Witaj na Wzgórzu Dobesława.*^

Wszelkie podobieństwo do osób rzeczywistych jest przypadkowe.\n\n""", delay=0.07, a=['underline'])

            cont()

            self.s.location = Front()
            self.desc()
            self.loop()

    def desc(self):
        hprint(self.s.location.name+"\n", 'blue')
        hprint("[Wyjścia: %s]\n" % ", ".join(self.s.location.directions), 'green')
        hprint(self.s.location.desc + "\n")

        for item in self.s.location.items:
            hprint("\t" + item.desc + "\n", 'green')

        hprint("W sali nr 9 trwa lekcja matematyki.\n", 'magenta')

        print()

    def loop(self):
        prompt = "(%d:%d %d%%hp %d%%dp) " % (self.s.hr, self.s.min, self.s.hp, self.s.dp)
        hprint(prompt, 'cyan')

        comm = input()

        self.loop()


if __name__ == "__main__":
    hill = HillShell()
    hill.start()

