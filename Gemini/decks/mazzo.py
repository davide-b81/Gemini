'''
Created on 31 dic 2021

@author: david
'''
import random

class Mazzo(object):

    carte = []

    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.ripristina()

    def mescola(self):
        self.ripristina()
        random.shuffle(self.carte)
    
    def pesca(self):
        try:
            if (len(self.carte) > 0):
                return self.carte.pop()
        except Exception as e:
            print("Estrai: An error occurred:", e.args[0])
        return None
    
    def ripristina(self):
        self.carte.clear()
    
    '''
    Legge l'ultima carta senza estrarla
    '''
    def get_last(self):
        try:
            return self.carte[-1]
        except Exception as e:
            print("get_last: An error occurred:", e.args[0])
        return None
