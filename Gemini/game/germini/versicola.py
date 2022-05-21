#   '''
#  Created on 20 3 2022
#  @author: david
#  '''
from copy import copy
from importlib.resources import _
from main.globals import *
from game.player import Player
from game.germini.punteggi import punti_vers, carte_conto
from decks.carta import CartaId, Carta
from main.exception_man import ExceptionMan

VERSICOLA_REGOLARE_ID = "VERSICOLE_REGOLARI_ID"
VERSICOLA_RE_ID = "VERSICOLA_RE_ID"
VERSICOLA_PAPI_ID = "VERSICOLA_PAPI_ID"
VERSICOLA_MATTO_ID = "VERSICOLA_MATTO_ID"
VERSICOLA_DIECINE_ID = "VERSICOLA_DIECINE_ID"
VERSICOLA_TREDICI_ID = "VERSICOLA_TREDICI_ID"
VERSICOLA_DEL29_ID = "VERSICOLA_DEL29_ID"
VERSICOLA_CARNE_ID = "VERSICOLA_CARNE_ID"

class Versicola(object):
    _id = None
    _cardset = None
    _owned = None
    _versicole = None
    _matto = None
    _delegate_nuova = None

    def __init__(self, id, ca_set):
        self._cardset = ca_set
        self._owned = []
        self._id = id
        self._versicole = []
        self._matto = False

    def set_delegate_nuova(self, f):
        assert f is not None
        self._delegate_nuova = f

    def get_id(self):
        return self._id

    def clear(self):
        try:
            self._owned.clear()
            self._versicole.clear()
            self._matto = False
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def count(self, cid):
        return self._owned.count(cid)

    def remove_cid(self, cid):
        try:
            if cid in self._cardset and self._owned.count(cid) == 1:
                self._owned.remove(cid)
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def append_cid(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def insert_cid(self, cid):
        try:
            if cid in self._cardset and self._owned.count(cid) == 0:
                print(self.__name__() + " append " + str(cid))
                self._owned.append(cid)
            elif cid == CartaId.MATTO_0:
                if CartaId.MATTO_0 not in self._cardset:
                    self._matto = True
                    print("Add " + str(cid) + " to " + str(self))
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def get_lista(self):
        return self._versicole

    def set_versicola_sub(self, v):
        self._delegate_nuova(v, self._id)
        self._versicole.append(copy(v))

    def set_versicole(self):
        try:
            first = None
            secon = None
            v = []

            for cid in self._cardset:
                if cid in self._owned:
                    if first is None:
                        first = cid
                        v.append(cid)
                    elif secon is None:
                        if self._cardset.index(cid) == self._cardset.index(first) + 1:
                            secon = cid
                            v.append(cid)
                        elif self._id == VERSICOLA_RE_ID:
                            secon = cid
                            v.append(cid)
                        else:
                            first = cid
                            secon = None
                            v.clear()
                            v.append(cid)
                    elif cid.value == v[-1].value + 1:
                        v.append(cid)
                    elif self._id == VERSICOLA_RE_ID:
                        v.append(cid)
                    else:
                        if len(v) > 2:
                            v.sort()
                            self._owned.append(v)
                            self.set_versicola_sub(v)
                            first = cid
                            secon = None
                            v.clear()
                            v.append(cid)
                else:
                    if len(v) > 2:
                        v.sort()
                        self._owned.append(v)
                        if self._matto:
                            self._owned.append(CartaId.MATTO_0)
                        self.set_versicola_sub(v)
                        first = None
                        secon = None
                        v.clear()

            if len(v) > 2:
                v.sort()
                self._owned.append(v)
                self.set_versicola_sub(v)
            v.clear()

        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def get_declaration(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def __name__(self):
        try:
            if self._id == VERSICOLA_RE_ID:
                return _("Versicola di Re")
            elif self._id == VERSICOLA_PAPI_ID:
                return _("Versicola dei Papi")
            elif self._id == VERSICOLA_MATTO_ID:
                return _("Versicola del Matto")
            elif self._id == VERSICOLA_DIECINE_ID:
                return _("Versicola delle Diecine")
            elif self._id == VERSICOLA_TREDICI_ID:
                return _("Versicola del tredici")
            elif self._id == VERSICOLA_CARNE_ID:
                return _("Versicola Demonio, Mondo, Carne")
            elif self._id == VERSICOLA_REGOLARE_ID:
                return _("Versicola regolare")
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def punti(llista):
        try:
            punti = 0
            if len(llista) >= 3:
                for cid in llista:
                    punti = punti + punti_vers[cid]
            return punti
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def __str__(self):
        return self.__name__()

