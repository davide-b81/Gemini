'''
Created on 5 gen 2022

@author: david
'''
from main.globals import *
from main.exception_man import ExceptionMan

class TavolaPosizione(object):
    '''
    classdocs
    '''
    giocatore = None
    carte_tavola = None
    carte_mostrate = None
    carte_mano = None
    
    def __init__(self, giocatore):
        '''
        Constructor
        '''
        self.giocatore = giocatore
        self.carte_tavola = []
        self.carte_mostrate = []
        self.carte_mano = []

    def get_nome_giocatore(self):
        return self.giocatore._name

    def get_carte_tavola(self):
        return self.carte_tavola

    def get_carte_mostrate(self):
        return self.carte_mostrate

    def show_carta(self, c):
        try:
            pass
            #echo_message("Mostra " +  str(c) + " in " + self.giocatore.get_position())
            #self.carte_mostrate.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_carta(self, c):
        try:
            self.carte_mostrate.clear()
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        try:
            self.carte_mano.clear()
            self.carte_mostrate.clear()
            self.carte_tavola.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
