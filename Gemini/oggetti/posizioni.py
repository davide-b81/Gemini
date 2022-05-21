'''
Created on 6 gen 2022

@author: david
'''
from enum import Enum
import pygame

from main.exception_man import ExceptionMan

POSTAZIONE_NORD = "Nord"
POSTAZIONE_OVEST = "Ovest"
POSTAZIONE_EST = "Est"
POSTAZIONE_SUD = "Sud"

class PosId(Enum):
    """ Indici di array, devono essere consecutivi e gli array riempiti in questo stesso ordine, altrimenti la insert crea problemi """
    POS_NORD = 0
    POS_SUD = 1
    POS_EST = 2
    POS_OVEST = 3

class DeckId(Enum):
    """ Indici di array, devono essere consecutivi e gli array riempiti in questo stesso ordine, altrimenti la insert crea problemi """
    DECK_TAGLIO = 0
    DECK_MAZZO = 1
    DECK_FOLA = 2
    DECK_RUBATE = 3
    DECK_TAVOLA = 4
    DECK_SCARTO = 5
    DECK_POZZO = 6
    DECK_MANO = 7
    DECK_PRESE = 8

class ElementoId(Enum):
    """ Indici di array, devono essere consecutivi e gli array riempiti in questo stesso ordine, altrimenti la insert crea problemi """
    ELEMENTO_TOKEN_TUR = 0
    ELEMENTO_TOKEN_MAZ = 1
    ELEMENTO_TOKEN_CAD = 2
    ELEMENTO_TOKEN_FOL = 3
    ELEMENTO_NOME_LABEL = 4
    ELEMENTO_MAZZO = 5
    ELEMENTO_FOLA = 6
    ELEMENTO_RUBATE = 7
    ELEMENTO_TAVOLA = 7
    ELEMENTO_SCARTI = 8
    ELEMENTO_FOLA_STESA = 9
    ELEMENTO_MANO = 10
    ELEMENTO_TAGLIO = 11
    ELEMENTO_MOSTRATE = 12
    ELEMENTO_CALATA = 14
    ELEMENTO_PRESA = 15

class SizeId(Enum):
    """ Indici di array, devono essere consecutivi e gli array riempiti in questo stesso ordine, altrimenti la insert crea problemi """
    SIZE_LABEL = 0

class PosizioniId(Enum):
    POS_DECK_DEFAULT = 8
    POS_TAGLIO_DEFAULT = 13

    POS_PRESA_NS = 20
    POS_PRESA_EW = 21

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

    RPOS_BUTTON_SAVE = 59
    RPOS_BUTTON_REST = 60
    RPOS_BUTTON_NEW = 61
    RPOS_BUTTON_STOP = 62
    RPOS_BUTTON_EXIT = 63
    SIZE_BUTTON = 64

    POS_RUBATE_DEFAULT = 103
    POS_MOSTRATE_DEFAULT = 104
    POS_SCARTO_DEFAULT = 110

    POS_TOKEN_M_N = 120
    POS_TOKEN_M_S = 121
    POS_TOKEN_M_E = 122
    POS_TOKEN_M_O = 123
    POS_TOKEN_D_N = 125
    POS_TOKEN_D_S = 126
    POS_TOKEN_D_E = 127
    POS_TOKEN_D_O = 128
    SIZE_TOKEN = 129
    SIZE_LABEL = 133

class Posizioni(object):
    '''
    classdocs
    '''
    screen = None
    titolo_pos = None
    text_pos = None
    desk_area = None
    desk_pos = None
    desk_centro = None
    left_bar_pos = (0, 0)
    left_bar_len = (250, 40)
    button_wi = 50
    button_he = 50
    mano_margin = 101
    margin = 25
    sfals = 50
    _sizemano = (50, 50)
    margine_mano_altrui = 5
    _card_size = None
    _posizioni = None
    _dimensioni = None
    _elementi = None
    _resolution = None

    def __init__(self, screen):
        try:
            '''
            Constructor
            '''
            self.screen = screen
            self._card_size = (126, 126 * 1.65)
            self._elementi = {}
            self._elementi[PosId.POS_NORD] = {}
            self._elementi[PosId.POS_SUD] = {}
            self._elementi[PosId.POS_OVEST] = {}
            self._elementi[PosId.POS_EST] = {}
            self._posizioni = {}
            self._dimensioni = {}
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
            self._elementi[PosId.POS_NORD].clear()
            self._elementi[PosId.POS_SUD].clear()
            self._elementi[PosId.POS_EST].clear()
            self._elementi[PosId.POS_OVEST].clear()

            wsize = (self.screen.get_width(), self.screen.get_height())
            self.update_card_size()
            self.update_sizemano()
            self._resolution = wsize
            centro = ((wsize[0] / 2, wsize[1] / 2))

            self._posizioni[PosizioniId.POS_SCREEN_CENTRO.value] = centro

            self.desk_area = pygame.Surface((self.screen.get_width() / 2.25, self.screen.get_height() / 2.0))
            self.desk_pos = ((self.screen.get_width() / 2) - (self.desk_area.get_width() / 2),
                             (self.screen.get_height() / 2.0) - (self.desk_area.get_height() / 2.0))
            self.desk_centro = (
                self.desk_pos[0] + (self.desk_area.get_width() / 2),
                self.desk_pos[1] + (self.desk_area.get_height() / 2))

            self._posizioni[PosizioniId.POS_DECK_DEFAULT] = (centro[0], centro[1])
            self._posizioni[PosizioniId.POS_TAGLIO_DEFAULT] = (self._posizioni[PosizioniId.POS_DECK_DEFAULT][0] + self._card_size[0] + self.margin, self._posizioni[PosizioniId.POS_DECK_DEFAULT][0])

            self._posizioni[PosizioniId.POS_PRESA_NS] = (self._card_size[0] + self.margin, self.margin)
            self._posizioni[PosizioniId.POS_PRESA_EW] = (self.margin, self._card_size[1] + self.margin)

            self._posizioni[PosizioniId.POS_MOSTRATE_DEFAULT] = (self._posizioni[PosizioniId.POS_DECK_DEFAULT][0] + self._card_size[0] + self.margin, self._posizioni[PosizioniId.POS_DECK_DEFAULT][0])

            self._posizioni[PosizioniId.POS_FRAME_RESTI] = 19

            self._posizioni[PosizioniId.POS_SCARTO_DEFAULT] = (0, 0)

            self._posizioni[PosizioniId.SIZE_PUNTEGGI] = (self._card_size[0] * 2.0, self._card_size[1] * 1.3)
            self._posizioni[PosizioniId.POS_FRAME_PUNTEGGI] = (5, 5)

            self._posizioni[PosizioniId.SIZE_FRAME_LOG] = (self._card_size[0] * 3, wsize[1] / 6)
            self._posizioni[PosizioniId.POS_FRAME_LOG] = (0, wsize[1] - self._posizioni[PosizioniId.SIZE_FRAME_LOG][1])

            self._posizioni[PosizioniId.POS_POPUP] = (centro[0], centro[1])
            self._posizioni[PosizioniId.SIZE_POPUP] = (wsize[0] / 4, wsize[1] / 4)

            self._posizioni[PosizioniId.POS_OCLOCK] = (wsize[0] - (4 * self.margin), self.margin)
            self._posizioni[PosizioniId.SIZE_OCLOCK] = ((2 * self.margin), self.margin)

            self._posizioni[PosizioniId.RPOS_BUTTON_SAVE] = (-30, -140)
            self._posizioni[PosizioniId.RPOS_BUTTON_REST] = (-30, -110)
            self._posizioni[PosizioniId.RPOS_BUTTON_NEW] = (-30, -50)
            self._posizioni[PosizioniId.RPOS_BUTTON_STOP] = (-30, -80)
            self._posizioni[PosizioniId.RPOS_BUTTON_EXIT] = (-30, -20)
            self._posizioni[PosizioniId.SIZE_BUTTON] = (100, 30)

            self._posizioni[PosizioniId.POS_SCARTO_DEFAULT] = (30, 0)

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_TOKEN_FOL] = ((5 + wsize[0]) / 2, 75)
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_TOKEN_FOL] = ((5 + wsize[0]) / 2, wsize[1] - 75)
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_TOKEN_FOL] = (5 + 75, wsize[1] / 2)
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_TOKEN_FOL] = (5 + wsize[0] - 75, wsize[1] / 2)

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_TOKEN_MAZ] = (10 + wsize[0] / 2, 75)
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_TOKEN_MAZ] = (10 + wsize[0] / 2, wsize[1] - 75)
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_TOKEN_MAZ] = (10 + 75, wsize[1] / 2)
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_TOKEN_MAZ] = (10 + wsize[0] - 75, wsize[1] / 2)

            self._posizioni[PosizioniId.SIZE_TOKEN] = (50, 50)
            radius = (self._posizioni[PosizioniId.SIZE_TOKEN][0] / 2, self._posizioni[PosizioniId.SIZE_TOKEN][1] / 2)
            tok_bord = ((2 * self.margin) + self._card_size[1] + (self._posizioni[PosizioniId.SIZE_TOKEN][0]/2), (2 * self.margin) + self._card_size[1] + (self._posizioni[PosizioniId.SIZE_TOKEN][1]/2))

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_TOKEN_TUR] = (centro[0], tok_bord[1] - radius[1])
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_TOKEN_TUR] = (centro[0], wsize[1] - tok_bord[1] - radius[1])
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_TOKEN_TUR] = (tok_bord[0] - radius[0], centro[1])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_TOKEN_TUR] = (wsize[0] - tok_bord[0] - radius[0], centro[1])

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_TOKEN_MAZ] = (wsize[0] / 2, 75)
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_TOKEN_MAZ] = (wsize[0] / 2, wsize[1] - 75)
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_TOKEN_MAZ] = (75, wsize[1] / 2)
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_TOKEN_MAZ] = (wsize[0] - 75, wsize[1] / 2)

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_RUBATE] = (centro[0], (2 * self.margin))
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_RUBATE] = (centro[0], wsize[1] - self._card_size[1] - (self._card_size[1] - self.margin))
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_RUBATE] = ((2 * self.margin), centro[1])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_RUBATE] = (wsize[0] - self._card_size[1] - (2 * self.margin), centro[1])

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_MANO] = (centro[0], self.margin)
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_MANO] = (centro[0], wsize[1] - self._card_size[1] - self.margin)
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MANO] = (self.margin, centro[1])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MANO] = (wsize[0] - self._card_size[1] - self.margin, centro[1])

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_CALATA] = (centro[0], centro[1] - self._card_size[1])
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_CALATA] = (centro[0], centro[1] + self._card_size[0])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_CALATA] = (centro[0] + self._card_size[0], centro[1])
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_CALATA] = (centro[0] - self._card_size[0], centro[1])

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_SCARTI] = (centro[0] - 2*self._card_size[0] + self.margin, centro[1] - self._card_size[1])
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_SCARTI] = (centro[0] + 2*self._card_size[0] + self.margin, centro[1] + self._card_size[0])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_SCARTI] = (centro[0] + self._card_size[0], centro[1] - self._card_size[0])
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_SCARTI] = (centro[0] - self._card_size[0], centro[1] + self._card_size[0])

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_FOLA] = (centro[0], self.margin + self._card_size[1] + self.margin)
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_FOLA] = (centro[0], wsize[1] - 3*self._card_size[1] + 2*self.margin)
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_FOLA] = (self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MANO][0] + self._card_size[1] + self.margin, centro[1])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_FOLA] = (self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MANO] [0] - self._card_size[1] - self.margin, centro[1])

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_FOLA_STESA] = self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_FOLA]
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_FOLA_STESA] = self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_FOLA]
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_FOLA_STESA] = self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_FOLA]
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_FOLA_STESA] = self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_FOLA]

            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_MAZZO] = (wsize[0] - (2 * self._card_size[0]), wsize[1] - self._card_size[1] - self.margin)
            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_MAZZO] = (2 * self._card_size[0], self._card_size[1])
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MAZZO] = (self._card_size[0], wsize[1] - (2 * self._card_size[1]))
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MAZZO] =(wsize[0] - (2 * self._card_size[1] - self.margin), self._card_size[0] + self.margin)

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_TAGLIO] = (self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_MAZZO][0] + self._card_size[0] + self.margin, self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_MAZZO][1])
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_TAGLIO] = (self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_MAZZO][0] - self._card_size[0] - self.margin, self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_MAZZO][1])
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_TAGLIO] = (self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MAZZO][0], self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MAZZO][1] - self._card_size[0] - self.margin)
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_TAGLIO] = (self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MAZZO][0], self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MAZZO][1] + self._card_size[0] + self.margin)

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_MOSTRATE] = self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_MAZZO]
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_MOSTRATE] = self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_MAZZO]
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MOSTRATE] = self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_MAZZO]
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MOSTRATE] = self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_MAZZO]

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_NOME_LABEL] = (wsize[0] / 2, self.margin / 3)
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_NOME_LABEL] = (wsize[0] / 2, wsize[1] - (self.margin / 2))
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_NOME_LABEL] = (24, wsize[1] / 2)
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_NOME_LABEL] = (wsize[0] - 75, wsize[1] / 2)
            self._dimensioni[SizeId.SIZE_LABEL] = (120, 12)

            self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_PRESA] = (self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_SCARTI][0] + self._card_size[0] + self.margin, self._elementi[PosId.POS_NORD][ElementoId.ELEMENTO_SCARTI][1])
            self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_PRESA] = (self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_SCARTI][0] - self._card_size[0] - self.margin, self._elementi[PosId.POS_SUD][ElementoId.ELEMENTO_SCARTI][1])
            self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_PRESA] = (self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_SCARTI][0], self._elementi[PosId.POS_EST][ElementoId.ELEMENTO_SCARTI][1] - self._card_size[0] - self.margin)
            self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_PRESA] = (self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_SCARTI][0], self._elementi[PosId.POS_OVEST][ElementoId.ELEMENTO_SCARTI][1] + self._card_size[0] + self.margin)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_size_elemento(self, elem):
        try:
            return self._dimensioni[elem]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_elemento(self, elem, ppos):
        try:
            if ppos == "Nord":
                pos_id = PosId.POS_NORD
            elif ppos == "Sud":
                pos_id = PosId.POS_SUD
            elif ppos == "Est":
                pos_id = PosId.POS_EST
            elif ppos == "Ovest":
                pos_id = PosId.POS_OVEST
            else:
                pos_id = PosId.POS_NORD
            return self._elementi[pos_id][elem]
        except Exception as e:
            ExceptionMan.manage_exception(str(pos_id) + ", " + str(elem), e, True)

    def get_posizione(self, id):
        try:
            assert self._posizioni[id] is not None
            return self._posizioni[id]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_id_deck(self, pos=None):
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

    def get_pos_id_mostrate(self, pos=None):
        try:
            if pos is None:
                return PosizioniId.POS_MOSTRATE_DEFAULT
            elif pos == "Nord":
                return PosizioniId.POS_MOSTRATE_N
            elif pos == "Sud":
                return PosizioniId.POS_MOSTRATE_S
            elif pos == "Est":
                return PosizioniId.POS_MOSTRATE_E
            elif pos == "Ovest":
                return PosizioniId.POS_MOSTRATE_O
            else:
                return PosizioniId.POS_MOSTRATE_DEFAULT
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_deck(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            elem = self.get_elemento_deck(deck)
            (x, y) = self.get_pos_elemento(elem, ppos)
            return (x, y)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_area_fola(self, pos=None):
        try:
            if pos is None:
                (x, y) = self.get_posizione(PosizioniId.POS_FOLA_DEFAULT)
            elif pos == "Nord":
                    (x, y) = self.get_pos_elemento(ElementoId.ELEMENTO_FOLA, PosId.POS_NORD)
            elif pos == "Sud":
                    (x, y) = self.get_pos_elemento(ElementoId.ELEMENTO_FOLA, PosId.POS_SUD)
            elif pos == "Est":
                    (x, y) = self.get_pos_elemento(ElementoId.ELEMENTO_FOLA, PosId.POS_EST)
                    margin = 20
            elif pos == "Ovest":
                    (x, y) = self.get_pos_elemento(ElementoId.ELEMENTO_FOLA, PosId.POS_OVEST)
            else:
                (x, y) = self.get_posizione(PosizioniId.POS_FOLA_DEFAULT)
            return (x, y)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_elemento_deck(self, deck):
        try:
            if deck == DeckId.DECK_MAZZO:
                elem = ElementoId.ELEMENTO_MAZZO
            elif deck == DeckId.DECK_MANO:
                elem = ElementoId.ELEMENTO_MANO
            elif deck == DeckId.DECK_FOLA:
                elem = ElementoId.ELEMENTO_FOLA
            elif deck == DeckId.DECK_RUBATE:
                elem = ElementoId.ELEMENTO_RUBATE
            elif deck == DeckId.DECK_TAGLIO:
                elem = ElementoId.ELEMENTO_TAGLIO
            elif deck == DeckId.DECK_TAVOLA:
                elem = ElementoId.ELEMENTO_TAVOLA
            elif deck == DeckId.DECK_SCARTO:
                elem = ElementoId.ELEMENTO_SCARTI
            elif deck == DeckId.DECK_POZZO:
                elem = ElementoId.ELEMENTO_SCARTI
            elif deck == DeckId.DECK_PRESE:
                elem = ElementoId.ELEMENTO_PRESA
            else:
                elem = None
            return elem
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_pos_stesa(self, deck, ppos, i, ntot, sfals=None):
        try:
            if sfals is None:
                if ppos == POSTAZIONE_NORD or ppos == POSTAZIONE_SUD:
                    sfals = self._card_size[0] / 2
                else:
                    # ppos == "Est" or ppos == "Ovest":
                    sfals = self._card_size[0] / 4

            idelem = self.get_elemento_deck(deck)
            (x, y) = self.get_pos_elemento(idelem, ppos)
            ofs = sfals * (i-1)

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

    def get_card_size(self):
        try:
            return self._card_size
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_area_mano(self, ppos):
        try:
            return self.get_pos_elemento(ElementoId.ELEMENTO_MANO, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_area_tavola(self, ppos):
        try:
            return self.get_pos_elemento(ElementoId.ELEMENTO_CALATA, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
