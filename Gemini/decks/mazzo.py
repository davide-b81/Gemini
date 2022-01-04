'''
Created on 31 dic 2021

@author: david
'''
import Logic.Carta
from Logic.Carta import carta
import random

class Mazzo(object):
    
    mazz = []
    
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        self.Ripristina()
    
    def PrintMaz(self):
        for s in self.mazz:
            print(s.name)

    def Shuffle(self):
        random.shuffle(self.mazz)
    
    def Estrai(self):
        try:
            if (len(self.mazz) > 0):
                return self.mazz.pop()
        except Exception as e:
            print("Estrai: An error occurred:", e.args[0])
        return None
    
    def Ripristina(self):
        pass
    
    '''
    Legge l'ultima carta senza estrarla
    '''
    def GetLast(self):
        try:
            return self.mazz[-1]
        except Exception as e:
            print("GetLast: An error occurred:", e.args[0])
        return None