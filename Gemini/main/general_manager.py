'''
Created on 4 gen 2022

@author: david
'''
import random

from decks import mazzo_97
from decks.carta_id import get_seme, CartaId
from game.germini.punteggi import carte_conto
from oggetti.posizioni import DeckId
from oggetti.stringhe import _
from main.globals import *
from main.exception_man import ExceptionMan

class GeneralManager(object):
    '''
    classdocs
    '''
    _globals = None
    _giocatori = None

    _mazzo = None
    _carte_mazzo = []
    _carte_tutte = []
    _carte_pozzo = []
    _col_carte_tavola = {}
    _col_carte_scarti = {}
    _col_carte_mano = {}
    _col_carte_prese = {}
    _col_carte_rubate = {}
    _col_carte_taglio = []
    _col_carte_fola = []

    _delegate_restore_mazzo = None
    _delegate_update_z = None
    _delegate_hovrable = None
    _delegate_set_fronte = None
    _delegate_is_coperta = None
    _delegate_show_carta = None
    _delegate_hide_carta = None
    _delegate_rotate_pos_carta = None
    _mazzo_scoperto = None
    _mazziere = None
    _player = None

    '''
    CONSTRUCTOR
    '''

    def __init__(self):
        try:
            '''
            Constructor
            '''
            self._globals = Globals()
            self._mazzo = mazzo_97.Mazzo97()
            self._col_carte_taglio = []
            self._col_carte_fola = []
            self._mazzo_scoperto = False
            self._mazziere = None
            self._giocatori = []
            self._player = None
            self._carte_tutte = self._mazzo.get_carte()
            self.restore_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            self._player = None
            self._mazziere = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_giocatore(self, giocatore):
        try:
            self._giocatori.append(giocatore)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_player(self):
        try:
            assert self._player is not None
            return self._player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_mazziere(self):
        try:
            if self._mazziere is None:
                if self._globals.get_debug():
                    self._mazziere = self.get_player_at_pos("Sud")
            return self._mazziere
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_mazziere(self, player):
        try:
            print("Mazziere " + str(player))
            self._mazziere = player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_player(self, player):
        try:
            self._player = player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_opposit_pos(self, pos):
        try:
            if pos == POSTAZIONE_NORD:
                return POSTAZIONE_SUD
            elif pos == POSTAZIONE_SUD:
                return POSTAZIONE_NORD
            elif pos == POSTAZIONE_EST:
                return POSTAZIONE_OVEST
            elif pos == POSTAZIONE_OVEST:
                return POSTAZIONE_EST
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_player_at_pos(self, pos):
        try:
            assert pos is not None
            for g in self._giocatori:
                if g.get_position() == pos:
                    return g
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def get_giocatori(self):
        try:
            return self._giocatori
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_postazioni(self, post):
        try:
            self._col_carte_tavola.clear()
            self._col_carte_scarti.clear()
            self._col_carte_mano.clear()
            self._col_carte_prese.clear()
            self._col_carte_rubate.clear()
            for ppos in post:
                self._col_carte_tavola[ppos] = []
                self._col_carte_scarti[ppos] = []
                self._col_carte_mano[ppos] = []
                self._col_carte_prese[ppos] = []
                self._col_carte_rubate[ppos] = []
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_giocatori(self, giocatori):
        try:
            assert self._col_carte_tavola is not None
            assert giocatori is not None
            self._giocatori.clear()

            for g in giocatori:
                self.add_giocatore(g)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_mano(self, player=None):
        try:
            if player is None:
                player = self._player
            if player.get_position() not in self._col_carte_mano:
                return None
            return self._col_carte_mano[player.get_position()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_rubate(self, player):
        try:
            return self._col_carte_rubate[player.get_position()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_fola(self):
        try:
            return self._col_carte_fola
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_prese(self, player):
        try:
            return self._col_carte_prese[player.get_position()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_fola(self):
        try:
            return len(self._col_carte_fola)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_gioco(self, g):
        try:
            assert g is not None
            self.gioco = g
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_player_deck(self, ppos, deck=DeckId.DECK_MAZZO):
        try:
            if deck == DeckId.DECK_TAGLIO:
                return self._col_carte_taglio[ppos]
            elif deck == DeckId.DECK_FOLA:
                return self._col_carte_fola[ppos]
            elif deck == DeckId.DECK_MANO:
                return self._col_carte_mano[ppos]
            else:
                raise Exception("Wrong player deck")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            if deck == DeckId.DECK_MAZZO:
                return self._carte_mazzo
            elif deck == DeckId.DECK_TAGLIO:
                return self._col_carte_taglio
            elif deck == DeckId.DECK_FOLA:
                return self._col_carte_fola
            elif deck == DeckId.DECK_POZZO:
                return self._carte_pozzo
            elif deck == DeckId.DECK_MANO:
                if ppos is not None:
                    if ppos in self._col_carte_mano:
                        return self._col_carte_mano[ppos]
            elif deck == DeckId.DECK_TAVOLA:
                if ppos is not None:
                    if ppos in self._col_carte_tavola:
                        return self._col_carte_tavola[ppos]
            if deck == DeckId.DECK_RUBATE:
                if ppos is not None:
                    if ppos in self._col_carte_rubate:
                        return self._col_carte_rubate[ppos]
            elif deck == DeckId.DECK_SCARTO:
                if ppos is not None:
                    if ppos in self._col_carte_scarti:
                        return self._col_carte_scarti[ppos]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_fola(self):
        try:
            return self._col_carte_fola
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fai_la_fola(self):
        try:
            self._col_carte_fola.clear()
            self._col_carte_fola = self._carte_mazzo.copy()
            self._carte_mazzo.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_taglio(self):
        try:
            return self._col_carte_taglio
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cat_mazzo(self, cid):
        try:
            for c in self._col_carte_taglio:
                self._carte_mazzo.append(c)
            self._col_carte_taglio.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def split_mazzo_n(self, n):
        try:
            i = 0
            c = None
            while i < len(self._carte_mazzo) and i < n:
                c = self._carte_mazzo.pop(0)
                self._col_carte_taglio.append(c)
                self._delegate_set_fronte(c, FRONTE_SCOPERTA, self._globals.get_instant())
                self._delegate_update_z(c, i)
                i = i + 1
            if c is not None:
                print("Taglio " + str(c))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def split_mazzo_cid(self, cid):
        try:
            found = False
            while len(self._carte_mazzo) != 0:
                if str(self._carte_mazzo[0].get_id()) == str(cid):
                    print("Break taglio " + str(cid))
                    break
                c = self._carte_mazzo.pop(0)
                self._col_carte_taglio.append(c)
                print("Pop " + str(c))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sort_mazzo(self, player):
        try:
            if len(self._col_carte_mano[player.get_position()]) > 1:
                self._col_carte_mano[player.get_position()].sort(reverse=True)
                self.update_z(self._col_carte_mano[player.get_position()])
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mazzo_is_coperto(self):
        try:
            return self._mazzo_scoperto is False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_z(self, ca):
        try:
            i = 0
            for c in ca:
                if not self._delegate_is_coperta(c):
                    self._delegate_update_z(c, i)
                i = i + 1

            for c in ca:
                if self._delegate_is_coperta(c):
                    self._delegate_update_z(c, i)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def merge_deck(self, deck_src, ppos_src, deck_dst, ppos_dst):
        try:
            src = self.get_deck(deck_src, ppos_src)
            dst = self.get_deck(deck_dst, ppos_dst)
            while len(src) > 0:
                c = self.pop_carta(-1, deck_src)
                dst.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raddrizza_mazzo(self):
        try:
            i = 0
            if self._mazzo_scoperto is True:
                self._mazzo_scoperto = False
                self._carte_mazzo.reverse()
                for c in self._carte_mazzo:
                    self._delegate_set_fronte(c, FRONTE_COPERTA, self._globals.get_instant())
                    self._delegate_update_z(c, i)
                    if i == 0:
                        self._delegate_hovrable(c, True)
                    else:
                        self._delegate_hovrable(c, False)
                    i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None, fronte=FRONTE_SCOPERTA):
        try:
            mazzo = self.get_deck(deck, ppos)
            i = 0
            if not self._mazzo_scoperto and fronte==FRONTE_SCOPERTA:
                mazzo.reverse()
                self._mazzo_scoperto = True
            if self._mazzo_scoperto and fronte==FRONTE_COPERTA:
                mazzo.reverse()
                self._mazzo_scoperto = False

            for c in mazzo:
                self._delegate_set_fronte(c, fronte, self._globals.get_instant())
                self._delegate_update_z(c, i)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def taglia_mazzo(self, cid):
        try:
            echo_message(_("Taglia il mazzo..."))
            self.split_mazzo_cid(cid)
            i = 0
            for c in self._col_carte_taglio:
                self._delegate_set_fronte(c, FRONTE_SCOPERTA, self._globals.get_instant())
                self._delegate_update_z(c, i)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola_mazzo(self):
        try:
            i = 0
            assert self._carte_mazzo is not None
            random.shuffle(self._carte_mazzo)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cls_deck(self, d):
        try:
            for col in d:
                d[col].clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_mazzo(self):
        try:
            assert self._carte_tutte is not None
            if self._delegate_restore_mazzo is not None:
                self._delegate_restore_mazzo()

            self._carte_mazzo.clear()
            self._carte_pozzo.clear()
            self._col_carte_taglio.clear()
            self._col_carte_fola.clear()

            self.cls_deck(self._col_carte_scarti)
            self.cls_deck(self._col_carte_mano)
            self.cls_deck(self._col_carte_prese)
            self.cls_deck(self._col_carte_rubate)

            self._carte_mazzo = self._carte_tutte.copy()

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_manche(self):
        try:
            assert self._carte_mazzo is not None
            echo_message(_("Raccoglie tutte le carte..."))
            self.restore_tavola()
            self.restore_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def remove_matto(self, c):
        try:
            for key, posto in self._col_carte_tavola.items():
                for car in posto:
                    if car.get_cid() == CartaId.MATTO_0 and c.get_id() == CartaId.MATTO_0:
                        self._col_carte_tavola[key].remove(c)
                        self._col_carte_prese[posto].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def remove_tavola(self, player, c):
        try:
            for key, posto in self._col_carte_tavola.items():
                for car in posto:
                    if car == c:
                        self._col_carte_tavola[key].remove(c)
                        self._col_carte_prese[player.get_position()].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_tavola(self):
        try:
            assert self._col_carte_tavola is not None
            echo_message("Restore tavola")
            for key, posto in self._col_carte_tavola.items():
                posto.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_giocatori(self):
        try:
            if self._giocatori is not None:
                for g in self._giocatori:
                    g.reset()
                    self._giocatori.remove(g)
                self._giocatori.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_fola(self):
        try:
            if self._col_carte_fola is not None:
                self._col_carte_fola.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_all(self):
        try:
            self.restore_manche()
            self.restore_tavola()
            self.restore_giocatori()
            self.restore_fola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def carta_giocata(self, posizione):
        try:
            assert posizione is not None
            assert self._col_carte_tavola is not None
            cc = self._col_carte_tavola[posizione]
            if cc is not None:
                if len(cc) > 0:
                    return cc[0]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def clear_carte_in_tavola(self, posizione):
        try:
            self._col_carte_tavola[posizione].clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_in_tavola_pos(self, posizione):
        try:
            if posizione is not None and self._col_carte_tavola is not None:
                if posizione in self._col_carte_tavola:
                    return self._col_carte_tavola[posizione]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def get_carte_tavola(self):
        try:
            list = []
            for key, vect in self._col_carte_tavola.items():
                if len(vect) > 0:
                    for c in vect:
                        list.append(c)
            return list
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def rimuove_carta_in_tavola(self, c):
        try:
            for key, vect in self._col_carte_tavola.items():
                if vect.count(c) > 0:
                    vect.remove(c)
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def carte_mostrate(self, posizione):
        try:
            return self._col_carte_tavola[posizione].get_carte_mostrate()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def termina_gioco(self):
        try:
            self.restore_manche()
            self.restore_giocatori()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def read_carta(self, i, deck, player):
        try:
            if player is None:
                ppos = None
            else:
                ppos = player.get_position()

            mazzo = self.get_deck(deck, ppos)
            if mazzo is not None:
                if len(mazzo) > i:
                    return mazzo[i]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop(self, i, mazzo):
        try:
            assert mazzo is not None
            assert len(mazzo) != 0
            return mazzo.pop(i)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop_carta(self, i, deck, ppos=None):
        try:
            return self.pop(i, self.get_deck(deck, ppos))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_ultima_mano(self):
        return len(self._col_carte_mano[self._player.get_position()]) == 1

    def read_ultima_carta(self):
        try:
            if len(self._carte_mazzo) != 0:
                return self._carte_mazzo[-1]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_rubate_giocatore(self, player, c):
        try:
            return self._col_carte_rubate[player.get_position()].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_mano_giocatore(self, player, c):
        try:
            print(str(player) + " riceve " + str(c))
            self._col_carte_mano[player.get_position()].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def deck_contains(self, cid, deck=DeckId.DECK_MAZZO, player=None):
        try:
            if player is not None:
                ppos = player.get_position()
            else:
                ppos = None
            d = self.get_deck(deck, ppos)
            if d is not None:
                for c in d:
                    if str(cid) == str(c.get_id()):
                        return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_carta(self, player, cid):
        try:
            for c in self._col_carte_mano[player.get_position()]:
                if str(cid) == str(c.get_id()):
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_seme(self, player, seed):
        try:
            for c in self._col_carte_mano[player.get_position()]:
                if get_seme(c.get_id()) == seed:
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return False

    def preleva_dal_mazzo(self, n):
        ca = []
        try:
            for i in range(n):
                c = self._carte_mazzo.pop()
                if c is None:
                    break
                ca.append(c)
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def pesca_dal_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            d = self.get_deck(deck, ppos)
            if d is not None:
                return d.pop()
            else:
                raise Exception(_("No card in the deck"))
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inserisci_nel_mazzo(self, c, deck, ppos):
        try:
            assert ppos is not None
            d = self.get_deck(deck, ppos)
            if d is not None:
                d.insert(0, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_in_tavola(self, c, ppos):
        try:
            if c in self._col_carte_mano[ppos]:
                self._col_carte_mano[ppos].remove(c)
                self._col_carte_tavola[ppos].insert(0, c)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def piglia_da_fola(self, player):
        ca = []
        try:
            for c in self._col_carte_fola:
                if c.get_id() in carte_conto:
                    print(str(player) + " piglia " + str(c))
                    ca.append(c)
                    self._col_carte_fola.remove(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def append_fola(self, c):
        try:
            self._col_carte_fola[self._mazziere()].append(c)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scarta(self, c, player=None):
        try:
            if player is None:
                player = self._player
            assert c in self._col_carte_mano[player.get_position()]
            self._col_carte_mano[player.get_position()].remove(c)
            self._col_carte_scarti[player.get_position()].append(c)
        except Exception as e:
            print(str(c))
            ExceptionMan.manage_exception("", e, True)

    def cid_to_carta(self, cid):
        try:
            for c in self._carte_tutte:
                if str(c.get_id()) == str(cid):
                    return c
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_carta(self, player, c):
        try:
            echo_message(player._name + " (" + player.get_position() + ") mostra " + str(c))
            self._col_carte_tavola[player.get_position()].insert(0, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def pesca_dagli_scarti(self, player):
        try:
            if self._col_carte_scarti:
                self._col_carte_scarti[player].pesca()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_restore_mazzo(self, f):
        try:
            self._delegate_restore_mazzo = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_hoverable(self, f):
        self._delegate_hovrable = f

    def set_delegate_update_z(self, f):
        self._delegate_update_z = f

    def set_delegate_show_carta(self, f):
        try:
            self._delegate_show_carta = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_hide_carta(self, f):
        try:
            self._delegate_hide_carta = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_set_fronte(self, f):
        try:
            self._delegate_set_fronte = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_is_coperta(self, f):
        try:
            self._delegate_is_coperta = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_rotate_pos_carta(self, f):
        try:
            self._delegate_rotate_pos_carta = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
