#   '''
#  Created on 11 3 2022
#  @author: david
#  '''

from importlib.resources import _

from game.germini.versicola import Versicola
from decks.carta import CartaId, Carta
from main.exception_man import ExceptionMan
from decks.carta_id import get_card_name

VERSICOLA_REGOLARE_ID = "VERSICOLA_REGOLARI_ID"
VERSICOLA_RE_ID = "VERSICOLA_RE_ID"
VERSICOLA_PAPI_ID = "VERSICOLA_PAPI_ID"
VERSICOLA_MATTO_ID = "VERSICOLA_MATTO_ID"
VERSICOLA_DIECINE_ID = "VERSICOLA_DIECINE_ID"
VERSICOLA_TREDICI_ID = "VERSICOLA_TREDICI_ID"
VERSICOLA_DEL29_ID = "VERSICOLA_DEL29_ID"
VERSICOLA_CARNE_ID = "VERSICOLA_CARNE_ID"

definizione = {}
definizione[VERSICOLA_REGOLARE_ID] = [CartaId.PAPA_I, CartaId.CARRO_X, CartaId.MORTE_XIII, CartaId.FUOCO_XX,\
                                      CartaId.CAPRIC_XXVIII, CartaId.SAGITT_XXIX, CartaId.CANCRO_XXX,\
                                      CartaId.PESCI_XXXI, CartaId.ACQUARIO_XXXII, CartaId.LEONE_XXXIII,\
                                      CartaId.TORO_XXXIV, CartaId.GEMINI_XXXV, CartaId.STELLA_XXXVI,\
                                      CartaId.LUNA_XXXVII, CartaId.SOLE_XXXVIII, CartaId.MONDO_XXXIX, CartaId.TROMBA_XL]
definizione[VERSICOLA_RE_ID] = [CartaId.BASTO_R, CartaId.COPPE_R, CartaId.DANAR_R, CartaId.SPADE_R]
definizione[VERSICOLA_PAPI_ID] = [CartaId.PAPA_I, CartaId.PAPA_II, CartaId.PAPA_III, CartaId.PAPA_IV, CartaId.PAPA_V]
definizione[VERSICOLA_MATTO_ID] = [CartaId.PAPA_I, CartaId.MATTO_0, CartaId.TROMBA_XL]
definizione[VERSICOLA_DIECINE_ID] = [CartaId.CARRO_X, CartaId.FUOCO_XX, CartaId.CANCRO_XXX, CartaId.TROMBA_XL]
definizione[VERSICOLA_TREDICI_ID] = [CartaId.PAPA_I, CartaId.MORTE_XIII, CartaId.CAPRIC_XXVIII]
definizione[VERSICOLA_CARNE_ID] = [CartaId.DIAVOLO_XIV, CartaId.MONDO_XXXIX, CartaId.GEMINI_XXXV]

class VersicoleManager(object):
    _o = None
    _pos = None
    _delegate_on_dichiara = None
    _delegate_on_punti = None

    def __init__(self, ppos):
        try:
            self._pos = ppos
            self._o = []
            self._delegate_on_dichiara = None
            self._delegate_on_punti = None
            self._delegate_on_allunga = None
            self._o.append(Versicola(VERSICOLA_RE_ID, definizione[VERSICOLA_RE_ID], ppos))
            self._o.append(Versicola(VERSICOLA_PAPI_ID, definizione[VERSICOLA_PAPI_ID], ppos))
            self._o.append(Versicola(VERSICOLA_MATTO_ID, definizione[VERSICOLA_MATTO_ID], ppos))
            self._o.append(Versicola(VERSICOLA_DIECINE_ID, definizione[VERSICOLA_DIECINE_ID], ppos))
            self._o.append(Versicola(VERSICOLA_TREDICI_ID, definizione[VERSICOLA_TREDICI_ID], ppos))
            self._o.append(Versicola(VERSICOLA_CARNE_ID, definizione[VERSICOLA_CARNE_ID], ppos))
            self._o.append(Versicola(VERSICOLA_REGOLARE_ID, definizione[VERSICOLA_REGOLARE_ID], ppos))

            for o in self._o:
                o.set_delegate_nuova(dichiara)
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def set_delegate_on_dichiara(self, f):
        self._delegate_on_dichiara = f

    def set_delegate_on_punti(self, f):
        self._delegate_on_punti = f

    @property
    def pos(self):
        return self._pos

    def reset(self):
        try:
            for o in self._o:
                o.restore()
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def riempi(self, ca):
        try:
            for d in self._o:
                for c in ca:
                    d.insert_cid(c.get_id())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_points(self, v):
        try:
            pts = 0
            for o in self._o:
                if v in self._own:
                    pts = pts + o.punti()

            return pts
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def gestisci_carte(self, ca):
        try:
            for o in self._o:
                for c in ca:
                    o.insert_cid(c.get_id())
            self.evaluate_versicole()
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def on_perdita(self, ca):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def on_distribuzione(self, ca):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def versicola(self, ca, vers):
        vers_set = set(vers)
        intersection = vers_set.intersection(ca)

    def is_valid(self, ca, vers, id):
        try:
            if ca.intersect(vers).count() >= 3:
                return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def on_presa(self, ca):
        """ Carte aggiunte """
        global definizione
        try:
            for c in ca:
                for v in self._own:
                    if v == VERSICOLA_REGOLARE_ID:
                        pass
                    else:
                        if len(self._own[v]) > 0:
                            if self.allunga_versicola(self._own[v], c):
                                pass
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def allunga_versicola(self, v, c):
        global definizione
        try:
            for o in self._o:
                o.set_versicole()
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def evaluate_versicole(self):
        try:
            for o in self._o:
                o.set_versicole()
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def get_lista_versicole(self, o):
        try:
            l = []
            a = o.get_lista()
            if len(a) > 0:
                for aa in a:
                    l.append(aa)
            return l
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def get_punti_totali(self):
        n = 0
        try:
            for o in self._o:
                lv = self.get_lista_versicole(o)
                for l in lv:
                    n = n + Versicola.punti(l)
            return n
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def get_txt_description(self):
        try:
            txt = ""
            for o in self._o:
                lv = self.get_lista_versicole(o)
                if len(lv) > 0:
                    txt = txt + str(o) + ":"
                    for l in lv:
                        txt = txt + " "
                        for cid in l:
                            txt = txt + get_card_name(cid)
                            if cid != l[-1]:
                                txt = txt + ", "
                            else:
                                txt = txt + ". "
                        txt = "<p>" + txt + "Punti " + str(Versicola.punti(l)) + ".</p>"
            if len(txt) <= 0:
                txt = txt + "<p>Nessuna versicola da dichiarare.</p>"
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def __iter__(self):
        try:
            self._i = 0
            return self
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __next__(self):
        try:
            if self._i < len(self._o):
                ret = self._o[self._i]
                self._i += 1
                return ret
            else:
                raise StopIteration
        except Exception as e:
            if not isinstance(e, StopIteration):
                ExceptionMan.manage_exception("", e, True)
            else:
                raise ExceptionMan.manage_exception("", e, True)

    def __dict__(self):
        return dict(
        _listv=self._o
        )

    def restore(self):
        try:
            for o in self._o:
                o.restore()
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def deserVers(self, v):
        try:
            for w in self._o:
                if str(v) == str(w):
                   w._owned = v._owned
                   w._versicole = v._versicole
                   w._matto = v._matto
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def reprJSON(self):
        return self.__dict__()

    @staticmethod
    def fromJSON(json_object):
        try:
            if json_object is None:
                return "None"
            if '_listv' in json_object.keys():
                return json_object
            elif '_id_vers' in json_object.keys():
                _id_vers = json_object['_id_vers']
                v = Versicola.fromJSON(json_object)
                return v
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

def dichiara(v, vers_id):
   pass

if __name__ == '__main__':
    """ Main program cycle """

    ca = [ Carta(CartaId.PAPA_I),
          Carta(CartaId.PAPA_III), Carta(CartaId.TORO_XXXIV), Carta(CartaId.PAPA_II),
          Carta(CartaId.LEONE_XXXIII), Carta(CartaId.SOLE_XXXVIII), Carta(CartaId.MONDO_XXXIX),Carta(CartaId.TROMBA_XL)]
    ca1 = [Carta(CartaId.COPPE_R), Carta(CartaId.BASTO_R), Carta(CartaId.SPADE_R), Carta(CartaId.CAPRIC_XXVIII), Carta(CartaId.SAGITT_XXIX), Carta(CartaId.CANCRO_XXX)]
    try:
        vm = VersicoleManager()
        vm.gestisci_carte(ca)
        vm.evaluate_versicole()
        print(vm.get_txt_description())
        #for v in vve:
        #    print("> " + str(v)  + " - " + str(Versicola.punti(v)) + " punti")
        #cc = [Carta(CartaId.BASTO_7), Carta(CartaId.BASTO_X)]
        #vm.on_presa(cc)
    except Exception as e:
        ExceptionMan.manage_exception("Error. ", e, True)