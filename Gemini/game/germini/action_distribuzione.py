#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message
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
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionDistribuzione - Distribuzione delle carte"))
            #self._fsm.giocatore_turno = self._fsm.game_man.get_next_player(self._fsm.general_man.get_mazziere())
            self._status = self.ACTSTATUS_DISTRIBUZIONE_I
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione_I(self):
        try:
            self.mostrata = None
            self._fsm.distribuzione(10, True)
            self._status = self.ACTSTATUS_DISTRIBUZIONE_II
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione_II(self):
        try:
            self.mostrata = None
            self._fsm.distribuzione(10, True)
            self._status = self.ACTSTATUS_DISTRIBUZIONE_ULTIMA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione_ultima(self):
        try:
            self._fsm.distribuzione(1, False)
            self._status = self.ACTSTATUS_SHOWULTIMA
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
                self._status = self.ACTSTATUS_END
            else:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)