'''
Created on 31 dic 2021

@author: david
'''
import numpy
from main.globals import *
from decks.carta_id import *
from game.germini.punteggi import carte_conto
from main.exception_man import ExceptionMan

class Player(object):
    # Cards enum id
    _cards = None
    _cards_mangiate = None
    _n_da_scartare = None
    _position = None
    _name = None
    _punti_mano = None
    _punti_partite = None
    _caduto = None
    _delegate_sort = None
    _delegate_dichiara = None
    _delegate_scopri = None
    _delegate_on_punti = None
    _delegate_append_html_text = None
    _simulated = None

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
            self._cards_mangiate = []
            self._punti_mano = 0
            self._punti_partite = 0
            self._resti = 0
            self._n_da_scartare = 0
            self._caduto = False
            self._simulated = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_scopri(self, f):
        self._delegate_scopri = f

    def set_delegate_dichiara(self, foo):
        self._delegate_dichiara = foo

    def set_delegate_sort(self, foo):
        self._delegate_sort = foo

    def set_delegate_append_html_text(self, foo):
        self._delegate_append_html_text = foo

    def set_delegate_on_punti(self, f):
        self._delegate_on_punti = f

    def set_position(self, ppos):
        try:
            self._position = ppos
            if ppos is not None:
                print(str(self) + " => " + ppos)
            else:
                print(str(self) + " reset posizione")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position(self):
        try:
            return self._position
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_simulated(self):
        try:
            return self._simulated
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_real(self, real=True):
        try:
            self._simulated = not real
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_label(self):
        try:
            s = self._name
            if self._punti_mano is not None:
                s = s + " - " + str(self._punti_mano)
            return s
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

    def giocatore_cade(self):
        try:
            if self._caduto == False:
                self._caduto = True
            return self._caduto
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_giocatore(self):
        try:
            self._punti_mano = 0
            self._caduto = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def segna_punti(self, pts):
        try:
            print(str(self) + " marca " + str(pts))
            self._punti_mano = self._punti_mano + pts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mangia_carta(self, c, pts):
        try:
            if c is not None:
                self._cards_mangiate.append(c)
                self._punti_mano = self._punti_mano + pts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_punti_mano(self):
        return self._punti_mano

    def get_punti_partite(self):
        return self._punti_partite

    def get_resti(self):
        return self._resti

    def on_fine_mano(self):
        self._punti_partite = self._punti_partite + self._punti_mano
        self._punti_mano = 0
        return self._punti_partite

    def on_fine_giro(self):
        self._punti_partite = 0

    def on_cade(self):
            pass

    def get_carte_mangiate(self):
        try:
            return self._cards_mangiate
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_all(self):
        try:
            self.reset()
            self._punti_partite = 0
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        try:
            self._cards_mangiate.clear()
            self._caduto = False
            self._punti_mano = 0
            self._n_da_scartare = 0
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if (other):
            return str(self) == str(other)
        return False

