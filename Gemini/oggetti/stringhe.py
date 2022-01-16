'''
Created on 2 gen 2022

@author: david
'''

from decks.carta_id import CartaId
#import gettext
#it = gettext.translation('base', localedir='locale', languages=['it'])
#it.install()
#_ = it.gettext # Greek

def TEMP(s):
    return s
_ = TEMP
 
nomigiocatore = ["Tizio", "Caio", "Sempronio", "Pippo"]


# DBG: Vedere https://phrase.com/blog/posts/translate-python-gnu-gettext/ su come gestire le traduzioni
class Stringhe(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        pass

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
    
    @staticmethod
    def get_card_name(s):
        return Stringhe.card_name[s]
    
    def get_nomi(self):
        return self.nomigiocatore
        