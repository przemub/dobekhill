#!/usr/bin/env python3

from helper import *
from structs import Player, Noun
from game import HillShell

HILL = """
    ___  ___  ___    __               _____  __    __  
   /   \/___\/ __\  /__\/\ /\   /\  /\\\_   \/ /   / /  
  / /\ //  //__\// /_\ / //_/  / /_/ / / /\/ /   / /   
 / /_// \_// \/  \//__/ __ \  / __  /\/ /_/ /___/ /___ 
/___,'\___/\_____/\__/\/  \/  \/ /_/\____/\____/\____/ 
"""

witaj = """
Witaj w świecie Dobek Hill.
Tylko w tej grze możesz wygrać w grze, jaką jest uczęszczanie do gdyńskiej Trójki. Powodzenia!

---

- (*N*)owa gra
- (*K*)ontynuuj
"""

gratulacje = """
Gratulacje! Właśnie zostałeś przyjęty do klasy matematyczno-informatycznej Gdyńskiej Trójki! W swoim powiatowym gimnazjum byłeś królem - wbiłeś dwa różne konkursy kuratoryjne, a Twoja średnia przyćmiła wszystkich uczniów kończących szkołę razem z Tobą.

Musisz jeszcze tylko złożyć resztę dokumentów w sekretariacie i Twoja przygoda ze szkołą na Wzgórzu św. Dobesława się rozpocznie.

Powodzenia!\n
"""

def new():
    hprint(gratulacje)

    gracz = Player()

    hprint("Jak masz na imię? >")
    gracz.imie = Noun(input())
    hprint("Jak się nazywasz? >")
    gracz.nazwisko = Noun(input())
    
    """wzrost = None
    while wzrost not in ('w', 'n', 'ś'):
        hprint("Jesteś (w)ysoki, (n)iski, czy (ś)redniego wzrostu? >")
        w = input()
        wzrost = w[0].lower()"""

    while gracz.ulub not in ('i', 'm', 'f'):
        hprint("Jaki jest twój ulubiony przedmiot? *Infa*, *matematyka*, czy może *fizyka*? > ")
        w = input()
        gracz.ulub = w[0].lower()

    while gracz.uslab not in ('i', 'm', 'f'):
        hprint("Który przedmiot idzie ci najgorzej? *Infa*, *matematyka*, czy może *fizyka*? > ")
        w = input()
        gracz.uslab = w[0].lower()

    while gracz.mocny not in ('a', 'p', 'd'):
        hprint("Jaki jest twój mocny drugorzędny przedmiot? Język *angielski*, *drugi język obcy*, czy może *polski*? > ")
        w = input()
        gracz.mocny = w[0].lower()

    while gracz.slaby not in ('a', 'p', 'd'):
        hprint("Który drugorzędny przedmiot idzie ci najgorzej? Język *angielski*, *drugi język obcy*, czy może *polski*? > ")
        w = input()
        gracz.slaby = w[0].lower()

    # Podsumowanie

    
    hprint("\nNazywasz się *%s* *%s*.\n\n" %
            (gracz.imie.mianownik, gracz.nazwisko.mianownik))

    if gracz.ulub == 'i':
        hprint("Od dziecka twoim marzeniem było zostać programistą w firmie tworzącej gry komputerowe. Formatowanie domowego komputera opanowałeś w wieku lat sześciu, a w swoim gimnazjum prowadziłeś szkolną stronę internetową. Olimpiada Informatyczna? Algorytmika? A co to takiego?\n\n")
    elif gracz.ulub == 'm':
        hprint("Twój świat to świat liczb. Od dziecka wolałeś „SuperZagadki” i zadania z „kaktusem” od spotkań z kolegami. Może chciałeś do mat-fizu, ale podkusiła cię wizja opieki merytorycznej p. Ryszarda „Prezesa” Szubartowskiego. Albo po prostu się nie dostałeś. Bywa.\n\n")
    elif gracz.ulub == 'f':
        hprint("Od zawsze fascynowało cię, jaką prędkość początkową należy nadać kluczom i pod jakim kątem je rzucić, by trafiły tam, gdzie chciałeś. Co z tego, że tylko na papierze. Chciałeś do mat-fizu, ale 200 punktów do ndw cię zaorało. Tylko nie mów tego głośno!\n\n")

    if gracz.mocny == 'a':
        hprint("Jakimś sposobem trafiłeś do oddziału dwujęzycznego. Od lat nudzisz się na lekcjach angielskiego i masz nadzieję, że w liceum będzie ciekawiej.\n\n")
    elif gracz.mocny == 'd':
        hprint("Padłeś ofiarą ambicji swoich rodziców i zamiast porządnie nauczyć się angielskiego, świetnie szprechasz/gawarisz/hablasz/cokolwiek i trafiłeś do najwyższej grupy językowej.\n\n")
    elif gracz.mocny == 'p':
        hprint("Patrz Kryśka! Human się trafił! Aby wyrównać półkule po wielogodzinnym wpatrywaniu się w cyferki, od małego filozofujesz, interesują cię poezja i filozofia.\n\n")

    hprint("Wszystko się zgadza? (t/n) >")
    o = input()
    if o[0].lower() != 't':
        new()
    else:
        hprint("\nWidaj w świecie Dobek Hill. Za moment otrzymasz pierwszego questa w tym piekielnym świecie…\n")

        cont()

        shell = HillShell()
        shell.gracz = gracz
        shell.start()

def main():
    print(HILL)

    hprint(witaj)
    
    wybor = -1
    while wybor == -1:
        print("> ", end="")
        w = input()

        if w[0].lower() == 'n':
            wybor = 0
        elif w[0].lower == 'k':
            wybor = 1

    new() 

if __name__ == '__main__':
    main()

