from helper import hprint, cont

import pickle
import threading


class Client:
    def __init__(self, redis, game):
        self.r = redis
        self.thread = self.NetThread(redis, game)

    def login(self, s):
        if self.r.sismember('players', s.player.id):
            hprint("Jesteś już zalogowany! Co ty knujesz? Jeżeli jest to wynikiem nagłego przerwania połączenia, "
                   + "to zostaniesz wylogowany po maks. 30 sekundach od zamknięcia klienta gry.\n")
            cont()
            # raise redis.exceptions.ConnectionError

        self.r.sadd('players', s.player.id)
        self.r.set('ref:%d', 10 ** 50)
        self.r.set(s.player.id, pickle.dumps(s, -1))

        self.thread.player = s.player
        self.thread.change_location(type(s.location).__name__)
        self.thread.start()

        self.thread.submit("all", "%s %s przyszedł do szkoły.\n" % (s.player.imie, s.player.nazwisko))

    def update(self, s):
        self.r.set('ref:%d', 10 ** 50)
        self.r.set(s.player.id, pickle.dumps(s, -1))

        self.thread.change_location(type(s.location).__name__)

    def logout(self, player):
        self.thread.submit("all", "%s %s wyszedł ze szkoły.\n" % (player.imie, player.nazwisko))

        self.r.srem('players', player.id)
        self.r.delete(player.id)

        self.thread.zabijSie = True

    def players(self):
        s = self.r.smembers('players')

        return [pickle.loads(self.r.get(gracz)).player for gracz in s]

    def players_in(self, location):
        s = self.r.smembers('players')
        p = [pickle.loads(self.r.get(gracz)) for gracz in s]

        return filter(lambda x: type(x.location) == type(location), p)

    class NetThread(threading.Thread):
        def __init__(self, redis, game):
            threading.Thread.__init__(self)

            self.game = game
            self.lastLocation = None
            self.player = None
            self.r = redis
            self.p = redis.pubsub()

            self.p.subscribe('all')

            self.zabijSie = False

        def change_location(self, location):
            if self.lastLocation:
                message = self.msg(self.player.id,  "%s %s poszedł sobie.\n" % (self.player.imie, self.player.nazwisko))
                self.r.publish(self.lastLocation, message)
                self.p.unsubscribe(self.lastLocation)

            self.lastLocation = location
            self.p.subscribe(location)

            message = self.msg(self.player.id,  "%s %s przyszedł tutaj.\n" % (self.player.imie, self.player.nazwisko))

            self.r.publish(location, message)

        def submit(self, channel, w, color='black'):
            message = self.msg(self.player.id, w, color)
            self.r.publish(channel, message)

        def run(self):
            for m in self.p.listen():
                if self.zabijSie:
                    break

                if m['type'] != 'message':
                    continue

                w = pickle.loads(m['data'])
                if w.sender != self.player.id:
                    hprint('\n')
                    hprint(w.msg, w.color)
                    self.game.prompt()

        @staticmethod
        def msg(sender, msg, color='black'):
            return pickle.dumps(Message(sender, msg, color))


class Message:
    def __init__(self, sender, msg, color):
        self.sender = sender
        self.msg = msg
        self.color = color
