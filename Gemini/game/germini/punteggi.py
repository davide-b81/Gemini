from decks.carta import CartaId
from main.globals import *
from main.exception_man import ExceptionMan

'''
Carte di conto punti
'''
punti_ger = {
    CartaId.MATTO_0: 5,
    CartaId.PAPA_I: 5,
    CartaId.PAPA_II: 3,
    CartaId.PAPA_III: 3,
    CartaId.PAPA_IV: 3,
    CartaId.PAPA_V: 3,
    CartaId.CARRO_X: 5,
    CartaId.MORTE_XIII: 5,
    CartaId.FUOCO_XX: 5,
    CartaId.CAPRIC_XXVIII: 5,
    CartaId.CANCRO_XXX: 5,
    CartaId.PESCI_XXXI: 5,
    CartaId.ACQUARIO_XXXII: 5,
    CartaId.LEONE_XXXIII: 5,
    CartaId.TORO_XXXIV: 5,
    CartaId.GEMINI_XXXV: 5,
    CartaId.STELLA_XXXVI: 10,
    CartaId.LUNA_XXXVII: 10,
    CartaId.SOLE_XXXVIII: 10,
    CartaId.MONDO_XXXIX: 10,
    CartaId.TROMBA_XL: 10,
    CartaId.DANAR_R: 5,
    CartaId.SPADE_R: 5,
    CartaId.COPPE_R: 5,
    CartaId.BASTO_R: 5
}

def is_conto(c):
    global punti_ger
    return c.get_id in punti_ger

punti_vers = {
    CartaId.MATTO_0: 5,
    CartaId.PAPA_I: 5,
    CartaId.PAPA_II: 3,
    CartaId.PAPA_III: 3,
    CartaId.PAPA_IV: 3,
    CartaId.PAPA_V: 3,
    CartaId.CARRO_X: 5,
    CartaId.MORTE_XIII: 5,
    CartaId.DIAVOLO_XIV: 5,
    CartaId.FUOCO_XX: 5,
    CartaId.CAPRIC_XXVIII: 5,
    CartaId.SAGITT_XXIX: 5,
    CartaId.CANCRO_XXX: 5,
    CartaId.PESCI_XXXI: 5,
    CartaId.ACQUARIO_XXXII: 5,
    CartaId.LEONE_XXXIII: 5,
    CartaId.TORO_XXXIV: 5,
    CartaId.GEMINI_XXXV: 5,
    CartaId.STELLA_XXXVI: 10,
    CartaId.LUNA_XXXVII: 10,
    CartaId.SOLE_XXXVIII: 10,
    CartaId.MONDO_XXXIX: 10,
    CartaId.TROMBA_XL: 10,
    CartaId.DANAR_R: 5,
    CartaId.SPADE_R: 5,
    CartaId.COPPE_R: 5,
    CartaId.BASTO_R: 5
}

class Versicole(object):
    vers_re = None
    vers_papi = None
    vers_matto = None
    vers_diecine = None
    vers_tredici = None
    vers_demoge = None
    vers_sopra27 = None
    giocatore = None

    VERSICOLA_RE = [CartaId.BASTO_R, CartaId.COPPE_R, CartaId.DANAR_R, CartaId.SPADE_R]
    VERSICOLA_PAPI = [CartaId.PAPA_I, CartaId.PAPA_II, CartaId.PAPA_III, CartaId.PAPA_IV, CartaId.PAPA_V]
    VERSICOLA_MATTO = [CartaId.PAPA_I, CartaId.MATTO_0, CartaId.TROMBA_XL]
    VERSICOLA_DIECINE = [CartaId.CARRO_X, CartaId.FUOCO_XX, CartaId.CANCRO_XXX, CartaId.TROMBA_XL]
    VERSICOLA_TREDICI = [CartaId.PAPA_I, CartaId.MORTE_XIII, CartaId.CAPRIC_XXVIII]
    VERSICOLA_DEL29 = [CartaId.CAPRIC_XXVIII, CartaId.SAGITT_XXIX, CartaId.CANCRO_XXX]
    VERSICOLA_DEMOGE = [CartaId.DIAVOLO_XIV, CartaId.MONDO_XXXIX, CartaId.GEMINI_XXXV]
    VERSICOLA_SOPRA27 = [CartaId.CAPRIC_XXVIII, CartaId.SAGITT_XXIX, CartaId.CANCRO_XXX, CartaId.PESCI_XXXI, CartaId.ACQUARIO_XXXII, CartaId.LEONE_XXXIII, CartaId.TORO_XXXIV, CartaId.GEMINI_XXXV, CartaId.STELLA_XXXVI, CartaId.LUNA_XXXVII,
       CartaId.SOLE_XXXVIII, CartaId.MONDO_XXXIX, CartaId.TROMBA_XL]

    VERS_TEST = [CartaId.CAPRIC_XXVIII, CartaId.SAGITT_XXIX, CartaId.PESCI_XXXI, CartaId.ACQUARIO_XXXII, CartaId.LEONE_XXXIII, CartaId.GEMINI_XXXV, CartaId.STELLA_XXXVI, CartaId.LUNA_XXXVII,
       CartaId.SOLE_XXXVIII, CartaId.MONDO_XXXIX, CartaId.TROMBA_XL]

    '''
    classdocs
    '''
    def __init__(self, giocatore = ""):
        self.vers_re = []
        self.vers_papi = []
        self.vers_matto = []
        self.vers_diecine = []
        self.vers_tredici = []
        self.vers_demoge = []
        self.vers_sopra27 = []
        self.giocatore = giocatore
        self._delegate_on_dichiara = None

    def set_delegate_on_dichiara(self, foo):
        self._delegate_on_dichiara = foo

    def add_car_versicola(self, c, dest, VERSICOLA):
        try:
            if VERSICOLA.count(c.get_id()) == 1:
                dest.append(c)
            elif VERSICOLA.count(c.get_id()) > 1:
                raise Exception("Composizione mano inattesa")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def riempi(self, mano, dest, VERSICOLA):
        try:
            for c in mano:
                self.add_car_versicola(c, dest, VERSICOLA)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        self.vers_re.clear()
        self.vers_papi.clear()
        self.vers_matto.clear()
        self.vers_diecine.clear()
        self.vers_tredici.clear()
        self.vers_demoge.clear()
        self.vers_sopra27.clear()

    def gestisci_carte(self, mano):
        try:
            self.riempi(mano, self.vers_re, self.VERSICOLA_RE)
            self.riempi(mano, self.vers_papi, self.VERSICOLA_PAPI)
            self.riempi(mano, self.vers_matto, self.VERSICOLA_MATTO)
            self.riempi(mano, self.vers_diecine, self.VERSICOLA_DIECINE)
            self.riempi(mano, self.vers_tredici, self.VERSICOLA_TREDICI)
            self.riempi(mano, self.vers_demoge, self.VERSICOLA_DEMOGE)
            self.riempi(mano, self.vers_sopra27, self.VERSICOLA_SOPRA27)

            self.dichiara()

        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def dichiara(self):
        try:

            self.versicola_verifica(self.vers_papi, self.VERSICOLA_PAPI)
            self.versicola_verifica(self.vers_matto, self.VERSICOLA_MATTO)
            self.versicola_verifica(self.vers_diecine, self.VERSICOLA_DIECINE)
            self.versicola_verifica(self.vers_tredici, self.VERSICOLA_TREDICI)
            self.versicola_verifica(self.vers_demoge, self.VERSICOLA_DEMOGE)
            self.versicola_verifica(self.vers_sopra27, self.VERSICOLA_SOPRA27)

        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def get_versicole(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def conta(self, mano):
        global punti_vers
        punti = 0

        #try:
        #    if mano.intersect(self.vers_re).count() >= 3:
        #        for c in mano:
        #            if c.get_id() in punti_vers:
        #                punti = punti + punti_vers[c.get_id()]
        #except Exception as e:
        #    ExceptionMan.manage_exception("Error: ", e, True)

        return punti

    def allunga_versicola(self, ver):
        # TODO: Si allungano solo le versicole con carte non giocate?
        pass

    def versicola(self, ca, vers):
        vers_set = set(vers)
        intersection = vers_set.intersection(ca)

    def versicola_verifica(self, vers, id):
        try:
            assert self.giocatore != None
            if self.conta(vers) >= 3:
                punti = self.conta(self.vers)
                self._delegate_on_dichiara(self.giocatore + " dichiara versicola " + str(id) + " punti " + punti)
                self.giocatore.somma_punti(punti)
                return punti

        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)
        return 0

    def verifica_sopra27(self):
        try:
            vv = []
            last = -1
            beg = None
            end = None
            if self.vers_sopra27 is not None:
                for c in self.vers_sopra27:
                    if c.get_id().value == last + 1:
                        last = c.get_id().value
                        end = c
                    else:
                        if beg is not None:
                            if end.get_id().value - beg.get_id().value > 1:
                                vv.append((beg, end))
                            beg = c
                            end = c
                            last = end.get_id().value
                        else:
                            beg = c
                            end = c
                            last = end.get_id().value

                if beg is not None and end is not None:
                    if beg.get_id() != end.get_id():
                        if end.get_id().value - beg.get_id().value > 1:
                            vv.append((beg, end))

                for v in vv:
                    punti = self.conta(v)
                    echo_message(v)
                    self._delegate_on_dichiara("Versicola sopra ventisette " + str(punti))

        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

        return vv