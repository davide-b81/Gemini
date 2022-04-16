#   '''
#  Created on 16 3 2022
#  @author: david
#  '''
from copy import copy
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message
from oggetti.posizioni import DeckId

'''
(1). Il mazziere scozza le carte terminando solo dopo aver verificato che in fondo al mazzo vi sia una cartiglia.
'''
class ActionPunteggi(Action):
    ACTSTATUS_CONTA_NORDSUD = "ACTSTATUS_CONTA_NORDSUD"
    ACTSTATUS_CONTA_ESTOVEST = "ACTSTATUS_CONTA_ESTOVEST"
    ACTSTATUS_CONTROLLA = "ACTSTATUS_WAIT_CLICK2"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    _t_action = None

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            self.reset()
            if self._status == self.ACTSTATUS_CONTA_NORDSUD:
                self._newsts = self.ACTSTATUS_CONTA_ESTOVEST
            elif self._status == self.ACTSTATUS_CONTA_ESTOVEST:
                self._newsts = self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        pass