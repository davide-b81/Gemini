#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message, FRONTE_SCOPERTA
from oggetti.posizioni import DeckId

'''
(3). Il mazziere distribuisce ora le carte nel seguente modo: prima dieci carte ciascuno partendo dal giocatore
seduto alla sua destra, quindi altre dieci ciascuno ed infine un'ultima carta scoperta agli altri tre giocatori.
Se queste carte scoperte sono carte di conto, il loro valore viene immediatamente segnato (vedremo in seguito come).
'''
class ActionDistribuzione(Action):
    ACTSTATUS_DISTRIBUZIONE_I = "ACTSTATUS_DISTRIBUZIONE_I"
    ACTSTATUS_DISTRIBUZIONE_II = "ACTSTATUS_DISTRIBUZIONE_II"
    ACTSTATUS_DISTRIBUZIONE_ULTIMA = "ACTSTATUS_DISTRIBUZIONE_ULTIMA"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    def __init__(self, fsm):
        try:
            super().__init__(fsm)
            self._t_action = monotonic()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionDistribuzione - Distribuzione delle carte"))
            self._newsts = self.ACTSTATUS_DISTRIBUZIONE_I
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione_I(self):
        try:
            self.mostrata = None
            self._fsm.distribuzione(10, True)
            self._newsts = self.ACTSTATUS_DISTRIBUZIONE_II
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione_II(self):
        try:
            self.mostrata = None
            self._fsm.distribuzione(10, True)
            self._newsts = self.ACTSTATUS_DISTRIBUZIONE_ULTIMA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione_ultima(self):
        try:
            for player in self._fsm.get_giocatori():
                c = self._fsm.pesca_dal_mazzo(DeckId.DECK_MAZZO)
                if c is not None:
                    self._fsm.marca_punti(c, player)
                    self._fsm.consegna_carta(c, FRONTE_SCOPERTA, player)
                else:
                    raise NotImplemented("Condizione mazziere senza ultima carta")
                self._newsts = self.ACTSTATUS_SHOWULTIMA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            if self._status == self.ACTSTATUS_DISTRIBUZIONE_I:
                self.distribuzione_I()
            elif self._status == self.ACTSTATUS_DISTRIBUZIONE_II:
                self.distribuzione_II()
            elif self._status == self.ACTSTATUS_DISTRIBUZIONE_ULTIMA:
                self.distribuzione_ultima()
            elif self._status == self.ACTSTATUS_SHOWULTIMA:
                self._newsts = self.ACTSTATUS_END
            else:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)