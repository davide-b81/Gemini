#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message, FRONTE_COPERTA, FRONTE_SCOPERTA
from oggetti.posizioni import *

'''
(1). Il mazziere scozza le carte terminando solo dopo aver verificato che in fondo al mazzo vi sia una cartiglia.
'''
class ActionMescola(Action):

    ACTSTATUS_VEDIULTIMA = "ACTSTATUS_VEDIULTIMA"
    ACTSTATUS_ROVESCIA = "ACTSTATUS_ROVESCIA"
    ACTSTATUS_CONTROLLA = "ACTSTATUS_WAIT_CLICK2"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            self.reset()
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionMescola - Il mazziere mescola le carte e controlla se l'ultima e' una cartiglia"))
            assert self._fsm.get_mazziere() is not None
            self._fsm.restore_manche()
            self._fsm.mescola_mazzo()
            self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_COPERTA, self._fsm.get_mazziere())
            if self._globals.controlla_ultima():
                self._newsts = self.ACTSTATUS_ROVESCIA
            else:
                self._newsts=self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            if self._status == self.ACTSTATUS_ROVESCIA:
                if self._fsm.simulated(self._fsm.get_mazziere()):
                    self._fsm.capovolgi_mazzo()
                    self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_SCOPERTA, self._fsm.get_mazziere())
                    self._newsts = self.ACTSTATUS_VEDIULTIMA
            elif self._status == self.ACTSTATUS_CONTROLLA:
                if self._fsm.simulated(self._fsm.get_mazziere()):
                    self._fsm.capovolgi_mazzo()
                    self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_COPERTA, self._fsm.get_mazziere())
                    c = self._fsm.get_prima(DeckId.DECK_MAZZO, self._fsm.get_player())
                    if is_cartiglia(c.get_id()):
                        print(_("Trovata: ") + str(c) + _(". Carte mescolate."))
                        self._fsm.mostrata = c
                        self._newsts = self.ACTSTATUS_END
                    else:
                        print(_("Trovata: ") + str(c) + _(". Mescola di nuovo."))
                        self._fsm.raddrizza_mazzo()
                        self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_COPERTA, self._fsm.get_mazziere())
                        self.start()
            elif self._status == self.ACTSTATUS_VEDIULTIMA:
                c = self._fsm.get_ultima(DeckId.DECK_MAZZO, self._fsm.get_player())
                self._newsts = self.ACTSTATUS_CONTROLLA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if self._status == self.ACTSTATUS_ROVESCIA:
                self._fsm.capovolgi_mazzo()
                self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_SCOPERTA, self._fsm.get_mazziere())
                self._newsts = self.ACTSTATUS_VEDIULTIMA

            if self._status == self.ACTSTATUS_CONTROLLA:
                self._fsm.capovolgi_mazzo()
                self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_COPERTA, self._fsm.get_mazziere())
                c = self._fsm.get_prima(DeckId.DECK_MAZZO, self._fsm.get_player())
                if is_cartiglia(c.get_id()):
                    print(_("Trovata: ") + str(c) + _(". Carte mescolate."))
                    self._fsm.mostrata = c
                    self._newsts = self.ACTSTATUS_END
                else:
                    print(_("Trovata: ") + str(c) + _(". Mescola di nuovo."))
                    self._fsm.raddrizza_mazzo()
                    self._fsm.show_deck_packed(DeckId.DECK_MAZZO, FRONTE_COPERTA, self._fsm.get_mazziere())
                    self.start()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reprJSON(self):
        return self.__dict__()

    def fromJSON(self, json_object):
        try:
            if '_id_action' in json_object.keys():
                _id_action = json_object['_id_action']
                _status = json_object['_status']
                _newsts = json_object['_newsts']
                a = ActionMescola("")
                return a
            else:
                return json_object
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)