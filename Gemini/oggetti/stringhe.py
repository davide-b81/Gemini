'''
Created on 2 gen 2022

@author: david
'''

from game.germini.carta import Carta
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
    card_name[Carta.DANAR_A] = "Asso di Denari"
    card_name[Carta.DANAR_2] = "Due di Denari"
    card_name[Carta.DANAR_3] = "Tre di Denari"
    card_name[Carta.DANAR_4] = "Quattro di Denari"
    card_name[Carta.DANAR_5] = "Cinque di Denari"
    card_name[Carta.DANAR_6] = "Sei di Denari"
    card_name[Carta.DANAR_7] = "Sette di Denari"
    card_name[Carta.DANAR_8] = "Otto di Denari"
    card_name[Carta.DANAR_9] = "Nove di Denari"
    card_name[Carta.DANAR_X] = "Dieci di Denari"
    card_name[Carta.DANAR_F] = "Fantina di Denari"
    card_name[Carta.DANAR_C] = "Cavallo di Denari"
    card_name[Carta.DANAR_D] = "Regina di Denari"
    card_name[Carta.DANAR_R] = "Re di Denari"
    card_name[Carta.SPADE_A] = "Asso di Spade"
    card_name[Carta.SPADE_2] = "Due di Spade"
    card_name[Carta.SPADE_3] = "Tre di Spade"
    card_name[Carta.SPADE_4] = "Quattro di Spade"
    card_name[Carta.SPADE_5] = "Cinque di Spade"
    card_name[Carta.SPADE_6] = "Sei di Spade"
    card_name[Carta.SPADE_7] = "Sette di Spade"
    card_name[Carta.SPADE_8] = "Otto di Spade"
    card_name[Carta.SPADE_9] = "Nove di Spade"
    card_name[Carta.SPADE_X] = "Dieci di Spade"
    card_name[Carta.SPADE_F] = "Fante di Spade"
    card_name[Carta.SPADE_C] = "Cavallo di Spade"
    card_name[Carta.SPADE_D] = "Regina di Spade"
    card_name[Carta.SPADE_R] = "Re di Spade"
    card_name[Carta.COPPE_A] = "Asso di Coppe"
    card_name[Carta.COPPE_2] = "Due di Coppe"
    card_name[Carta.COPPE_3] = "Tre di Coppe"
    card_name[Carta.COPPE_4] = "Quattro di Coppe"
    card_name[Carta.COPPE_5] = "Cinque di Coppe"
    card_name[Carta.COPPE_6] = "Sei di Coppe"
    card_name[Carta.COPPE_7] = "Sette di Coppe"
    card_name[Carta.COPPE_8] = "Otto di Coppe"
    card_name[Carta.COPPE_9] = "Nove di Coppe"
    card_name[Carta.COPPE_X] = "Dieci di Coppe"
    card_name[Carta.COPPE_F] = "Fantina di Coppe"
    card_name[Carta.COPPE_C] = "Cavallo di Coppe"
    card_name[Carta.COPPE_D] = "Regina di Coppe"
    card_name[Carta.COPPE_R] = "Re di Coppe"
    card_name[Carta.BASTO_A] = "Asso di Bastoni"
    card_name[Carta.BASTO_2] = "Due di Bastoni"
    card_name[Carta.BASTO_3] = "Tre di Bastoni"
    card_name[Carta.BASTO_4] = "Quattro di Bastoni"
    card_name[Carta.BASTO_5] = "Cinque di Bastoni"
    card_name[Carta.BASTO_6] = "Sei di Bastoni"
    card_name[Carta.BASTO_7] = "Sette di Bastoni"
    card_name[Carta.BASTO_8] = "Otto di Bastoni"
    card_name[Carta.BASTO_9] = "Nove di Bastoni"
    card_name[Carta.BASTO_X] = "Dieci di Bastoni"
    card_name[Carta.BASTO_F] = "Fante di Bastoni"
    card_name[Carta.BASTO_C] = "Cavallo di Bastoni"
    card_name[Carta.BASTO_D] = "Regina di Bastoni"
    card_name[Carta.BASTO_R] = "Re di Bastoni"
    card_name[Carta.MATTO_0] = "Il Matto"
    card_name[Carta.PAPA_I] = " Il Papino" 
    card_name[Carta.PAPA_II] = "Il Granduca"
    card_name[Carta.PAPA_III] = "L'Imperatore"
    card_name[Carta.PAPA_IV] = "L'imperatrice"
    card_name[Carta.PAPA_V] = "L'Innamorato"
    card_name[Carta.TEMPER_VI] = "La Temperanza"
    card_name[Carta.FORZA_VII] = "La Forza"
    card_name[Carta.GIUST_VIII] = "La Giustizia"
    card_name[Carta.ROTA_IX] = "La Ruota di Fortuna"
    card_name[Carta.CARRO_X] = "Il Carro"
    card_name[Carta.TEMPO_XI] = "Il Gobbo"
    card_name[Carta.APPESO_XII] = "L'Appeso"
    card_name[Carta.MORTE_XIII] = "XIII"
    card_name[Carta.DIAVOLO_XIV] = "Il Diavolo"
    card_name[Carta.TORRE_XV] = "La Casa del Diavolo"
    card_name[Carta.SPERANZA_XVI] = "La Speranza"
    card_name[Carta.PRUDENZA_XVII] = "La Prudenza"
    card_name[Carta.FEDE_XVIII] = "La Fede"
    card_name[Carta.CARITA_XIX] = "La Carita'"
    card_name[Carta.FUOCO_XX] = "Il Fuoco"
    card_name[Carta.ACQUA_XXI] = "L'Acqua"
    card_name[Carta.TERRA_XXII] = "La Terra"
    card_name[Carta.ARIA_XXIII] = "L'Aria"
    card_name[Carta.BILANCIA_XXIV] = "La Bilancia"
    card_name[Carta.VERGINE_XXV] = "La Vergine"
    card_name[Carta.SCORP_XXVI] = "Lo Scorpione"
    card_name[Carta.ARIETE_XXVII] = "L'Ariete" 
    card_name[Carta.CAPRIC_XXVIII] = "Il Capricorno"
    card_name[Carta.SAGITT_XXIX] = "Il Sagittario"
    card_name[Carta.CANCRO_XXX] = "Il Cancro"
    card_name[Carta.PESCI_XXXI] = "I Pesci"
    card_name[Carta.ACQUARIO_XXXII] = "L'Acquario"
    card_name[Carta.LEONE_XXXIII] = "Il Leone"
    card_name[Carta.TORO_XXXIV] = "Il Toro"
    card_name[Carta.GEMINI_XXXV] = "I Gemelli"
    card_name[Carta.STELLA_XXXVI] = "La Stella"
    card_name[Carta.LUNA_XXXVII] = "La Luna"
    card_name[Carta.SOLE_XXXVIII] = "Il Sole"
    card_name[Carta.MONDO_XXXIX] = "Il Mondo"
    card_name[Carta.GIUDIZIO_XL] = "La Tromba"
    
    @staticmethod
    def get_card_name(s):
        return Stringhe.card_name[s]
    
    def get_nomi(self):
        return self.nomigiocatore
        