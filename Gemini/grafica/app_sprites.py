'''
Created on 6 gen 2022

@author: david
'''
import traceback

import pygame.sprite

from grafica.my_sprite import MySprite
from grafica.sprite_carta import SpriteCarta
from main.globals import *
from oggetti.posizioni import *
from main.exception_man import ExceptionMan

TOKEN_MANO = "TokenMano"
TOKEN_DEAL = "TokenDealer"
TOKEN_FOLA = "TokenFola"
TOKEN_CADE = "TokenCade"

def reset_sprite(spr):
    try:
        spr.reset()
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

class SpriteManager(object):
    '''
    classdocs
    '''
    _globals = None
    all_sprites = None
    sprite_dic = None
    visible_dic = None
    img_man = None
    pos_man = None
    _hovered_sprite = None
    _colliding_sprite = None
    _delegate_click = None
    _delegate_carta_click = None
    _stable_draw = None
    _evt_queue = None
    _extern_sprites = None

    def __init__(self, img_man, pos_man):
        try:
            '''
            Constructor
            '''
            self._globals = Globals()
            self.all_sprites = pygame.sprite.OrderedUpdates()
            self.img_man = img_man
            self.pos_man = pos_man
            self.sprite_dic = {}
            self.visible_dic = {}
            self._extern_sprites = {}
            self._stable_draw = False
            self._colliding_sprite = None
            self._hovered_sprite = None
            self.set_token_info(self.img_man.get_image_tokenM(), TOKEN_MANO)
            self.set_token_info(self.img_man.get_image_tokenD(), TOKEN_DEAL)
            self.set_token_info(self.img_man.get_image_tokenF(), TOKEN_FOLA)
            self.set_token_info(self.img_man.get_image_tokenC(), TOKEN_CADE)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_token_info(self, img, name):
        try:
            self._extern_sprites[name] = MySprite(name, pygame.transform.scale(img, self._globals.get_positions().get_posizione(PosizioniId.SIZE_TOKEN)))
            self._extern_sprites[name].set_visible(False)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_click(self, f):
        self._delegate_click = f

    def set_delegate_carta_click(self, f):
        self._delegate_carta_click = f

    def add_sprite(self, name, spr):
        try:
            spr.set_visible(False)
            self.all_sprites.add(spr)
            self.sprite_dic[name] = spr
            self.update_sprite_list()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_visible(self, c):
        try:
            return self.sprite_dic[str(c)].get_visible()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_coperta(self, c):
        try:
            return self.sprite_dic[str(c)].get_coperta()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_sprite_carta(self, cid):
        try:
            return self.sprite_dic[str(cid)]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_stable(self):
        try:
            return self.stable_sprites()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_z(self, cid, z):
        try:
            print("z=" + str(cid))
            self.sprite_dic[str(cid)].set_z(z)
            self.update_sprite_list()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def enable_hoover(self, cid, h):
        try:
            self.sprite_dic[str(cid)].enable_hoover(h)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_lato(self, cid, coperta, inst):
        try:
            if self._globals.get_uncover():
                coperta = False
            self._hovered_sprite = None
            if coperta:
                return self.sprite_dic[str(cid)].set_lato(coperta, inst)
            else:
                return self.sprite_dic[str(cid)].set_lato(coperta, inst)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_angolo(self, cid, deg, inst):
        try:
            return self.sprite_dic[str(cid)].set_angolo(deg, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_sprite(self, cid):
        try:
            self.sprite_dic[str(cid)].mostra()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_sprite(self, cid):
        try:
            self.sprite_dic[str(cid)].nascondi()
        except Exception as e:
            ExceptionMan.manage_exception("Error.", e, True)

    def set_pos_carta(self, cid, pos, instant):
        try:
            self.sprite_dic[str(cid)].set_position(pos, instant)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_token(self, name, ppos, visible=True):
        try:
            (x, y) = (0, 0)
            if self._extern_sprites[name] is not None:
                if ppos is None:
                    self._extern_sprites[name].set_visible(False)
                else:
                    self._extern_sprites[name].set_visible(visible)
                    if visible:
                        if name == TOKEN_DEAL:
                            (x, y) = self.pos_man.get_pos_elemento(ElementoId.ELEMENTO_TOKEN_MAZ, ppos)
                        elif name == TOKEN_FOLA:
                            (x, y) = self.pos_man.get_pos_elemento(ElementoId.ELEMENTO_TOKEN_FOL, ppos)
                        elif name == TOKEN_CADE:
                            (x, y) = self.pos_man.get_pos_elemento(ElementoId.ELEMENTO_TOKEN_CAD, ppos)
                        elif name == TOKEN_MANO:
                            (x, y) = self.pos_man.get_pos_elemento(ElementoId.ELEMENTO_TOKEN_TUR, ppos)
                        else:
                            (x, y) = (0, 0)
                        self._extern_sprites[name].set_position((x, y), True)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_carta(self, spr, coord, inst):
        try:
            ppos = self.pos_man.get_area_tavola(coord)
            spr.set_z(0)
            spr.set_position(ppos, inst)
            spr.scopri()
            spr.mostra()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_carte_tavola(self, coord, cctav, inst):
        try:
            if cctav != None:
                if len(cctav) != 0:
                    for ca in cctav:
                        self.show_carta(self.sprite_dic[ca.get_name()], coord, inst)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_carte_tavola(self, coord, cctav):
        try:
            if cctav != None:
                if len(cctav) != 0:
                    for ca in cctav:
                        self.sprite_dic[ca.get_name()].copri()
                        self.sprite_dic[ca.get_name()].nascondi()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sprite_list(self):
        try:
            list = []
            self.all_sprites.empty()

            for key, spr in self.sprite_dic.items():
                if spr.get_visible():
                    list.append(spr)

            for key, spr in self._extern_sprites.items():
                if spr.get_visible():
                    list.append(spr)

            # TODO: Ordinare solo se cambia
            list_sorted = sorted(list, key=lambda x: x.get_z(), reverse=True)

            for spr in list_sorted:
                spr.update()

            self.all_sprites.add(list_sorted)

            self.update_areas()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sort(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("Error.", e, True)

    def redraw(self):
        try:
            self.update_sprite_list()
        except Exception as e:
            ExceptionMan.manage_exception("Error.", e, True)

    def reset(self):
        try:
            for key, spr in self.sprite_dic.items():
                reset_sprite(spr)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def stable_sprites(self):
        try:
            for key, spr in self.sprite_dic.items():
                if not spr.get_stable():
                    return False
            return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self, screen):
        try:
            if screen is not None:
                self._stable_draw = self.stable_sprites()
                self.update_sprite_list()
                self.all_sprites.draw(screen)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_areas(self):
        try:
            collision = False
            mouse = pygame.mouse.get_pos()
            z = 100
            newhover = None

            if self._hovered_sprite is None:
                for spr in self.all_sprites.sprites():
                    if spr.get_collide(mouse):
                        collision = True
                        if spr.get_z() < z:
                            self._colliding_sprite = spr
                            z = spr.get_z()
                            if spr.get_hoverable():
                                newhover = spr

            elif self._hovered_sprite.get_collide(mouse):
                # Still
                newhover = self._hovered_sprite
                collision = True
            else:
                for spr in self.all_sprites.sprites():
                    if spr.get_collide(mouse):
                        collision = True
                        if spr.get_z() < z:
                            self._colliding_sprite = spr
                            z = spr.get_z()
                            if spr.get_hoverable():
                                newhover = spr

            if newhover is not None:
                if newhover != self._hovered_sprite:
                    if self._hovered_sprite is not None:
                        self._hovered_sprite.set_hover(False)
                    self._hovered_sprite = newhover
                    self._hovered_sprite.set_hover(True)
                    #z = newhover.get_z()
                    #print("Hovered " + str(newhover) + " z=" + str(z))
            elif self._hovered_sprite is not None:
                self._hovered_sprite.set_hover(False)
                #print("Unhovered " + str(self._hovered_sprite) + " z=" + str(z))
                self._hovered_sprite = None
            if not collision:
                self._colliding_sprite = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, e):
        try:
            if self._stable_draw:
                if e.type == pygame.MOUSEBUTTONUP and e.button == LEFT_CLICK:
                    if isinstance(self._colliding_sprite, SpriteCarta):
                        self._delegate_carta_click(self._colliding_sprite.get_cid())
                    self._delegate_click()
                elif e.type == pygame.MOUSEMOTION:
                    self.update_areas()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
