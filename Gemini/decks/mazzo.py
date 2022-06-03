#   '''
#  Created on 30 4 2022
#  @author: david
#  '''
import json
import random
from io import StringIO
from json import JSONEncoder, JSONDecoder

import decks
import main.globals
from decks.carta_id import Qualita, CartaId
from game.germini.punteggi import carte_conto
from main.exception_man import ExceptionMan


class Mazzo(object):
    _id = None
    _list = None
    _mazzo_coperto = None

    def __init__(self, nome=""):
        try:
            self._list = []
            self._id = nome
            self._mazzo_coperto = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __name__(self):
        try:
            return self._id
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def __str__(self):
        try:
            s =  self.__name__() + " - " + str(len(self._list))
            for c in self._list:
                s = s + "\n- " + str(c)
            return s
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    """
    >> 
    """
    def __rshift__(self, other):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    """
    <<
    """
    def __lshift__(self, other):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    """
    deck1 <<= deck2
    Sposta le carte da 2 a 1
    """
    def __ilshift__(self, other):
        try:
            self.append_carte(other.get_carte())
            other.flush_carte()
            self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    """
    deck1 >>= deck2
    Sposta le carte da 1 a 2
    """
    def __irshift__(self, other):
        try:
            other.append_carte(self._list)
            self.flush_carte()
            other.update()
            return other
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __add__(self, other):
        try:
            return self._list.append(other.get_carte())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __iter__(self):
        try:
            self._i = 0
            return self
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __next__(self):
        try:
            if self._i < len(self._list):
                ret = self._list[self._i]
                self._i += 1
                return ret
            else:
                raise StopIteration
        except Exception as e:
            if not isinstance(e, StopIteration):
                ExceptionMan.manage_exception("", e, True)
            else:
                raise ExceptionMan.manage_exception("", e, True)

    def __len__(self):
        try:
            return len(self._list)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __getitem__(self, subscript):
        try:
            return self._list[subscript]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __setitem__(self, subscript, item):
        try:
            self._list[subscript] = item
            #item.set_coperta(not self._mazzo_coperto)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __delitem__(self, subscript):
        try:
            self._list.pop(subscript)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __contains__(self, c):
        """ operator 'in' """
        return c in self._list

    def update(self):
        try:
            for c in self._list:
                pass
                #c.set_coperta(not self._mazzo_coperto)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
    """
    def __getslice__(selfself):
        try:
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
    def __setslice__(selfself):
        try:
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
    def __delslice__(selfself):
        try:
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
    """

    def taglia(self, n):
        try:
            lista = []
            i = 0
            while i < len(self._list) and i < n:
                c = self._list.pop(0)
                lista.append(c)
            return lista
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_id(self):
        return self._id

    def get_carte(self):
        try:
            return self._list
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carta(self, i):
        try:
            if len(self._list) != 0:
                return self._list[i]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def count(self, c):
        return self._list.count(c)

    def remove(self, c):
        try:
            if self.count(c) > 0:
                self._list.remove(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop(self, i=0):
        try:
            assert self._list is not None
            return self._list.pop(i)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def append(self, c):
        try:
            self.reset_attributes_carta(c)
            self._list.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def insert(self, c, i=0):
        try:
            self.reset_attributes_carta(c)
            self._list.insert(i, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_attributes_lista(self, ca):
        """ Quando la carta passa ad un altro mazzo """
        try:
            for c in ca:
                self.reset_attributes_carta(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_attributes_carta(self, c):
        """ Quando la carta passa ad un altro mazzo """
        try:
            c.set_hoverable(False)
            if self._mazzo_coperto:
                c.set_coperta(main.globals.FRONTE_COPERTA)
            else:
                c.set_coperta(main.globals.FRONTE_SCOPERTA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def append_carte(self, ca):
        try:
            self.reset_attributes_lista(ca)
            self._list.extend(ca)
            self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def flush_carte(self):
        try:
            self._list.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_fronte(self):
        try:
            if self._mazzo_coperto:
                self._list.reverse()
                self._mazzo_coperto = False
                self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_dorso(self):
        try:
            if not self._mazzo_coperto:
                self._list.reverse()
                self._mazzo_coperto = True
                self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, enable=True):
        try:
            for c in self._list:
                c.set_visible(enable)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola(self):
        try:
            i = 0
            assert self._list is not None
            random.shuffle(self._list)
            self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_coperto(self):
        return self._mazzo_coperto

    def is_scoperto(self):
        return not self._mazzo_coperto

    def print_carte(self):
        try:
            print("Mazzo " + str(self) + ":")
            for c in self._list:
                print("    - " + str(c))
        except Exception as e:
            print("Error printing mazzo")

    def pop_carta(self, qual):
        try:
            cret = None
            if qual == Qualita.CARTA_DICONTO:
                for c in self._list:
                    if c.get_id() in carte_conto:
                        cret = c
                        self._list.remove(c)
                        break
            elif qual == Qualita. CARTA_CONTO_0:
                for c in self._list:
                    if c.get_id() not in carte_conto:
                        cret = c
                        self._list.remove(c)
                        break
            return cret
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __dict__(self):
        return dict(_id_deck=self._id, _list=[ob for ob in self._list])

    def reprJSON(self):
        return dict(_id_deck=self._id, _list=[ob for ob in self._list])

    def fromJSON(self, json_object):
        try:
            if '_id_carta' in json_object.keys():
                # Se è una sotto struttura uso il relativo tipo
                c = decks.carta.Carta.fromJSON(json_object)
                self._list.insert(-1, c)
            elif '_id_deck' in json_object.keys():
                _id = json_object['_id_deck']
                _list = json_object['_list']
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


if __name__ == '__main__':
    """ Main program cycle """
    mm = Mazzo("MIO")
    from decks.carta import Carta

    mm.insert(Carta(CartaId.COPPE_R))
    mm.insert(Carta(CartaId.BASTO_R))
    try:
        cc = json.dumps(mm.reprJSON(), cls=main.globals.ComplexEncoder)
        print(cc)
        f = JSONDecoder(object_hook=Mazzo.fromJSON).decode(cc)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)