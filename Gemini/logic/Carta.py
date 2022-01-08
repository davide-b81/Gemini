'''
Created on 31 dic 2021

@author: david
'''
from enum import Enum
from pickle import TRUE

class seme(Enum):
    BASTONI = 0,
    COPPE = 1,
    SPADE = 2,
    DENARI = 3,
    TRIONFO = 4
    
class carta(Enum):

    '''
    classdocs
    '''
    MATTO_0 = 0
    
    DANAR_A = 1
    DANAR_2 = 2
    DANAR_3 = 3
    DANAR_4 = 4
    DANAR_5 = 5
    DANAR_6 = 6
    DANAR_7 = 7
    DANAR_8 = 8
    DANAR_9 = 9
    DANAR_X = 10
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

    COPPE_A = 29
    COPPE_2 = 30
    COPPE_3 = 31
    COPPE_4 = 32
    COPPE_5 = 33
    COPPE_6 = 34
    COPPE_7 = 35
    COPPE_8 = 36
    COPPE_9 = 37
    COPPE_X = 38
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
    ARIETE_XXVII =  83
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
    GIUDIZIO_XL = 96

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def NameString(self):
        try:
            return(self.name)
        except Exception as e:
            print("Mazzo: An error occurred:", e.args[0])
            return "?"        
        
        
cartiglie =[carta.DANAR_A, carta.DANAR_2, carta.DANAR_3, carta.DANAR_4, carta.DANAR_5, carta.DANAR_6, carta.DANAR_7, carta.DANAR_8, carta.DANAR_9, carta.DANAR_X, carta.DANAR_F, carta.DANAR_C, carta.DANAR_D,
     carta.SPADE_A, carta.SPADE_2, carta.SPADE_3, carta.SPADE_4, carta.SPADE_5, carta.SPADE_6, carta.SPADE_7, carta.SPADE_8, carta.SPADE_9, carta.SPADE_X, carta.SPADE_F, carta.SPADE_C, carta.SPADE_D,
     carta.COPPE_A, carta.COPPE_2, carta.COPPE_3, carta.COPPE_4, carta.COPPE_5, carta.COPPE_6, carta.COPPE_7, carta.COPPE_8, carta.COPPE_9, carta.COPPE_X, carta.COPPE_F, carta.COPPE_C, carta.COPPE_D,
     carta.BASTO_A, carta.BASTO_2, carta.BASTO_3, carta.BASTO_4, carta.BASTO_5, carta.BASTO_6, carta.BASTO_7, carta.BASTO_8, carta.BASTO_9, carta.BASTO_X, carta.BASTO_F, carta.BASTO_C, carta.BASTO_D]



denari = [carta.DANAR_A, carta.DANAR_2, carta.DANAR_3, carta.DANAR_4, carta.DANAR_5, carta.DANAR_6, carta.DANAR_7, carta.DANAR_8, carta.DANAR_9, carta.DANAR_X, carta.DANAR_F, carta.DANAR_C, carta.DANAR_D, carta.DANAR_R]
spade = [carta.SPADE_A, carta.SPADE_2, carta.SPADE_3, carta.SPADE_4, carta.SPADE_5, carta.SPADE_6, carta.SPADE_7, carta.SPADE_8, carta.SPADE_9, carta.SPADE_X, carta.SPADE_F, carta.SPADE_C, carta.SPADE_D, carta.SPADE_R]
coppe = [carta.COPPE_A, carta.COPPE_2, carta.COPPE_3, carta.COPPE_4, carta.COPPE_5, carta.COPPE_6, carta.COPPE_7, carta.COPPE_8, carta.COPPE_9, carta.COPPE_X, carta.COPPE_F, carta.COPPE_C, carta.COPPE_D, carta.COPPE_R]
bastoni = [carta.BASTO_A, carta.BASTO_2, carta.BASTO_3, carta.BASTO_4, carta.BASTO_5, carta.BASTO_6, carta.BASTO_7, carta.BASTO_8, carta.BASTO_9, carta.BASTO_X, carta.BASTO_F, carta.BASTO_C, carta.BASTO_D, carta.BASTO_R]
tar = [carta.MATTO_0, carta.PAPA_I, carta.PAPA_II, carta.PAPA_III, carta.PAPA_IV, carta.PAPA_V, carta.TEMPER_VI, carta.FORZA_VII, carta.GIUST_VIII, carta.ROTA_IX, carta.CARRO_X, carta.TEMPO_XI, carta.APPESO_XII, carta.MORTE_XIII, carta.DIAVOLO_XIV,
       carta.TORRE_XV, carta.SPERANZA_XVI, carta.PRUDENZA_XVII , carta.FEDE_XVIII, carta. CARITA_XIX, carta.FUOCO_XX, carta.ACQUA_XXI, carta.TERRA_XXII, carta.ARIA_XXIII, carta.BILANCIA_XXIV, carta.VERGINE_XXV, carta.SCORP_XXVI,
       carta.ARIETE_XXVII, carta.CAPRIC_XXVIII, carta.SAGITT_XXIX, carta.CANCRO_XXX, carta.PESCI_XXXI, carta.ACQUARIO_XXXII, carta.LEONE_XXXIII, carta.TORO_XXXIV, carta.GEMINI_XXXV, carta.STELLA_XXXVI, carta.LUNA_XXXVII,
       carta.SOLE_XXXVIII, carta.MONDO_XXXIX, carta.GIUDIZIO_XL]

def IsCartiglia(a):
    try:
        if cartiglie.__contains__(a):
            return True
    except Exception as e:
        print("IsCartiglia: An error occurred:", e.args[0])
    return False
    
def GetSeme(a):
    try:
        if (denari.__contains__(a)):
            return seme.DENARI.value
        elif (spade.__contains__(a)):
            return seme.SPADE.value
        elif (coppe.__contains__(a)):
            return seme.COPPE.value
        elif (bastoni.__contains__(a)):
            return seme.BASTONI.value
        else:
            return seme.TRIONFO.value
    except Exception as e:
        print("GetSeme: An error occurred:", e.args[0])
        return seme.DENARI

def GetNumerale(a):
    if (a.value == carta.MATTO_0):
        return 0
    elif (a.value <= carta.DANAR_R.value):
        return a.value
    elif (a.value <= carta.SPADE_R.value):
        return a.value - carta.SPADE_A.value + 1
    elif (a.value <= carta.COPPE_R.value):
        return a.value - carta.COPPE_A.value + 1
    elif (a.value <= carta.BASTO_R.value):
        return a.value - carta.BASTO_A.value + 1
    else:
        return a.value - carta.PAPA_I.value + 1

'''
'''
def GetGreater(a, b):
    try:
        if (a == None):
            return b
        elif (b == None):
            return a
        elif (GetSeme(a) == GetSeme(b)):
            if (GetNumerale(a) >= GetNumerale(b)):
                return a
            else:
                return b
        elif (GetSeme(a) == seme.TRIONFO.value):
            return a
        elif (GetSeme(b) == seme.TRIONFO.value):
                return b
        elif (GetNumerale(a) == GetNumerale(b)):
            if (GetSeme(a) > GetSeme(b)):
                return a
            else:
                return b
        elif (GetNumerale(a) > GetNumerale(b)):
            return a
        else:
            return b
    except Exception as e:
        print("GetGreater: An error occurred:", e.args[0])
        
        return a

