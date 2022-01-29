'''
Created on 31 dic 2021

@author: david
'''

import random

from main.exception_man import ExceptionMan
from main.globals import *


class Mazzo(object):

    _carte = None
    _pos = None

    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        try:
            self._carte = []
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def mescola(self):
        try:
            random.shuffle(self._carte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def pesca(self):
        try:
            if (len(self._carte) > 0):
                return self._carte.pop()
        except Exception as e:
            echo_message("Estrai: An error occurred:", e.args[0])
        return None


    def set_visible(self, b = True):
        try:
            self.v = b
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def ripristina(self):
        try:
            self._carte.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def inserisci(self, c):
        try:
            self._carte.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    '''
    Legge l'ultima carta senza estrarla
    '''
    def get_last(self):
        try:
            return self._carte[-1]
        except Exception as e:
            echo_message("get_last: An error occurred:", e.args[0])
        return None
