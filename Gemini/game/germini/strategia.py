from decks.carta_id import *
from main.globals import *
from game.player import Player

class Strategia(object):
    manager = object

    @staticmethod
    def __init__(manager):
        Strategia.manager = manager

    @staticmethod
    def gioca_carta(player):
        try:
            for c in player.get_carte_mano():
                print("Test " + str(c))
                if Strategia.manager.gioco_carta.game is not None:
                    if Strategia.manager.gioco_carta.game.is_giocabile(c.get_id()):
                        echo_message(player._name + " gioca " + str(c))
                        return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    @staticmethod
    def on_carta_tavola(player, cid):
        pass

    @staticmethod
    def on_distribuzione(player, cid):
        pass

    @staticmethod
    def on_faglio(player, cid):
        pass

    @staticmethod
    def update_mano():
        pass
