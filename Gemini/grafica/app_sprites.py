'''
Created on 6 gen 2022

@author: david
'''
import traceback

import pygame.sprite

from grafica.my_sprite import MySprite
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

class Sprites(object):
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
    delegate_click = None
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

    def set_delegate_click(self, foo):
        try:
            self.delegate_click = foo
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_sprite(self, name, spr):
        try:
            spr.set_visible(False)
            spr.set_z(len(self.all_sprites))
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

    def get_stable(self):
        try:
            return self.stable_sprites()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_z(self, cid, z):
        try:
            self.sprite_dic[str(cid)].set_z(z)
            self.update_sprite_list()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_lato(self, cid, coperta=FRONTE_COPERTA, inst=True):
        try:
            if coperta:
                return self.sprite_dic[str(cid)].set_lato(coperta, inst)
            else:
                return self.sprite_dic[str(cid)].set_lato(coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_angolo(self, cid, deg=0, inst=True):
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

    def set_pos_carta(self, cid, pos=None, instant=False):
        try:
            self.sprite_dic[str(cid)].set_position(pos, instant)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_show_index(self, i, j):
        try:
            """update_show_index(a, b) -> (i, j)
            Calcola l'indice per il posizionamento di carte sovrapposte (a gruppi di 10)
            """
            i = i + 1
            if i >= 10:
                i = 0
                j = j + 1
            return (i, j)
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
                            (x, y) = self.pos_man.get_pos_elemento(ELEMENTO_TOKEN_MAZ, ppos)
                            #print("Move to " + str(x) + " " + str(y))
                        elif name == TOKEN_FOLA:
                            (x, y) = self.pos_man.get_pos_elemento(ELEMENTO_TOKEN_FOL, ppos)
                        elif name == TOKEN_CADE:
                            (x, y) = self.pos_man.get_pos_elemento(ELEMENTO_TOKEN_CAD, ppos)
                        elif name == TOKEN_MANO:
                            (x, y) = self.pos_man.get_pos_elemento(ELEMENTO_TOKEN_TUR, ppos)
                        else:
                            (x, y) = (1030, 1000)
                        self._extern_sprites[name].move_to(x, y)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_carte_tavola(self, coord, cctav):
        try:
            if cctav != None:
                if len(cctav) != 0:
                    for ca in cctav:
                        ppos = self.pos_man.get_area_tavola(coord)

                        self.sprite_dic[ca.get_name()].set_z(0)
                        self.sprite_dic[ca.get_name()].set_position(ppos)
                        self.sprite_dic[ca.get_name()].scopri()
                        self.sprite_dic[ca.get_name()].mostra()
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

            for key, spr in self._extern_sprites.items():
                if spr.get_visible():
                    list.append(spr)

            for key, spr in self.sprite_dic.items():
                if spr.get_visible():
                    if spr.get_visible() and spr.is_front() and str(self._hovered_sprite) == str(spr):
                        pass
                    else:
                        list.append(spr)
            # TODO: Ordinare solo se cambia
            list_sorted = sorted(list, key=lambda x: x.get_z_index(), reverse=True)
            for spr in list_sorted:
                spr.update()
            self.all_sprites.add(list_sorted)
            if self._hovered_sprite is not None:
                self.all_sprites.add(self._hovered_sprite)
            self.update_areas()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_carte_mano(self, coord, ccman):
        ic = 0
        jc = 0
        z = 0

        try:
            if ccman != None:
                for ca in ccman:
                    if ca is not None:
                        spr = self.sprite_dic[ca.get_name()]
                        pos = self.pos_man.get_pos_carta_mano(coord, z, len(ccman))
                        if coord == POSTAZIONE_NORD:
                            spr.set_grad(DEG_FLIP)
                        elif coord == POSTAZIONE_EST:
                            spr.set_grad(DEG_ANTC_RECT)
                        elif coord == POSTAZIONE_OVEST:
                            spr.set_grad(DEG_CLOC_RECT)
                        elif coord == POSTAZIONE_SUD:
                            spr.set_grad(DEG_NORMAL)
                        else:
                            pass
                        '''                        
                            ppos = self.pos_man.get_pos_carta_mano
                                self.pos_man.get_area_mano(coord, ic, 0)
                            ic = ic + 1
                            ppos = self.pos_man.get_area_mano(coord, ic, 0)
                            ic = ic + 1
                            ppos = self.pos_man.get_area_mano(coord, jc, ic)
                            (ic, jc) = self.update_show_index(ic, jc)
                            ppos = self.pos_man.get_area_mano(coord, jc, ic)
                            (ic, jc) = self.update_show_index(ic, jc)

                        # To sort the list in place...
                        # ut.sort(key=lambda x: x.count, reverse=True)
'''
                        spr.set_visible(True)
                        spr.set_position(pos)
                        spr.set_z(z)
                        z = z + 1

                    # Sort by z-index (overlapped correctly)
                    #list = sorted(list, key=lambda x: x.get_z_index(), reverse=False)
                    #self.all_sprites.add(list)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_carte_mano(self, ccman):
        try:
            if ccman != None:
                for c in ccman:
                    if c is not None:
                        spr = self.sprite_dic[c.get_name()]
                        spr.set_visible(False)
                        spr.nascondi()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_mazzo(self, ccmazz, plpos = None):
        try:
            i = 0
            for c in ccmazz:
                spr = self.sprite_dic[c.get_name()]
                ppos = self.pos_man.get_area_mazzo(plpos)
                (x, y) = (ppos[0] + i, ppos[1])
                spr.set_position((x, y))
                spr.set_z(i)
                spr.set_visible(True)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_mazzo(self, ccmazz):
        try:
            for ca in ccmazz:
                self.sprite_dic[ca.get_name()].set_visible(False)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_pozzo(self, ca):
        try:
            echo_message("Pozzo visibile")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_pozzo(self, ca):
        try:
            echo_message("Pozzo nascosto")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_fola(self, ca):
        try:
            echo_message("Fola visibile")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def hide_fola(self, ca):
        try:
            echo_message("Fola nascosta")
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
            hovered = None
            flag = False
            mouse = pygame.mouse.get_pos()
            z = 100

            for spr in self.all_sprites.sprites():
                if spr.get_z_index() < z:
                    if spr.get_visible():
                        if spr.get_collide(mouse):
                            flag = True
                            z = spr.get_z_index()
                            hovered = spr
            if not flag:
                self._hovered_sprite = None
            elif str(self._hovered_sprite) != str(hovered):
                self._hovered_sprite = hovered
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, e):
        try:
            if e.type == pygame.MOUSEBUTTONUP and e.button == LEFT_CLICK:
                if self.delegate_click is not None and self._hovered_sprite is not None:
                    self.delegate_click(self._hovered_sprite)
            if e.type == pygame.MOUSEMOTION:
                    self.update_areas()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
