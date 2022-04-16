#   '''
#  Created on 7 4 2022
#  @author: david
#  '''
from copy import copy
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia, get_greater, seme_name, get_seme, CartaId, is_tarocco
from game.germini.action import Action
from game.germini.punteggi import is_conto
from main.exception_man import ExceptionMan
from main.globals import echo_message, POSTAZIONE_SUD, POSTAZIONE_NORD, POSTAZIONE_EST, POSTAZIONE_OVEST, \
    FRONTE_SCOPERTA
from oggetti.posizioni import DeckId


class ActionGiro(Action):
    """

    (). Il giocatore che ha estratto la terza carta farà coppia con il primo mazziere. Dopo tre giri il gioco ha termine.

    """
    ACTSTATUS_PESCA_1 = "ACTSTATUS_PESCA_1"
    ACTSTATUS_PESCA_2 = "ACTSTATUS_PESCA_2"
    ACTSTATUS_PESCA_3 = "ACTSTATUS_PESCA_3"
    ACTSTATUS_PESCA_4 = "ACTSTATUS_PESCA_4"
    ACTSTATUS_NOTIFICA = "ACTSTATUS_NOTIFICA"
    ACTSTATUS_PARTITA_1 = "ACTSTATUS_PARTITA_1"
    ACTSTATUS_PARTITA_2 = "ACTSTATUS_PARTITA_2"
    ACTSTATUS_PARTITA_3 = "ACTSTATUS_PARTITA_3"
    ACTSTATUS_RISULTATI = "ACTSTATUS_RISULTATI"

    _n = None
    _c = None
    _d = None
    _sorteggio = None

    def __init__(self, fsm):
        try:
            super().__init__(fsm)
            self._t_action = monotonic()
            self._newsts = self.ACTSTATUS_PESCA_1
            self._n = 0
            self._c = {}
            self._d = []
            self._sorteggio = []
            self._c["Nord"] = None
            self._c["Ovest"] = None
            self._c["Sud"] = None
            self._c["Est"] = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        """
        (). Prima di iniziare ogni giocatore pesca una carta dal mazzo.
        """
        try:
            if self._status == self.ACTSTATUS_PESCA_1:
                if self.giocatore_pesca(self._fsm.get_giocatori()[0], POSTAZIONE_NORD):
                    self._newsts = self.ACTSTATUS_PESCA_2
            elif self._status == self.ACTSTATUS_PESCA_2:
                if self.giocatore_pesca(self._fsm.get_giocatori()[1], POSTAZIONE_OVEST):
                    self._newsts = self.ACTSTATUS_PESCA_3
            elif self._status == self.ACTSTATUS_PESCA_3:
                if self.giocatore_pesca(self._fsm.get_giocatori()[2], POSTAZIONE_SUD):
                    self._newsts = self.ACTSTATUS_PESCA_4
            elif self._status == self.ACTSTATUS_PESCA_4:
                if self.giocatore_pesca(self._fsm.get_giocatori()[3], POSTAZIONE_EST):
                    self._newsts = self.ACTSTATUS_NOTIFICA
            elif self._status == self.ACTSTATUS_NOTIFICA:
                if self.ripesca():
                    self.show_timed_popup("Ripesca")
                else:
                    self.ordina()
                    txt = "<p>Classifica:</p>"
                    txt += "<p>1. " + str(self._sorteggio[0][1]) + " - " + str(self._sorteggio[0][0]) + "</p>"
                    txt += "<p>2. " + str(self._sorteggio[1][1]) + " - " + str(self._sorteggio[1][0]) + "</p>"
                    txt += "<p>3. " + str(self._sorteggio[2][1]) + " - " + str(self._sorteggio[2][0]) + "</p>"
                    txt += "<p>4. " + str(self._sorteggio[3][1]) + " - " + str(self._sorteggio[3][0]) + "</p>"
                    txt += "<br/><p>Partita 1/4</p>"
                    self.show_timed_popup(txt, 0.01)
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
            c = self._fsm.pesca_dal_mazzo(DeckId.DECK_MAZZO)
            self._c[ppos] = c
            self._d.append((c, player))
            self._fsm.inserisci_nel_mazzo(c, DeckId.DECK_TAVOLA, ppos)
            if c.get_id() == CartaId.MATTO_0:
                echo_message(str(player) + " ha pescato " + str(self._c[ppos]) + ". Pesca di nuovo.")
                return False
            else:
                echo_message(str(player) + " ha pescato " + str(self._c[ppos]))
                return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ripesca(self):
        try:
            res = []
            for key, value in self._c.items():
                if value is not None:
                    if is_tarocco(value.get_id()):
                        if len (res) == 0:
                            res.append((key, value))
                        else:
                            pass
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ordina(self):
        try:
            self._sorteggio.clear()
            for cpl in self._d:
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
            self._status = self.ACTSTATUS_PESCA_1
            self._newsts = self.ACTSTATUS_PESCA_1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_status(self):
        return self._status

