'''
Created on 20 gen 2022

@author: david
'''

import pygame
from pygame.sprite import Sprite
import oggetti.posizioni

from main.globals import *
from main.exception_man import ExceptionMan


class SpriteMazzo(pygame.sprite.Sprite):
    top_rect = None
    img_back = None
    visible = None
    _pos_dest = None
    _pos = None

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.img_back = img.convert()
        self.image = self.img_back
        self.rect = self.img_back.get_rect()
        self.rect.center = (0, 0)
        self._pos_dest = (0, 0)
        self._pos = (0, 0)
        self.visible = False

    def get_nome(self):
        return "Mazzo"

    def set_visible(self, visible, scoperta=False, pos=None, z=None):
        try:
            if self.visible != visible:
                self.visible = visible
                if self.visible:
                    if pos is not None:
                        self._pos = pos
                        self.rect = self.image.get_rect()
                        self.rect.center = self._pos
                    if z is not None:
                        self.z_index = None
                else:
                    self.z_index = 0
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide(self):
        try:
            self.set_visible(False, False, (0,0), 1)
            echo_message("Nascondi mazzo")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show(self):
        try:
            self.set_visible(True, False, (0,0), 1)
            echo_message("Visualizza mazzo")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position(self):
        return self.rect.center

    def move(self, pos):
        if self.pos_dest != pos:
            self.pos_dest = pos

    def set_lato(self, fronte = True):
        try:
            if self.lato_fronte != fronte:
                self.lato_fronte = fronte
                if fronte:
                    self.image = self.img_front
            #        self.rect = self.image.get_rect()
            #        self.rect.center = (0, 0)
            #        echo_message("Scopri carta")
                else:
                    self.image = self.img_back
            #        self.rect = self.image.get_rect()
            #        self.rect.center = (0, 0)
            #        echo_message("Copri carta")
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_position(self, pos):
        try:
            self._pos = pos
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_visible(self, visible, scoperta=False, pos=None, z=None):
        try:
            self.visible = visible
            self.lato_fronte = scoperta
            if self.visible:
                if pos is not None:
                    self.rect = self.image.get_rect()
                    self.rect.center = pos
                if z is not None:
                    self.z_index = z
            else:
                self.z_index = 0
                #self.rect = self.image.get_rect()
                #self.rect.center = (0, 0)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_scoperta(self):
        return True #self.lato_fronte

    def update(self):
        try:
            #if self.lato_fronte:
            #    self.image = self.img_front
            #else:
            #    self.image = self.img_back

            super().update()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_z_index(self):
        return self.z_index

    def get_visible(self):
        return self.visible

    def get_collide(self, mouse):
        return self.rect.collidepoint(mouse)


class ButtonPygame:
    gui_font = None
    screen = None
    elevation = 5
    hndl = None

    def __init__(self, screen, text, width, height, pos, hndl=None):
        # Core attributes
        self.pressed = False
        self.hndl = hndl
        self.dynamic_elecation = self.elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'
        # self.translation = translation
        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text

        self.gui_font = pygame.font.SysFont("Arial", 20)
        self.text_surf = self.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.screen = screen

    '''
    '''

    def change_text(self, newtext):
        self.text_surf = self.gui_font.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)

        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                # self.change_text(f"{self.translation}")
            else:
                self.dynamic_elecation = self.elevation
                # self.change_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                # self.change_text(f"{self.translation}")
            else:
                if self.pressed == True:
                    if (self.hndl):
                        self.hndl()
                    self.pressed = False
                    # self.change_text(self.text)
