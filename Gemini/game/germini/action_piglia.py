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
(7). Le carte che sono avanzate vengono ora dette la fola; da questa il mazziere scopre la prima carta e, se
 si tratta di una carta di conto o di un sopraventi, la pone sul tavolo segnandone subito a suo vantaggio il valore.
 Il mazziere continua quindi a scoprire una carta alla volta della fola finché trova carte di conto o sopraventi
 segnandone subito il valore.
(8). Appena trova una carta diversa, il mazziere la rimette nella fola che poi guarda tutta quanta senza però
 mostrarla agli avversari.
(9). Dalla fola prende quindi tutte le carte di conto (ma non i sopraventi) ponendole scoperte davanti a sé e
 senza segnarne il valore. Ci si riferisce a questa parte del gioco con il termine “pigliare”.
'''
class ActionPiglia(Action):

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("Action - I"))
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
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)