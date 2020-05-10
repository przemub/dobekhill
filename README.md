Dobek Hill
==========

```
    ___  ___  ___    __               _____  __    __
   /   \/___\/ __\  /__\/\ /\   /\  /\\\_   \/ /   / /
  / /\ //  //__\// /_\ / //_/  / /_/ / / /\/ /   / /
 / /_// \_// \/  \//__/ __ \  / __  /\/ /_/ /___/ /___
/___,'\___/\_____/\__/\/  \/  \/ /_/\____/\____/\____/

Witaj w świecie Dobek Hill.
Tylko w tej grze możesz wygrać w grze, jaką jest uczęszczanie do gdyńskiej Trójki. Powodzenia!
```

Dobek Hill to [MUD](https://pl.wikipedia.org/wiki/MUD_(RPG)) - czyli tekstowa gra MMORPG - osadzona w realiach III Liceum Ogólnokształcącego im. Marynarki Wojennej RP.

Gra nigdy nie wyszła poza fazę proof-of-concept i jest moją pierwszą próbą napisania gry sieciowej, także proszę się nie obrażać jeżeli Twój ruter zajmie się ogniem a brzydota kodu wypali Ci oczy.

Działająca instancja gry znajduje się pod adresem https://1mi.pl/shell - username: dobekhill, pass: dobekhill.

Wymagania
---------

Aby postawić własną instancję Dobek Hilla lub zabrać się za development, potrzebujesz:
* Pythona 3.6+,
* [pipenv](https://pipenv-fork.readthedocs.io/en/latest/).

Opcjonalnie, do części sieciowej:
* serwera [Redis](https://redis.io/) na porcie domyślnym.

Przykładowo, na systemie Arch Linux:
```bash
pacman -S --needed python python-pipenv redis 
systemctl enable --now redis
```

Instalacja
----------
Instalacja bibliotek:
```bash
pipenv install
```

Uruchamianie klienta:
```bash
pipenv run dobekhill/main.py
```

Rozwój
------

Trwał krótko i umarł lata temu, ale chętnie przyjmę łatki.

* *main.py* - uruchamia pętlę gry, wczytując zapis lub tworząc nową postać.
* *game.py* - definiuje pętlę gry (`HillShell.loop`) i polecenia (funkcje o nazwach `HillShell.do_*`, wykrywane dynamicznie).
* *locations.py* - definiuje mapę gry, lokacje (podklasy `locations.Location`) i przedmioty (`locations.Item`).
* *lessons.py* - definiuje lekcje i fabułę. Wczesna faza alfa.
* *structs.py* - definiuje przydatne obiekty.
* *helper.py* - definiuje funkcje używane w różnych miejscach kodu.
* *server/client.py* - obsługuje komunikację klienta z serwerem Redis.

**TODO:**
* dokumentacja kodu,
* podniesienie jakości kodu do jakiegokolwiek standardu,
* wyjście poza alfę z system lekcji i mijania czasu,
* nakreślenie fabuły,
* wszystko inne, na co pozwoli wyobraźnia(tm).
