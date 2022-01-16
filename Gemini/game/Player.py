'''
Created on 31 dic 2021

@author: david
'''
import oggetti.posizioni
from oggetti.stringhe import Stringhe, _
from main.exception_man import ExceptionMan
from game.germini.punteggi import Versicole, punti_ger


class Giocatore(object):
    # Cards enum id
    cards = None
    cards_mano = None
    cards_mostra = None
    score = None
    position = None
    name = None
    versicole = None
    punti_mano = None
    punti_totali = None

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
        self.cards_mangiate = []
        self.versicole = Versicole(name)
        self.punti_mano = 0
        self.punti_totali = 0
    
    def set_posizione(self, pos):
        self.position = pos
    
    def get_posizione(self):
        return self.position
    
    def get_label(self):
        s = self.name
        if (self.punti_mano != None):
            s = s + " - " + str(self.punti_mano)
        return s
        
    def add_carta(self, c):
        self.cards.append(c)
    
    def assegna_carte(self, cc):
        for c in cc:
            self.cards_mano.append(c)
            print(self.name + " (" + self.position + ")" + _(" riceve ") + str(c))
        self.cards_mano.sort()

    def dichiara(self):
        try:
            self.versicole.gestisci_carte(self.cards_mano)
        except Exception as e:
            ExceptionMan.manage_exception("Error managing versicolae", e, True)

    def restore_giocatore(self):
        self.cards.clear()
        self.cards_mano.clear()
        self.punti_mano = 0

    def mangia_carta(self, c):
        try:
            if c != None:
                self.cards_mangiate.append(c)
                if c.get_id() in punti_ger:
                    self.punti_mano = self.punti_mano + punti_ger[c.get_id()]
                # TODO: Se ultima presa 10 punti
        except Exception as e:
            ExceptionMan.manage_exception("Error.", e, True)

    def get_num_cartemano(self):
        try:
            return len(self.cards_mano)
        except Exception as e:
            ExceptionMan.manage_exception("get_num_cartemano. Error managing events", e, True)

    def cala_carta(self, cid):
        try:
            for c in self.cards_mano:
                if (cid == c.get_id()):
                    print(str(self.name) + " cala " + str(cid))
                    self.cards_mano.remove(c)
                    return c
        except Exception as e:
            ExceptionMan.manage_exception("cala_carta. Error managing events", e, True)
        return None

    def cala_prima_carta(self):
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

    def get_carte_mangiate(self):
        return self.cards_mangiate

    def get_carte(self):
        return self.cards

    def has_carta(self, cid):
        try:
            for c in self.cards_mano:
                if (cid == c.get_id()):
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("Error managing events", e, True)

    def __str__(self):
        return self.name