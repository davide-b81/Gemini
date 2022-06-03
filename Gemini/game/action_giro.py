#   '''
#  Created on 7 4 2022
#  @author: david
#  '''
from copy import copy
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia, get_greatest_card, seme_name, get_seme, CartaId, is_tarocco
from game.germini.action import Action
from game.germini.punteggi import is_conto
from main.exception_man import ExceptionMan
from oggetti.posizioni import *
from main.globals import echo_message, FRONTE_SCOPERTA


class ActionGiro(Action):
    """

    (). Il giocatore che ha estratto la terza carta farà coppia con il primo mazziere. Dopo tre giri il gioco ha termine.

    """
    ACTSTATUS_PESCA_1 = "ACTSTATUS_PESCA_1"
    ACTSTATUS_PESCA_2 = "ACTSTATUS_PESCA_2"
    ACTSTATUS_PESCA_3 = "ACTSTATUS_PESCA_3"
    ACTSTATUS_PESCA_4 = "ACTSTATUS_PESCA_4"
    ACTSTATUS_VALIDA = "ACTSTATUS_VALIDA"
    ACTSTATUS_NOTIFICA = "ACTSTATUS_NOTIFICA"
    ACTSTATUS_PARTITA_1 = "ACTSTATUS_PARTITA_1"
    ACTSTATUS_PARTITA_2 = "ACTSTATUS_PARTITA_2"
    ACTSTATUS_PARTITA_3 = "ACTSTATUS_PARTITA_3"
    ACTSTATUS_RISULTATI = "ACTSTATUS_RISULTATI"

    _n = None
    _d = None
    _sorteggio = None

    def __init__(self, fsm):
        try:
            super().__init__(fsm)
            self._sorteggio = []
            self._n = 0
            self._d = []
            self._t_action = monotonic()
            self._newsts = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        """
        (). Prima di iniziare ogni giocatore pesca una carta dal mazzo.
        (). Se due o più giocatori estraggono carte con lo stesso valore questi le estraggono di nuovo; anche il matto
        non è considerato un'estrazione valida.
        """
        try:
            if self._status == self.ACTSTATUS_PESCA_1:
                d = self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_SUD)
                if len(d) == 0:
                    self.giocatore_pesca(self.get_disposizione_iniziale(POSTAZIONE_SUD), POSTAZIONE_SUD)
                self._newsts = self.ACTSTATUS_PESCA_2
            elif self._status == self.ACTSTATUS_PESCA_2:
                d = self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_EST)
                if len(d) == 0:
                    self.giocatore_pesca(self.get_disposizione_iniziale(POSTAZIONE_EST), POSTAZIONE_EST)
                self._newsts = self.ACTSTATUS_PESCA_3

            elif self._status == self.ACTSTATUS_PESCA_3:
                d = self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_NORD)
                if len(d) == 0:
                    self.giocatore_pesca(self.get_disposizione_iniziale(POSTAZIONE_NORD), POSTAZIONE_NORD)
                self._newsts = self.ACTSTATUS_PESCA_4

            elif self._status == self.ACTSTATUS_PESCA_4:
                d = self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_OVEST)
                if len(d) == 0:
                    self.giocatore_pesca(self.get_disposizione_iniziale(POSTAZIONE_OVEST), POSTAZIONE_OVEST)
                self._newsts = self.ACTSTATUS_VALIDA

            elif self._status == self.ACTSTATUS_VALIDA:
                for pos in self._fsm.posizioni:
                    d = self._fsm.get_deck(DeckId.DECK_TAVOLA, pos)
                    if len(d) > 0 and d[0].get_id() == CartaId.MATTO_0:
                        d.remove(d[0])
                        self._status = self.ACTSTATUS_PESCA_1
                        break

                if self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_SUD).get_carta(-1) %\
                        self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_EST).get_carta(-1) == 0:
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_SUD)
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_EST)
                    self.show_timed_popup(str(self._fsm.get_giocatori()[0]) +  " e " + str(self._fsm.get_giocatori()[1]) + " ripescano.")
                    self._newsts = self.ACTSTATUS_PESCA_1
                elif self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_SUD).get_carta(-1) %\
                        self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_NORD).get_carta(-1) == 0:
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_SUD)
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_NORD)
                    self.show_timed_popup(str(self._fsm.get_giocatori()[0]) +  " e " + str(self._fsm.get_giocatori()[2]) + " ripescano.")
                    self._newsts = self.ACTSTATUS_PESCA_1
                elif self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_SUD).get_carta(-1) %\
                        self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_OVEST).get_carta(-1) == 0:
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_SUD)
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_OVEST)
                    self.show_timed_popup(str(self._fsm.get_giocatori()[0]) + " e " + str(self._fsm.get_giocatori()[3]) + " ripescano.")
                    self._newsts = self.ACTSTATUS_PESCA_1
                elif self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_EST).get_carta(-1) %\
                        self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_OVEST).get_carta(-1) == 0:
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_EST)
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_OVEST)
                    self.show_timed_popup(str(self._fsm.get_giocatori()[1]) + " e " + str(self._fsm.get_giocatori()[3]) + " ripescano.")
                    self._newsts = self.ACTSTATUS_PESCA_1
                elif self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_NORD).get_carta(-1) %\
                        self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_OVEST).get_carta(-1) == 0:
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_NORD)
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_OVEST)
                    self.show_timed_popup(str(self._fsm.get_giocatori()[2]) + " e " + str(self._fsm.get_giocatori()[3]) + " ripescano.")
                    self._newsts = self.ACTSTATUS_PESCA_1
                elif self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_NORD).get_carta(-1) %\
                        self._fsm.get_deck(DeckId.DECK_TAVOLA, POSTAZIONE_EST).get_carta(-1) == 0:
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_NORD)
                    self._fsm.clear_carte_in_tavola(POSTAZIONE_EST)
                    self.show_timed_popup(str(self._fsm.get_giocatori()[2]) + " e " + str(self._fsm.get_giocatori()[1]) + " ripescano.")
                    self._newsts = self.ACTSTATUS_PESCA_1
                else:
                    self._newsts = self.ACTSTATUS_NOTIFICA
            elif self._status == self.ACTSTATUS_NOTIFICA:
                if self._globals.get_force_mazziere():
                    ppl = self._fsm.get_giocatori()
                    self._sorteggio.append((POSTAZIONE_SUD, ppl[0]))
                    self._sorteggio.append((POSTAZIONE_EST, ppl[1]))
                    self._sorteggio.append((POSTAZIONE_NORD, ppl[2]))
                    self._sorteggio.append((POSTAZIONE_OVEST, ppl[3]))
                else:
                    self.ordina()
                    txt = "<p>Classifica:</p>"
                    txt += "<p>1. " + str(self._sorteggio[0][1]) + " - " + str(self._sorteggio[0][0]) + "</p>"
                    txt += "<p>2. " + str(self._sorteggio[1][1]) + " - " + str(self._sorteggio[1][0]) + "</p>"
                    txt += "<p>3. " + str(self._sorteggio[2][1]) + " - " + str(self._sorteggio[2][0]) + "</p>"
                    txt += "<p>4. " + str(self._sorteggio[3][1]) + " - " + str(self._sorteggio[3][0]) + "</p>"
                    txt += "<br/><p>Partita 1/4</p>"
                    self.show_timed_popup(txt)
                    self.set_coppie_1()
                self._newsts = self.ACTSTATUS_PARTITA_1

            elif self._status == self.ACTSTATUS_PARTITA_1:
                pass
            elif self._status == self.ACTSTATUS_PARTITA_2:
                pass
            elif self._status == self.ACTSTATUS_PARTITA_3:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def giocatore_pesca(self, player, ppos):
        try:
            if ppos is None:
                ppos = player.get_position()
            c = self._fsm.pesca_dal_mazzo(DeckId.DECK_MAZZO)
            self._fsm.inserisci_nel_mazzo(c, DeckId.DECK_TAVOLA, FRONTE_SCOPERTA, ppos)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_disposizione_iniziale(self, pos):
        try:
            if pos == POSTAZIONE_SUD:
                return self._fsm.get_giocatori()[0]
            elif pos == POSTAZIONE_EST:
                return self._fsm.get_giocatori()[1]
            elif pos == POSTAZIONE_NORD:
                return self._fsm.get_giocatori()[2]
            elif pos == POSTAZIONE_OVEST:
                return self._fsm.get_giocatori()[3]
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ordina(self):
        try:
            self._sorteggio.clear()
            for p in self._fsm.posizioni:
                d = self._fsm.get_deck(DeckId.DECK_TAVOLA, p)
                player = self.get_disposizione_iniziale(p)

                assert len(d) > 0
                cpl = (d[-1], player)
                if len(self._sorteggio) == 0:
                    self._sorteggio.append(cpl)
                else:
                    for i in range(0, len(self._sorteggio)):
                        if is_tarocco(cpl[0].get_id()) and not is_tarocco(self._sorteggio[i][0].get_id()):
                            self._sorteggio.insert(i, cpl)
                            break
                        elif is_tarocco(cpl[0].get_id()) and is_tarocco(self._sorteggio[i][0].get_id()) and\
                                self._sorteggio[i][0].get_numerale() < cpl[0].get_numerale():
                            self._sorteggio.insert(i, cpl)
                            break
                        elif self._sorteggio[i][0].get_numerale() < cpl[0].get_numerale():
                            self._sorteggio.insert(i, cpl)
                            break
                        elif i + 1 >= len(self._sorteggio):
                            self._sorteggio.append(cpl)
                            break
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_coppie_1(self):
        """
        (). Quello che ha estratto la carta più alta sarà il mazziere e avrà come compagno quello con la seconda carta
        """
        try:
            c1 = (self._sorteggio[0][1], self._sorteggio[1][1])
            c2 = (self._sorteggio[2][1], self._sorteggio[3][1])
            mazziere = self._sorteggio[0][1]
            self._fsm.on_coppie(c1, c2, mazziere)
            assert self._fsm.get_mazziere() is not None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_coppie_2(self):
        """
        (). Alla fine del primo giro cambiano le coppie. Il giocatore con la terza carta gioca assieme al mazziere
        """
        try:
            c1 = (self._sorteggio[0][1], self._sorteggio[2][1])
            c2 = (self._sorteggio[1][1], self._sorteggio[3][1])
            mazziere = self._sorteggio[0][1]
            self._fsm.on_coppie(c1, c2, mazziere)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_coppie_3(self):
        """
        (). Al terzo giro il compagno del mazziere sarà il giocatore che ha estratto la carta più bassa
        """
        try:
            c1 = (self._sorteggio[0][1], self._sorteggio[3][1])
            c2 = (self._sorteggio[1][1], self._sorteggio[2][1])
            mazziere = self._sorteggio[0][1]
            self._fsm.on_coppie(c1, c2, mazziere)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start_partita(self):
        """
        (). Quattro partite sono dette giro; alla fine del primo giro cambiano le coppie.
        """
        try:
            if self._n + 1 < 4:
                self._n = self._n + 1
            else:
                if self._status == self.ACTSTATUS_PARTITA_1:
                    self.show_timed_popup("Partita 2/4")
                    self._newsts = self.ACTSTATUS_PARTITA_2
                    self._n = 0
                elif self._status == self.ACTSTATUS_PARTITA_2:
                    self.show_timed_popup("Partita 3/4")
                    self._newsts = self.ACTSTATUS_PARTITA_3
                    self._n = 0
                elif self._status == self.ACTSTATUS_PARTITA_3:
                    self.show_timed_popup("Partita 4/4")
                    self._newsts = self.ACTSTATUS_RISULTATI
                    self._n = 0
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            self._sorteggio.clear()
            self._d.clear()
            if not self._globals.get_force_mazziere():
                self._status = self.ACTSTATUS_PESCA_1
                self._newsts = self.ACTSTATUS_PESCA_1
            else:
                self._status = self.ACTSTATUS_NOTIFICA
                self._newsts = self.ACTSTATUS_NOTIFICA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_status(self):
        return self._status

    def reprJSON(self):
        return self.__dict__()

    @staticmethod
    def fromJSON(self, json_object):
        try:
            if '_id_action' in json_object.keys():
                _id_action = json_object['_id_action']
                _status = json_object['_status']
                _newsts = json_object['_newsts']
                a = ActionGiro("")
                return a
            else:
                return json_object
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)