from enum import Enum

class Location:
    pass

class Item:
    pass

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
Możesz podejść pod główne wejście do szkoły (północ), pod wejście boczne (północny wschód), pójść do sklepu (zachód) lub wrócić do internatu (wschód)."""

    directions = [dirs["N"], dirs["NE"], dirs["W"], dirs["E"]]

    class Tabliczka(Item):
        name = "tabliczka"
        desc = "Na płocie wisi tabliczka z napisem „patrz tabliczka”."
        look = "Nic tu jeszcze nie ma. Wróć później!"

    items = [Tabliczka()]

    def exit(e):
        pass


