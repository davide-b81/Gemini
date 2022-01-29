'''
Created on 18 gen 2022

@author: david
'''
from pygame_gui.core import ObjectID
from grafica.sprite_carta import *
from main.gioco_frame import GiocoFrame
from game.player import Player
from main.gioco_manager import GiocoManager
from main.globals import *
from main.exception_man import ExceptionMan
from oggetti.posizioni import Posizioni
from oggetti.stringhe import _
import pygame_gui

class Gestore(object):
    clock = None
    manager = None
    button_new = None
    button_exit = None
    button_layout_rect = None
    button_exit_layout_rect = None
    button_new_layout_rect = None
    _gioco_frame = None
    running = None
    _players = None
    _gioco_man = None


    def __init__(self, manager, screen):
        try:
            self.manager = manager
            self.init_buttons()
            self.clock = pygame.time.Clock()
            self._posizioni = Posizioni(screen)
            self._gioco_man = GiocoManager(self._posizioni)
            self._gioco_frame = GiocoFrame(manager, screen, self._posizioni, self._gioco_man)
            self.running = True
            self._players = []
            self.screen = screen
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def init_buttons(self):
        try:
            obj = ObjectID(class_id='@friendly_buttons',  object_id='#nuovo_button')

            self.button_new_layout_rect = pygame.Rect(0, 0, 100, 30)
            self.button_new_layout_rect.bottomright = (-30, -50)
            self.button_new = pygame_gui.elements.UIButton(relative_rect=self.button_new_layout_rect,
                                                        text=_("Nuovo"),
                                                        manager=self.manager,
                                                        anchors={   'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom'},
                                                                    object_id=obj)

            obj = ObjectID(class_id='@friendly_buttons',  object_id='#esci_button')
            self.button_exit_layout_rect = pygame.Rect(0, 0, 100, 30)
            self.button_exit_layout_rect.bottomright = (-30, -20)
            self.button_exit = pygame_gui.elements.UIButton(relative_rect=self.button_exit_layout_rect,
                                                        text=_("Esci"),
                                                        manager=self.manager,
                                                        anchors={   'left': 'right',
                                                                    'right': 'right',
                                                                    'top': 'bottom',
                                                                    'bottom': 'bottom'},
                                                                    object_id=obj)

        except Exception as e:
            echo_message("init_buttons: An error occurred:", e.args[0])


    def event_handler(self, evt):
        try:
            if evt.type == pygame.QUIT:
                self.on_exit(evt)
            if evt.type == pygame_gui.UI_BUTTON_PRESSED:
                self.on_click(evt)
            if evt.type == pygame.MOUSEBUTTONUP:
                self.on_click(evt)
            if evt.type == pygame.VIDEORESIZE:
                self.on_resize(evt)
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_r:
                    self.on_r(evt)
            self._gioco_frame.on_event(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_r(self, evt):
        echo_message("Sort event")
        self._gioco_frame.on_sort(evt)


    def on_resize(self, evt):
        try:
            self.button_exit.update_containing_rect_position()
            self.button_new.update_containing_rect_position()
            self._gioco_frame.on_resize(evt)
            echo_message("Resize event")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_exit(self, evt):
        try:
            self.running = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_update(self, window_surface):
        try:
            if self.clock != None:
                time_delta = self.clock.tick(60) / 1000.0
                self.manager.update(time_delta)
                self._gioco_frame.update_handler(window_surface)
                self.manager.draw_ui(window_surface)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

        return self.running


    def add_player(self, name, pos):
        try:
            player = Player(name, pos)
            self._players.append(player)

            player.set_delegate_sort(self.on_sort)
            player.set_delegate_dichiara(self.on_dichiara)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_nuovo(self, evt):
        try:
            self.add_player("Davide", "Sud")
            self.add_player("Tizio", "Ovest")
            self.add_player("Caio", "Nord")
            self.add_player("Sempronio", "Est")

            self._gioco_frame.gioco_man.set_gioco(self._players, "FsmCartaPiuAlta")
            self._gioco_frame.gioco_man.inizia_gioco()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_termina(self, evt):
        self._gioco_frame.gioco_man.termina_gioco()
        self.running = False


    def on_sort(self, evt):
        self._gioco_frame.on_sort(evt)


    def on_dichiara(self, text):
        try:
            self._gioco_frame.write_box_punti(text)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_click(self, evt):
        try:
            if evt.type == pygame_gui.UI_BUTTON_PRESSED:
                if evt.ui_element == self.button_exit:
                    self.on_termina(evt)
                    self.on_exit(evt)
                elif evt.ui_element == self.button_new:
                    self.on_nuovo(evt)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_mescola(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

