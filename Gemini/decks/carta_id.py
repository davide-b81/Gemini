from enum import Enum, IntEnum
from main.exception_man import ExceptionMan

class Palo(Enum):
    BASTONI = 0,
    COPPE = 1,
    SPADE = 2,
    DENARI = 3,
    TRIONFO = 4


class CartaId(IntEnum):
    '''
    classdocs
    '''
    MATTO_0 = 0

    DANAR_X = 1
    DANAR_9 = 2
    DANAR_8 = 3
    DANAR_7 = 4
    DANAR_6 = 5
    DANAR_5 = 6
    DANAR_4 = 7
    DANAR_3 = 8
    DANAR_2 = 9
    DANAR_A = 10
    DANAR_F = 11
    DANAR_C = 12
    DANAR_D = 13
    DANAR_R = 14

    SPADE_A = 15
    SPADE_2 = 16
    SPADE_3 = 17
    SPADE_4 = 18
    SPADE_5 = 19
    SPADE_6 = 20
    SPADE_7 = 21
    SPADE_8 = 22
    SPADE_9 = 23
    SPADE_X = 24
    SPADE_F = 25
    SPADE_C = 26
    SPADE_D = 27
    SPADE_R = 28

    COPPE_X = 29
    COPPE_9 = 30
    COPPE_8 = 31
    COPPE_7 = 32
    COPPE_6 = 33
    COPPE_5 = 34
    COPPE_4 = 35
    COPPE_3 = 36
    COPPE_2 = 37
    COPPE_A = 38
    COPPE_F = 39
    COPPE_C = 40
    COPPE_D = 41
    COPPE_R = 42

    BASTO_A = 43
    BASTO_2 = 44
    BASTO_3 = 45
    BASTO_4 = 46
    BASTO_5 = 47
    BASTO_6 = 48
    BASTO_7 = 49
    BASTO_8 = 50
    BASTO_9 = 51
    BASTO_X = 52
    BASTO_F = 53
    BASTO_C = 54
    BASTO_D = 55
    BASTO_R = 56

    PAPA_I = 57
    PAPA_II = 58
    PAPA_III = 59
    PAPA_IV = 60
    PAPA_V = 61
    TEMPER_VI = 62
    FORZA_VII = 63
    GIUST_VIII = 64
    ROTA_IX = 65
    CARRO_X = 66
    TEMPO_XI = 67
    APPESO_XII = 68
    MORTE_XIII = 69
    DIAVOLO_XIV = 70
    TORRE_XV = 71
    SPERANZA_XVI = 72
    PRUDENZA_XVII = 73
    FEDE_XVIII = 74
    CARITA_XIX = 75
    FUOCO_XX = 76
    ACQUA_XXI = 77
    TERRA_XXII = 78
    ARIA_XXIII = 79
    BILANCIA_XXIV = 80
    VERGINE_XXV = 81
    SCORP_XXVI = 82
    ARIETE_XXVII = 83
    CAPRIC_XXVIII = 84
    SAGITT_XXIX = 85
    CANCRO_XXX = 86
    PESCI_XXXI = 87
    ACQUARIO_XXXII = 88
    LEONE_XXXIII = 89
    TORO_XXXIV = 90
    GEMINI_XXXV = 91
    STELLA_XXXVI = 92
    LUNA_XXXVII = 93
    SOLE_XXXVIII = 94
    MONDO_XXXIX = 95
    TROMBA_XL = 96

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

cartiglie = [CartaId.DANAR_A, CartaId.DANAR_2, CartaId.DANAR_3, CartaId.DANAR_4, CartaId.DANAR_5, CartaId.DANAR_6,
             CartaId.DANAR_7, CartaId.DANAR_8, CartaId.DANAR_9, CartaId.DANAR_X, CartaId.DANAR_F, CartaId.DANAR_C,
             CartaId.DANAR_D,
             CartaId.SPADE_A, CartaId.SPADE_2, CartaId.SPADE_3, CartaId.SPADE_4, CartaId.SPADE_5, CartaId.SPADE_6,
             CartaId.SPADE_7, CartaId.SPADE_8, CartaId.SPADE_9, CartaId.SPADE_X, CartaId.SPADE_F, CartaId.SPADE_C,
             CartaId.SPADE_D,
             CartaId.COPPE_A, CartaId.COPPE_2, CartaId.COPPE_3, CartaId.COPPE_4, CartaId.COPPE_5, CartaId.COPPE_6,
             CartaId.COPPE_7, CartaId.COPPE_8, CartaId.COPPE_9, CartaId.COPPE_X, CartaId.COPPE_F, CartaId.COPPE_C,
             CartaId.COPPE_D,
             CartaId.BASTO_A, CartaId.BASTO_2, CartaId.BASTO_3, CartaId.BASTO_4, CartaId.BASTO_5, CartaId.BASTO_6,
             CartaId.BASTO_7, CartaId.BASTO_8, CartaId.BASTO_9, CartaId.BASTO_X, CartaId.BASTO_F, CartaId.BASTO_C,
             CartaId.BASTO_D]

carte_lunghe = [CartaId.SPADE_A, CartaId.SPADE_2, CartaId.SPADE_3, CartaId.SPADE_4, CartaId.SPADE_5, CartaId.SPADE_6,
                CartaId.SPADE_7, CartaId.SPADE_8, CartaId.SPADE_9, CartaId.SPADE_X, CartaId.SPADE_F, CartaId.SPADE_C,
                CartaId.SPADE_D,
                CartaId.BASTO_A, CartaId.BASTO_2, CartaId.BASTO_3, CartaId.BASTO_4, CartaId.BASTO_5, CartaId.BASTO_6,
                CartaId.BASTO_7, CartaId.BASTO_8, CartaId.BASTO_9, CartaId.BASTO_X, CartaId.BASTO_F, CartaId.BASTO_C,
                CartaId.BASTO_D]

carte_corte = [CartaId.DANAR_A, CartaId.DANAR_2, CartaId.DANAR_3, CartaId.DANAR_4, CartaId.DANAR_5, CartaId.DANAR_6,
               CartaId.DANAR_7, CartaId.DANAR_8, CartaId.DANAR_9, CartaId.DANAR_X, CartaId.DANAR_F, CartaId.DANAR_C,
               CartaId.DANAR_D,
               CartaId.COPPE_A, CartaId.COPPE_2, CartaId.COPPE_3, CartaId.COPPE_4, CartaId.COPPE_5, CartaId.COPPE_6,
               CartaId.COPPE_7, CartaId.COPPE_8, CartaId.COPPE_9, CartaId.COPPE_X, CartaId.COPPE_F, CartaId.COPPE_C,
               CartaId.COPPE_D]

denari = [CartaId.DANAR_A, CartaId.DANAR_2, CartaId.DANAR_3, CartaId.DANAR_4, CartaId.DANAR_5, CartaId.DANAR_6,
          CartaId.DANAR_7, CartaId.DANAR_8, CartaId.DANAR_9, CartaId.DANAR_X, CartaId.DANAR_F, CartaId.DANAR_C,
          CartaId.DANAR_D, CartaId.DANAR_R]
spade = [CartaId.SPADE_A, CartaId.SPADE_2, CartaId.SPADE_3, CartaId.SPADE_4, CartaId.SPADE_5, CartaId.SPADE_6,
         CartaId.SPADE_7, CartaId.SPADE_8, CartaId.SPADE_9, CartaId.SPADE_X, CartaId.SPADE_F, CartaId.SPADE_C,
         CartaId.SPADE_D, CartaId.SPADE_R]
coppe = [CartaId.COPPE_A, CartaId.COPPE_2, CartaId.COPPE_3, CartaId.COPPE_4, CartaId.COPPE_5, CartaId.COPPE_6,
         CartaId.COPPE_7, CartaId.COPPE_8, CartaId.COPPE_9, CartaId.COPPE_X, CartaId.COPPE_F, CartaId.COPPE_C,
         CartaId.COPPE_D, CartaId.COPPE_R]
bastoni = [CartaId.BASTO_A, CartaId.BASTO_2, CartaId.BASTO_3, CartaId.BASTO_4, CartaId.BASTO_5, CartaId.BASTO_6,
           CartaId.BASTO_7, CartaId.BASTO_8, CartaId.BASTO_9, CartaId.BASTO_X, CartaId.BASTO_F, CartaId.BASTO_C,
           CartaId.BASTO_D, CartaId.BASTO_R]
tarocco = [CartaId.MATTO_0, CartaId.PAPA_I, CartaId.PAPA_II, CartaId.PAPA_III, CartaId.PAPA_IV, CartaId.PAPA_V,
           CartaId.TEMPER_VI, CartaId.FORZA_VII, CartaId.GIUST_VIII, CartaId.ROTA_IX, CartaId.CARRO_X, CartaId.TEMPO_XI,
           CartaId.APPESO_XII, CartaId.MORTE_XIII, CartaId.DIAVOLO_XIV,
           CartaId.TORRE_XV, CartaId.SPERANZA_XVI, CartaId.PRUDENZA_XVII, CartaId.FEDE_XVIII, CartaId.CARITA_XIX,
           CartaId.FUOCO_XX, CartaId.ACQUA_XXI, CartaId.TERRA_XXII, CartaId.ARIA_XXIII, CartaId.BILANCIA_XXIV,
           CartaId.VERGINE_XXV, CartaId.SCORP_XXVI,
           CartaId.ARIETE_XXVII, CartaId.CAPRIC_XXVIII, CartaId.SAGITT_XXIX, CartaId.CANCRO_XXX, CartaId.PESCI_XXXI,
           CartaId.ACQUARIO_XXXII, CartaId.LEONE_XXXIII, CartaId.TORO_XXXIV, CartaId.GEMINI_XXXV, CartaId.STELLA_XXXVI,
           CartaId.LUNA_XXXVII,
           CartaId.SOLE_XXXVIII, CartaId.MONDO_XXXIX, CartaId.TROMBA_XL]

card_name = {}
card_name[CartaId.DANAR_A] = "Asso di Denari"
card_name[CartaId.DANAR_2] = "Due di Denari"
card_name[CartaId.DANAR_3] = "Tre di Denari"
card_name[CartaId.DANAR_4] = "Quattro di Denari"
card_name[CartaId.DANAR_5] = "Cinque di Denari"
card_name[CartaId.DANAR_6] = "Sei di Denari"
card_name[CartaId.DANAR_7] = "Sette di Denari"
card_name[CartaId.DANAR_8] = "Otto di Denari"
card_name[CartaId.DANAR_9] = "Nove di Denari"
card_name[CartaId.DANAR_X] = "Dieci di Denari"
card_name[CartaId.DANAR_F] = "Fantina di Denari"
card_name[CartaId.DANAR_C] = "Cavallo di Denari"
card_name[CartaId.DANAR_D] = "Regina di Denari"
card_name[CartaId.DANAR_R] = "Re di Denari"
card_name[CartaId.SPADE_A] = "Asso di Spade"
card_name[CartaId.SPADE_2] = "Due di Spade"
card_name[CartaId.SPADE_3] = "Tre di Spade"
card_name[CartaId.SPADE_4] = "Quattro di Spade"
card_name[CartaId.SPADE_5] = "Cinque di Spade"
card_name[CartaId.SPADE_6] = "Sei di Spade"
card_name[CartaId.SPADE_7] = "Sette di Spade"
card_name[CartaId.SPADE_8] = "Otto di Spade"
card_name[CartaId.SPADE_9] = "Nove di Spade"
card_name[CartaId.SPADE_X] = "Dieci di Spade"
card_name[CartaId.SPADE_F] = "Fante di Spade"
card_name[CartaId.SPADE_C] = "Cavallo di Spade"
card_name[CartaId.SPADE_D] = "Regina di Spade"
card_name[CartaId.SPADE_R] = "Re di Spade"
card_name[CartaId.COPPE_A] = "Asso di Coppe"
card_name[CartaId.COPPE_2] = "Due di Coppe"
card_name[CartaId.COPPE_3] = "Tre di Coppe"
card_name[CartaId.COPPE_4] = "Quattro di Coppe"
card_name[CartaId.COPPE_5] = "Cinque di Coppe"
card_name[CartaId.COPPE_6] = "Sei di Coppe"
card_name[CartaId.COPPE_7] = "Sette di Coppe"
card_name[CartaId.COPPE_8] = "Otto di Coppe"
card_name[CartaId.COPPE_9] = "Nove di Coppe"
card_name[CartaId.COPPE_X] = "Dieci di Coppe"
card_name[CartaId.COPPE_F] = "Fantina di Coppe"
card_name[CartaId.COPPE_C] = "Cavallo di Coppe"
card_name[CartaId.COPPE_D] = "Regina di Coppe"
card_name[CartaId.COPPE_R] = "Re di Coppe"
card_name[CartaId.BASTO_A] = "Asso di Bastoni"
card_name[CartaId.BASTO_2] = "Due di Bastoni"
card_name[CartaId.BASTO_3] = "Tre di Bastoni"
card_name[CartaId.BASTO_4] = "Quattro di Bastoni"
card_name[CartaId.BASTO_5] = "Cinque di Bastoni"
card_name[CartaId.BASTO_6] = "Sei di Bastoni"
card_name[CartaId.BASTO_7] = "Sette di Bastoni"
card_name[CartaId.BASTO_8] = "Otto di Bastoni"
card_name[CartaId.BASTO_9] = "Nove di Bastoni"
card_name[CartaId.BASTO_X] = "Dieci di Bastoni"
card_name[CartaId.BASTO_F] = "Fante di Bastoni"
card_name[CartaId.BASTO_C] = "Cavallo di Bastoni"
card_name[CartaId.BASTO_D] = "Regina di Bastoni"
card_name[CartaId.BASTO_R] = "Re di Bastoni"
card_name[CartaId.MATTO_0] = "Il Matto"
card_name[CartaId.PAPA_I] = " Il Papino"
card_name[CartaId.PAPA_II] = "Il Granduca"
card_name[CartaId.PAPA_III] = "L'Imperatore"
card_name[CartaId.PAPA_IV] = "L'imperatrice"
card_name[CartaId.PAPA_V] = "L'Innamorato"
card_name[CartaId.TEMPER_VI] = "La Temperanza"
card_name[CartaId.FORZA_VII] = "La Forza"
card_name[CartaId.GIUST_VIII] = "La Giustizia"
card_name[CartaId.ROTA_IX] = "La Ruota di Fortuna"
card_name[CartaId.CARRO_X] = "Il Carro"
card_name[CartaId.TEMPO_XI] = "Il Gobbo"
card_name[CartaId.APPESO_XII] = "L'Appeso"
card_name[CartaId.MORTE_XIII] = "XIII"
card_name[CartaId.DIAVOLO_XIV] = "Il Diavolo"
card_name[CartaId.TORRE_XV] = "La Casa del Diavolo"
card_name[CartaId.SPERANZA_XVI] = "La Speranza"
card_name[CartaId.PRUDENZA_XVII] = "La Prudenza"
card_name[CartaId.FEDE_XVIII] = "La Fede"
card_name[CartaId.CARITA_XIX] = "La Carita'"
card_name[CartaId.FUOCO_XX] = "Il Fuoco"
card_name[CartaId.ACQUA_XXI] = "L'Acqua"
card_name[CartaId.TERRA_XXII] = "La Terra"
card_name[CartaId.ARIA_XXIII] = "L'Aria"
card_name[CartaId.BILANCIA_XXIV] = "La Bilancia"
card_name[CartaId.VERGINE_XXV] = "La Vergine"
card_name[CartaId.SCORP_XXVI] = "Lo Scorpione"
card_name[CartaId.ARIETE_XXVII] = "L'Ariete"
card_name[CartaId.CAPRIC_XXVIII] = "Il Capricorno"
card_name[CartaId.SAGITT_XXIX] = "Il Sagittario"
card_name[CartaId.CANCRO_XXX] = "Il Cancro"
card_name[CartaId.PESCI_XXXI] = "I Pesci"
card_name[CartaId.ACQUARIO_XXXII] = "L'Acquario"
card_name[CartaId.LEONE_XXXIII] = "Il Leone"
card_name[CartaId.TORO_XXXIV] = "Il Toro"
card_name[CartaId.GEMINI_XXXV] = "I Gemelli"
card_name[CartaId.STELLA_XXXVI] = "La Stella"
card_name[CartaId.LUNA_XXXVII] = "La Luna"
card_name[CartaId.SOLE_XXXVIII] = "Il Sole"
card_name[CartaId.MONDO_XXXIX] = "Il Mondo"
card_name[CartaId.TROMBA_XL] = "La Tromba"

card_short_name = {}
card_short_name[CartaId.DANAR_A] = "AD"
card_short_name[CartaId.DANAR_2] = "2D"
card_short_name[CartaId.DANAR_3] = "3D"
card_short_name[CartaId.DANAR_4] = "4D"
card_short_name[CartaId.DANAR_5] = "5D"
card_short_name[CartaId.DANAR_6] = "6D"
card_short_name[CartaId.DANAR_7] = "7D"
card_short_name[CartaId.DANAR_8] = "8D"
card_short_name[CartaId.DANAR_9] = "9D"
card_short_name[CartaId.DANAR_X] = "XD"
card_short_name[CartaId.DANAR_F] = "FD"
card_short_name[CartaId.DANAR_C] = "CD"
card_short_name[CartaId.DANAR_D] = "QD"
card_short_name[CartaId.DANAR_R] = "KD"
card_short_name[CartaId.SPADE_A] = "AS"
card_short_name[CartaId.SPADE_2] = "2S"
card_short_name[CartaId.SPADE_3] = "3S"
card_short_name[CartaId.SPADE_4] = "4S"
card_short_name[CartaId.SPADE_5] = "5S"
card_short_name[CartaId.SPADE_6] = "6S"
card_short_name[CartaId.SPADE_7] = "7S"
card_short_name[CartaId.SPADE_8] = "8S"
card_short_name[CartaId.SPADE_9] = "9S"
card_short_name[CartaId.SPADE_X] = "XS"
card_short_name[CartaId.SPADE_F] = "FS"
card_short_name[CartaId.SPADE_C] = "CS"
card_short_name[CartaId.SPADE_D] = "QS"
card_short_name[CartaId.SPADE_R] = "KS"
card_short_name[CartaId.COPPE_A] = "AC"
card_short_name[CartaId.COPPE_2] = "2C"
card_short_name[CartaId.COPPE_3] = "3C"
card_short_name[CartaId.COPPE_4] = "4C"
card_short_name[CartaId.COPPE_5] = "5C"
card_short_name[CartaId.COPPE_6] = "6C"
card_short_name[CartaId.COPPE_7] = "7C"
card_short_name[CartaId.COPPE_8] = "8C"
card_short_name[CartaId.COPPE_9] = "9C"
card_short_name[CartaId.COPPE_X] = "XC"
card_short_name[CartaId.COPPE_F] = "FC"
card_short_name[CartaId.COPPE_C] = "CC"
card_short_name[CartaId.COPPE_D] = "QC"
card_short_name[CartaId.COPPE_R] = "KC"
card_short_name[CartaId.BASTO_A] = "AB"
card_short_name[CartaId.BASTO_2] = "2B"
card_short_name[CartaId.BASTO_3] = "3B"
card_short_name[CartaId.BASTO_4] = "4B"
card_short_name[CartaId.BASTO_5] = "5B"
card_short_name[CartaId.BASTO_6] = "6B"
card_short_name[CartaId.BASTO_7] = "7B"
card_short_name[CartaId.BASTO_8] = "8B"
card_short_name[CartaId.BASTO_9] = "9B"
card_short_name[CartaId.BASTO_X] = "XB"
card_short_name[CartaId.BASTO_F] = "FB"
card_short_name[CartaId.BASTO_C] = "CB"
card_short_name[CartaId.BASTO_D] = "QB"
card_short_name[CartaId.BASTO_R] = "KB"
card_short_name[CartaId.MATTO_0] = "0"
card_short_name[CartaId.PAPA_I] = " I"
card_short_name[CartaId.PAPA_II] = "II"
card_short_name[CartaId.PAPA_III] = "III"
card_short_name[CartaId.PAPA_IV] = "IV"
card_short_name[CartaId.PAPA_V] = "V"
card_short_name[CartaId.TEMPER_VI] = "VI"
card_short_name[CartaId.FORZA_VII] = "VII"
card_short_name[CartaId.GIUST_VIII] = "VIII"
card_short_name[CartaId.ROTA_IX] = "IX"
card_short_name[CartaId.CARRO_X] = "X"
card_short_name[CartaId.TEMPO_XI] = "XI"
card_short_name[CartaId.APPESO_XII] = "XII"
card_short_name[CartaId.MORTE_XIII] = "XIII"
card_short_name[CartaId.DIAVOLO_XIV] = "XIV"
card_short_name[CartaId.TORRE_XV] = "XV"
card_short_name[CartaId.SPERANZA_XVI] = "XVI"
card_short_name[CartaId.PRUDENZA_XVII] = "XVII"
card_short_name[CartaId.FEDE_XVIII] = "XVIII"
card_short_name[CartaId.CARITA_XIX] = "XIX"
card_short_name[CartaId.FUOCO_XX] = "XX"
card_short_name[CartaId.ACQUA_XXI] = "XXI"
card_short_name[CartaId.TERRA_XXII] = "XXII"
card_short_name[CartaId.ARIA_XXIII] = "XXIII"
card_short_name[CartaId.BILANCIA_XXIV] = "XXIV"
card_short_name[CartaId.VERGINE_XXV] = "XXV"
card_short_name[CartaId.SCORP_XXVI] = "XXVI"
card_short_name[CartaId.ARIETE_XXVII] = "XXVII"
card_short_name[CartaId.CAPRIC_XXVIII] = "XXVIII"
card_short_name[CartaId.SAGITT_XXIX] = "XXIX"
card_short_name[CartaId.CANCRO_XXX] = "XX"
card_short_name[CartaId.PESCI_XXXI] = "XXXI"
card_short_name[CartaId.ACQUARIO_XXXII] = "XXXII"
card_short_name[CartaId.LEONE_XXXIII] = "XXXIII"
card_short_name[CartaId.TORO_XXXIV] = "XXXIV"
card_short_name[CartaId.GEMINI_XXXV] = "XXXV"
card_short_name[CartaId.STELLA_XXXVI] = "XXXVI"
card_short_name[CartaId.LUNA_XXXVII] = "XXXVII"
card_short_name[CartaId.SOLE_XXXVIII] = "XXXVIII"
card_short_name[CartaId.MONDO_XXXIX] = "XXXIX"
card_short_name[CartaId.TROMBA_XL] = "XL"

seme_name = {}
seme_name[Palo.DENARI] = "Denari"
seme_name[Palo.SPADE] = "Spade"
seme_name[Palo.COPPE] = "Coppe"
seme_name[Palo.BASTONI] = "Bastoni"
seme_name[Palo.TRIONFO] = "Tarocco"

def is_tarocco(cid):
    global tarocco
    try:
        return tarocco.count(cid) > 0
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
    return None

def count_seme(ca, seme):
    try:
        n = 0
        for c in ca:
            if str(get_seme(c.get_id())) == str(seme):
                n = n + 1
        return n
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def seme_carta(a):
    global denari, spade, coppe, bastoni, tarocco
    try:
        if a in denari:
            return Palo.DENARI
        elif a in spade:
            return Palo.SPADE
        elif a in coppe:
            return Palo.COPPE
        elif a in bastoni:
            return Palo.BASTONI
        else:
            return Palo.TRIONFO
    except Exception as e:
        ExceptionMan.manage_exception(str(a), e, True)
    return None

def get_seme(cid):
    try:
        return seme_carta(cid)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
    return None

def get_numerale(id):
    try:
        if (id.value == CartaId.MATTO_0):
            return 0
        elif (id.value <= CartaId.DANAR_R.value):
            return id.value
        elif (id.value <= CartaId.SPADE_R.value):
            return id.value - CartaId.SPADE_A.value + 1
        elif (id.value <= CartaId.COPPE_R.value):
            return id.value - CartaId.COPPE_A.value + 1
        elif (id.value <= CartaId.BASTO_R.value):
            return id.value - CartaId.BASTO_A.value + 1
        else:
            return id.value - CartaId.PAPA_I.value + 1
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def get_greater(clist):
    try:
        g = None
        for c in clist:
            if g is None:
                g = c
            elif get_seme(c.get_id()) == get_seme(g.get_id()):
                if get_numerale(c.get_id()) > get_numerale(g.get_id()):
                    g = c
            elif get_seme(c.get_id()) == Palo.TRIONFO:
                g = c
            elif get_seme(g.get_id()) == Palo.TRIONFO:
                pass
            elif get_numerale(c.get_id()) == get_numerale(g.get_id()):
                pass
            elif get_numerale(c.get_id()) > get_numerale(g.get_id()):
                g = c
            else:
                pass
        return g
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def is_sopraventi(cid):
    try:
        if cid == CartaId.ACQUA_XXI:
            return True
        elif cid == CartaId.TERRA_XXII:
            return True
        elif cid == CartaId.ARIA_XXIII:
            return True
        elif cid == CartaId.BILANCIA_XXIV:
            return True
        elif cid == CartaId.VERGINE_XXV:
            return True
        elif cid == CartaId.SCORP_XXVI:
            return True
        elif cid == CartaId.ARIETE_XXVII:
            return True
        elif cid == CartaId.CAPRIC_XXVIII:
            return True
        elif cid == CartaId.SAGITT_XXIX:
            return True
        elif cid == CartaId.CANCRO_XXX:
            return True
        elif cid == CartaId.PESCI_XXXI:
            return True
        elif cid == CartaId.ACQUARIO_XXXII:
            return True
        elif cid == CartaId.LEONE_XXXIII:
            return True
        elif cid == CartaId.TORO_XXXIV:
            return True
        elif cid == CartaId.GEMINI_XXXV:
            return True
        elif cid == CartaId.STELLA_XXXVI:
            return True
        elif cid == CartaId.LUNA_XXXVII:
            return True
        elif cid == CartaId.SOLE_XXXVIII:
            return True
        elif cid == CartaId.MONDO_XXXIX:
            return True
        elif cid == CartaId.TROMBA_XL:
            return True
        else:
            return False
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def is_cartiglia(cid):
    try:
        if cid in cartiglie:
            return True
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
    return None

def get_short_name(cid):
    global card_short_name
    try:
        return card_short_name[cid]
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
    return None

def get_card_name(cid):
    global card_name
    try:
        return card_name[cid]
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
    return None
