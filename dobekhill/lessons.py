from structs import Noun

class Lesson:
    pass

class Matematyka(Lesson):
    name = Noun("matematyka", "matematyki")

class WF(Lesson):
    name = Noun("WF", "WF-u")

class Historia(Lesson):
    name = Noun("historia", "historii")

class Informatyka(Lesson):
    name = Noun("informatyka", "informatyki")

class TimeTable:
    pass

class Lament1(TimeTable):
    table = [
            [ Matematyka(), Matematyka(), Matematyka(), WF(), Historia(), Informatyka(), Informatyka() ],
            [],
            [],
            [],
            []
            ]


