'''
Created on 3 gen 2022

@author: david
'''
from importlib import resources

from decks.carta import CartaId as c
import pygame
from main.exception_man import ExceptionMan

class ImageManager(object):
    '''
    classdocs
    '''
    
    imgs = {}
    img_retro = None
    img_background = None
    img_popup = None
    img_tokenD = None
    img_tokenM = None
    image_name = {}
    retro_name = "retro.gif"
    background_name = "Sfondo.gif"
    popupbackgnd_name = "4806075532_c9356c8aaa_o.gif"
    token_deal = "tokenD.gif"
    token_mano = "tokenM.gif"
    token_cade = "tokenC.gif"
    token_fola = "tokenF.gif"

    def __init__(self, card_size):
        try:
            '''
            Constructor
            '''
            self.image_name[c.DANAR_A] = "MF_DA.gif"
            self.image_name[c.DANAR_2] = "MF_D2.gif"
            self.image_name[c.DANAR_3] = "MF_D3.gif"
            self.image_name[c.DANAR_4] = "MF_D4.gif"
            self.image_name[c.DANAR_5] = "MF_D5.gif"
            self.image_name[c.DANAR_6] = "MF_D6.gif"
            self.image_name[c.DANAR_7] = "MF_D7.gif"
            self.image_name[c.DANAR_8] = "MF_D8.gif"
            self.image_name[c.DANAR_9] = "MF_D9.gif"
            self.image_name[c.DANAR_X] = "MF_DX.gif"
            self.image_name[c.DANAR_F] = "MF_DF.gif"
            self.image_name[c.DANAR_C] = "MF_DC.gif"
            self.image_name[c.DANAR_D] = "MF_DD.gif"
            self.image_name[c.DANAR_R] = "MF_DR.gif"
            self.image_name[c.SPADE_A] = "MF_SA.gif"
            self.image_name[c.SPADE_2] = "MF_S2.gif"
            self.image_name[c.SPADE_3] = "MF_S3.gif"
            self.image_name[c.SPADE_4] = "MF_S4.gif"
            self.image_name[c.SPADE_5] = "MF_S5.gif"
            self.image_name[c.SPADE_6] = "MF_S6.gif"
            self.image_name[c.SPADE_7] = "MF_S7.gif"
            self.image_name[c.SPADE_8] = "MF_S8.gif"
            self.image_name[c.SPADE_9] = "MF_S9.gif"
            self.image_name[c.SPADE_X] = "MF_SX.gif"
            self.image_name[c.SPADE_F] = "MF_SF.gif"
            self.image_name[c.SPADE_C] = "MF_SC.gif"
            self.image_name[c.SPADE_D] = "MF_SD.gif"
            self.image_name[c.SPADE_R] = "MF_SR.gif"
            self.image_name[c.COPPE_A] = "MF_CA.gif"
            self.image_name[c.COPPE_2] = "MF_C2.gif"
            self.image_name[c.COPPE_3] = "MF_C3.gif"
            self.image_name[c.COPPE_4] = "MF_C4.gif"
            self.image_name[c.COPPE_5] = "MF_C5.gif"
            self.image_name[c.COPPE_6] = "MF_C6.gif"
            self.image_name[c.COPPE_7] = "MF_C7.gif"
            self.image_name[c.COPPE_8] = "MF_C8.gif"
            self.image_name[c.COPPE_9] = "MF_C9.gif"
            self.image_name[c.COPPE_X] = "MF_CX.gif"
            self.image_name[c.COPPE_F] = "MF_CF.gif"
            self.image_name[c.COPPE_C] = "MF_CC.gif"
            self.image_name[c.COPPE_D] = "MF_CD.gif"
            self.image_name[c.COPPE_R] = "MF_CR.gif"
            self.image_name[c.BASTO_A] = "MF_BA.gif"
            self.image_name[c.BASTO_2] = "MF_B2.gif"
            self.image_name[c.BASTO_3] = "MF_B3.gif"
            self.image_name[c.BASTO_4] = "MF_B4.gif"
            self.image_name[c.BASTO_5] = "MF_B5.gif"
            self.image_name[c.BASTO_6] = "MF_B6.gif"
            self.image_name[c.BASTO_7] = "MF_B7.gif"
            self.image_name[c.BASTO_8] = "MF_B8.gif"
            self.image_name[c.BASTO_9] = "MF_B9.gif"
            self.image_name[c.BASTO_X] = "MF_BX.gif"
            self.image_name[c.BASTO_F] = "MF_BF.gif"
            self.image_name[c.BASTO_C] = "MF_BC.gif"
            self.image_name[c.BASTO_D] = "MF_BD.gif"
            self.image_name[c.BASTO_R] = "MF_BR.gif"
            self.image_name[c.MATTO_0] = "MF_T0.gif"
            self.image_name[c.PAPA_I] = "MF_T1.gif"
            self.image_name[c.PAPA_II] = "MF_T2.gif"
            self.image_name[c.PAPA_III] = "MF_T3.gif"
            self.image_name[c.PAPA_IV] = "MF_T4.gif"
            self.image_name[c.PAPA_V] = "MF_T5.gif"
            self.image_name[c.TEMPER_VI] = "MF_T6.gif"
            self.image_name[c.FORZA_VII] = "MF_T7.gif"
            self.image_name[c.GIUST_VIII] = "MF_T8.gif"
            self.image_name[c.ROTA_IX] = "MF_T9.gif"
            self.image_name[c.CARRO_X] = "MF_T10.gif"
            self.image_name[c.TEMPO_XI] = "MF_T11.gif"
            self.image_name[c.APPESO_XII] = "MF_T12.gif"
            self.image_name[c.MORTE_XIII] = "MF_T13.gif"
            self.image_name[c.DIAVOLO_XIV] = "MF_T14.gif"
            self.image_name[c.TORRE_XV] = "MF_T15.gif"
            self.image_name[c.SPERANZA_XVI] = "MF_T16.gif"
            self.image_name[c.PRUDENZA_XVII] = "MF_T17.gif"
            self.image_name[c.FEDE_XVIII] = "MF_T18.gif"
            self.image_name[c.CARITA_XIX] = "MF_T19.gif"
            self.image_name[c.FUOCO_XX] = "MF_T20.gif"
            self.image_name[c.ACQUA_XXI] = "MF_T21.gif"
            self.image_name[c.TERRA_XXII] = "MF_T22.gif"
            self.image_name[c.ARIA_XXIII] = "MF_T23.gif"
            self.image_name[c.BILANCIA_XXIV] = "MF_T24.gif"
            self.image_name[c.VERGINE_XXV] = "MF_T25.gif"
            self.image_name[c.SCORP_XXVI] = "MF_T26.gif"
            self.image_name[c.ARIETE_XXVII] = "MF_T27.gif"
            self.image_name[c.CAPRIC_XXVIII] = "MF_T28.gif"
            self.image_name[c.SAGITT_XXIX] = "MF_T29.gif"
            self.image_name[c.CANCRO_XXX] = "MF_T30.gif"
            self.image_name[c.PESCI_XXXI] = "MF_T31.gif"
            self.image_name[c.ACQUARIO_XXXII] = "MF_T32.gif"
            self.image_name[c.LEONE_XXXIII] = "MF_T33.gif"
            self.image_name[c.TORO_XXXIV] = "MF_T34.gif"
            self.image_name[c.GEMINI_XXXV] = "MF_T35.gif"
            self.image_name[c.STELLA_XXXVI] = "MF_T36.gif"
            self.image_name[c.LUNA_XXXVII] = "MF_T37.gif"
            self.image_name[c.SOLE_XXXVIII] = "MF_T38.gif"
            self.image_name[c.MONDO_XXXIX] = "MF_T39.gif"
            self.image_name[c.TROMBA_XL] = "MF_T40.gif"

            for key in self.image_name:
                path = resources.path('images', self.image_name[key])
                img = pygame.image.load(path)
                self.imgs[key] = pygame.transform.scale(img, card_size)
                assert self.imgs[key] is not None

            path = resources.path('images', self.retro_name)
            img = pygame.image.load(path)
            self.img_retro = pygame.transform.scale(img, card_size)
            assert self.img_retro is not None

            path = resources.path('images', self.background_name)
            self.img_background = pygame.image.load(path)
            assert self.img_background is not None

            path = resources.path('images', self.popupbackgnd_name)
            self.img_popup = pygame.image.load(path)
            assert self.img_popup is not None

            # Tokens
            path = resources.path('images', self.token_deal)
            self.img_tokenD = pygame.image.load(path)

            path = resources.path('images', self.token_mano)
            self.img_tokenM = pygame.image.load(path)

            path = resources.path('images', self.token_cade)
            self.img_tokenC = pygame.image.load(path)

            path = resources.path('images', self.token_fola)
            self.img_tokenF = pygame.image.load(path)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_image_tokenD(self):
        try:
            return self.img_tokenD
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_image_tokenM(self):
        try:
            return self.img_tokenM
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_image_tokenF(self):
        try:
            return self.img_tokenF
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_image_tokenC(self):
        try:
            return self.img_tokenC
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_image_ca(self, c):
        try:
            return self.imgs[c]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_popup_image(self):
        try:
            return self.img_popup
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_background_image(self):
        try:
            return self.img_background
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_retro(self):
        try:
            return self.img_retro
        except Exception as e:
            ExceptionMan.manage_exception("Error. ", e, True)