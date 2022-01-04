'''
Created on 31 dic 2021

@author: david
'''

class Giocatore(object):
    cards = []
    score = 0
    position = ""
    
    name = ""
    mazziere = False
    '''
    classdocs
    '''

    def __init__(self, name, pos = None):
        '''
        Constructor
        '''
        self.name = name
        self.position = pos
    
    def SetPosition(self, pos):
        self.position = pos
    
    def GetPosition(self):
        return self.position
    
    def GetName(self):
        return self.name
        
    def GiveCard(self, c):
        self.cards.append(c)
    
    def RitiraCarte(self):
        self.cards.clear()
    
    def GetCardList(self):
        return self.cards
    