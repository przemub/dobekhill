from structs import Noun

import bisect

class Lesson:
    def __init__(self, *args, **kwargs):
        self.classroom = args[0]
        self.length = args[1]

    def teacher_desc(self):
        return "Przy biurku stoi pan profesor %s." % self.teacher.mianownik

    def teacher_look(self):
        return self.teacher_desc()


class Matematyka(Lesson):
    name = Noun("matematyka", "matematyki", n="matematyką")
    teacher = Noun("Szymon Dobecki", "Szymona Dobeckiego", n="Szymonem Dobeckim")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)


class WF(Lesson):
    name = Noun("WF", "WF-u", n="WF-em")
    teacher = Noun("Grzegorz Henicz", "Grzegorza Henicza", n="Grzegorzem Heniczem")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)


class Historia(Lesson):
    name = Noun("historia", "historii", n="historią")
    teacher = Noun("Dariusz Piasek", "Dariusza Piaska", n="Dariuszem Piaskiem")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)


class Informatyka(Lesson):
    name = Noun("informatyka", "informatyki", n="informatyką")
    teacher = Noun("Ryszard „Prezes” Szubartowski", "Ryszardem „Prezesem” Szubartowskim",
            n="Ryszarda „Prezesa” Szubartowskiego")

    def __init__(self, *args, **kwargs):
        Lesson.__init__(self, *args, **kwargs)


class TimeTable:
    pass


"""timetominutes"""
def ttm(hr, min):
    return hr*60 + min

"""timetominutes"""
def mtt(min):
    return "%02d:%02d" % (min // 60, min % 60)

table = [ ttm(7, 45), ttm(8, 40), ttm(9, 35), ttm(10, 30), ttm(11, 25), ttm(12, 30), ttm(13, 25),
            ttm(14, 25), ttm(15, 15) ]

"""minutestolesson
(nrLekcji, Lekcja/Przerwa)"""
def mtl(time):
    i = bisect.bisect_left(table, time+1)
    if i == 0:
        return (0, False)
    return (i, time-1 - table[i-1] < 44)

def curless(table, hr, start):
    i = start-1
    for lesson in table:
        i += lesson.length
        if i >= hr:
            return lesson

class Lament1(TimeTable):
    table = [
            [ Matematyka(9, 3), WF(100, 1),
                Historia(9, 1), Informatyka(23, 2) ],
            [],
            [],
            [],
            []
            ]
    length = [ (1, 7), (0, 0)*6 ]

    def status(self, state):
        lek, brk = mtl(state.time)
        day = state.weekday

        if self.length[day][1] == 0:
            state.lesson = None
            return "Dziś masz wolne od szkoły!"
        elif lek < self.length[day][0]:
            state.lesson = self.table[day][0]
            return "Dziś zaczynasz %s o godzinie %s w sali nr %d." % (self.table[day][0].name.narzednik, 
                    mtt(table[self.length[day-1][0]]), self.table[day][0].classroom)
        elif (lek >= self.length[day][1] and brk) or (lek > self.length[day][1]):
            state.lesson = None
            return "Skończyłeś już lekcje na dzisiaj."
        elif brk:
            cur = curless(self.table[day], lek, self.length[day][0])
            state.lesson = cur
            return "W sali nr %d trwa lekcja %s." % \
                    (cur.classroom, cur.name.dopelniacz)
        elif not brk:
            cur = curless(self.table[day], lek+1, self.length[day][0])
            state.lesson = cur
            return "Następna lekcja to %s w sali %d." % \
                    (cur.name.mianownik, cur.classroom)
                    
        return ""

