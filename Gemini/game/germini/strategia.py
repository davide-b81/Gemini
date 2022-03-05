from decks.carta_id import *
from main.globals import *
from main.general_manager import *

class Strategia(object):
    manager = object

    @staticmethod
    def __init__(manager):
        Strategia.manager = manager

    @staticmethod
    def gioca_carta(player):
        try:
            for c in Strategia.manager.get_carte_mano(player):
                if Strategia.manager.gioco_carta.game is not None:
                    if Strategia.manager.gioco_carta.game.is_giocabile(c.get_id()):
                        echo_message(player._name + " gioca " + str(c))
                        return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    @staticmethod
    def scarta_carte(player, n):
        ca = []
        try:
            i = 0
            #crub = Strategia.manager.get_carte_rubate(player)
            #n = len(crub)
            mano = Strategia.manager.get_carte_mano(player)
            for i in range(n):
                c = mano.pop(0)
                ca.append(c)
                echo_message(player._name + " scarta " + str(c))
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def on_carta_tavola(player, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def on_distribuzione(player, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def on_faglio(player, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def update_mano():
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
