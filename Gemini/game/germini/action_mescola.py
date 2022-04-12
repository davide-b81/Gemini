#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message, FRONTE_COPERTA
from oggetti.posizioni import DeckId

'''
(1). Il mazziere scozza le carte terminando solo dopo aver verificato che in fondo al mazzo vi sia una cartiglia.
'''
class ActionMescola(Action):

    ACTSTATUS_VEDIULTIMA = "ACTSTATUS_VEDIULTIMA"
    ACTSTATUS_ROVESCIA = "ACTSTATUS_ROVESCIA"
    ACTSTATUS_CONTROLLA = "ACTSTATUS_WAIT_CLICK2"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    _t_action = None

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
            self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
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
                    self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
                    self._newsts = self.ACTSTATUS_VEDIULTIMA
            elif self._status == self.ACTSTATUS_CONTROLLA:
                if self._fsm.simulated(self._fsm.get_mazziere()):
                    self._fsm.capovolgi_mazzo()
                    self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
                    c = self._fsm.get_prima(DeckId.DECK_MAZZO, self._fsm.get_player())
                    if is_cartiglia(c.get_id()):
                        print(_("Trovata: ") + str(c) + _(". Carte mescolate."))
                        self._fsm.mostrata = c
                        self._newsts = self.ACTSTATUS_END
                    else:
                        print(_("Trovata: ") + str(c) + _(". Mescola di nuovo."))
                        self._fsm.raddrizza_mazzo()
                        self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
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
                self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
                self._newsts = self.ACTSTATUS_VEDIULTIMA

            if self._status == self.ACTSTATUS_CONTROLLA:
                self._fsm.capovolgi_mazzo()
                self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
                c = self._fsm.get_prima(DeckId.DECK_MAZZO, self._fsm.get_player())
                if is_cartiglia(c.get_id()):
                    print(_("Trovata: ") + str(c) + _(". Carte mescolate."))
                    self._fsm.mostrata = c
                    self._newsts = self.ACTSTATUS_END
                else:
                    print(_("Trovata: ") + str(c) + _(". Mescola di nuovo."))
                    self._fsm.raddrizza_mazzo()
                    self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
                    self.start()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)