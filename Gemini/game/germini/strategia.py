from decks.carta_id import is_cartiglia, cartiglie, denari, spade, coppe, bastoni, Palo
from game.germini.punteggi import carte_sopraventi
from main.general_manager import *
from main.exception_man import ExceptionMan

class Strategia(object):
    manager = object
    n_bastoni = 0
    n_denari  = 0
    n_coppe   = 0
    n_spade   = 0

    @staticmethod
    def __init__(manager):
        Strategia.manager = manager

    @staticmethod
    def get_randomness():
        return random.randint(0, 3)

    @staticmethod
    def get_scarta(player):
        return

    @staticmethod
    def on_prima(c):
        s = get_seme(c.get_id())
        try:
            if s in denari:
                Strategia.n_denari = Strategia.n_denari + 1
            elif s in spade:
                Strategia.n_spade = Strategia.n_spade + 1
            elif s in coppe:
                Strategia.n_coppe = Strategia.n_coppe + 1
            elif s in bastoni:
                Strategia.n_bastoni = Strategia.n_bastoni + 1
            else:
                pass
        except Exception as e:
            ExceptionMan.manage_exception(str(a), e, True)

    @staticmethod
    def reset():
        Strategia.n_bastoni = 0
        Strategia.n_denari = 0
        Strategia.n_coppe = 0
        Strategia.n_spade = 0

    @staticmethod
    def get_piglia(player):
        try:
            for c in Strategia.manager.get_carte_fola(player):
                if c in carte_conto or c in carte_sopraventi:
                    return c
            return None
        except Exception as e:
            echo_message("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_carta(player):
        try:
            # Per prima cosa si libera delle cartiglie
            c = Strategia.get_cartiglia(player)

            if c is None:
                return Strategia.gioca_carta_fallback(player)
            return c
        except Exception as e:
            echo_message("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_carta_caduto(player, caduto):
        try:
            for c in Strategia.manager.get_carte_mano(caduto):
                if Strategia.manager.game is not None:
                    if Strategia.manager.game.is_giocabile(c.get_id()):
                        echo_message(str(player) + " gioca " + str(c) + " di " + str(caduto))
                        return c
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            echo_message("Error in strategy management of " + player._name + ". Fallback function.")
            return Strategia.gioca_carta_caduto_fallback(player)

    @staticmethod
    def criterio_scarto(player, c):
        return c.get_id() in cartiglie

    @staticmethod
    def scarta_carte(player, n):
        sca = []
        try:
            i = 0
            #crub = Strategia.manager.get_carte_rubate(player)
            #n = len(crub)
            mano = Strategia.manager.get_carte_mano(player)
            for c in mano:
                if len(sca) < n:
                    if Strategia.criterio_scarto(player, c):
                        sca.append(c)
                else:
                    break
                echo_message("Strategia. " + str(player) + " scarta " + str(c))
            return sca
        except Exception as e:
            echo_message("Error in strategy management of " + player._name + ". Fallback function.")
            return Strategia.scarta_carte_fallback(player, n)

    @staticmethod
    def gioca_carta_fallback(player):
        try:
            for c in Strategia.manager.get_carte_mano(player):
                if Strategia.manager.game is not None:
                    if Strategia.manager.game.is_giocabile(c.get_id()):
                        echo_message("Fallback " + player._name + " gioca " + str(c))
                        return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def gioca_carta_caduto_fallback(player, caduto):
        try:
            for c in Strategia.manager.get_carte_mano(caduto):
                if Strategia.manager.game is not None:
                    if Strategia.manager.game.is_giocabile(c.get_id()):
                        echo_message(str(player) + " gioca " + str(c) + " di " + str(caduto))
                        return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def scarta_carte_fallback(player, n):
        ca = []
        try:
            i = 0
            #crub = Strategia.manager.get_carte_rubate(player)
            #n = len(crub)
            mano = Strategia.manager.get_carte_mano(player)
            for i in range(n):
                c = mano.pop(0)
                ca.append(c)
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

    @staticmethod
    def fumata():
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_cartiglia(player):
        """
        I. Per prima cosa il giocatore cerca di liberarsi delle proprie cartiglie
        """
        try:
            for c in Strategia.manager.get_carte_mano(player):
                if is_cartiglia(c.get_id()) and Strategia.manager.game.is_giocabile(c.get_id()):
                    return c
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)