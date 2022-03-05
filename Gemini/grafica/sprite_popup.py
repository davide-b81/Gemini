#   '''
#  Created on 2 2 2022
#  @author: david
#  '''
'''
Created on 6 gen 2022

@author: david
'''
from cmath import cos
from oggetti.stringhe import _
from math import radians

import pygame
import pygame_gui

from pygame import SRCALPHA
from pygame_gui.core import ObjectID

from main.exception_man import ExceptionMan

# Colors (R, G, B)
from main.globals import Globals
from oggetti.posizioni import PosizioniId, Posizioni
from oggetti.text_box import UITextBox

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class SpritePopUp(UITextBox):
    '''
    classdocs
    '''
    ROTATE_STEP = 1
    MOVE_STEP = 18
    REFRESH_PERIOD = 0.02

    rect = None
    _size = None
    _angle = None
    _angle_dest = None
    _pos_dest = None
    _pos = None
    _z_index = None
    _txt = None
    image = None
    orig_image = None
    _posizioni = None
    _button_exit = None
    _button_exit_lay = None
    _box_lay = None
    _ui_manager = None
    _globals = None
    _visible = None
    _text_box = None

    def __init__(self, manager, name, image):
        '''
        Constructor
        '''
        try:
            pygame.sprite.Sprite.__init__(self)
            self._globals = Globals()
            super().update()

            self._visible = False
            self._ui_manager = manager
            self.orig_image = image.convert()
            self._size = ((800, 600))
            self.image = pygame.Surface(self._size)#pygame.transform.scale(self.orig_image, self._size)
            self.image.set_alpha(50)
            self._angle = 0
            self._angle_dest = 0
            self._name = name
            self._posizioni = self._globals.get_positions()
            self._pos = self._posizioni.get_posizione(PosizioniId.POS_FRAME_PUNTEGGI)
            self._pos_dest = self._pos

            self.rect = self.image.get_rect()
            self.rect.center = self._pos
            self._z_index = 0

            # Text box
            self._box_lay = pygame.Rect(0, 0, 120, 200)
            self._box_lay.center = ((-self._pos[0],-self._pos[1]))
            obj = ObjectID(class_id='@messages', object_id='#text_box')
            self._text_box = UITextBox(relative_rect=self._box_lay,
                html_text=_(" - Il nobilissimo gioco delle Minchiate Fiorentine - <br/>===========================================================<br/>"),
                manager=self._ui_manager,
                visible=1,
                anchors={'left': 'right',
                         'right': 'right',
                         'top': 'bottom',
                         'bottom': 'bottom'},
                object_id=obj)
            self._text_box.set_image(pygame.transform.scale(self.orig_image, self._size))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __str__(self):
        return self._name

    def get_popup_size(self):
        return self.rect.size

    def get_position(self):
        return self._pos

    def set_position(self, pos, z=0):
        try:
            self._z_index = z
            self._pos_dest = pos
            self._pos = pos
            assert self._pos_dest is not None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_image_current(self, image):
        try:
            if self.image != image:
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.center = self._pos
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_txt(self, txt="Default"):
        try:
            self._txt = txt

            if self._visible:
                #self._text_box.set_image(pygame.transform.scale(self.orig_image, self._size))
                if self._text_box is not None:
                    self._text_box.visible = True
                    self._text_box.append_html_text("<p>XDXDXDXD</p>")
                    self.image.blit(self._text_box, self._size)
            elif self._text_box is not None:
                del(self._text_box)


        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, visible, pos=None, z=None):
        try:

            if self._visible != visible or self._pos != pos:
                self._visible = visible
                if self._button_exit is not None:
                    self._button_exit.visible = visible

                if self._text_box is not None:
                    self._text_box.visible = visible

                if pos is not None:
                    self._pos = pos
                    self._pos_dest = self._pos

                if z is not None:
                    self._z_index = z

                self.update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def move_to(self, x, y):
        try:
            pass
            #self._pos = (x, y)
            #self.rect.x = self._pos[0]
            #self.rect.y = self._pos[1]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self):
        try:
            super().update()
            self.rotate()
            self.traslate()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_stable(self):
        try:
            #if self._visible:
            #    return self._pos != self._pos_dest or self._angle != self._angle_dest
            #else:
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_z_index(self):
        try:
            return self._z_index
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_z_index(self, z):
        try:
            self._z_index = z
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_visible(self):
        try:
            return self._visible
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_collide(self, mouse):
        try:
            return self.rect.collidepoint(mouse)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def traslate(self):
        try:
            if self._pos != self._pos_dest:
                if self._visible:
                    x = min(self._pos_dest[0], self._pos[0] + self.MOVE_STEP)
                    y = min(self._pos_dest[1], self._pos[1] + self.MOVE_STEP)
                    self.move_to(x, y)
                else:
                    self._pos = self._pos_dest
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def rotate(self, clockwise=True):
        n = 0
        try:
            if self._visible:
                if self._angle != self._angle_dest:
                    cardSurface = pygame.Surface(self._size, SRCALPHA)
                    if self._angle > 90:
                        cardSurface.blit(self.img_front, (0, 0))
                    else:
                        cardSurface.blit(self.img_back, (0, 0))
                    if self.lato_fronte:
                        n = self._angle + self.ROTATE_STEP
                        self._angle = min(self._angle_dest, n)
                    else:
                        n = self._angle - self.ROTATE_STEP
                        n = max(0, n)
                        self._angle = max(self._angle_dest, n)

                    w = cos(radians(self._angle)) * self._size[0]
                    siz = ((abs(w.real), self._size[1]))
                    if self._angle > 90:
                        self.image = pygame.transform.scale(cardSurface, siz)
                    else:
                        self.image = pygame.transform.scale(cardSurface, siz)
                    self.rect = self.image.get_rect()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

