'''
Created on 20 gen 2022

@author: david
'''

import pygame

from grafica.my_sprite import MySprite
from main.globals import *
from pygame.sprite import Sprite
import oggetti.posizioni
from main.exception_man import ExceptionMan


class SpriteMazzo(MySprite):
    top_rect = None
    img_back = None
    img_front = None
    img_back_orig = None
    img_front_orig = None
    visible = None
    _pos_dest = None
    _pos = None
    _angle_dest = None
    _angle = None
    lato_fronte = None

    def __init__(self, img):
        super().__init__("", img=img)
        self.img_back = img.convert()
        self.image = self.img_back
        self.rect = self.img_back.get_rect()
        self.rect.center = (0, 0)
        self._pos_dest = (0, 0)
        self._pos = (0, 0)
        self._angle = 0
        self._angle_dest = 0
        self.visible = False

    def get_nome(self):
        return "Mazzo"

    def hide(self):
        try:
            self.set_visible(False, False, 1)
            echo_message("Nascondi mazzo")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position(self):
        return self.rect.center

    def move(self, pos):
        if self._pos_dest != pos:
            self._pos_dest = pos

    def set_lato(self, coperto=True):
        try:
            if coperto:
                self.image = self.img_back
            #        self.rect = self.image.get_rect()
            #        self.rect.center = (0, 0)
            #        echo_message("Scopri carta")
            #    else:
            #        self.image = self.img_back
            #        self.rect = self.image.get_rect()
            #        self.rect.center = (0, 0)
            #        echo_message("Copri carta")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_position(self, pos, instant=False):
        try:
            self._pos = pos
            self.rect = self.image.get_rect()
            self.rect.center = pos
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, visible, scoperta=False, z=None):
        try:
            self.visible = visible
            self.set_lato(scoperta)
            if self.visible:
                if z is not None:
                    self.z_index = z
            else:
                self.z_index = 0
                #self.rect = self.image.get_rect()
                #self.rect.center = (0, 0)
            self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_coperta(self):
        try:
            if not self.lato_fronte:
                return True
            else:
                return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self):
        try:
            super().update()
            if self.lato_fronte:
                self.image = self.img_front
            else:
                self.image = self.img_back

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_z_index(self):
        return 0

    def get_visible(self):
        return self.visible

    def get_collide(self, mouse):
        return self.rect.collidepoint(mouse)

    def is_animating(self):
        try:
            if self.visible:
                return self._pos != self._pos_dest or self._angle != self._angle_dest
            else:
                return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
