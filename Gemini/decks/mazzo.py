'''
Created on 31 dic 2021

@author: david
'''
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
        self.ripristina()
    
    def PrintMaz(self):
        for s in self.mazz:
            print(s.name)

    def     mescola(self):
        self.ripristina()
        random.shuffle(self.mazz)
    
    def pesca(self):
        try:
            if (len(self.mazz) > 0):
                return self.mazz.pop()
        except Exception as e:
            print("Estrai: An error occurred:", e.args[0])
        return None
    
    def ripristina(self):
        self.mazz.clear()
    
    '''
    Legge l'ultima carta senza estrarla
    '''
    def get_last(self):
        try:
            return self.mazz[-1]
        except Exception as e:
            print("get_last: An error occurred:", e.args[0])
        return None

    