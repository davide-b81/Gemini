'''
Created on 19 gen 2022

@author: david
'''

from decks.carta_id import CartaId
from grafica.image_manager import ImageManager
from grafica.sprite_carta import SpriteCarta
from grafica.sprite_mazzo import SpriteMazzo
from grafica.app_sprites import Sprites
from oggetti.posizioni import *
from oggetti.stringhe import _
from oggetti.text_box import TextBox
from main.globals import *
from main.exception_man import ExceptionMan


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
    _box_punti = None
    _manager = None

    '''
    classdocs
    '''
    def __init__(self, manager, screen, pos, gioco_man):
        try:
            self._manager = manager
            self.screen = screen
            self._posizioni = pos
            self.img_man = ImageManager(self._posizioni.get_card_size())
            self._sfondo = self.img_man.get_background_image()
            self._cur_sfondo = pygame.transform.scale(self._sfondo, pygame.display.get_window_size())
            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_PUNTEGGI)
            (w, h) = self._posizioni.get_posizione(PosizioniId.SIZE_PUNTEGGI)
            self._box_punti = TextBox(
                html_text=_(" - Il nobilissimo gioco delle Minchiate Fiorentine - "),
                relative_rect=pygame.Rect(x, y, w, h),
                manager=self._manager,
                visible = 1)

            self.gioco_man = gioco_man
            self.gioco_man.set_delegate_append_text_box(self.write_box_punti)
            self._sprite_man = Sprites(self.img_man, self._posizioni)
            self._mazzo = SpriteMazzo(self.img_man.get_retro())
            self._sprite_man.add_sprite(self._mazzo.get_nome(), self._mazzo)
            for ca in CartaId:
                spr = SpriteCarta(str(ca), self.img_man.get_image(ca), self.img_man.get_retro())
                self._sprite_man.add_sprite(ca, spr)

            self._sprite_man.set_delegate_click(self.gioco_man.on_carta_click)
            self.gioco_man.set_delegate_mescola(self.on_mescola)
            self.gioco_man.set_delegate_show_mano(self._sprite_man.show_carte_mano)
            self.gioco_man.set_delegate_show_tavola(self._sprite_man.show_carte_tavola)
            self.gioco_man.set_delegate_hide_carta(self.on_hide)
            #self.gioco_man.set_delegate_show_carta(self.on_show)
            self.gioco_man.set_delegate_side_carta(self.on_side)
            self.gioco_man.set_delegate_card_move(self.on_move)
            self.gioco_man.set_delegate_restore(self.on_restore)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def imposta_giocatori(self, giocatori):
        try:
            self.gioco_man.set_giocatori(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def imposta_gioco(self, giocatori):
        try:
            self.gioco_man.set_gioco(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def write_box_punti(self, htxt):
        try:
            self._box_punti.append_html_text("<p>" + htxt + "</p>")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_restore(self):
        try:

            self._sprite_man.reset()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_move(self, c, pos):
        try:
            echo_message("On muove " + str(c) + " in (" + str(pos[0]) + ", " + str(pos[1]) + ")")
            #self._sprite_man.set_position(c.get_id(), pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_hide(self, c):
        try:
            self._sprite_man.hide_carta(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_show(self, c):
        try:
            self._sprite_man.show_carta(c.get_id())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_side(self, c, fronte = True):
        try:
            self._sprite_man.set_side(c.get_id(), fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_mescola(self):
        try:
            self._sprite_man.reset()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_event(self, e):
        try:
            self.gioco_man.on_event(e)
            self._sprite_man.on_event(e)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def on_sort(self, evt):
        # TODO: riordinare gli sprite
        self._sprite_man.reset()


    def on_resize(self, evt):
        try:
            self._posizioni.on_resize(evt)
            (x, y) = self._posizioni.get_posizione(PosizioniId.POS_FRAME_PUNTEGGI)
            self._box_punti.set_position((x, y))
            if self._cur_sfondo != None:
                self._cur_sfondo = pygame.transform.scale(self._sfondo, evt.dict['size'])
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def inizia_gioco(self):
        try:
            self._sprite_man.reset()
            self.gioco_man.inizia_gioco()
            self.message_manager.show()
            self.mazzo.show()
            self._sprite_man.update(self.screen)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def update_handler(self, surface):
        try:
            if self._cur_sfondo != None:
                surface.blit(self._cur_sfondo, (0, 0))
            self.gioco_man.update_gioco(self.screen)
            self._sprite_man.update(self.screen)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
