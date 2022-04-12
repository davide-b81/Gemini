'''
Created on 6 gen 2022

@author: david
'''
from decks.carta_id import CartaId
from grafica.my_sprite import MySprite
from main.globals import *
from cmath import cos
from math import radians
import pygame
from pygame import SRCALPHA

from main.exception_man import ExceptionMan

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class SpriteCarta(MySprite):
    '''
    classdocs
    '''
    ROTATE_STEP = 10
    MOVE_STEP = 18
    REFRESH_PERIOD = 0.02

    _cid = None
    img_back = None
    img_front = None
    img_back_orig = None
    img_front_orig = None

    def __init__(self, cid : CartaId, img, imgback=None):
        '''
        Constructor
        '''
        try:
            super().__init__(str(cid), img)
            self._hoverable = True
            self.img_front_orig = img.convert()
            self.img_back_orig = imgback.convert()
            self.img_front = self.img_front_orig
            self.img_back = self.img_back_orig
            self.image = self.img_back
            self._size = self.image.get_size()
            self.rect.center = self._pos
            self._cid = cid
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_image_current(self, image):
        try:
            assert image is not None
            self.image = image
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_coperta(self):
        try:
            if self._asse_dest > DEG_CLOC_RECT:
                return False
            return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_cid(self):
        return self._cid

    def copri(self):
        try:
            self.set_asse(DEG_SIDE_BACK, True)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri(self):
        try:
            self.set_asse(DEG_SIDE_FRONT, True)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self, *args, **kwargs):
        try:
            super().update(args, kwargs)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def draw_image(self):
        try:
            if self._asse == DEG_SIDE_FRONT:
                self.image = self.img_front
            elif self._asse == DEG_SIDE_BACK:
                self.image = self.img_back
            else:
                w = cos(radians(self._asse)) * self._size[0]
                siz = ((abs(w.real), self._size[1]))
                if self._asse > DEG_SIDE_FRONT / 2:
                    self.image = pygame.transform.scale(self.img_front, siz)
                else:
                    self.image = pygame.transform.scale(self.img_back, siz)

            self.set_image_current(self.image)

            super().draw_image()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)