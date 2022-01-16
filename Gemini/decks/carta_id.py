
from enum import Enum

class Seme(Enum):
    BASTONI = 0,
    COPPE = 1,
    SPADE = 2,
    DENARI = 3,
    TRIONFO = 4


class CartaId(Enum):
    '''
    classdocs
    '''
    MATTO_0 = 0

    DANAR_A = 10
    DANAR_2 = 9
    DANAR_3 = 8
    DANAR_4 = 7
    DANAR_5 = 6
    DANAR_6 = 5
    DANAR_7 = 4
    DANAR_8 = 3
    DANAR_9 = 2
    DANAR_X = 1
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

    COPPE_A = 38
    COPPE_2 = 37
    COPPE_3 = 36
    COPPE_4 = 35
    COPPE_5 = 34
    COPPE_6 = 33
    COPPE_7 = 32
    COPPE_8 = 31
    COPPE_9 = 30
    COPPE_X = 29
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

cartiglie = [CartaId.DANAR_A, CartaId.DANAR_2, CartaId.DANAR_3, CartaId.DANAR_4, CartaId.DANAR_5, CartaId.DANAR_6, CartaId.DANAR_7, CartaId.DANAR_8, CartaId.DANAR_9, CartaId.DANAR_X, CartaId.DANAR_F, CartaId.DANAR_C, CartaId.DANAR_D,
     CartaId.SPADE_A, CartaId.SPADE_2, CartaId.SPADE_3, CartaId.SPADE_4, CartaId.SPADE_5, CartaId.SPADE_6, CartaId.SPADE_7, CartaId.SPADE_8, CartaId.SPADE_9, CartaId.SPADE_X, CartaId.SPADE_F, CartaId.SPADE_C, CartaId.SPADE_D,
     CartaId.COPPE_A, CartaId.COPPE_2, CartaId.COPPE_3, CartaId.COPPE_4, CartaId.COPPE_5, CartaId.COPPE_6, CartaId.COPPE_7, CartaId.COPPE_8, CartaId.COPPE_9, CartaId.COPPE_X, CartaId.COPPE_F, CartaId.COPPE_C, CartaId.COPPE_D,
     CartaId.BASTO_A, CartaId.BASTO_2, CartaId.BASTO_3, CartaId.BASTO_4, CartaId.BASTO_5, CartaId.BASTO_6, CartaId.BASTO_7, CartaId.BASTO_8, CartaId.BASTO_9, CartaId.BASTO_X, CartaId.BASTO_F, CartaId.BASTO_C, CartaId.BASTO_D]

carte_lunghe = [CartaId.SPADE_A, CartaId.SPADE_2, CartaId.SPADE_3, CartaId.SPADE_4, CartaId.SPADE_5, CartaId.SPADE_6, CartaId.SPADE_7, CartaId.SPADE_8, CartaId.SPADE_9, CartaId.SPADE_X, CartaId.SPADE_F, CartaId.SPADE_C, CartaId.SPADE_D,
     CartaId.BASTO_A, CartaId.BASTO_2, CartaId.BASTO_3, CartaId.BASTO_4, CartaId.BASTO_5, CartaId.BASTO_6, CartaId.BASTO_7, CartaId.BASTO_8, CartaId.BASTO_9, CartaId.BASTO_X, CartaId.BASTO_F, CartaId.BASTO_C, CartaId.BASTO_D]


carte_corte = [CartaId.DANAR_A, CartaId.DANAR_2, CartaId.DANAR_3, CartaId.DANAR_4, CartaId.DANAR_5, CartaId.DANAR_6, CartaId.DANAR_7, CartaId.DANAR_8, CartaId.DANAR_9, CartaId.DANAR_X, CartaId.DANAR_F, CartaId.DANAR_C, CartaId.DANAR_D,
     CartaId.COPPE_A, CartaId.COPPE_2, CartaId.COPPE_3, CartaId.COPPE_4, CartaId.COPPE_5, CartaId.COPPE_6, CartaId.COPPE_7, CartaId.COPPE_8, CartaId.COPPE_9, CartaId.COPPE_X, CartaId.COPPE_F, CartaId.COPPE_C, CartaId.COPPE_D]

denari = [CartaId.DANAR_A, CartaId.DANAR_2, CartaId.DANAR_3, CartaId.DANAR_4, CartaId.DANAR_5, CartaId.DANAR_6, CartaId.DANAR_7, CartaId.DANAR_8, CartaId.DANAR_9, CartaId.DANAR_X, CartaId.DANAR_F, CartaId.DANAR_C, CartaId.DANAR_D, CartaId.DANAR_R]
spade = [CartaId.SPADE_A, CartaId.SPADE_2, CartaId.SPADE_3, CartaId.SPADE_4, CartaId.SPADE_5, CartaId.SPADE_6, CartaId.SPADE_7, CartaId.SPADE_8, CartaId.SPADE_9, CartaId.SPADE_X, CartaId.SPADE_F, CartaId.SPADE_C, CartaId.SPADE_D, CartaId.SPADE_R]
coppe = [CartaId.COPPE_A, CartaId.COPPE_2, CartaId.COPPE_3, CartaId.COPPE_4, CartaId.COPPE_5, CartaId.COPPE_6, CartaId.COPPE_7, CartaId.COPPE_8, CartaId.COPPE_9, CartaId.COPPE_X, CartaId.COPPE_F, CartaId.COPPE_C, CartaId.COPPE_D, CartaId.COPPE_R]
bastoni = [CartaId.BASTO_A, CartaId.BASTO_2, CartaId.BASTO_3, CartaId.BASTO_4, CartaId.BASTO_5, CartaId.BASTO_6, CartaId.BASTO_7, CartaId.BASTO_8, CartaId.BASTO_9, CartaId.BASTO_X, CartaId.BASTO_F, CartaId.BASTO_C, CartaId.BASTO_D, CartaId.BASTO_R]
tarocco = [CartaId.MATTO_0, CartaId.PAPA_I, CartaId.PAPA_II, CartaId.PAPA_III, CartaId.PAPA_IV, CartaId.PAPA_V, CartaId.TEMPER_VI, CartaId.FORZA_VII, CartaId.GIUST_VIII, CartaId.ROTA_IX, CartaId.CARRO_X, CartaId.TEMPO_XI, CartaId.APPESO_XII, CartaId.MORTE_XIII, CartaId.DIAVOLO_XIV,
       CartaId.TORRE_XV, CartaId.SPERANZA_XVI, CartaId.PRUDENZA_XVII , CartaId.FEDE_XVIII, CartaId. CARITA_XIX, CartaId.FUOCO_XX, CartaId.ACQUA_XXI, CartaId.TERRA_XXII, CartaId.ARIA_XXIII, CartaId.BILANCIA_XXIV, CartaId.VERGINE_XXV, CartaId.SCORP_XXVI,
       CartaId.ARIETE_XXVII, CartaId.CAPRIC_XXVIII, CartaId.SAGITT_XXIX, CartaId.CANCRO_XXX, CartaId.PESCI_XXXI, CartaId.ACQUARIO_XXXII, CartaId.LEONE_XXXIII, CartaId.TORO_XXXIV, CartaId.GEMINI_XXXV, CartaId.STELLA_XXXVI, CartaId.LUNA_XXXVII,
       CartaId.SOLE_XXXVIII, CartaId.MONDO_XXXIX, CartaId.TROMBA_XL]

def is_tarocco(c):
    if tarocco.count(c) > 0:
        return True
    return False
