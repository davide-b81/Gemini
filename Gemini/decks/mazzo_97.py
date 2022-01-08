'''
Created on 4 gen 2022

@author: david
'''
from decks.mazzo import Mazzo
from game.germini.carta import Carta

NUMERO_C = 97

class Mazzo97(Mazzo):
    '''
    classdocs
    '''

    def __init__(self, params=None):
        '''
        Constructor
        '''
        super().__init__(params)
        
    def ripristina(self):
        super().ripristina()
        
        for s in Carta:
            self.mazz.insert(0, s)
