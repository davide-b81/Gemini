'''
Created on 31 dic 2021

@author: david
'''
from decks.carta_id import *
from game.germini.punteggi import Versicole, punti_ger
from main.globals import *
from main.exception_man import ExceptionMan

class Player(object):
    # Cards enum id
    cards = None
    cards_mano = None
    cards_mostra = None
    score = None
    _position = None
    _name = None
    versicole = None
    _punti_mano = None
    _punti_totali = None
    _caduto = None
    _delegate_sort = None
    _delegate_dichiara = None
    _delegate_append_html_text = None

    '''
    classdocs
    '''

    def __init__(self, name, pos=None):
        try:
            '''
            Constructor
            '''
            self._name = name
            self._position = pos
            self.cards = []
            self.cards_mano = []
            self.cards_mangiate = []
            self.versicole = Versicole(name)
            self._punti_mano = 0
            self._punti_totali = 0
            self._caduto = False
            self.versicole.set_delegate_on_dichiara(self.on_versicola)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_dichiara(self, foo):
        self._delegate_dichiara = foo

    def set_delegate_sort(self, foo):
        self._delegate_sort = foo

    def set_delegate_append_html_text(self, foo):
        self._delegate_append_html_text = foo

    def get_position(self):
        try:
            return self._position
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_label(self):
        try:
            s = self._name
            if (self._punti_mano is not None):
                s = s + " - " + str(self._punti_mano)
            return s
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_carta(self, c):
        try:
            self.cards.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_mano(self):
        try:
            # self.cards_mano.sort()
            self._delegate_sort(self)
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def assegna_carta(self, c, fronte=False):
        try:
            if c is None:
                raise Exception("Carta non specificata")
            self.cards_mano.append(c)
            if fronte:
                echo_message("\t - " + str(c) + " scoperta")
            else:
                echo_message("\t - " + str(c))
            self.update_mano()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def dichiara(self):
        try:
            self.versicole.gestisci_carte(self.cards_mano)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_versicola(self, txt):
        try:
            self._delegate_dichiara(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_caduto(self):
        try:
            return self._caduto
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_caduto(self):
        try:
            for c in self.cards_mano:
                if c.get_id() in tarocco:
                    self._caduto = False
                    return self._caduto

            for c in self.cards_mano:
                if c.get_id() in punti_ger:
                    self._caduto = False
                    return self._caduto

            self._caduto = True
            return self._caduto

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def giocatore_cade(self):
        try:
            if self._caduto == False:
                echo_message(self._name + " cade.")
                self._caduto = True
            return self._caduto
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_giocatore(self):
        try:
            self.cards.clear()
            self.cards_mano.clear()
            self._punti_mano = 0
            self._caduto = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mangia_carta(self, c, pts):
        try:
            if c is not None:
                self.cards_mangiate.append(c)
                self._punti_mano = self._punti_mano + pts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def somma_punti(self, pts):
        self._punti_mano = self._punti_mano + pts
        return self._punti_mano

    def get_punti_mano(self):
        return self._punti_mano

    def get_punti_totale(self):
        return self._punti_totali

    def on_fine_mano(self):
        self._punti_totali = self._punti_totali + self._punti_mano
        return self._punti_totali

    def get_num_cartemano(self):
        try:
            return len(self.cards_mano)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cala_carta(self, carta):
        try:
            if carta in self.cards_mano:
                self.cards_mano.remove(carta)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carta(self, carta):
        try:
            if (carta in self.cards):
                self.cards.remove(carta)
                return carta
            else:
                raise Exception("Carta non trovata!")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def get_carte_mano(self):
        try:
            return self.cards_mano
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_mangiate(self):
        try:
            return self.cards_mangiate
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte(self):
        try:
            return self.cards
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_carta(self, cid):
        try:
            for c in self.cards_mano:
                if cid == c.get_id():
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_seme(self, seed):
        try:
            for c in self.cards_mano:
                if get_seme(c.get_id()) == seed:
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return False

    def __str__(self):
        return self._name
