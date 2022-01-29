'''
Created on 2 gen 2022

@author: david

Requirements:

python3 -m pip install Pillow

'''
from decks import carta
from tkinter import PhotoImage

class Foto(object):
    '''
    classdocs
    '''

    imgs = []
    
    dict_files = {
        carta.DANAR_A : "MF_DA.gif",
        carta.DANAR_2 : "MF_D2.gif",
        carta.DANAR_3 : "MF_D3.gif",  
        carta.DANAR_4 : "MF_D4.gif",  
        carta.DANAR_5 : "MF_D5.gif",  
        carta.DANAR_6 : "MF_D6.gif",  
        carta.DANAR_7 : "MF_D7.gif",  
        carta.DANAR_8 : "MF_D8.gif",  
        carta.DANAR_9 : "MF_D9.gif",  
        carta.DANAR_X : "MF_DX.gif",  
        carta.DANAR_F : "MF_DF.gif",  
        carta.DANAR_C : "MF_DC.gif",  
        carta.DANAR_D : "MF_DD.gif",  
        carta.DANAR_R : "MF_DR.gif",  
        carta.SPADE_A : "MF_SA.gif",  
        carta.SPADE_2 : "MF_S2.gif",  
        carta.SPADE_3 : "MF_S3.gif",  
        carta.SPADE_4 : "MF_S4.gif",  
        carta.SPADE_5 : "MF_S5.gif",  
        carta.SPADE_6 : "MF_S6.gif",  
        carta.SPADE_7 : "MF_S7.gif",  
        carta.SPADE_8 : "MF_S8.gif",  
        carta.SPADE_9 : "MF_S9.gif",  
        carta.SPADE_X : "MF_SX.gif",  
        carta.SPADE_F : "MF_SF.gif",  
        carta.SPADE_C : "MF_SC.gif",  
        carta.SPADE_D : "MF_SD.gif",  
        carta.SPADE_R : "MF_SR.gif",  
        carta.COPPE_A : "MF_CA.gif",  
        carta.COPPE_2 : "MF_C2.gif",  
        carta.COPPE_3 : "MF_C3.gif",  
        carta.COPPE_4 : "MF_C4.gif",  
        carta.COPPE_5 : "MF_C5.gif",  
        carta.COPPE_6 : "MF_C6.gif",  
        carta.COPPE_7 : "MF_C7.gif",  
        carta.COPPE_8 : "MF_C8.gif",  
        carta.COPPE_9 : "MF_C9.gif",  
        carta.COPPE_X : "MF_CX.gif",  
        carta.COPPE_F : "MF_CF.gif",  
        carta.COPPE_C : "MF_CC.gif",  
        carta.COPPE_D : "MF_CD.gif",  
        carta.COPPE_R : "MF_CR.gif",  
        carta.BASTO_A : "MF_BA.gif",  
        carta.BASTO_2 : "MF_B2.gif",  
        carta.BASTO_3 : "MF_B3.gif",  
        carta.BASTO_4 : "MF_B4.gif",  
        carta.BASTO_5 : "MF_B5.gif",  
        carta.BASTO_6 : "MF_B6.gif",  
        carta.BASTO_7 : "MF_B7.gif",  
        carta.BASTO_8 : "MF_B8.gif",  
        carta.BASTO_9 : "MF_B9.gif",  
        carta.BASTO_X : "MF_BX.gif",  
        carta.BASTO_F : "MF_BF.gif",  
        carta.BASTO_C : "MF_BC.gif",  
        carta.BASTO_D : "MF_BD.gif",  
        carta.BASTO_R : "MF_BR.gif",  
        carta.MATTO_0 : "MF_T0.gif",  
        carta.PAPA_I : "MF_T1.gif",   
        carta.PAPA_II : "MF_T2.gif",  
        carta.PAPA_III : "MF_T3.gif", 
        carta.PAPA_IV : "MF_T4.gif",  
        carta.PAPA_V : "MF_T5.gif",                 
        carta.TEMPER_VI : "MF_T6.gif",              
        carta.FORZA_VII : "MF_T7.gif",              
        carta.GIUST_VIII : "MF_T8.gif",             
        carta.ROTA_IX : "MF_T9.gif",                
        carta.CARRO_X : "MF_T10.gif",                
        carta.TEMPO_XI : "MF_T11.gif",               
        carta.APPESO_XII : "MF_T12.gif",             
        carta.MORTE_XIII : "MF_T13.gif",             
        carta.DIAVOLO_XIV : "MF_T14.gif",            
        carta.TORRE_XV : "MF_T15.gif",               
        carta.SPERANZA_XVI : "MF_T16.gif",           
        carta.PRUDENZA_XVII : "MF_T17.gif",          
        carta.FEDE_XVIII : "MF_T18.gif",             
        carta.CARITA_XIX : "MF_T19.gif",             
        carta.FUOCO_XX : "MF_T20.gif",               
        carta.ACQUA_XXI : "MF_T21.gif",              
        carta.TERRA_XXII : "MF_T22.gif",             
        carta.ARIA_XXIII : "MF_T23.gif",             
        carta.BILANCIA_XXIV : "MF_T24.gif",          
        carta.VERGINE_XXV : "MF_T25.gif",            
        carta.SCORP_XXVI : "MF_T26.gif",             
        carta.ARIETE_XXVII : "MF_T27.gif",           
        carta.CAPRIC_XXVIII : "MF_T28.gif",          
        carta.SAGITT_XXIX : "MF_T29.gif",            
        carta.CANCRO_XXX : "MF_T30.gif",             
        carta.PESCI_XXXI : "MF_T31.gif",             
        carta.ACQUARIO_XXXII : "MF_T32.gif",         
        carta.LEONE_XXXIII : "MF_T33.gif",           
        carta.TORO_XXXIV : "MF_T34.gif",             
        carta.GEMINI_XXXV : "MF_T35.gif",            
        carta.STELLA_XXXVI : "MF_T36.gif",           
        carta.LUNA_XXXVII : "MF_T37.gif",            
        carta.SOLE_XXXVIII : "MF_T38.gif",           
        carta.MONDO_XXXIX : "MF_T39.gif",            
        carta.GIUDIZIO_XL : "MF_T40.gif"  
        }
        
    def getgif(self, c):
        return self.imgs[0]

    def __init__(self):
        '''
        Constructor
        '''
        for key, value in Foto.dict_files.items():
            echo_message("Load " + key._name)
            self.imgs.append(PhotoImage(file="images\\"+value))
            