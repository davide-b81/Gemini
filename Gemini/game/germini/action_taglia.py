#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
import random
from time import monotonic

from decks.carta_id import *
from game.germini.action import Action
from game.germini.punteggi import punti_ger
from main.exception_man import ExceptionMan
from main.globals import *
from oggetti.posizioni import DECK_TAGLIO, DECK_MAZZO

'''
(2). Il mazziere passa il mazzo al giocatore che si trova alla sua sinistra il quale taglia il mazzo   
'''
class ActionTaglia(Action):
    ACTSTATUS_VEDIULTIMA = "ACTSTATUS_VEDIULTIMA"
    ACTSTATUS_WAIT_TAGLIO = "ACTSTATUS_WAIT_CLICK1"
    ACTSTATUS_MOSTRA_TAGLIO = "ACTSTATUS_MOSTRA_TAGLIO"
    ACTSTATUS_RUBA = "ACTSTATUS_WAIT_CLICK2"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    _t_action = None
    _player = None

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()
        self._player = None

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionTaglia - Il mazziere dà al giocatore alla sua sinistra il mazzo da tagliare "))
            self._fsm.game_man.raddrizza_mazzo()
            self._player = self._fsm.update_next_player(self._fsm.game_man.get_mazziere(), False)
            self._fsm.game_man.mostra_mazzo(self._player.get_position())
            self._status = self.ACTSTATUS_WAIT_TAGLIO
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            if self._status == self.ACTSTATUS_WAIT_TAGLIO:
                if self._fsm.simulated(self._player):
                    nc = len(self._fsm.get_deck(DECK_MAZZO)) - 1
                    self._fsm.general_man.split_mazzo_n(random.randint(2, nc))
                    self._fsm.game_man.mostra_taglio(self._player.get_position())
                    self.wait_seconds(1)
                    self._status = self.ACTSTATUS_MOSTRA_TAGLIO
            elif self._status == self.ACTSTATUS_MOSTRA_TAGLIO:
                    self._status = self.ACTSTATUS_RUBA
            elif self._status == self.ACTSTATUS_RUBA:
                if self._fsm.simulated(self._player):
                    c = self._fsm.game_man.get_prima(DECK_TAGLIO)
                    if c is not None:
                        if is_sopraventi(c.get_id()) or c.get_id() in punti_ger:
                            c = self._fsm.game_man.pop_prima(DECK_TAGLIO)
                            self._fsm.add_rubate_giocatore(self._player, c)
                            self._fsm.game_man.mostra_rubate(self._player.get_position())
                            self.wait_seconds(1)
                        else:
                            self._fsm.game_man.ricomponi_taglio()
                            self._player = self._fsm.set_player(self._fsm.game_man.get_mazziere())
                            self._fsm.game_man.mostra_mazzo(self._player.get_position())
                            self._status = self.ACTSTATUS_END
            elif self._status == self.ACTSTATUS_VEDIULTIMA:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if not self._fsm.simulated(self._player):
                if self._status == self.ACTSTATUS_WAIT_TAGLIO:
                    c = self._fsm.game_man.get_prima(DECK_MAZZO)
                    if str(cid) != str(c.get_id()):
                        self._fsm.game_man.taglia_mazzo(cid)
                        self._fsm.game_man.mostra_taglio(self._player.get_position())
                        c = self._fsm.game_man.get_prima(DECK_TAGLIO)
                        if is_sopraventi(c.get_id()) or c.get_id() in punti_ger:
                            self._status = self.ACTSTATUS_RUBA
                        else:
                            self.wait_seconds(1)
                            self._status = self.ACTSTATUS_MOSTRA_TAGLIO
                elif self._status == self.ACTSTATUS_RUBA:
                    c = self._fsm.game_man.get_prima(DECK_TAGLIO)
                    if c is not None and str(cid) == c.get_name():
                        if is_sopraventi(c.get_id()) or c.get_id() in punti_ger:
                            c = self._fsm.game_man.pop_prima(DECK_TAGLIO)
                            self._fsm.add_rubate_giocatore(self._player, c)
                            self._fsm.game_man.mostra_rubate(self._player.get_position())
                        else:
                            self._fsm.game_man.ricomponi_taglio()
                            self._player = self._fsm.set_player(self._fsm.game_man.get_mazziere())
                            self._fsm.game_man.mostra_mazzo(self._player.get_position())
                            #TODO: Vede le prime 13 carte
                            self._status = self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
