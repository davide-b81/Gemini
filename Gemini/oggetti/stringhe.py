'''
Created on 2 gen 2022

@author: david
'''

from Logic.Carta import carta

nomigiocatore = ["Tizio", "Caio", "Sempronio", "Pippo"]


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
    card_name[carta.DANAR_A] = "Asso di Denari"
    card_name[carta.DANAR_2] = "Due di Denari"
    card_name[carta.DANAR_3] = "Tre di Denari"
    card_name[carta.DANAR_4] = "Quattro di Denari"
    card_name[carta.DANAR_5] = "Cinque di Denari"
    card_name[carta.DANAR_6] = "Sei di Denari"
    card_name[carta.DANAR_7] = "Sette di Denari"
    card_name[carta.DANAR_8] = "Otto di Denari"
    card_name[carta.DANAR_9] = "Nove di Denari"
    card_name[carta.DANAR_X] = "Dieci di Denari"
    card_name[carta.DANAR_F] = "Fante di Denari"
    card_name[carta.DANAR_C] = "Cavallo di Denari"
    card_name[carta.DANAR_D] = "Regina di Denari"
    card_name[carta.DANAR_R] = "Re di Denari"
    card_name[carta.SPADE_A] = "Asso di Spade"
    card_name[carta.SPADE_2] = "Due di Spade"
    card_name[carta.SPADE_3] = "Tre di Spade"
    card_name[carta.SPADE_4] = "Quattro di Spade"
    card_name[carta.SPADE_5] = "Cinque di Spade"
    card_name[carta.SPADE_6] = "Sei di Spade"
    card_name[carta.SPADE_7] = "Sette di Spade"
    card_name[carta.SPADE_8] = "Otto di Spade"
    card_name[carta.SPADE_9] = "Nove di Spade"
    card_name[carta.SPADE_X] = "Dieci di Spade"
    card_name[carta.SPADE_F] = "Fante di Spade"
    card_name[carta.SPADE_C] = "Cavallo di Spade"
    card_name[carta.SPADE_D] = "Regina di Spade"
    card_name[carta.SPADE_R] = "Re di Spade"
    card_name[carta.COPPE_A] = "Asso di Coppe"
    card_name[carta.COPPE_2] = "Due di Coppe"
    card_name[carta.COPPE_3] = "Tre di Coppe"
    card_name[carta.COPPE_4] = "Quattro di Coppe"
    card_name[carta.COPPE_5] = "Cinque di Coppe"
    card_name[carta.COPPE_6] = "Sei di Coppe"
    card_name[carta.COPPE_7] = "Sette di Coppe"
    card_name[carta.COPPE_8] = "Otto di Coppe"
    card_name[carta.COPPE_9] = "Nove di Coppe"
    card_name[carta.COPPE_X] = "Dieci di Coppe"
    card_name[carta.COPPE_F] = "Fante di Coppe"
    card_name[carta.COPPE_C] = "Cavallo di Coppe"
    card_name[carta.COPPE_D] = "Regina di Coppe"
    card_name[carta.COPPE_R] = "Re di Coppe"
    card_name[carta.BASTO_A] = "Asso di Bastoni"
    card_name[carta.BASTO_2] = "Due di Bastoni"
    card_name[carta.BASTO_3] = "Tre di Bastoni"
    card_name[carta.BASTO_4] = "Quattro di Bastoni"
    card_name[carta.BASTO_5] = "Cinque di Bastoni"
    card_name[carta.BASTO_6] = "Sei di Bastoni"
    card_name[carta.BASTO_7] = "Sette di Bastoni"
    card_name[carta.BASTO_8] = "Otto di Bastoni"
    card_name[carta.BASTO_9] = "Nove di Bastoni"
    card_name[carta.BASTO_X] = "Dieci di Bastoni"
    card_name[carta.BASTO_F] = "Fante di Bastoni"
    card_name[carta.BASTO_C] = "Cavallo di Bastoni"
    card_name[carta.BASTO_D] = "Regina di Bastoni"
    card_name[carta.BASTO_R] = "Re di Bastoni"
    card_name[carta.MATTO_0] = "Il Matto"
    card_name[carta.PAPA_I] = " Papa I" 
    card_name[carta.PAPA_II] = "Papa II"
    card_name[carta.PAPA_III] = "Papa III"
    card_name[carta.PAPA_IV] = "Papa IV"
    card_name[carta.PAPA_V] = "Papa V"
    card_name[carta.TEMPER_VI] = "La Temperanza"
    card_name[carta.FORZA_VII] = "La Forza"
    card_name[carta.GIUST_VIII] = "La Giustizia"
    card_name[carta.ROTA_IX] = "La Ruota di Fortuna"
    card_name[carta.CARRO_X] = "Il Carro"
    card_name[carta.TEMPO_XI] = "Il Tempo"
    card_name[carta.APPESO_XII] = "L'Appeso"
    card_name[carta.MORTE_XIII] = "XIII"
    card_name[carta.DIAVOLO_XIV] = "Il Diavolo"
    card_name[carta.TORRE_XV] = "La Torre"
    card_name[carta.SPERANZA_XVI] = "La Speranza"
    card_name[carta.PRUDENZA_XVII] = "La Prudenza"
    card_name[carta.FEDE_XVIII] = "La Fede"
    card_name[carta.CARITA_XIX] = "La Carita'"
    card_name[carta.FUOCO_XX] = "Il Fuoco"
    card_name[carta.ACQUA_XXI] = "L'Acqua"
    card_name[carta.TERRA_XXII] = "La Terra"
    card_name[carta.ARIA_XXIII] = "L'Aria"
    card_name[carta.BILANCIA_XXIV] = "La Bilancia"
    card_name[carta.VERGINE_XXV] = "La Vergine"
    card_name[carta.SCORP_XXVI] = "Lo Scorpione"
    card_name[carta.ARIETE_XXVII] = "L'Ariete" 
    card_name[carta.CAPRIC_XXVIII] = "Il Capricorno"
    card_name[carta.SAGITT_XXIX] = "Il Sagittario"
    card_name[carta.CANCRO_XXX] = "Il Cancro"
    card_name[carta.PESCI_XXXI] = "I Pesci"
    card_name[carta.ACQUARIO_XXXII] = "L'Acquario"
    card_name[carta.LEONE_XXXIII] = "Il Leone"
    card_name[carta.TORO_XXXIV] = "Il Toro"
    card_name[carta.GEMINI_XXXV] = "I Gemelli"
    card_name[carta.STELLA_XXXVI] = "La Stella"
    card_name[carta.LUNA_XXXVII] = "La Luna"
    card_name[carta.SOLE_XXXVIII] = "Il Sole"
    card_name[carta.MONDO_XXXIX] = "Il Mondo"
    card_name[carta.GIUDIZIO_XL] = "La Tromba"
    
    @staticmethod
    def get_card_name(s):
        return Stringhe.card_name[s]
    
    def get_nomi(self):
        return self.nomigiocatore
        