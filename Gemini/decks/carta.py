'''
Created on 31 dic 2021

@author: david
'''
#   '''
#  Created on 25 1 2022
#  @author: david
#  '''
import json
from json import JSONEncoder, JSONDecoder

import dill as dill

from decks.carta_id import *
from oggetti.posizioni import POSTAZIONE_NORD, POSTAZIONE_SUD, POSTAZIONE_OVEST, POSTAZIONE_EST
from main.globals import FRONTE_COPERTA, Globals, FRONTE_SCOPERTA, DEG_CLOC_RECT, \
    DEG_FLIP, DEG_ANTC_RECT, DEG_NORMAL, ComplexEncoder


class Carta(object):
    _id = None
    _coperta = None
    _sprite = None
    #_globals = None

    def __init__(self, id):
        '''
        Constructor
        '''
        try:
            #self._globals = Globals()
            self._id = id
            self._coperta = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_sprite(self, s):
        self._sprite = s

    def get_coperta(self):
        return not self._sprite.is_front()

    def set_coperta(self, coperta=FRONTE_COPERTA, inst=True):
        try:
            g = Globals()
            if g.get_uncover(): #self._globals.get_uncover():
                self._coperta = False
            else:
                self._coperta = coperta
            if self._sprite is not None:
                self._sprite.set_lato(coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sprite(self, z):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_z(self, z):
        try:
            #if z == 0:
            #    print("NULL z")
            #else:
            #    print(str(self) + " set z = " + str(z))
            self._sprite.set_z(z)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_hoverable(self, enable=True):
        try:
            if self._sprite is not None:
                self._sprite.enable_hoover(enable)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_deg_from_ppos(self, ppos, instant=True):
        try:
            if ppos == POSTAZIONE_NORD:
                self.set_angle(DEG_FLIP, instant)
            elif ppos == POSTAZIONE_OVEST:
                self.set_angle(DEG_CLOC_RECT, instant)
            elif ppos == POSTAZIONE_EST:
                self.set_angle(DEG_ANTC_RECT, instant)
            elif ppos == POSTAZIONE_SUD:
                self.set_angle(DEG_NORMAL, instant)
            else:
                c.set_angle(DEG_NORMAL, instant)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_pos(self, pos, instant=True):
        try:
            #print(str(self) + " set pos (" + str(pos[0]) + ","  + str(pos[1]) + ")")
            self._sprite.set_position(pos, instant)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_angle(self, deg, inst):
        try:
            self._sprite.set_angolo(deg, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, enable=True):
        try:
            #print(str(self) + " set visible " + str(enable))
            self._sprite.set_visible(enable)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_seme(self):
        try:
            return get_seme(self._id)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_numerale(self):
        try:
            return get_numerale(self._id)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_tarocco(self):
        try:
            return is_tarocco(self._id)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_name(self):
        return str(self._id)

    def get_id(self):
        assert self._id is not None
        return self._id

    def get_short_name(self):
        return get_short_name(self._id)

    def __name__(self):
        return get_card_name(self._id)

    def __str__(self):
        return get_card_name(self._id)

    def __gt__(self, other):
        try:
            if (self.is_tarocco()):
                if other.is_tarocco():
                    return self.get_numerale() > other.get_numerale()
                else:
                    return True
            else:
                if other.is_tarocco():
                    return False
                elif self.get_seme() != other.get_seme():
                    return True
                else:
                    return self.get_numerale() > other.get_numerale()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __lt__(self, other):
        if (other):
            return not self.__gt__(other) and self._id != other._id
        else:
            return False

    def __le__(self, other):
        if (other):
            return not self.__gt__(other)
        else:
            return False

    def __eq__(self, other):
        if (other):
            return self._id == other._id
        else:
            return False

    def __ne__(self, other):
        if (other):
            return self._id != other._id
        else:
            return True

    def __ge__(self, other):
        if (other):
            return self.__gt__(other) or self._id == other._id
        else:
            return False

    def __dict__(self):
        return dict(_id_carta=str(self._id), _coperta=str(self._coperta))

    def reprJSON(self):
        return self.__dict__()

    @staticmethod
    def fromJSON(json_object):
        try:
            if '_id_carta' in json_object:
                id = json_object['_id_carta']
                c = Carta(CartaId[id])
                return c
            else:
                return json_object
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


if __name__ == '__main__':
    c = Carta(CartaId.SPADE_R)
    #cc = CartaEncoder().encode(c)
    cc = json.dumps(c.reprJSON(), cls=ComplexEncoder)
    log_file = open("pippo.json", "w", encoding="utf8")
    log_file.write(cc)
    log_file.close()

    f = JSONDecoder(object_hook=Carta.fromJSON).decode(cc)