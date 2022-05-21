#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
import random
from time import monotonic

from decks.carta_id import *
from game.germini.action import Action
from game.germini.punteggi import carte_conto
from main.exception_man import ExceptionMan
from main.globals import *
from oggetti.posizioni import *

'''
(2). Il mazziere passa il mazzo al giocatore che si trova alla sua sinistra il quale taglia il mazzo   
'''
class ActionTaglia(Action):
    ACTSTATUS_WAIT_TAGLIO = "ACTSTATUS_WAIT_TAGLIO"
    ACTSTATUS_MOSTRA_TAGLIO = "ACTSTATUS_MOSTRA_TAGLIO"
    ACTSTATUS_RUBA = "ACTSTATUS_RUBA"
    ACTSTATUS_VEDIPRIME13 = "ACTSTATUS_VEDIPRIME13"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    _t_action = None

    def __init__(self, fsm):
        try:
            super().__init__(fsm)
            self._t_action = monotonic()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            self.reset()
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionTaglia - Il mazziere dà al giocatore alla sua sinistra il mazzo da tagliare "))
            self._fsm.raddrizza_mazzo()
            self._fsm.set_player(self._fsm.get_mazziere())
            print("Mazziere " + str(self._fsm.get_mazziere()) + " (" + self._fsm.get_position_turno() + ")")
            self._fsm.update_next_player(False)
            self._fsm.show_deck_packed(DeckId.DECK_MAZZO, self._fsm.get_position_turno())
            self._newsts = self.ACTSTATUS_WAIT_TAGLIO
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
                if self._fsm.simulated():
                    nc = len(self._fsm.get_carte(DeckId.DECK_MAZZO)) - 1
                    self._fsm.split_mazzo_n(random.randint(2, nc))
                    self._fsm.show_deck_packed(DeckId.DECK_TAGLIO, FRONTE_SCOPERTA)
                    self._newsts = self.ACTSTATUS_MOSTRA_TAGLIO

            elif self._status == self.ACTSTATUS_MOSTRA_TAGLIO:
                if self._fsm.simulated():
                    c = self._fsm.get_prima(DeckId.DECK_TAGLIO, self._fsm.get_player())
                    if self.is_rubabile(c):
                        self._newsts = self.ACTSTATUS_RUBA
                    else:
                        self._fsm.ricomponi_taglio(self._fsm.get_player())
                        self._newsts = self.ACTSTATUS_END

            elif self._status == self.ACTSTATUS_RUBA:
                if self._fsm.simulated():
                    c = self._fsm.get_prima(DeckId.DECK_TAGLIO, self._fsm.get_player())
                    if c is not None:
                        if self.is_rubabile(c):
                            c = self._fsm.pop_prima(DeckId.DECK_TAGLIO, self._fsm.get_position_turno())
                            self._fsm.add_rubate_giocatore(self._fsm.get_player(), c)
                            self._fsm.mostra_rubate(self._fsm.get_position_turno())
                            print(str(self._fsm.get_player()) + " ruba " + str(c))
                        else:
                            self._fsm.ricomponi_taglio(self._fsm.get_player())
                            print("Finisce il rubare di " + str(self._fsm.get_player()))
                            self._fsm.set_player(self._fsm.get_mazziere())
                            self._fsm.show_deck_packed(DeckId.DECK_MAZZO, self._fsm.get_position_turno())
                            self._fsm.get_carte(DeckId.DECK_RUBATE, self._fsm.get_player())
                            self._newsts = self.ACTSTATUS_END

            elif self._status == self.ACTSTATUS_VEDIPRIME13:
                if self._fsm.simulated():
                    self._newsts = self.ACTSTATUS_END

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if not self._fsm.simulated():
                if self._status == self.ACTSTATUS_WAIT_TAGLIO:
                    if not self._globals.get_uncover():
                        c = self._fsm.get_prima(DeckId.DECK_MAZZO)
                    else:
                        c = self._fsm.get_ultima(DeckId.DECK_MAZZO)
                    if c is not None and str(cid) != str(c.get_id()):
                        self._fsm.taglia_mazzo(cid)
                        self._fsm.show_deck_packed(DeckId.DECK_TAGLIO, FRONTE_SCOPERTA)
                        #self._fsm.mostra_mazzo(DeckId.DECK_TAGLIO, self._fsm.get_position_turno(), FRONTE_SCOPERTA)
                        self._newsts = self.ACTSTATUS_MOSTRA_TAGLIO

                elif self._status == self.ACTSTATUS_RUBA or self._status == self.ACTSTATUS_MOSTRA_TAGLIO:
                    c = self._fsm.get_prima(DeckId.DECK_TAGLIO, self._fsm.get_player())
                    if c is not None and str(cid) == c.get_name():
                        if self.is_rubabile(c):
                            c = self._fsm.pop_prima(DeckId.DECK_TAGLIO, self._fsm.get_position_turno())
                            self._fsm.add_rubate_giocatore(self._fsm.get_player(), c)
                            self._fsm.mostra_rubate(self._fsm.get_position_turno())
                            print(str(self._fsm.get_player()) + " ruba " + str(c))
                        else:
                            self._fsm.ricomponi_taglio(self._fsm.get_player())
                            print("Finisce il rubare di " + str(self._fsm.get_player()))
                            # Mostra le restanti delle prime 13 carte
                            #n = 13 - self._fsm.get_num_carte_mano(self._fsm.get_player())
                            #self._fsm.mostra_mazzo(self._fsm.get_position_turno(), DeckId.DECK_MAZZO, n)
                            #self._newsts = self.ACTSTATUS_VEDIPRIME13
                            self._fsm.show_deck_packed(DeckId.DECK_MAZZO, self._fsm.get_position_turno())
                            self._newsts = self.ACTSTATUS_END
                elif self._status == self.ACTSTATUS_VEDIPRIME13:
                    if not self._fsm.simulated():
                        self._fsm.mostra_fola(self._fsm.get_player())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_rubabile(self, c):
        '''
        Ruba fino a 13 carte che siano sopraventi o di conto
        '''
        try:
            if self._fsm.get_deck_len(DeckId.DECK_MANO, self._fsm.get_player()) <= 13:
                if is_sopraventi(c.get_id()) or c.get_id() in carte_conto:
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)