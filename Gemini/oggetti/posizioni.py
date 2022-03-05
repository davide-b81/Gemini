'''
Created on 6 gen 2022

@author: david
'''
from enum import Enum

import pygame
from main.exception_man import ExceptionMan

POS_NORD = 0
POS_SUD = 1
POS_EST = 2
POS_OVEST = 3

DECK_TAGLIO = 1
DECK_MAZZO = 2
DECK_FOLA = 3
DECK_RUBATE = 4
DECK_SCARTO = 5

ELEMENTO_TOKEN_TUR = 0
ELEMENTO_TOKEN_MAZ = 1
ELEMENTO_TOKEN_CAD = 1
ELEMENTO_TOKEN_FOL = 1
ELEMENTO_FOLA = 2
ELEMENTO_MANO = 3

class PosizioniId(Enum):
    POS_MANO_N = 0
    POS_MANO_S = 1
    POS_MANO_E = 2
    POS_MANO_O = 3

    POS_CALATA_N = 4
    POS_CALATA_S = 5
    POS_CALATA_E = 6
    POS_CALATA_O = 7

    POS_DECK_DEFAULT = 8
    POS_DECK_N = 9
    POS_DECK_S = 10
    POS_DECK_E = 11
    POS_DECK_O = 12

    POS_TAGLIO_DEFAULT = 13
    POS_TAGLIO_N = 14
    POS_TAGLIO_S = 15
    POS_TAGLIO_E = 16
    POS_TAGLIO_O = 17

    POS_PRESA_NS = 20
    POS_PRESA_EW = 21

    POS_MOSTRATA_N = 25
    POS_MOSTRATA_S = 26
    POS_MOSTRATA_E = 27
    POS_MOSTRATA_O = 28

    POS_FRAME_PUNTEGGI = 32

    POS_FRAME_LOG = 33
    SIZE_FRAME_LOG = 34

    POS_FRAME_RESTI = 35
    SIZE_RESTI = 36

    POS_SCREEN_CENTRO = 37

    POS_INVISIBLE = 40
    SIZE_PUNTEGGI = 41

    POS_POPUP = 45
    SIZE_POPUP = 46

    POS_OCLOCK = 50
    SIZE_OCLOCK = 51

    RPOS_BUTTON_TEST = 60
    RPOS_BUTTON_NEW = 61
    RPOS_BUTTON_STOP = 62
    RPOS_BUTTON_EXIT = 63
    SIZE_BUTTON = 64

    POS_FOLA_N = 80
    POS_FOLA_S = 81
    POS_FOLA_E = 82
    POS_FOLA_O = 83
    POS_FOLA_SHOW_N = 90
    POS_FOLA_SHOW_S = 91
    POS_FOLA_SHOW_E = 93
    POS_FOLA_SHOW_O = 93

    POS_RUBATE_N = 100
    POS_RUBATE_S = 101
    POS_RUBATE_E = 102
    POS_RUBATE_O = 103

    POS_SCARTO_DEFAULT = 110
    POS_SCARTO_N = 111
    POS_SCARTO_S = 112
    POS_SCARTO_E = 113
    POS_SCARTO_O = 114

    POS_TOKEN_M_N = 120
    POS_TOKEN_M_S = 121
    POS_TOKEN_M_E = 122
    POS_TOKEN_M_O = 123
    POS_TOKEN_D_N = 125
    POS_TOKEN_D_S = 126
    POS_TOKEN_D_E = 127
    POS_TOKEN_D_O = 128
    SIZE_TOKEN = 129


class Posizioni(object):
    '''
    classdocs
    '''
    screen = None
    titolo_pos = None
    text_pos = None
    desk_area = None
    desk_pos = None
    etic_pos_n = None
    etic_pos_s = None
    etic_pos_e = None
    etic_pos_o = None
    gioc_pos_n = None
    gioc_pos_s = None
    gioc_pos_e = None
    gioc_pos_o = None
    desk_centro = None
    left_bar_pos = (0, 0)
    left_bar_len = (250, 40)
    button_wi = 50
    button_he = 50
    mano_margin = 100
    margin = 25
    sfals = 50
    _sizemano = (50, 50)
    margine_mano_altrui = 5
    _card_size = None
    posizioni = {}
    _elementi = []
    _resolution = None

    def __init__(self, screen):
        try:
            '''
            Constructor
            '''
            self.screen = screen
            self._card_size = (126, 126 * 1.65)
            self._elementi.append([])
            self._elementi.append([])
            self._elementi.append([])
            self._elementi.append([])
            self.init_positions()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_card_size(self):
        try:
            w = 0.065 * self.screen.get_width()
            h = 0.15 * self.screen.get_height()

            self._card_size = ((w, h))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sizemano(self):
        try:
            siz_x = self.screen.get_width() - (6 * self._card_size[0])
            siz_y = self.screen.get_height() - (4 * self._card_size[0])
            self._sizemano = (siz_x, siz_y)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_resize(self, evt):
        try:
            wsize = (self.screen.get_width(), self.screen.get_height())
            if self._resolution is None or self._resolution != wsize:
                self.init_positions()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def init_positions(self):
        try:
            self._elementi[POS_NORD].clear()
            self._elementi[POS_SUD].clear()
            self._elementi[POS_EST].clear()
            self._elementi[POS_OVEST].clear()

            wsize = (self.screen.get_width(), self.screen.get_height())
            self.update_card_size()
            self.update_sizemano()
            self._resolution = wsize
            centro = ((wsize[0] / 2, wsize[1] / 2))

            self.posizioni[PosizioniId.POS_SCREEN_CENTRO] = centro

            self.desk_area = pygame.Surface((self.screen.get_width() / 2.25, self.screen.get_height() / 2.0))
            self.desk_pos = ((self.screen.get_width() / 2) - (self.desk_area.get_width() / 2),
                             (self.screen.get_height() / 2.0) - (self.desk_area.get_height() / 2.0))
            self.desk_centro = (
                self.desk_pos[0] + (self.desk_area.get_width() / 2),
                self.desk_pos[1] + (self.desk_area.get_height() / 2))
            self.gioc_pos_n = (self.desk_centro[0], self.desk_pos[1])
            self.gioc_pos_s = (self.desk_centro[0], self.desk_pos[1] + (self.screen.get_height() / 2))
            self.gioc_pos_e = (self.desk_area.get_width() + self.desk_pos[0], self.desk_centro[1])
            self.gioc_pos_o = (self.desk_pos[0], self.desk_centro[1])

            self.mano_area = pygame.Surface(
                ((self.screen.get_width() / 3), (self.screen.get_height() - (self.desk_area.get_height()) / 2)))
            self.mano_pos = ((self.desk_area.get_width() / 2), self.desk_pos[1] + self.desk_area.get_height())

            self.etic_pos_n = ((self.screen.get_width() / 2), self.desk_pos[1])
            self.etic_pos_s = ((self.screen.get_width() / 2), self.desk_pos[1] + self.desk_area.get_height())
            self.etic_pos_e = (self.desk_pos[0] + self.desk_area.get_width(), self.desk_centro[1])
            self.etic_pos_o = (self.desk_pos[0], self.desk_centro[1])

            self.posizioni[PosizioniId.POS_MANO_N] = (centro[0], self.margin)
            self.posizioni[PosizioniId.POS_MANO_S] = (centro[0], wsize[1] - self._card_size[1] - self.margin)
            self.posizioni[PosizioniId.POS_MANO_O] = (self.margin, centro[1])
            self.posizioni[PosizioniId.POS_MANO_E] = (wsize[0] - self._card_size[0] - self.margin, centro[1])

            self.posizioni[PosizioniId.POS_FOLA_N] = (centro[0], self.margin + self._card_size[1] + self.margin)
            self.posizioni[PosizioniId.POS_FOLA_S] = (centro[0], wsize[1] - self._card_size[1] - self.margin - self._card_size[1] - self.margin)
            self.posizioni[PosizioniId.POS_FOLA_E] = (self.posizioni[PosizioniId.POS_MANO_O][0] - self._card_size[1] - self.margin, centro[1])
            self.posizioni[PosizioniId.POS_FOLA_O] = (self.posizioni[PosizioniId.POS_MANO_O][0] + self._card_size[1] + self.margin, centro[1])
            self.posizioni[PosizioniId.POS_FOLA_SHOW_N] = self.posizioni[PosizioniId.POS_FOLA_N]
            self.posizioni[PosizioniId.POS_FOLA_SHOW_S] = self.posizioni[PosizioniId.POS_FOLA_S]
            self.posizioni[PosizioniId.POS_FOLA_SHOW_E] = self.posizioni[PosizioniId.POS_FOLA_E]
            self.posizioni[PosizioniId.POS_FOLA_SHOW_O] = self.posizioni[PosizioniId.POS_FOLA_O]

            self.posizioni[PosizioniId.POS_CALATA_N] = (centro[0], centro[1] - self._card_size[1])
            self.posizioni[PosizioniId.POS_CALATA_S] = (centro[0], centro[1] + self._card_size[0])
            self.posizioni[PosizioniId.POS_CALATA_E] = (centro[0] + self._card_size[0], centro[1])
            self.posizioni[PosizioniId.POS_CALATA_O] = (centro[0] - self._card_size[0], centro[1])

            self.posizioni[PosizioniId.POS_DECK_DEFAULT] = centro
            self.posizioni[PosizioniId.POS_DECK_N] = (2 * self._card_size[0], self._card_size[1])
            self.posizioni[PosizioniId.POS_DECK_S] = (wsize[0] - (2 * self._card_size[0]), wsize[1] - self._card_size[1] - self.margin)
            self.posizioni[PosizioniId.POS_DECK_E] = (wsize[0] - (2 * self._card_size[1] - self.margin), self._card_size[0] + self.margin)
            self.posizioni[PosizioniId.POS_DECK_O] = (self._card_size[0], wsize[1] - (2 * self._card_size[1]))

            self.posizioni[PosizioniId.POS_TAGLIO_DEFAULT] = (self.posizioni[PosizioniId.POS_DECK_DEFAULT][0] + self._card_size[0] + self.margin, self.posizioni[PosizioniId.POS_DECK_DEFAULT][0])
            self.posizioni[PosizioniId.POS_TAGLIO_N] = (self.posizioni[PosizioniId.POS_DECK_N][0] + self._card_size[0] + self.margin, self.posizioni[PosizioniId.POS_DECK_N][1])
            self.posizioni[PosizioniId.POS_TAGLIO_S] = (self.posizioni[PosizioniId.POS_DECK_S][0] - self._card_size[0] - self.margin, self.posizioni[PosizioniId.POS_DECK_S][1])
            self.posizioni[PosizioniId.POS_TAGLIO_O] = (self.posizioni[PosizioniId.POS_DECK_O][0], self.posizioni[PosizioniId.POS_DECK_O][1] - self._card_size[0] - self.margin)
            self.posizioni[PosizioniId.POS_TAGLIO_E] = (self.posizioni[PosizioniId.POS_DECK_E][0], self.posizioni[PosizioniId.POS_DECK_E][1] + self._card_size[0] + self.margin)

            self.posizioni[PosizioniId.POS_PRESA_NS] = (self._card_size[0] + self.margin,  self.margin)
            self.posizioni[PosizioniId.POS_PRESA_EW] = (self.margin,  self._card_size[1] + self.margin)

            self.posizioni[PosizioniId.POS_MOSTRATA_N] = self.posizioni[PosizioniId.POS_DECK_N]
            self.posizioni[PosizioniId.POS_MOSTRATA_S] = self.posizioni[PosizioniId.POS_DECK_S]
            self.posizioni[PosizioniId.POS_MOSTRATA_E] = self.posizioni[PosizioniId.POS_DECK_E]
            self.posizioni[PosizioniId.POS_MOSTRATA_O] = self.posizioni[PosizioniId.POS_DECK_O]
            self.posizioni[PosizioniId.POS_FRAME_RESTI] = 19

            self.posizioni[PosizioniId.POS_RUBATE_N] = self.posizioni[PosizioniId.POS_MOSTRATA_N]
            self.posizioni[PosizioniId.POS_RUBATE_S] = self.posizioni[PosizioniId.POS_MOSTRATA_S]
            self.posizioni[PosizioniId.POS_RUBATE_E] = self.posizioni[PosizioniId.POS_MOSTRATA_E]
            self.posizioni[PosizioniId.POS_RUBATE_O] = self.posizioni[PosizioniId.POS_MOSTRATA_O]

            self.posizioni[PosizioniId.SIZE_PUNTEGGI] = (self._card_size[0] * 3, wsize[1] / 3)
            self.posizioni[PosizioniId.POS_FRAME_PUNTEGGI] = (self.margin, self.margin)

            self.posizioni[PosizioniId.SIZE_FRAME_LOG] = (self._card_size[0] * 3, wsize[1] / 6)
            self.posizioni[PosizioniId.POS_FRAME_LOG] = (0, wsize[1] - self.posizioni[PosizioniId.SIZE_FRAME_LOG][1])

            self.posizioni[PosizioniId.POS_POPUP] = (centro[0], centro[1])
            self.posizioni[PosizioniId.SIZE_POPUP] = (wsize[0] / 4, wsize[1] / 4)

            self.posizioni[PosizioniId.POS_OCLOCK] = (wsize[0]-(4*self.margin), self.margin)
            self.posizioni[PosizioniId.SIZE_OCLOCK] = ((2*self.margin),  self.margin)

            self.posizioni[PosizioniId.RPOS_BUTTON_TEST] = (-30, -110)
            self.posizioni[PosizioniId.RPOS_BUTTON_NEW] = (-30, -50)
            self.posizioni[PosizioniId.RPOS_BUTTON_STOP] = (-30, -80)
            self.posizioni[PosizioniId.RPOS_BUTTON_EXIT] = (-30, -20)
            self.posizioni[PosizioniId.SIZE_BUTTON] = (100, 30)

            self.posizioni[PosizioniId.POS_SCARTO_DEFAULT] = (30, 0)

            self._elementi[POS_NORD].insert(ELEMENTO_TOKEN_FOL, (wsize[0] + 5/ 2, 75))
            self._elementi[POS_SUD].insert(ELEMENTO_TOKEN_FOL, (5 + wsize[0] / 2, wsize[1] - 75))
            self._elementi[POS_OVEST].insert(ELEMENTO_TOKEN_FOL, (5 + 75, wsize[1] / 2))
            self._elementi[POS_EST].insert(ELEMENTO_TOKEN_FOL, (5 + wsize[0] - 75, wsize[1] / 2))

            self._elementi[POS_NORD].insert(ELEMENTO_TOKEN_MAZ, (10 + wsize[0] / 2, 75))
            self._elementi[POS_SUD].insert(ELEMENTO_TOKEN_MAZ, (10 + wsize[0] / 2, wsize[1] - 75))
            self._elementi[POS_OVEST].insert(ELEMENTO_TOKEN_MAZ, (10 + 75, wsize[1] / 2))
            self._elementi[POS_EST].insert(ELEMENTO_TOKEN_MAZ, (10 + wsize[0] - 75, wsize[1] / 2))

            self._elementi[POS_NORD].insert(ELEMENTO_TOKEN_TUR, (wsize[0] / 2, wsize[1] / 4))
            self._elementi[POS_SUD].insert(ELEMENTO_TOKEN_TUR, (wsize[0] / 2, 3 * wsize[1] / 4))
            self._elementi[POS_OVEST].insert(ELEMENTO_TOKEN_TUR, (wsize[0] / 4, wsize[1] / 2))
            self._elementi[POS_EST].insert(ELEMENTO_TOKEN_TUR, (3 * wsize[0] / 4, wsize[1] / 2))

            self._elementi[POS_NORD].insert(ELEMENTO_TOKEN_MAZ, (wsize[0] / 2, 75))
            self._elementi[POS_SUD].insert(ELEMENTO_TOKEN_MAZ, (wsize[0] / 2, wsize[1] - 75))
            self._elementi[POS_OVEST].insert(ELEMENTO_TOKEN_MAZ, (75, wsize[1] / 2))
            self._elementi[POS_EST].insert(ELEMENTO_TOKEN_MAZ, (wsize[0] - 75, wsize[1] / 2))
            self.posizioni[PosizioniId.SIZE_TOKEN] = (50, 50)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_elemento(self, elem, ppos):
        try:
            if ppos == "Nord":
                pos_id = POS_NORD
            elif ppos == "Sud":
                pos_id = POS_SUD
            elif ppos == "Est":
                pos_id = POS_EST
            elif ppos == "Ovest":
                pos_id = POS_OVEST
            else:
                pos_id = POS_NORD
            return self._elementi[pos_id][elem]
        except Exception as e:
            print(str(self._elementi))
            ExceptionMan.manage_exception(str(pos_id) + ", " + str(elem), e, True)

    def get_posizione(self, id):
        try:
            assert self.posizioni[id] is not None
            return self.posizioni[id]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_id_mazzo(self, pos=None):
        try:
            if pos is None:
                return PosizioniId.POS_DECK_DEFAULT
            elif pos == "Nord":
                return PosizioniId.POS_DECK_N
            elif pos == "Sud":
                return PosizioniId.POS_DECK_S
            elif pos == "Est":
                return PosizioniId.POS_DECK_E
            elif pos == "Ovest":
                return PosizioniId.POS_DECK_O
            else:
                return PosizioniId.POS_DECK_DEFAULT
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_id_taglio(self, pos=None):
        try:
            if pos is None:
                return PosizioniId.POS_TAGLIO_DEFAULT
            elif pos == "Nord":
                return PosizioniId.POS_TAGLIO_N
            elif pos == "Sud":
                return PosizioniId.POS_TAGLIO_S
            elif pos == "Est":
                return PosizioniId.POS_TAGLIO_E
            elif pos == "Ovest":
                return PosizioniId.POS_TAGLIO_O
            else:
                return PosizioniId.POS_TAGLIO_DEFAULT
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_id_fola(self, pos=None):
        try:
            if pos is None:
                return PosizioniId.POS_FOLA_DEFAULT
            elif pos == "Nord":
                return PosizioniId.POS_FOLA_N
            elif pos == "Sud":
                return PosizioniId.POS_FOLA_S
            elif pos == "Est":
                return PosizioniId.POS_FOLA_E
            elif pos == "Ovest":
                return PosizioniId.POS_FOLA_O
            else:
                return PosizioniId.POS_FOLA_DEFAULT
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_id_scarti(self, pos=None):
        try:
            if pos is None:
                return PosizioniId.POS_SCARTO_DEFAULT
            elif pos == "Nord":
                return PosizioniId.POS_SCARTO_N
            elif pos == "Sud":
                return PosizioniId.POS_SCARTO_S
            elif pos == "Est":
                return PosizioniId.POS_SCARTO_E
            elif pos == "Ovest":
                return PosizioniId.POS_SCARTO_O
            else:
                return PosizioniId.POS_SCARTO_DEFAULT
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_id_rubate(self, pos=None):
        try:
            if pos is None:
                return PosizioniId.POS_FOLA_DEFAULT
            elif pos == "Nord":
                return PosizioniId.POS_RUBATE_N
            elif pos == "Sud":
                return PosizioniId.POS_RUBATE_S
            elif pos == "Est":
                return PosizioniId.POS_RUBATE_E
            elif pos == "Ovest":
                return PosizioniId.POS_RUBATE_O
            else:
                return PosizioniId.POS_FOLA_DEFAULT
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_area_mazzo(self, pos=None):
        try:
            if pos is None:
                (x, y) = self.get_posizione(PosizioniId.POS_DECK_DEFAULT)
            elif pos == "Nord":
                    (x, y) = self.get_posizione(PosizioniId.POS_DECK_N)
            elif pos == "Sud":
                    (x, y) = self.get_posizione(PosizioniId.POS_DECK_S)
            elif pos == "Est":
                    (x, y) = self.get_posizione(PosizioniId.POS_DECK_E)
                    margin = 20
            elif pos == "Ovest":
                    (x, y) = self.get_posizione(PosizioniId.POS_DECK_O)
            else:
                raise Exception("Wrong position " + str(pos))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return (x, y)

    def get_scoperte_davavanti_a_se(self, pos=None):
        try:
            if pos is None:
                (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_DEFAULT)
            elif pos == "Nord":
                    (x, y) = self.get_posizione(PosizioniId.POS_RUBATE_N)
            elif pos == "Sud":
                    (x, y) = self.get_posizione(PosizioniId.POS_RUBATE_S)
            elif pos == "Est":
                    (x, y) = self.get_posizione(PosizioniId.POS_RUBATE_E)
                    margin = 20
            elif pos == "Ovest":
                    (x, y) = self.get_posizione(PosizioniId.POS_RUBATE_O)
            else:
                (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_DEFAULT)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return (x, y)

    def get_area_taglio(self, pos=None):
        try:
            if pos is None:
                (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_DEFAULT)
            elif pos == "Nord":
                    (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_N)
            elif pos == "Sud":
                    (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_S)
            elif pos == "Est":
                    (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_E)
                    margin = 20
            elif pos == "Ovest":
                    (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_O)
            else:
                (x, y) = self.get_posizione(PosizioniId.POS_TAGLIO_DEFAULT)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return (x, y)

    def get_area_fola(self, pos=None):
        try:
            if pos is None:
                (x, y) = self.get_posizione(PosizioniId.POS_FOLA_DEFAULT)
            elif pos == "Nord":
                    (x, y) = self.get_posizione(PosizioniId.POS_FOLA_N)
            elif pos == "Sud":
                    (x, y) = self.get_posizione(PosizioniId.POS_FOLA_S)
            elif pos == "Est":
                    (x, y) = self.get_posizione(PosizioniId.POS_FOLA_E)
                    margin = 20
            elif pos == "Ovest":
                    (x, y) = self.get_posizione(PosizioniId.POS_FOLA_O)
            else:
                (x, y) = self.get_posizione(PosizioniId.POS_FOLA_DEFAULT)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return (x, y)

    def get_id_pos(self, deck, ppos):
        try:
            if deck == DECK_MAZZO:
                return self.get_pos_id_mazzo(ppos)
            elif deck == DECK_TAGLIO:
                return self.get_pos_id_taglio(ppos)
            elif deck == DECK_FOLA:
                return self.get_pos_id_fola(ppos)
            elif deck == DECK_RUBATE:
                return self.get_pos_id_rubate(ppos)
            else:
                raise Exception("Unknown deck id")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_stesa(self, ppos, deck, i, ntot, sfals):
        try:
            idpos = self.get_id_pos(deck, ppos)
            (x, y) = self.get_posizione(idpos)
            ofs = sfals * i

            if ppos == "Nord":
                len = self._card_size[0] + (sfals * ntot) - sfals
                x0 = self.desk_centro[0] + (len/2) - (self._card_size[0]/2)
                pos = (x0 - ofs, y)
            elif ppos == "Sud":
                len = self._card_size[0] + (sfals * ntot) - sfals
                x0 = self.desk_centro[0] - (len/2) + (self._card_size[0]/2)
                pos = (x0 + ofs, y)
            elif ppos == "Est":
                len = self._card_size[1] + (sfals * ntot) - sfals
                y0 = self.desk_centro[1] + (len/2) - (self._card_size[0]/2)
                pos = (x, y0 - ofs)
            elif ppos == "Ovest":
                len = self._card_size[1] + (sfals * ntot) - sfals
                y0 = self.desk_centro[1] - (len/2) + (self._card_size[0]/2)
                pos = (x, y0 + ofs)
            else:
                pos = (0, 0)
            return pos
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_carta_mano(self, ppos, i, ntot):
        try:
            if ppos == "Nord" or ppos == "Sud":
                sfals = self._sizemano[0] / ntot
                len = self._card_size[0] + (sfals * ntot) - sfals
            elif ppos == "Est" or ppos == "Ovest":
                sfals = self._sizemano[1] / ntot
                len = self._card_size[1] + (sfals * ntot) - sfals

            ofs = sfals * i
            if ppos == "Nord":
                (x, y) = self.get_posizione(PosizioniId.POS_MANO_N)
                x0 = self.desk_centro[0] + (len/2) - (self._card_size[0]/2)
                pos = (x0 - ofs, y)
            elif ppos == "Sud":
                (x, y) = self.get_posizione(PosizioniId.POS_MANO_S)
                x0 = self.desk_centro[0] - (len/2) + (self._card_size[0]/2)
                pos = (x0 + ofs, y)
            elif ppos == "Est":
                (x, y) = self.get_posizione(PosizioniId.POS_MANO_E)
                y0 = self.desk_centro[1] + (len/2) - (self._card_size[0]/2)
                pos = (x, y0 - ofs)
            elif ppos == "Ovest":
                (x, y) = self.get_posizione(PosizioniId.POS_MANO_O)
                y0 = self.desk_centro[1] - (len/2) + (self._card_size[0]/2)
                pos = (x, y0 + ofs)
            else:
                pos = (0, 0)
            return pos
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_card_size(self):
        try:
            return self._card_size
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_area_tavola(self, coord):
        try:
            if coord == "Nord":
                return self.posizioni[PosizioniId.POS_CALATA_N]
            elif coord == "Sud":
                return self.posizioni[PosizioniId.POS_CALATA_S]
            elif coord == "Est":
                return self.posizioni[PosizioniId.POS_CALATA_E]
            elif coord == "Ovest":
                return self.posizioni[PosizioniId.POS_CALATA_O]
            else:
                raise Exception("Posizione", coord, "sconosciuta")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_etichetta_pos(self, coord):
        try:
            if coord == "Nord":
                return self.etic_pos_n
            elif coord == "Sud":
                return self.etic_pos_s
            elif coord == "Est":
                return self.etic_pos_e
            elif coord == "Ovest":
                return self.etic_pos_o
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
