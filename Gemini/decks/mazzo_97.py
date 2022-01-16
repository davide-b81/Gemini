'''
Created on 4 gen 2022

@author: david
'''
from decks.mazzo import Mazzo
from game.carta import Carta, CartaId

NUMERO_C = 97

class Mazzo97(Mazzo):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()

    def ripristina(self):
        super().ripristina()
        
        for id in CartaId:
            c = Carta(id)
            self.carte.insert(0, c)
