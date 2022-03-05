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

class ActionDichiara(Action):
    ACTION_DICHIARA1 = "ACTION_DICHIARA1"
    ACTION_DICHIARA2 = "ACTION_DICHIARA2"
    ACTION_DICHIARA3 = "ACTION_DICHIARA3"
    ACTION_DICHIARA4 = "ACTION_DICHIARA4"

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("Action - Dichiara"))
            self._status = self.ACTION_DICHIARA1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            if self._status == self.ACTION_DICHIARA1:
                self._fsm._player.dichiara()
                self._fsm._player = self._fsm.game_man.get_next_player(self._fsm._player, True)
                self._status = self.ACTION_DICHIARA2
            elif self._status == self.ACTION_DICHIARA2:
                self._fsm._player.dichiara()
                self._fsm._player = self._fsm.game_man.get_next_player(self._fsm._player, True)
                self._status = self.ACTION_DICHIARA3
            elif self._status == self.ACTION_DICHIARA3:
                self._fsm._player.dichiara()
                self._fsm._player = self._fsm.game_man.get_next_player(self._fsm._player, True)
                self._status = self.ACTION_DICHIARA4
            elif self._status == self.ACTION_DICHIARA4:
                self._fsm._player.dichiara()
                self._fsm._player = self._fsm.game_man.get_next_player(self._fsm._player, True)
                self._status = self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def dichiarazione(self):
        try:
            if self._status == self.ACTION_DICHIARA1:
                self.giocatore_turno.dichiara()
                self.giocatore_turno = self.game_man.get_next_player(self.giocatore_turno, True)
                self._status = self.ACTION_DICHIARA2
            elif self._status == self.SUB_DICHIARA2:
                self._status = self.ACTION_DICHIARA3
            elif self._status == self.ACTION_DICHIARA3:
                self._status = self.ACTION_DICHIARA4
            elif self._status == self.ACTION_DICHIARA4:
                self.giocatore_turno.dichiara()
                self.giocatore_turno = self.game_man.get_next_player(self.giocatore_turno, True)
                self._status = self.ACTSTATUS_END
                self.cid_apertura = None
            elif self._status is not None:
                raise Exception("Sotto-stato " + self._status + " non previsto!")
            else:
                raise Exception("Sotto-stato non definito!")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)