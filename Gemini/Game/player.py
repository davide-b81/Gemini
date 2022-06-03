'''
Created on 31 dic 2021

@author: david
'''
import json
from json import JSONDecoder

from c14n.Canonicalize import JSONEncoder

from main.globals import ComplexEncoder
from oggetti.posizioni import *

class Player(object):
    # Cards enum id
    _position = None
    _name = None
    _punti_mano = None
    _punti_partite = None
    _caduto = None
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
            self.reset()
            self._simulated = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_position(self, ppos):
        try:
            self._position = ppos
            if ppos is not None:
                print(str(self) + " => " + ppos)
            else:
                print(str(self) + " reset posizione")
            if ppos == POSTAZIONE_SUD:
                self._simulated = False
            else:
                self._simulated = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position(self):
        try:
            return self._position
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_simulated(self):
        return self._simulated

    def set_simulated(self, act=True):
        self._simulated = act

    def get_label(self):
        try:
            s = self._name
            if self._punti_mano is not None:
                s = s + " - " + str(self._punti_mano)
            return s
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_caduto(self):
        return self._caduto

    def set_caduto(self, act):
        self._caduto = act

    def giocatore_cade(self):
        try:
            if self._caduto == False:
                self._caduto = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def segna_punti(self, pts):
        try:
            print(str(self) + " marca " + str(pts))
            self._punti_mano = self._punti_mano + pts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_punti_partite(self, pts):
        self._punti_partite = pts

    def get_punti_partite(self):
        return self._punti_partite

    def set_punti_mano(self, pts):
        self._punti_mano = pts

    def get_punti_mano(self):
        return self._punti_mano

    def get_resti(self):
        return self._resti

    def add_resti(self, n):
        try:
            self._resti = self._resti + n
            return self._resti
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_fine_mano(self):
        try:
            self._punti_partite = self._punti_partite + self._punti_mano
            self._caduto = False
            self._punti_mano = 0
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_fine_giro(self):
        try:
            self.reset_all()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        try:
            self._caduto = False
            self._punti_mano = 0
            self._punti_partite = 0
            self._resti = 0
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __str__(self):
        try:
            return self._name
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __eq__(self, other):
        try:
            if (other):
                return str(self) == str(other)
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __dict__(self):
        return dict(_id_player=str(self._name),
                    _position=self._position,
                    _punti_mano=self._punti_mano,
                    _punti_partite=self._punti_partite,
                    _caduto=self._caduto,
                    _simulated=self._simulated)

    def reprJSON(self):
        return self.__dict__()

    @staticmethod
    def fromJSON(json_object):
        try:
            _id_player = json_object['_id_player']
            _position = json_object['_position']
            _punti_mano = json_object['_punti_mano']
            _punti_partite = json_object['_punti_partite']
            _caduto = json_object['_caduto']
            _simulated = json_object['_simulated']
            p = Player(_id_player)
            p.set_position(_position)
            p.set_punti_mano(_punti_mano)
            p.set_punti_partite(_punti_partite)
            p.set_caduto(_caduto)
            p.set_simulated(_simulated)
            return p
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


if __name__ == '__main__':
    c = Player("XXXX")
    c.set_punti_partite(18)
    c.set_position(POSTAZIONE_EST)
    cc = json.dumps(c.reprJSON(), cls=ComplexEncoder)
    print(cc)
    f = JSONDecoder(object_hook=Player.fromJSON).decode(cc)