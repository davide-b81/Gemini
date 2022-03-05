'''
Created on 19 gen 2022

@author: david
'''
import time
from threading import Timer
from time import strftime

import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextBox, UILabel

from main.globals import *
from decks.carta_id import CartaId
from grafica.image_manager import ImageManager
from grafica.sprite_carta import SpriteCarta
from grafica.sprite_mazzo import SpriteMazzo
from grafica.app_sprites import Sprites, TOKEN_DEAL, TOKEN_MANO, TOKEN_FOLA, TOKEN_CADE
from oggetti.posizioni import *
from oggetti.stringhe import _
from main.exception_man import ExceptionMan

WAIT_SECONDS = 0.5

class GiocoFrame(object):
    visible = None
    gioco_man = None
    screen = None
    _sprite_man = None
    _posizioni = None
    _mazzo = None
    img_man = None
    _sfondo = None
    _cur_sfondo = None
    _window_surface = None
    _box_logging = None
    _box_punti = None
    _popup_box = None
    _clock_lab = None
    _popup_hover = None
    _ui_manager = None
    _globals = None
    _delegate_on_click = None

    '''
    classdocs
    '''
    def __init__(self, manager, screen, pos, gioco_man):
        try:
            self._globals = Globals()
            self._ui_manager = manager
            self.screen = screen
            self._posizioni = pos
            self._popup_hover = False
            self.img_man = ImageManager(self._posizioni.get_card_size())
            self._sfondo = self.img_man.get_background_image()
            self._cur_sfondo = pygame.transform.scale(self._sfondo, pygame.display.get_window_size())
            self._window_surface = pygame.Surface((screen.get_width(), screen.get_height()))
            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_LOG)
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_FRAME_LOG)
            obj = ObjectID(class_id='@messages', object_id='#text_box')
            self._box_logging = UITextBox(
                html_text=_(
                    "Il nobilissimo gioco delle Minchiate Fiorentine<br/>====================================================<br/>"),
                relative_rect=pygame.Rect(x, y, w, h),
                manager=self._ui_manager,
                visible=1,
                object_id=obj)

            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_OCLOCK)
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_OCLOCK)
            obj = ObjectID(class_id='@oclock', object_id='#clock_label')
            self._clock_lab = UILabel(
                text=_(strftime('%H:%M')),
                relative_rect=pygame.Rect(x, y, w, h),
                manager=self._ui_manager,
                visible=1,
                object_id=obj)

            self.draw_box_punteggi("")
            self.gioco_man = gioco_man
            self.gioco_man.set_delegate_append_text_box(self.write_log_box)
            self._sprite_man = Sprites(self.img_man, self._posizioni)
            self._mazzo = SpriteMazzo(self.img_man.get_retro())
            #self._sprite_man.add_sprite(self._mazzo.get_nome(), self._mazzo)
            # self._popup = SpritePopUp(self._ui_manager, "POPUP", self.img_man.get_popup_image())
            # self._sprite_man.add_sprite("POPUP", self._popup)
            for ca in CartaId:
                spr = SpriteCarta(str(ca), self.img_man.get_image_ca(ca), self.img_man.get_retro())
                self._sprite_man.add_sprite(str(ca), spr)

            self._sprite_man.set_delegate_click(self.gioco_man.on_carta_click)
            # self._globals.set_delegate_show_popup(self.show_popup)
            self.update_clock()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_click(self, f):
        try:
            self._delegate_on_click = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def imposta_giocatori(self, giocatori):
        try:
            self.gioco_man.set_giocatori(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_stable(self):
        try:
            return self._sprite_man.get_stable()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def imposta_gioco(self, giocatori):
        try:
            self.gioco_man.set_gioco(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def draw_box_punteggi(self, txt=""):
        try:
            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_PUNTEGGI)
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_PUNTEGGI)
            obj = ObjectID(class_id='@points', object_id='#text_punti')
            self._box_punti = UITextBox(
                html_text=_(txt),
                relative_rect=pygame.Rect(x, y, w, h),
                manager=self._ui_manager,
                visible=1,
                object_id=obj)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_update_punteggi(self):
        try:
            txt="<p>"
            for p in self.gioco_man.get_giocatori():
                txt = txt + str(p) + ": " + str(p.get_punti_mano()) + "<br/>"
            txt = txt + "</p>"
            for p in self.gioco_man.get_giocatori():
                txt = txt + "<p>" + str(p) + ":"
                ca = p.get_carte_mano()
                for c in ca:
                    txt = txt + " " + c.get_short_name()
            self.write_log_box(txt)
            self._box_punti.appended_text = txt
            self._box_punti.rebuild()

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def write_log_box(self, htxt):
        try:
            self._box_logging.append_html_text("<p>" + htxt + "</p>")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_carte_mano(self, coord, ccman):
        try:
            self._sprite_man.show_carte_mano(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_carte_mano(self, coord, ccman):
        try:
            self._sprite_man.show_carte_mano(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_carte_mano(self, coord, ccman):
        try:
            self._sprite_man.hide_carte_mano(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_carte_tavola(self, coord, ccman):
        try:
            return self._sprite_man.show_carte_tavola(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_carte_tavola(self, coord, ccman):
        try:
            return self._sprite_man.hide_carte_tavola(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_restore_mazzo(self):
        try:
            self._sprite_man.reset()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_restore(self):
        try:
            self._sprite_man.reset()
            self.gioco_man.on_reset()
            if self._popup_box is not None:
                self._popup_box.visible=False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizia_gioco(self):
        try:
            self.on_restore()
            self.gioco_man.inizia_gioco()
            self.message_manager.show()
            self._mazzo.show_mazzo()
            self._sprite_man.update(self._ui_manager)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_move(self, c, pos, inst=False):
        try:
            #print("On muove " + str(c) + " in (" + str(pos[0]) + ", " + str(pos[1]) + ")")
            self._sprite_man.set_pos_carta(c.get_id(), pos, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_set_z(self, c, z):
        try:
            self._sprite_man.set_z(c.get_id(), z)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_coperta(self, c):
        try:
            return self._sprite_man.is_coperta(c.get_id())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_carta(self, c):
        try:
            self._sprite_man.show_sprite(c.get_id())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def nascondi_carta(self, c):
        try:
            self._sprite_man.hide_sprite(c.get_id())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_fronte(self, c, coperta=FRONTE_COPERTA, inst=True):
        try:
            self._sprite_man.set_lato(c.get_id(), coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ruota_carta(self, c, angle=0, inst=True):
        try:
            self._sprite_man.set_angolo(c.get_id(), angle, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_mescola(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, evt):
        try:
            self.gioco_man.on_event(evt)

            if evt.type == pygame.MOUSEBUTTONUP:
                if self._popup_hover:
                    self.on_click()

            if evt.type == pygame.MOUSEMOTION:
                if self._popup_box is not None:
                    self._popup_hover = self._popup_box.rect.collidepoint(pygame.mouse.get_pos())

            if self._sprite_man is not None:
                self._sprite_man.on_event(evt)

            if self._popup_box is not None:
                self._popup_box.process_event(evt)

            if self._box_punti is not None:
                self._box_punti.process_event(evt)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_sort(self):
        try:
            # TODO: riordinare gli sprite
            pass#self._sprite_man.sort()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_fola(self):
        try:
            self._sprite_man.show_fola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_fola(self):
        try:
            self._sprite_man.hide_fola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_pozzo(self):
        try:
            self._sprite_man.show_pozzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_pozzo(self):
        try:
            self._sprite_man.hide_pozzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_redraw(self):
        try:
            self._sprite_man.update_sprite_list()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_mazzo(self, ca, ppos=None):
        try:
            print("Mostra mazzo")
            #for c in ca:
            #    if ppos is not None:
            #        self._sprite_man.set_pos_carta(c.get_id(), ppos)
            #    self._sprite_man.show_sprite(c.get_id())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def nascondi_mazzo(self, ca):
        try:
            print("Nascondi mazzo")
            #self._sprite_man.hide_mazzo(ca)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_resize(self, evt):
        try:
            self._posizioni.on_resize(evt)
            if self._cur_sfondo != None:
                self._cur_sfondo = pygame.transform.scale(self._sfondo, evt.dict['size'])
            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_LOG)
            self._box_logging.set_position((x, y))

            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_PUNTEGGI)
            self._box_punti.set_position((x, y))

            if self._popup_box is not None:
                (x, y) = self._posizioni.get_posizione(PosizioniId.POS_POPUP)
                (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_POPUP)
                self._popup_box.set_position((x - int(w / 2), y - int(h / 2)))
                self._popup_box.set_dimensions((w, h))

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_areas(self):
        try:
            self._popup_box.rect.collidepoint(pygame.mouse.get_pos())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_clock(self):
        try:
            #if ':' in self._clock_lab.text:
            #    self._clock_lab.set_text(strftime('%H %M'))
            #else:
            self._clock_lab.set_text(strftime('%H:%M'))
            #self.update_handler(self._window_surface, 0)
            self._clock_lab.update(0.5)
            #threading.Timer(WAIT_SECONDS, self.update_clock).start()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_handler(self, surface, time_delta):
        try:
            if self._cur_sfondo is not None:
                self._window_surface.blit(self._cur_sfondo, (0, 0))

            if self._sprite_man is not None:
                self._sprite_man.update(self._window_surface)

            if self._box_punti is not None:
                self._box_punti.update(time_delta)

            if self._popup_box is not None:
                self._popup_box.update(time_delta)

            if self._clock_lab is not None:
                self.update_clock()
                self._clock_lab.update(time_delta)

            surface.blit(self._window_surface, (0, 0))

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_popup(self):
        try:
            if self._popup_box is not None:
                self._popup_box.visible = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_popup(self, txt, visible=True):
        try:
            if visible:
                (x, y) = self._posizioni.get_posizione(PosizioniId.POS_POPUP)
                (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_POPUP)
                obj = ObjectID(class_id='@popups', object_id='#popup_box')
                self._popup_box = UITextBox(
                    html_text=_(txt),
                    relative_rect=pygame.Rect(x - (w / 2), y - (h / 2), w, h),
                    manager=self._ui_manager,
                    visible=1,
                object_id=obj)
                self._popup_box.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_IN)
                #self._popup_box.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='test')
            elif self._popup_box is not None:
                self._popup_box.visible = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_click(self):
        try:
            self.hide_popup()
            self.gioco_man.on_popup_click()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_mazziere(self, ppos, visible=True):
        try:
            self._sprite_man.show_token(TOKEN_DEAL, ppos, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_turno(self, ppos, visible=True):
        try:
            self._sprite_man.show_token(TOKEN_MANO, ppos, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_fola(self, ppos, visible=True):
        try:
            self._sprite_man.show_token(TOKEN_FOLA, ppos, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_cade(self, ppos, visible=True):
        try:
            self._sprite_man.show_token(TOKEN_CADE, ppos, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)