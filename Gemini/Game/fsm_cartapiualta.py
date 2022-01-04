'''
Created on 4 gen 2022

@author: david
'''
from Game.fsm_gioco import FsmGioco

class FsmCartaPiuAlta(FsmGioco):
    '''
    classdocs
    '''

    def __init__(self, params = None):
        '''
        Constructor
        '''
        super().__init__(params)
        
    def update_game(self):
        pass