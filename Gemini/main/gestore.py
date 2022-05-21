'''
Created on 18 gen 2022

@author: david
'''
import os

import pygame_gui
from pygame_gui.core import ObjectID
from main.gioco_frame import GiocoFrame
from game.player import Player
from main.game_manager import GiocoManager
from main.globals import *
from oggetti.posizioni import *
from oggetti.stringhe import _
from main.exception_man import ExceptionMan

from style.style import thfile


class Gestore(object):
    _clock = None
    _ui_manager = None
    _button_new = None
    _button_termina = None
    _button_save = None
    _button_restore = None
    _button_exit = None
    button_layout_rect = None
    button_exit_layout_rect = None
    button_new_layout_rect = None
    _btnsave_layout_rect = None
    _btnrest_layout_rect = None
    _gioco_frame = None
    _running = None
    _players = None
    _gioco_man = None
    _draw_stable = None
    _globals = None
    _posizioni = None
    _delegate_exit = None
    _delegate_run = None


    def __init__(self, screen, debug):
        try:
            self._globals = Globals()
            self._globals.set_debug(debug)
            self.screen = screen
            self._posizioni = self._globals.init_positions(screen)
            self._ui_manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()), thfile)

            self.init_buttons()
            self._clock = pygame.time.Clock()
            self._gioco_man = GiocoManager(self._posizioni)
            self._gioco_frame = GiocoFrame(self._ui_manager, screen, self._posizioni, self._gioco_man)
            self._gioco_man.set_delegate_get_sprite(self._gioco_frame.get_sprite)
            self._players = []
            self._draw_stable = False
            self._running = True

            self._gioco_man.set_delegate_mescola(self.on_mescola)
            self._gioco_man.set_delegate_redraw(self.on_redraw)
            self._gioco_man.set_delegate_turno(self.on_turno)
            self._gioco_man.set_delegate_fola(self.on_fola)
            self._gioco_man.set_delegate_cade(self.on_cade)
            self._gioco_man.set_delegate_mazziere(self.on_mazziere)
            self._gioco_man.set_delegete_on_players(self.on_players)
            self._gioco_man.set_delegate_show_carta(self.on_show_carta)
            self._gioco_man.set_delegate_hide_carta(self.on_hide_carta)
            self._gioco_man.set_delegate_set_fronte(self.on_set_fronte)
            self._gioco_man.set_delegate_is_coperta(self.is_coperta)
            self._gioco_man.set_delegate_show_pozzo(self.on_show_pozzo)
            self._gioco_man.set_delegate_hide_pozzo(self.on_hide_pozzo)
            self._gioco_man.set_delegate_show_presa(self.on_show_presa)
            self._gioco_man.set_delegate_hide_presa(self.on_hide_presa)
            self._gioco_man.set_delegate_hide_mano(self.on_hide_mano)
            self._gioco_man.set_delegate_show_tavola(self.on_show_tavola)
            self._gioco_man.set_delegate_hide_tavola(self.on_hide_tavola)

            #self._gioco_man.set_delegate_posiziona_carta(self.on_move)
            self._gioco_man.set_delegate_restore_mazzo(self.on_restore_mazzo)
            self._gioco_man.set_delegate_rotate_pos_carta(self.on_rotate_pos_carta)
            self._gioco_man.set_delegate_set_z(self.on_set_z)
            self._gioco_man.set_delegate_set_hoverable(self.on_set_hoverable)

            self._gioco_man.set_delegate_draw_stable(self.get_draw_stable)
            self._gioco_man.set_delegate_frame_show_popup(self.on_popup)
            self._gioco_man.set_delegete_presa(self.on_presa)
            if self._globals.get_quick():
                self._button_new.disable()
                self._button_new.visible = False
                self._button_termina.enable()
                self._button_termina.visible = True
                self.on_nuovo("FsmGermini")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_run(self, f):
        try:
            self._delegate_run = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_exit(self, f):
        try:
            self._delegate_exit = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_draw_stable(self):
        try:
            return self._gioco_frame.get_stable()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def init_buttons(self):
        try:
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_BUTTON)

            if self._globals.get_debug() == True:
                obj = ObjectID(class_id='@friendly_buttons', object_id='#save_button')
                self._btnsave_layout_rect = pygame.Rect(0, 0, w, h)
                self._btnsave_layout_rect.bottomright = self._posizioni.get_posizione(PosizioniId.RPOS_BUTTON_SAVE)
                self._button_save = pygame_gui.elements.UIButton(relative_rect=self._btnsave_layout_rect,
                                                                text=_("Save"),
                                                                manager=self._ui_manager,
                                                                anchors={'left': 'right',
                                                                        'right': 'right',
                                                                        'top': 'bottom',
                                                                        'bottom': 'bottom'},
                                                                object_id=obj)

                obj = ObjectID(class_id='@friendly_buttons', object_id='#rest_button')
                self._btnrest_layout_rect = pygame.Rect(0, 0, w, h)
                self._btnrest_layout_rect.bottomright = self._posizioni.get_posizione(PosizioniId.RPOS_BUTTON_REST)
                self._button_restore = pygame_gui.elements.UIButton(relative_rect=self._btnrest_layout_rect,
                                                                text=_("Restore"),
                                                                manager=self._ui_manager,
                                                                anchors={'left': 'right',
                                                                        'right': 'right',
                                                                        'top': 'bottom',
                                                                        'bottom': 'bottom'},
                                                                object_id=obj)

            obj = ObjectID(class_id='@friendly_buttons', object_id='#nuovo_button')

            self.button_new_layout_rect = pygame.Rect(0, 0, w, h)
            self.button_new_layout_rect.bottomright = self._posizioni.get_posizione(PosizioniId.RPOS_BUTTON_NEW)
            self._button_new = pygame_gui.elements.UIButton(relative_rect=self.button_new_layout_rect,
                                                            text=_("Nuovo"),
                                                            manager=self._ui_manager,
                                                            anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom'},
                                                            object_id=obj)

            self.button_stop_layout_rect = pygame.Rect(0, 0, w, h)
            self.button_stop_layout_rect.bottomright = self._posizioni.get_posizione(PosizioniId.RPOS_BUTTON_STOP)
            self._button_termina = pygame_gui.elements.UIButton(relative_rect=self.button_stop_layout_rect,
                                                                text=_("Termina"),
                                                                manager=self._ui_manager,
                                                                anchors={'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom'},
                                                                visible=0,
                                                                object_id=obj)

            obj = ObjectID(class_id='@friendly_buttons', object_id='#esci_button')
            self.button_exit_layout_rect = pygame.Rect(0, 0, w, h)
            self.button_exit_layout_rect.bottomright = self._posizioni.get_posizione(PosizioniId.RPOS_BUTTON_EXIT)
            self._button_exit = pygame_gui.elements.UIButton(relative_rect=self.button_exit_layout_rect,
                                                             text=_("Esci"),
                                                             manager=self._ui_manager,
                                                             anchors={'left': 'right',
                                                                     'right': 'right',
                                                                     'top': 'bottom',
                                                                     'bottom': 'bottom'},
                                                             object_id=obj)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def process_events(self, evt):
        try:
            self._ui_manager.process_events(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def event_handler(self, evt):
        try:
            # if user clicks the close X
            if evt.type == pygame.QUIT:
                running = False
            if evt.type == pygame.VIDEORESIZE:
                # echo_message("Resize")
                pygame.display.flip()
            if evt.type == pygame_gui.UI_BUTTON_PRESSED:
                self.on_click(evt)
            if evt.type == pygame.MOUSEBUTTONUP:
                self.on_click(evt)
            if evt.type == pygame.VIDEORESIZE:
                self.on_resize(evt)
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_r:
                    self.on_r(evt)
            if evt.type == pygame.MOUSEMOTION:
                if self._globals.get_debug():
                    if self._gioco_man.is_running() == False:
                        self.on_nuovo("FsmGermini")
            if self.get_draw_stable():
                self._gioco_frame.on_event(evt)
        except Exception as e:
           ExceptionMan.manage_exception("", e, True)

    def on_r(self, evt):
        echo_message("Sort event")

    def on_resize(self, evt):
        try:
            self._button_exit.update_containing_rect_position()
            self._button_new.update_containing_rect_position()
            self._gioco_frame.on_resize(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_exit(self, evt):
        try:
            self._running = False
            self._delegate_exit()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_update(self):
        try:
            if self._running and self._clock != None:
                #time_delta = self._clock.tick(25) / 1000.0
                #self._gioco_frame.update_handler(self.screen, time_delta)
                self._gioco_man.update_gioco(self.screen)
                #self._ui_manager.update(time_delta)
                #self._ui_manager.draw_ui(self.screen)
                self._draw_stable = self._gioco_frame.get_stable()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_update_ui(self):
        try:
            if self._clock != None:
                time_delta = self._clock.tick(25) / 1000.0
                self._gioco_frame.update_handler(self.screen, time_delta)
                #self._gioco_man.update_gioco(self.screen)
                self._ui_manager.update(time_delta)
                self._ui_manager.draw_ui(self.screen)
                #self._draw_stable = self._gioco_frame.get_stable()

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

        return self._running

    def add_player(self, name, real=False):
        try:
            player = Player(name)
            player.set_simulated(not real)
            self._players.append(player)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
    EVENT HANDLERs
    '''
    def on_nuovo(self, game="FsmGermini"):
        try:
            self._players.clear()
            """
            (). Le minchiate vengono giocate in quattro.
            """
            self.add_player("Davide", True)
            self.add_player("Tizio")
            self.add_player("Caio")
            self.add_player("Sempronio")
            self._gioco_frame.inizia_gioco(self._players, game)
            self._running = True
            self._delegate_run()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_termina(self):
        try:
            self._players.clear()
            self._gioco_frame.on_termina()
            self._running = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_sort(self, evt):
        try:
            self._gioco_frame.on_sort()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_dichiara(self, text):
        try:
            self._gioco_frame.write_log_box(text)
            self._gioco_frame.show_popup(text)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_click(self, evt):
        try:
            if evt.type == pygame_gui.UI_BUTTON_PRESSED:
                if evt.ui_element == self._button_exit:
                    self.on_termina()
                    self.on_exit(evt)
                elif evt.ui_element == self._button_new:
                    self._button_new.disable()
                    self._button_new.visible = False
                    self._button_termina.enable()
                    self._button_termina.visible = True
                    self.on_nuovo()
                elif evt.ui_element == self._button_termina:
                    self._button_termina.disable()
                    self._button_termina.visible = False
                    self._button_new.enable()
                    self._button_new.visible = True
                    self.on_termina()
                elif evt.ui_element == self._button_save:
                    self.on_save()
                elif evt.ui_element == self._button_restore:
                    self.on_termina()
                    self.on_restore()
                    self.on_load()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_mescola(self, ca):
        try:
            self._gioco_frame.on_update_z(ca)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_save(self):
        try:
            with open("test.json", "w", encoding="utf8") as outfile:
                self._gioco_frame.dump_gioco(outfile)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_load(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_restore(self):
        try:
            self._gioco_frame.on_restore()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_restore_mazzo(self):
        try:
            self._gioco_frame.on_restore_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_move(self, c, pos, inst):
        try:
            self._gioco_frame.on_move(c, pos, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_set_z(self, c, z):
        try:
            self._gioco_frame.on_set_z(c, z)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_set_hoverable(self, c, enable=True):
        try:
            c.set_hoverable(enable)
            #self._gioco_frame.on_set_hoverable(c, h)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_front(self, c):
        try:
            return self._gioco_frame.is_front(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_carta(self, c, pos=None):
        try:
            if pos is not None:
                self._gioco_frame.on_move(c, pos, True)
            self._gioco_frame.mostra_carta(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_carta(self, c):
        try:
            self._gioco_frame.nascondi_carta(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_rotate_pos_carta(self, c, ppos, inst):
        try:
            c.set_deg_from_ppos(ppos, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_pozzo(self, c):
        try:
            self._gioco_frame.mostra_pozzo(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_pozzo(self, c):
        try:
            self._gioco_frame.nascondi_pozzo(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_presa(self, c):
        try:
            self._gioco_frame.mostra_presa(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_presa(self, c):
        try:
            self._gioco_frame.nascondi_presa(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_set_fronte(self, c, coperta, inst):
        try:
            self._gioco_frame.set_fronte(c, coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_coperta(self, c):
        try:
            return self._gioco_frame.is_coperta(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_sort(self, evt):
        # TODO: riordinare gli sprite
        self._gioco_frame.on_sort()

    def on_resize(self, evt):
        try:
            self._gioco_frame.on_resize(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_mano(self, coord, ccman):
        try:
            self._gioco_frame.on_show_carte_mano(coord, ccman, self._globals.get_instant())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_mano(self, coord, ccman):
        try:
            self._gioco_frame.on_hide_carte_mano(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_tavola(self, coord, ccman):
        try:
            self._gioco_frame.on_show_carte_tavola(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_tavola(self, coord, ccman):
        try:
            self._gioco_frame.on_hide_carte_tavola(coord, ccman)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_presa(self, player, c_list):
        try:
            self._gioco_frame.on_update_punteggi()
            self._gioco_man.on_presa(player, c_list)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_popup(self, txt, visible):
        try:
            return self._gioco_frame.show_popup(txt, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_redraw(self):
        try:
            # TODO Eliminare, serve per stampare le carte in mano
            self._gioco_frame.on_update_punteggi()
            self._gioco_frame.on_redraw()
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)

    def on_cade(self, ppos):
        try:
            self._gioco_frame.update_cade(ppos)
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)

    def on_fola(self, ppos):
        try:
            self._gioco_frame.update_fola(ppos)
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)

    def on_turno(self, ppos):
        try:
            self._gioco_frame.update_turno(ppos)
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)

    def on_players(self):
        try:
            for p in self._gioco_man.get_giocatori():
                self._gioco_frame.set_player_labels(p)
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)

    def on_mazziere(self, ppos, visible=True):
        try:
            self._gioco_frame.update_mazziere(ppos, visible)
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)

    def get_sprite(self, cid):
        try:
            return self._gioco_frame.get_sprite(cid)
        except Exception as e:
                ExceptionMan.manage_exception("", e, True)