'''
Created on 4 gen 2022

@author: david
'''
from decks.deck import Deck
from decks.carta import Carta, CartaId

NUMERO_C = 97


class Deck97(Deck):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.ripristina()


    def ripristina(self):
        super().ripristina()
        
        for id in CartaId:
            c = Carta(id)
            self._carte.insert(0, c)
