from structs import Noun
from helper import hprint, k100

import bisect
import random
import time


class Lesson:
    def __init__(self, *args, **kwargs):
        self.teacher = None
        self.classroom = args[0]
        self.length = args[1]
        self.start = args[2]
        self.state = None
        self.random = random.randint(0, 4)
        # Prawdopodobieństwo wpisania spóźnienia
        self.late = 50

    def teacher_desc(self):
        return "Przy biurku stoi pan profesor %s." % self.teacher.mianownik

    def teacher_look(self):
        return self.teacher_desc()

    def enter(self, state):
        if state.time < self.start + self.random:
            if state.time >= self.start:
                hprint("^Spóźniłeś się odrobinę, ale lekcja jeszcze się nie zaczęła.^ ")
            hprint("Siadasz w ławce i czekasz na rozpoczęcie lekcji.^\n")
            state.time = self.start + self.random
        else:
            hprint("Ogłaszasz swoje przybycie: Dzień dobry i przepraszam za spóźnienie.^\n", 'yellow')
            hprint("Spóźniłeś się.^ ")
            if k100(self.late):
                hprint("Dostajesz spóźnienie do dziennika.^\n")
                state.player.spoznienia += 1
            else:
                hprint("Upiekło ci się.^^\n")

    def exit(self, state):
        lek, brk = mtl(state.time)
        if not brk:
            return True

        hprint("%s mówi: A ty gdzie się wybierasz, %s?^\n" % (self.teacher.mianownik,
                                                              state.player.imie.mianownik), 'yellow')
        hprint("Wracasz się do ławki.\n")
        return False

    def quote(self):
        return False

    def koniec(self):
        hprint("Zadzwonił dzwonek na koniec lekcji.")
        self.state.time = self.start + 45

    def śpij(self):
        hprint("Nie masz siły, żeby żyć, a co dopiero, by uważać na lekcji. Zawieszasz wzrok na %s i zasypiasz…" %
               self.teacher.miejscownik)
        time.sleep(2)

        if k100(30):
            hprint("Nauczyciel zauważył twoją nieprzytomność. Dostaniesz ocenę niedostateczną.")
            self.state.mod_dp(-random.randint(1, 5))
        hprint("Co nieco odespałeś.")
        self.state.mod_hp(random.randint(5, 10))

        self.koniec()

    śpij.name = "śpij"

    def actions(self):
        return [self.śpij]


class Matematyka(Lesson):
    name = Noun("matematyka", "matematyki", n="matematyką")
    teacher = Noun("Szymon Dobecki", "Szymona Dobeckiego", n="Szymonem Dobeckim")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)

    def teacher_look(self):
        return """Widzisz łysygo człowieka o bujnej fryzurze. Blask jego majestatu oświetla twoje wewnętrze \
matematyczne oko, wykluczając je z dziedziny.
Za uchem schowany ma krzywik, a z kieszeni wystaje okładka na której widnieje nieco starty napis *PAWŁOWSKI*."""

    def quote(self):
        base = ["bo tu jest taka ukryta kolumna",
                "ty nie masz tu prawa głosu, ty weź dupę w troki i do roboty",
                "ja to bym te wszystkie ferie zlikwidował",
                "te uprawnienia laureata ci zostaja na nastepny rok jak nie zdasz?",
                "ja cię nie przepuszczę do następnej klasy",
                "i tu stosujemy taki myk",
                "w tej klasie to ze 30% osób cokolwiek robi",
                "jakbyśmy byli u mnie w szkole to bym cię wypieprzył z klasy",
                "na ostatniej wejściówce nikt nie zapunktował",
                "wyciągnijcie kartki, napiszemy sobie pracę własną",
                "to na jutrzejszą lekcję obejrzyjcie sobie 2 wykłady, nie są długie, pół godziny każdy"
                ]

        hprint("\nSzymon Dobecki mówi: (…) %s.\n" % random.choice(base), 'yellow')

        return True


class WF(Lesson):
    name = Noun("WF", "WF-u", n="WF-em")
    teacher = Noun("Grzegorz Henicz", "Grzegorza Henicza", n="Grzegorzem Heniczem")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)

    def teacher_look(self):
        return """Z całych sił próbujesz dostrzec charakterystyczne cechy najlepszego wuefisty, lecz jego prędkość \
względem twojej jest zbyt wysoka.
(Interakcja z postacią jest niemożliwa.)"""


class Historia(Lesson):
    name = Noun("historia", "historii", n="historią")
    teacher = Noun("Dariusz Piasek", "Dariusza Piaska", n="Dariuszem Piaskiem")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)


class Informatyka(Lesson):
    name = Noun("informatyka", "informatyki", n="informatyką")
    teacher = Noun("Ryszard „Prezes” Szubartowski", b="Ryszardem „Prezesem” Szubartowskim",
                   d="Ryszarda „Prezesa” Szubartowskiego")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)


class TimeTable:
    pass


"""timetominutes"""


def ttm(hr, min):
    return hr * 60 + min


"""timetominutes"""


def mtt(min):
    return "%02d:%02d" % (min // 60, min % 60)


table = [ttm(7, 45), ttm(8, 40), ttm(9, 35), ttm(10, 30), ttm(11, 25), ttm(12, 30), ttm(13, 25),
         ttm(14, 25), ttm(15, 15)]

"""minutestolesson
(nrLekcji, Lekcja/Przerwa)"""


def mtl(time):
    i = bisect.bisect_left(table, time + 1)
    if i == 0:
        return 0, False
    return i, time - 1 - table[i - 1] < 44


def curless(timetable, hr, start):
    i = start - 1
    for lesson in timetable:
        i += lesson.length
        if i >= hr:
            return lesson


class Lament1(TimeTable):
    table = [
        [Matematyka(9, 3, 1), WF(100, 1, 4),
         Historia(9, 1, 5), Informatyka(23, 2, 6)],
        [],
        [],
        [],
        []
    ]
    length = [(1, 7), (0, 0) * 6]

    def status(self, state):
        lek, brk = mtl(state.time)
        day = state.weekday

        if self.length[day][1] == 0:
            state.lesson = None
            return "Dziś masz wolne od szkoły!"
        elif lek < self.length[day][0]:
            state.lesson = self.table[day][0]
            return "Dziś zaczynasz %s o godzinie %s w sali nr %d." % (self.table[day][0].name.narzednik,
                                                                      mtt(table[self.length[day - 1][0]]),
                                                                      self.table[day][0].classroom)
        elif (lek >= self.length[day][1] and brk) or (lek > self.length[day][1]):
            state.lesson = None
            return "Skończyłeś już lekcje na dzisiaj."
        elif brk:
            cur = curless(self.table[day], lek, self.length[day][0])
            state.lesson = cur
            return "W sali nr %d trwa lekcja %s." % \
                   (cur.classroom, cur.name.dopelniacz)
        elif not brk:
            cur = curless(self.table[day], lek + 1, self.length[day][0])
            state.lesson = cur
            return "Następna lekcja to %s w sali %d." % \
                   (cur.name.mianownik, cur.classroom)

        return ""
