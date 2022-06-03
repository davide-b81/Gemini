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
    MOVE_STEP = 150

    REFRESH_PERIOD = 0.02

    _name = None

    _z_index = None
    _hoverable = None
    _hover = None
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

            self._z_index = 0
            self._hoverable = False
            self._hover = False
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
            assert isinstance(self._visible, bool)
            return self._visible
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, visible=True):
        try:
            assert isinstance(visible, bool)
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

    def move_to(self, pos):
        try:
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @property
    def x(self):
        return self._pos[0]

    @x.setter
    def x(self, coo):
        self._pos = (coo, self._pos[1])
        self._pos_dest = (coo, self._pos[1])

    @property
    def y(self):
        return self._pos[1]

    @y.setter
    def y(self, coo):
        self._pos = (self._pos[0], coo)
        self._pos_dest = (self._pos_dest[0], coo)

    @property
    def z(self):
        return self._z_index

    def get_z(self):
        try:
            if self._hover:
                return 0
            else:
                return self._z_index
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_z(self, z=0):
        #print(str(self) + " set sprite hoverable z = " + str(self._z_index))
        self._z_index = z

    @z.setter
    def z(self, i):
        self._z_index = i

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, v):
        self._visible = v

    def set_position(self, pos, inst):
        try:
            pos = (round(pos[0]), round(pos[1]))
            if pos[0] != self._pos_dest[0] or pos[1] != self._pos_dest[1]:
                #print("Posiziona " + str(self) + " in " + str(pos))
                self._pos_dest = pos
                if inst:
                    self._pos = pos
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

    def get_hoverable(self):
        return self._hoverable

    def enable_hoover(self, h=False):
        self._hoverable = h

    def get_hover(self):
        return self._hover

    def set_hover(self, enable):
        try:
            self._hover = enable
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_rect(self):
        try:
            return self.rect
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_collide(self, mouse):
        try:
            if self._visible:
                return self.rect.collidepoint(mouse)
            else:
                return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        try:
            self._visible = False
            self._pos_dest = (0, 0)
            self._pos = (0, 0)
            self._z_index = 0
            self._angle = 0
            self._angle_dest = 0
            self._asse = DEG_SIDE_BACK
            self._asse_dest = DEG_SIDE_BACK
            self._stable_draw = False
            self._hoverable = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_translated_coord(self, dst, cur):
        try:
            if dst != cur:
                if abs(dst - cur) > self.MOVE_STEP:
                    if dst > cur:
                        cur = cur + self.MOVE_STEP
                    else:
                        cur = cur - self.MOVE_STEP
                else:
                    cur = dst
            return cur
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def translate(self):
        try:
            if self._pos[0] != self._pos_dest[0] or self._pos[1] != self._pos_dest[1]:
                self._pos = (self.get_translated_coord(self._pos_dest[0], self._pos[0]), self.get_translated_coord(self._pos_dest[1], self._pos[1]))
                #print("Translate " + str(self) + " in " + str(self._pos) + " finale " + str(self._pos_dest))
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
                if self._asse_dest == DEG_SIDE_FRONT:
                    self._asse = min(self._asse_dest, max(DEG_SIDE_FRONT, self._asse - self.ROTATE_STEP))
                else:
                    self._asse = max(self._asse_dest, min(self._asse + self.ROTATE_STEP, DEG_SIDE_BACK))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_stable(self):
        try:
            if not self._visible:
                self._stable_draw = True
            elif self._asse != self._asse_dest:
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
            self.move_to(self._pos)
        except Exception as e:
            ExceptionMan.manage_exception(self._name, e, True)