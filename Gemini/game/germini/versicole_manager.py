#   '''
#  Created on 11 3 2022
#  @author: david
#  '''

from importlib.resources import _

from game.germini.versicola import Versicola
from decks.carta import CartaId, Carta
from main.exception_man import ExceptionMan
from decks.carta_id import get_card_name

VERSICOLA_REGOLARE_ID = "VERSICOLE_REGOLARI_ID"
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
    _delegate_on_dichiara = None
    _delegate_on_punti = None

    def __init__(self):
        try:
            self._o = []
            self._delegate_on_dichiara = None
            self._delegate_on_punti = None
            self._delegate_on_allunga = None
            self._o.append(Versicola(VERSICOLA_RE_ID, definizione[VERSICOLA_RE_ID]))
            self._o.append(Versicola(VERSICOLA_PAPI_ID, definizione[VERSICOLA_PAPI_ID]))
            self._o.append(Versicola(VERSICOLA_MATTO_ID, definizione[VERSICOLA_MATTO_ID]))
            self._o.append(Versicola(VERSICOLA_DIECINE_ID, definizione[VERSICOLA_DIECINE_ID]))
            self._o.append(Versicola(VERSICOLA_TREDICI_ID, definizione[VERSICOLA_TREDICI_ID]))
            self._o.append(Versicola(VERSICOLA_CARNE_ID, definizione[VERSICOLA_CARNE_ID]))
            self._o.append(Versicola(VERSICOLA_REGOLARE_ID, definizione[VERSICOLA_REGOLARE_ID]))

            for o in self._o:
                o.set_delegate_nuova(dichiara)
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def set_delegate_on_dichiara(self, f):
        self._delegate_on_dichiara = f

    def set_delegate_on_punti(self, f):
        self._delegate_on_punti = f

    def reset(self):
        try:
            for o in self._o:
                o.clear()
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

    def evaluate_versicole(self, callback):
        try:
            for o in self._o:
                #print("> " + str(o))
                o.set_versicole()
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def get_lista_versicole(self):
        try:
            l = []
            for o in self._o:
                a = o.get_lista()
                if len(a) > 0:
                    for aa in a:
                        l.append(aa)
            return l
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

    def get_txt_description(self):
        try:
            txt = ""
            for o in self._o:
                lv = o.get_lista()
                if len(lv) > 0:
                    txt = txt + "> " + str(o) + ":"
                    for l in lv:
                        txt = txt + " "
                        for cid in l:
                            txt = txt + get_card_name(cid)
                            if cid != l[-1]:
                                txt = txt + ", "
                            else:
                                txt = txt + ". "
                        txt = txt + "Punti " + str(Versicola.punti(l)) + ".\n"
            if len(txt) <= 0:
                txt = txt + "Nessuna versicola da dichiarare."
            else:
                print("TXT " + str(len(txt)))
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

def dichiara(v, vers_id):
    print("Versicola")

if __name__ == '__main__':
    """ Main program cycle """

    ca = [ Carta(CartaId.PAPA_I),
          Carta(CartaId.PAPA_III), Carta(CartaId.TORO_XXXIV), Carta(CartaId.PAPA_II),
          Carta(CartaId.LEONE_XXXIII), Carta(CartaId.SOLE_XXXVIII), Carta(CartaId.MONDO_XXXIX),Carta(CartaId.TROMBA_XL)]
    ca1 =  [Carta(CartaId.COPPE_R), Carta(CartaId.BASTO_R), Carta(CartaId.SPADE_R), Carta(CartaId.CAPRIC_XXVIII), Carta(CartaId.SAGITT_XXIX), Carta(CartaId.CANCRO_XXX)]
    try:
        vm = VersicoleManager()
        vm.gestisci_carte(ca)
        vm.evaluate_versicole(dichiara)

        vve = vm.get_lista_versicole()
        print(vm.get_txt_description())
        #for v in vve:
        #    print("> " + str(v)  + " - " + str(Versicola.punti(v)) + " punti")
        #cc = [Carta(CartaId.BASTO_7), Carta(CartaId.BASTO_X)]
        #vm.on_presa(cc)
    except Exception as e:
        ExceptionMan.manage_exception("Error. ", e, True)