'''
Created on 19 gen 2022

@author: david
'''
from json import JSONDecoder
from time import strftime

import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextBox, UILabel

from main.game_manager import GiocoManager
from main.globals import *
from decks.carta_id import CartaId
from images.image_manager import ImageManager
from grafica.sprite_carta import SpriteCarta
from grafica.sprite_mazzo import SpriteMazzo
from grafica.app_sprites import SpriteManager, TOKEN_DEAL, TOKEN_MANO, TOKEN_FOLA, TOKEN_CADE
from oggetti.posizioni import *
from oggetti.stringhe import _
from main.exception_man import ExceptionMan

WAIT_SECONDS = 0.5

class GiocoFrame(object):
    visible = None
    _game_man = None
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
    _ui_manager = None
    _globals = None

    _nome_n_lab = None
    _nome_o_lab = None
    _nome_e_lab = None
    _nome_s_lab = None

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

            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_OCLOCK)
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_OCLOCK)
            obj = ObjectID(class_id='@oclock', object_id='#clock_label')
            self._clock_lab = UILabel(
                text=_(strftime('%H:%M')),
                relative_rect=pygame.Rect(x, y, w, h),
                manager=self._ui_manager,
                visible=1,
                object_id=obj)

            self.init_player_label(POSTAZIONE_SUD)
            self.init_player_label(POSTAZIONE_NORD)
            self.init_player_label(POSTAZIONE_OVEST)
            self.init_player_label(POSTAZIONE_EST)

            self.draw_box_punteggi("")
            self._game_man = gioco_man
            self._game_man.set_delegate_append_text_box(self.write_log_box)
            self._sprite_man = SpriteManager(self.img_man, self._posizioni)
            self._sprite_man.set_delegate_click(self.on_click)
            self._sprite_man.set_delegate_carta_click(self.on_carta_click)
            self._mazzo = SpriteMazzo(self.img_man.get_retro())
            for cid in CartaId:
                spr = SpriteCarta(cid, self.img_man.get_image_ca(cid), self.img_man.get_retro())
                self._sprite_man.add_sprite(str(cid), spr)
            self.update_clock()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def init_player_label(self, ppos):
        try:
            (x, y) = self._posizioni.get_pos_elemento(ElementoId.ELEMENTO_NOME_LABEL, ppos)
            (w, h) = self._posizioni.get_size_elemento(SizeId.SIZE_LABEL)

            obj = ObjectID(class_id='@labplayer', object_id='#player_label')
            rect = pygame.Rect(x, y, w, h)
            lab = UILabel(
                text="",
                relative_rect=rect,
                manager=self._ui_manager,
                visible=1,
                object_id=obj)
            if ppos == POSTAZIONE_NORD:
                self._nome_n_lab = lab
            if ppos == POSTAZIONE_SUD:
                self._nome_s_lab = lab
            if ppos == POSTAZIONE_OVEST:
                self._nome_o_lab = lab
            if ppos == POSTAZIONE_EST:
                self._nome_e_lab = lab
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_player_labels(self):
        try:
            self._nome_n_lab.set_text("")
            self._nome_s_lab.set_text("")
            self._nome_o_lab.set_text("")
            self._nome_e_lab.set_text("")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_player_labels(self, player):
        try:
            if player.get_position() == POSTAZIONE_NORD:
                self._nome_n_lab.set_text(str(player))
            if player.get_position() == POSTAZIONE_SUD:
                self._nome_s_lab.set_text(str(player))
            if player.get_position() == POSTAZIONE_OVEST:
                self._nome_o_lab.set_text(str(player))
                self._nome_o_lab.set_text_rotation(90, str(player))
            if player.get_position() == POSTAZIONE_EST:
                self._nome_e_lab.set_text(str(player))
                self._nome_e_lab.set_text_rotation(-90, str(player))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_stable(self):
        try:
            return self._sprite_man.get_stable()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def imposta_gioco(self, giocatori):
        try:
            self._game_man.set_gioco(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def draw_box_logging(self, txt=""):
        try:
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
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def draw_box_punteggi(self, txt=""):
        try:
            if self._box_punti is not None:
                self._box_punti.hide()
                self._box_punti.kill()
                del self._box_punti
            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_PUNTEGGI)
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_PUNTEGGI)
            obj = ObjectID(class_id='@points', object_id='#text_punti')
            self._box_punti = UITextBox(
                html_text=txt,
                relative_rect=pygame.Rect(x, y, w, h),
                manager=self._ui_manager,
                visible=1,
                object_id=obj)
            #self._box_punti.append_html_text(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_update_punteggi(self):
        try:
            txt = self._game_man.get_text_punti_mano()
            txt = txt + self._game_man.get_text_resti()
            self.draw_box_punteggi(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def write_log_box(self, htxt):
        try:
            if self._box_logging is not None:
                self._box_logging.append_html_text("<p>" + htxt + "</p>")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_carte_mano(self, coord, ccman, inst):
        try:
            self._sprite_man.show_carte_mano(coord, ccman, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_carte_mano(self, coord, ccman):
        try:
            self._sprite_man.hide_carte_mano(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_carte_tavola(self, coord, ccman):
        try:
            return self._sprite_man.show_carte_tavola(coord, ccman, self._globals.get_instant_pos())
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
            self.reset_player_labels()
            self.draw_box_punteggi()
            self._sprite_man.reset()
            if self._popup_box is not None:
                self._popup_box.visible=False
            self._game_man.on_reset()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizia_gioco(self, players, game="FsmGermini"):
        try:
            self.on_restore()
            self.draw_box_punteggi()
            self._game_man.inizia_gioco(players, game)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_serialize(self, file):
        try:
            self._running = False
            print(" =======> Save status in JSON ==>")
            txt = self._game_man.on_serialize()
            print("Save status in JSON <==")
            file.write(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_deserialize(self, file):
        try:
            # read all lines at once
            self.on_termina()
            self.on_restore()
            all_of_it = file.read()
            print(" =======> Load status from JSON ==>")
            f = JSONDecoder(object_hook=self._game_man.fromJSON).decode(all_of_it)
            print("Load status from JSON <==")
            self._game_man.on_deserialize_complete()
            self.on_redraw()
            self._running = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_move(self, c, pos, inst=False):
        try:
            self._sprite_man.set_pos_carta(c.get_id(), pos, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_set_z(self, c, z):
        try:
            self._sprite_man.set_z(c.get_id(), z)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_set_hoverable(self, c, h):
        try:
            self._sprite_man.enable_hoover(c.get_id(), h)
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

    def set_fronte(self, c, coperta, inst):
        try:
            self._sprite_man.set_lato(c.get_id(), coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ruota_carta(self, c, angle, inst):
        try:
            self._sprite_man.set_angolo(c.get_id(), angle, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_termina(self):
        try:
            self._game_man.termina_gioco()
            if self._box_punti is not None:
                self._box_punti.hide()
                #self.appended_text = ""
                self._sprite_man.show_token(TOKEN_MANO, None, False)
                self._sprite_man.show_token(TOKEN_DEAL, None, False)
                del self._box_punti
                self._box_punti = None
            self.draw_box_punteggi("")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, evt):
        try:
            self._game_man.on_event(evt)

            self._sprite_man.on_event(evt)

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

    def on_resize(self, evt):
        try:
            self._posizioni.on_resize(evt)
            if self._cur_sfondo != None:
                self._cur_sfondo = pygame.transform.scale(self._sfondo, evt.dict['size'])

            if self._box_logging is not None:
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
            self._clock_lab.set_text(strftime('%H:%M'))
            self._clock_lab.update(0.5)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_handler(self, surface, time_delta):
        try:
            if self._cur_sfondo is not None:
                self._window_surface.blit(self._cur_sfondo, (0, 0))

            if self._sprite_man is not None:
                self._sprite_man.update(self._window_surface)

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
                self._popup_box.kill()
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

            elif self._popup_box is not None:
                self._popup_box.visible = False
                self._popup_box = None

            return self._popup_box
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_turno(self, ppos, visible=True):
        try:
            self._sprite_man.show_token(TOKEN_MANO, ppos, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_mazziere(self, ppos, visible=True):
        try:
            self._sprite_man.show_token(TOKEN_DEAL, ppos, visible)
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

    def on_click(self):
        try:
            if self._popup_hover:
                self._game_man.on_popup_click()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            print("Click su " + str(cid))
            self._game_man.on_carta_click(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_partita(self):
        try:
            # Update player's position
            for p in self._game_man.get_giocatori():
                print(str(p.get_position()) + ": " +str(p))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_sprite(self, cid):
        try:
            return self._sprite_man.get_sprite_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)