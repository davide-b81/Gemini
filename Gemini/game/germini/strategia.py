from random import random

from decks.carta_id import *
from game.germini.punteggi import carte_conto, carte_sopraventi
from main.exception_man import ExceptionMan
from oggetti.posizioni import *

posizioni = [POSTAZIONE_NORD, POSTAZIONE_EST, POSTAZIONE_SUD, POSTAZIONE_OVEST]

class Struttura(object):
    _c_giocate_x_seme = None

class Strategia(object):
    _fsm = object
    _game_man = object
    n_bastoni = 0
    n_denari  = 0
    n_coppe   = 0
    n_spade   = 0
    _taglio_den = False
    _taglio_bas = False
    _taglio_cop = False
    _taglio_spa = False

    _taglio = {}
    _prima = None

    @staticmethod
    def __init__(fsm, game_man):
        Strategia._fsm = fsm
        Strategia._game_man = game_man
        Strategia.reset()

    @staticmethod
    def is_taglio(c, player):
        try:
            if Strategia._game_man.has_seme(player, c.get_seme()):
                return False
            else:
                return True
            ca = Strategia._game_man.get_carte_mano(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def reset():
        try:
            for ppos in posizioni:
                Strategia._taglio[ppos] = {}
                for seme in Palo:
                    Strategia._taglio[ppos][seme] = 0
            Strategia.n_bastoni = 0
            Strategia.n_denari = 0
            Strategia.n_coppe = 0
            Strategia.n_spade = 0
            Strategia._taglio_den = False
            Strategia._taglio_bas = False
            Strategia._taglio_cop = False
            Strategia._taglio_spa = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_randomness():
        return random.randint(0, 3)

    @staticmethod
    def get_scarta(player):
        return

    @staticmethod
    def on_prima(c):
        Strategia._prima = c
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
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def play_fallio(player, num):
        try:
            if num <= 0:
                Strategia.play_una_prima(player, Strategia._prima.get_seme())
            elif num == 1:
                Strategia.play_una_seconda(player, Strategia._prima.get_seme())
            elif num == 2:
                Strategia.play_una_terza(player, Strategia._prima.get_seme())
            else:
                print("Fallio di " + str(player) + " seme " + str(Strategia._prima.get_seme()))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    @staticmethod
    def get_n_fallio(player, c):
        try:
            if c.get_seme() == Palo.DENARI:
                return Strategia._taglio[player.get_position()][c.get_seme()]
            elif c.get_seme() == Palo.SPADE:
                return Strategia._taglio[player.get_position()][c.get_seme()]
            elif c.get_seme() == Palo.COPPE:
                return Strategia._taglio[player.get_position()][c.get_seme()]
            elif c.get_seme() == Palo.BASTONI:
                return Strategia._taglio[player.get_position()][c.get_seme()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def on_carta(player, c):
        try:
            if Strategia._prima == CartaId.MATTO_0:
                Strategia._prima = c
            if Strategia._prima is not None:
                if Strategia._prima.get_seme() != c.get_seme() and c.get_seme() == Palo.TRIONFO:
                    if Strategia._prima.get_seme() == Palo.DENARI and not Strategia._taglio_den:
                        Strategia.play_fallio(player, Strategia.get_n_fallio(player, c))
                        Strategia._taglio_den = True
                        Strategia._taglio[player.get_position()][c.get_seme()] = Strategia._taglio[player.get_position()][c.get_seme()] + 1
                    if Strategia._prima.get_seme() == Palo.COPPE and not Strategia._taglio_cop:
                        Strategia.play_fallio(player, Strategia.get_n_fallio(player, c))
                        Strategia._taglio_cop = True
                        Strategia._taglio[player.get_position()][c.get_seme()] = Strategia._taglio[player.get_position()][c.get_seme()] + 1
                    if Strategia._prima.get_seme() == Palo.SPADE and not Strategia._taglio_spa:
                        Strategia.play_fallio(player, Strategia.get_n_fallio(player, c))
                        Strategia._taglio_spa = True
                        Strategia._taglio[player.get_position()][c.get_seme()] = Strategia._taglio[player.get_position()][c.get_seme()] + 1
                    if Strategia._prima.get_seme() == Palo.BASTONI and not Strategia._taglio_bas:
                        Strategia.play_fallio(player, Strategia.get_n_fallio(player, c))
                        Strategia._taglio_bas = True
                        Strategia._taglio[player.get_position()][c.get_seme()] = Strategia._taglio[player.get_position()][c.get_seme()] + 1
                print("Strategia: " + str(player) + " gioca " + str(c))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def on_presa(player, c_list):
        try:
            for c in c_list:
                print("Strategia: " + str(player) + " prende " + str(c))
            Strategia._prima = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_piglia(player):
        try:
            for c in Strategia._game_man.get_deck(DeckId.DECK_FOLA):
                if c.get_id() in carte_conto or c.get_id() in carte_sopraventi:
                    return c
            return None
        except Exception as e:
            print("get_piglia - Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_carta(player):
        try:
            c_list = Strategia._game_man.get_all_tavola()

            turno = len(c_list)

            if turno == 0:
                return Strategia.gioca_prima_carta(player)
            elif turno == 1:
                return Strategia.gioca_seconda_carta(player)
            elif turno == 2:
                return Strategia.gioca_terza_carta(player)
            elif turno == 3:
                return Strategia.gioca_ultima_carta(player)
            else:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("gioca_carta - Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_prima_carta(player):
        try:
            c = None
            # Per prima cosa si libera delle cartiglie
            s = Strategia.get_seme_apertura(player)

            n = Strategia.count_seme_mano_others(player, s)
            if n > 8:
                c = Strategia.get_king(player, s)

            if c is None:
                return Strategia.gioca_carta_fallback(player)
            return c
        except Exception as e:
            print("gioca_prima_carta - Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_seconda_carta(player):
        try:
            c = None
            if c is None:
                return Strategia.gioca_carta_fallback(player)
            return c
        except Exception as e:
            print("gioca_seconda_carta - Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_terza_carta(player):
        try:
            c = None
            if c is None:
                return Strategia.gioca_carta_fallback(player)
            return c
        except Exception as e:
            print("gioca_terza_carta - Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_ultima_carta(player):
        try:
            c = None
            if Strategia._prima != CartaId.MATTO_0:
                prima = Strategia._prima
            else:
                pass

            if Strategia._fsm.get_winner() == Strategia._fsm.get_compagno(player):
                print("Lascia al compagno")
                return Strategia.get_lascia(player)

            if prima.get_seme() != Palo.TRIONFO:
                c = Strategia.get_king(player, prima.get_seme())
                if c is not None:
                    return c

            if c is None:
                return Strategia.gioca_carta_fallback(player)
            return c
        except Exception as e:
            print("gioca_ultima_carta - Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_altra_carta(player):
        """
        (). La prima carta è già stata giocata
        """
        try:
            c = None
            if len(Strategia._game_man.get_deck_merged(DeckId.DECK_TAVOLA)) == 1:
                c = Strategia.rispondi_1(player)
            elif len(Strategia._game_man.get_deck_merged(DeckId.DECK_TAVOLA)) == 2:
                c = Strategia.rispondi_2(player)
            elif len(Strategia._game_man.get_deck_merged(DeckId.DECK_TAVOLA)) == 3:
                c = Strategia.rispondi_3(player)
            else:
                raise Exception("Error in strategia input")

            if c is None:
                return Strategia.gioca_carta_fallback(player)
            return c
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def apri_mano(player):
        try:
            c = None
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def play_taglio(player, seme):
        try:
            c = None
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def play_una_prima(player, seme):
        try:
            c = None
            print("Fatta una prima di " + str(player) + " seme " + str(seme))
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def play_una_seconda(player, seme):
        try:
            c = None
            print("Fatta una seconda di " + str(player) + " seme " + str(seme))
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            echo_message("Error in strategy management of " + player._name + ". Fallback function.")
    @staticmethod

    def play_una_terza(player, seme):
        try:
            c = None
            print("Fatta una terza di " + str(player) + " seme " + str(seme))
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def rispondi_1(player):
        try:
            c = None
            if Strategia._prima is None:
                raise Exception("Error in Strategia (1)")
            else:
                if Strategia.is_taglio(Strategia._prima, player):
                    if Strategia._game_man.has_seme(player, Palo.TRIONFO):
                        # Il giocatore tirerà un trionfo
                        Strategia.play_fallio(player, Strategia._prima.get_seme())
                pass
            return c
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def rispondi_2(player):
        try:
            c = None
            if Strategia._prima is None:
                raise Exception("Error in Strategia (2)")
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def rispondi_3(player):
        try:
            c = None
            if Strategia._prima is None:
                raise Exception("Error in Strategia (3)")
            # Se il compagno è il vincitore...
            if Strategia._fsm.get_winner() == Strategia._fsm.get_compagno():
                pass
            else:
                pass
                # Se non c'è taglio e ho il re

            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")

    @staticmethod
    def gioca_carta_caduto(player, caduto):
        try:
            c = None
            for c in Strategia._game_man.get_carte_mano(caduto):
                if Strategia._game_man is not None:
                    if Strategia._fsm.is_giocabile(c.get_id()):
                        echo_message(str(player) + " gioca " + str(c) + " di " + str(caduto))
                        return c
            if c is None:
                return Strategia.gioca_carta_fallback(player)
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")
            return Strategia.gioca_carta_caduto_fallback(player, caduto)

    @staticmethod
    def criterio_scarto(player, c):
        return True #c.get_id() in cartiglie

    @staticmethod
    def scarta_carta(player):
        try:
            c = None
            mano = Strategia._fsm.get_carte_mano(player)
            for c in mano:
                if Strategia.criterio_scarto(player, c):
                   return c
            raise Exception("Nessuna carta selezionata per essere scartata")
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")
            return Strategia.scarta_carta_fallback(player)

    @staticmethod
    def scarta_carte(player, n):
        sca = []
        try:
            i = 0
            #crub = Strategia._game_man.get_carte_rubate(player)
            #n = len(crub)
            mano = Strategia._fsm.get_carte_mano(player)
            for c in mano:
                if len(sca) < n:
                    if Strategia.criterio_scarto(player, c):
                        sca.append(c)
                else:
                    break
                print("Strategia. " + str(player) + " scarta " + str(c))
            return sca
        except Exception as e:
            print("Error in strategy management of " + player._name + ". Fallback function.")
            return Strategia.scarta_carte_fallback(player, n)

    @staticmethod
    def gioca_carta_fallback(player):
        try:
            if Strategia._fsm.get_carte_mano(player):
                for c in Strategia._fsm.get_carte_mano(player):
                    if Strategia._game_man is not None:
                        if Strategia._fsm.is_giocabile(c.get_id()):
                            print("Fallback " + player._name + " gioca " + str(c))
                            return c
                return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def gioca_carta_caduto_fallback(player, caduto):
        try:
            for c in Strategia._fsm.get_carte_mano(caduto):
                if Strategia._game_man is not None:
                    if Strategia._fsm.is_giocabile(c.get_id()):
                        print(str(player) + " gioca " + str(c) + " di " + str(caduto))
                        return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def scarta_carte_fallback(player, n):
        ca = []
        try:
            i = 0
            #crub = Strategia._game_man.get_carte_rubate(player)
            #n = len(crub)
            mano = Strategia._game_man.get_carte_mano(player)
            for i in range(n):
                c = mano.pop(0)
                ca.append(c)
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def scarta_carta_fallback(player):
        return Strategia.scarta_carte_fallback(player, 1)

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
    def on_fallio(player, cid):
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


    #-------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_cartiglia(player):
        """
        I. Per prima cosa il giocatore cerca di liberarsi delle proprie cartiglie;
        Se non sono il primo cerco:
        - Di rimanere ultimo di mano giocando la cartiglia più bassa
        - Di liberarmi delle cartiglie più alte
        - Se quello che ha giocato la carta più alta è il compagno, devo giocare la più alta che ho se sono ultimo di mano
        """
        try:
            for c in Strategia._fsm.get_carte_mano(player):
                if is_cartiglia(c.get_id()) and Strategia._fsm.is_giocabile(c.get_id()):
                    return c
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    # - Se sono state gioate poche carte di un seme posso provare a tirare il Re

    # - Se il compagno ha giocato punti cerco di forzare se sono ultimo di mano

    @staticmethod
    def get_posizione_mano(player):
        """
        Conta le carte già calate -> capisco se sono ultimo di mano
        """
        try:
            c = None
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def count_seme_mano_others(player, seme):
        """
        Valuta quante carte di un seme sono in mano agli altri giocatori
        """
        try:
            n = 0
            for p in Strategia._game_man.get_giocatori():
                if p != player:
                    for c in Strategia._fsm.get_carte_mano(p):
                        if c.get_seme() == seme:
                            n = n + 1
            return n
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_forza(player):
        """
        Restituisce la minima carta che vince la mano
        """
        try:
            cret = None

            for c in Strategia._fsm.get_carte_mano(player):
                if Strategia._fsm.is_giocabile(c):
                    if cret is None:
                        cret = c
                    else:
                        pass
            return cret
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_lascia(player):
        """
        Restituisce la minima carta giocabile
        """
        try:
            cret = None

            for c in Strategia._fsm.get_carte_mano(player):
                if Strategia._fsm.is_giocabile(c):
                    if cret is None:
                        cret = c
                    else:
                        if get_punti_carta(cret) > get_punti_carta(c):
                            cret = c
            return cret
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_fumata():
        """
        Restituisce la carta da giocare come "fumata" (solo se sono il primo della coppia a giocare)
        """
        try:
            c = None
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_cade():
        """
        Indica se ci sono le condizioni per tirarsi indietro e scoprire le carte
        """
        try:
            c = None
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_taglio():
        """
        Trova il Trionfo da giocare (in base al fatto che gli altri possono avere o meno da rispondere al seme iniziale)
        """
        try:
            c = None
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_taglio():
        """
        Trova il Trionfo da giocare al primo taglio
        - Se sono il primo a tagliare posso provare a giocare un papino o il tarocco con maggiore punteggio
        """
        try:
            c = None
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_seme_apertura(player):
        try:
            for c in Strategia._fsm.get_carte_mano(player):
                if c.get_seme() != Palo.TRIONFO:
                    return c.get_seme()
            return Palo.TRIONFO
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @staticmethod
    def get_king(player, seme):
        try:
            for c in Strategia._fsm.get_carte_mano(player):
                if c.get_seme() == seme:
                    if c.get_id() == CartaId.DANAR_R:
                        return c
                    if c.get_id() == CartaId.SPADE_R:
                        return c
                    if c.get_id() == CartaId.COPPE_R:
                        return c
                    if c.get_id() == CartaId.BASTO_R:
                        return c
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)