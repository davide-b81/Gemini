'''
Created on 6 gen 2022

@author: david
'''
from main.globals import *
from cmath import cos
from math import radians
import pygame
from pygame import SRCALPHA

from main.exception_man import ExceptionMan

class MySprite(pygame.sprite.Sprite):
    '''
    classdocs
    '''
    ROTATE_STEP = 10
    MOVE_STEP = 18

    REFRESH_PERIOD = 0.02

    _name = None

    _z_index = None
    _img_dorso = None
    _img_fronte = None

    _img_dorso_orig = None
    _img_fronte_orig = None

    rect = None
    _size = None

    _visible = None
    _blink = None

    _angle = None
    _angle_dest = None

    _pos = None
    _pos_dest = None

    _asse = None
    _asse_dest = None
    _stable_draw = None

    def __init__(self, name, img):
        try:
            super().update()
            '''
            Constructor
            '''
            pygame.sprite.Sprite.__init__(self)
            self._name = name
            self._stable_draw = False
            self.reset()
            self._pos = (0, 0)
            self._pos_dest = (0, 0)
            self.image = img
            self.rect = self.image.get_rect()
            self._visible = False
            self._blink = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def __str__(self):
        try:
            return self._name
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_name(self):
        try:
            return self._name
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def nascondi(self):
        try:
            self.set_visible(False)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra(self):
        try:
            self.set_visible(True)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_front(self):
        try:
            return self._asse > DEG_SIDE_FRONT / 2
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_lato(self, coperta, inst=True):
        try:
            if coperta:
                self._asse_dest = DEG_SIDE_BACK
            else:
                self._asse_dest = DEG_SIDE_FRONT
            if inst:
                self._asse = self._asse_dest
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_visible(self):
        try:
            return self._visible
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, visible=True):
        try:
            self._visible = visible
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position(self):
        try:
            return self._pos
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_stable(self):
        try:
            self.update_stable()
            return self._stable_draw
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def move_to(self, x, y):
        try:
            self._pos = (x, y)
            self._pos_dest = (x, y)
            self.rect = self.image.get_rect()
            self.rect.x = self._pos[0]
            self.rect.y = self._pos[1]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_position(self, pos, inst=False):
        try:
            if inst and self._pos_dest != pos:
                self._pos_dest = pos
                self._pos = pos
            elif self._pos_dest != pos:
                self._pos_dest = pos
            assert self._pos_dest is not None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_grad(self, deg):
        n = 0
        try:
            if self._angle_dest != deg:
                self._angle_dest = deg
                #print(self._name + " ruota " + str(deg))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_angolo(self, deg, inst):
        try:
            if inst and self._angle != deg:
                self._angle = deg
                self._angle_dest = deg
                #print("Rotate now " + str(self._name) + " to " + str(deg) + "°")
                self._stable_draw = False
            elif self._angle_dest != deg:
                self._angle_dest = deg
                #print("Rotate " + str(self._name) + " to " + str(deg) + "°")
                self._stable_draw = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_asse(self, deg, inst):
        try:
            if self._asse_dest != deg:
                self._asse_dest = deg
            if inst:
                self._asse = deg
                self._stable_draw = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_z(self, z=0):
        try:
            self._z_index = z
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_rect(self):
        try:
            return self.rect
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_z_index(self):
        try:
            return self._z_index
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_collide(self, mouse):
        try:
            return self.rect.collidepoint(mouse)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        try:
            #print("Sprite reset")
            self._visible = False
            self._pos_dest = (0, 0)
            self._pos = (0, 0)
            self._z_index = 0
            self._angle = 0
            self._angle_dest = 0
            self._asse = DEG_SIDE_BACK
            self._asse_dest = DEG_SIDE_BACK
            self._stable_draw = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def translate(self):
        try:
            if self._visible:
                if self._pos_dest is not None and self._pos != self._pos_dest:
                    self._pos = (min(self._pos_dest[0], self._pos[0] + self.MOVE_STEP), min(self._pos_dest[1], self._pos[1] + self.MOVE_STEP))
            else:
                self._pos = self._pos_dest
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def rotate(self):
        try:
            if self._angle > self._angle_dest:
                self._angle = max(self._angle_dest, self._angle - self.ROTATE_STEP)
            else:
                self._angle = min(self._angle_dest, self._angle + self.ROTATE_STEP)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def flip(self):
        try:
            if self._asse_dest != self._asse:
                print("Update asse " + str(self._asse_dest))
                if self._asse_dest > self._asse:
                    self._asse = min(self._asse_dest, self._asse + self.ROTATE_STEP)
                else:
                    self._asse = max(self._asse_dest, self._asse - self.ROTATE_STEP)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_stable(self):
        try:
            if self._asse != self._asse_dest:
                self._stable_draw = False
            elif self._angle != self._angle_dest:
                self._stable_draw = False
            elif self._pos != self._pos_dest:
                self._stable_draw = False
            else:
                self._stable_draw = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self, *args, **kwargs):
        try:
            self.translate()
            self.flip()
            self.rotate()
            if self._visible:
                self.draw_image()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def draw_image(self):
        try:
            if self._angle == DEG_FLIP:
                self.image = pygame.transform.flip(self.image, True, False)
            elif self._angle == DEG_CLOC_RECT or self._angle == DEG_ANTC_RECT:
                self.image = pygame.transform.rotate(self.image, -self._angle)
            self.move_to(self._pos[0], self._pos[1])
        except Exception as e:
            ExceptionMan.manage_exception(self._name, e, True)