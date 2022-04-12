'''
Created on 6 mar 2022

@author: david
'''
from game.tarocchi.action_distribuzione import ActionDistribuzione
from main.globals import *
from game.fsm_gioco import FsmGioco
from main.exception_man import ExceptionMan


class FsmTarocchi(FsmGioco):
    '''
    classdocs
    '''
    numero_giocatori = 3
    STATUS_DISTRIBUZIONE = "STATUS_DISTRIBUZIONE"
    STATUS_SCARTA = "STATUS_SCARTA"
    STATUS_ = "STATUS_"

    def __init__(self, gamman=None, genman=None):
        try:
            '''
            Constructor
            '''
            super().__init__(gamman, genman)

            # Actions
            self.add_action(self.STATUS_DISTRIBUZIONE, ActionDistribuzione(self))

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
