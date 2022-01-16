from game.carta import Carta, CartaId
from main.exception_man import ExceptionMan
import re

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
    Carte valide per versicole
    '''
    punti_vers = {
        CartaId.SAGITT_XXIX: 5,
        CartaId.DIAVOLO_XIV: 5
    }

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

    def riempi(self, mano, dest, VERSICOLA):
        try:
            for c in mano:
                if VERSICOLA.count(c.get_id()) == 1:
                    dest.append(c)
                elif VERSICOLA.count(c.get_id()) > 1:
                    raise Exception("Composizione mano inattesa")
        except Exception as e:
            ExceptionMan.manage_exception(".conta: ", e, True)

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
            self.versicola_verifica(self.VERSICOLA_RE)
            self.versicola_verifica(self.VERSICOLA_PAPI)
            self.versicola_verifica(self.VERSICOLA_MATTO)
            self.versicola_verifica(self.VERSICOLA_DIECINE)
            self.versicola_verifica(self.VERSICOLA_TREDICI)
            self.versicola_verifica(self.VERSICOLA_DEMOGE)
            self.versicola_verifica(self.VERSICOLA_SOPRA27)
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def get_versicole(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

    def conta(self, mano):
        global punti_ger
        punti = 0
        try:
            for c in mano:
                if c.get_id() in punti_ger:
                    punti = punti + punti_ger[c.get_id()]
                elif c.get_id() in self.punti_vers:
                    punti = punti + self.punti_vers[c.get_id()]
        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

        return punti

    def versicola_verifica(self, ver):

        punti = 0

        try:
            if (ver == self.VERSICOLA_RE):
                if len(self.vers_re) >= 3:
                    punti = self.conta(self.vers_re)
                    print(self.giocatore + " dichiara versicola dei re - " + str(punti) + " punti.")

            elif (ver == self.VERSICOLA_PAPI):
                if len(self.vers_papi) >= 3:
                    punti = self.conta(self.vers_papi)
                    print(self.giocatore + " dichiara versicola dei papi - " + str(punti) + " punti.")
            elif (ver == self.VERSICOLA_MATTO):
                if len(self.vers_matto) >= 3:
                    punti = self.conta(self.vers_matto)
                    print(self.giocatore + " dichiara versicola del matto - " + str(punti) + " punti.")

            elif (ver == self.VERSICOLA_DIECINE):
                if len(self.vers_diecine) >= 3:
                    punti = self.conta(self.vers_diecine)
                    print(self.giocatore + " dichiara versicola delle diecine - " + str(punti) + " punti.")

            elif  (ver == self.VERSICOLA_TREDICI):
                if len(self.vers_tredici) >= 3:
                    punti = self.conta(self.vers_tredici)
                    print(self.giocatore + " dichiara versicola del tredici - " + str(punti) + " punti.")

            elif (ver == self.VERSICOLA_DEMOGE):
                if len(self.vers_demoge) >= 3:
                    punti = self.conta(self.vers_demoge)
                    print("Versicola della carne - punti " + str(punti))

            else:
                punti = self.verifica_sopra27()

        except Exception as e:
            ExceptionMan.manage_exception("Error: ", e, True)

        return punti

    def verifica_sopra27(self):
        try:
            vv = []
            last = -1
            beg = None
            end = None
            if self.vers_sopra27 != None:
                for c in self.vers_sopra27:
                    if c.get_id().value == last + 1:
                        last = c.get_id().value
                        end = c
                    else:
                        if beg != None:
                            if end.get_id().value - beg.get_id().value > 1:
                                vv.append((beg, end))
                            beg = c
                            end = c
                            last = end.get_id().value
                        else:
                            beg = c
                            end = c
                            last = end.get_id().value

                if beg != None and end != None:
                    if beg.get_id() != end.get_id():
                        if end.get_id().value - beg.get_id().value > 1:
                            vv.append((beg, end))

                for v in vv:
                    punti = self.conta(v)
                    print(v)
                    print("Versicola sopra ventisette " + str(punti))

        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)

        return vv