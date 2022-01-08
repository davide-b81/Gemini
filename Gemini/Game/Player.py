'''
Created on 31 dic 2021

@author: david
'''
import oggetti.posizioni
from oggetti.stringhe import Stringhe, _

class Giocatore(object):
    # Cards enum id
    cards = None
    cards_mano = None
    cards_mostra = None
    score = None
    position = None
    name = None
    
    '''
    classdocs
    '''
    def __init__(self, name, pos = None):
        '''
        Constructor
        '''
        self.name = name
        self.position = pos
        self.cards = []
        self.cards_mano = []
        self.cards_mostra = []
    
    def set_posizione(self, pos):
        self.position = pos
    
    def get_posizione(self):
        return self.position
    
    def get_nome(self):
        return self.name
        
    def add_carta(self, c):
        self.cards.append(c)
    
    def assegna_carte(self, cc):
        for c in cc:
            self.cards_mano.append(c)
            print(self.name + " (" + self.position + ")" + _(" riceve ") + str(c))

    def restore_giocatore(self):
        self.cards.clear()
        self.cards_mano.clear()

    def mostra_carta(self):
        return self.cards_mostra[0]

    def cala_carta(self):
        if len(self.cards) >= 1:
            return self.cards.pop(0)
        else:
            raise Exception("Giocatore.cala_carta: Nessuna carta presente per " + self.name)
                
    def get_carta(self, carta):
        if (carta in self.cards):
            self.cards.remove(carta)
            return carta
        else:
            print("cala_carta: Carta " + carta + " non trovata!")
            return None

    def get_carte_mano(self):
        return self.cards_mano

    def get_carte_mostra(self):
        return self.cards_mostra

    def get_carte(self):
        return self.cards