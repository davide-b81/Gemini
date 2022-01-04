'''
Created on 4 gen 2022

@author: david
'''
from decks.mazzo import Mazzo
from Logic.Carta import carta

class Mazzo97(Mazzo):
    '''
    classdocs
    '''

    def __init__(self, params = None):
        '''
        Constructor
        '''
        super().__init__(params)
        
    def Ripristina(self):
        self.mazz.clear()
        for s in carta:
            self.mazz.insert(0, s)