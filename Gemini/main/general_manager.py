'''
Created on 4 gen 2022

@author: david
'''
import random

import numpy

from decks import mazzo_97
from decks.carta_id import get_seme
from game.germini.punteggi import punti_ger
from oggetti.posizioni import DECK_MAZZO, DECK_TAGLIO, DECK_FOLA
from oggetti.stringhe import _
from main.globals import *
from main.exception_man import ExceptionMan

class GeneralManager(object):
    '''
    classdocs
    '''
    _globals = None
    _giocatori = []
    gioco_carta = None

    _mazzo = None
    _carte_mazzo = None

    _col_carte_tavola = {}
    _col_carte_scarti = {}
    _col_carte_mano = {}
    _col_carte_prese = {}
    _col_carte_rubate = {}
    _col_carte_taglio = []
    _col_carte_fola = []

    _delegate_restore_mazzo = None
    _delegate_update_z = None
    _delegate_set_fronte = None
    _delegate_is_coperta = None
    _delegate_show_carta = None
    _delegate_hide_carta = None
    _delegate_rotate_pos_carta = None
    _mazziere = None
    _mazzo_scoperto = None

    '''
    CONSTRUCTOR
    '''

    def __init__(self, man):
        try:
            '''
            Constructor
            '''
            self._globals = Globals()
            self._mazzo = mazzo_97.Mazzo97()
            self._carte_mazzo = self._mazzo.get_carte()
            self._col_carte_taglio = []
            self._col_carte_fola = []
            self.gioco_carta = man
            self._mazzo_scoperto = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_giocatore(self, giocatore):
        try:
            self._giocatori.append(giocatore)
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

    def get_compagno_mazziere(self):
        try:
            if self._mazziere is not None:
                if self._globals.get_debug():
                    self._mazziere = self.get_player_at_pos("Sud")

                pos = self.get_opposit_pos(self._mazziere.get_position())
                return self.get_player_at_pos(pos)
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_mazziere(self, player):
        try:
            self._mazziere = player
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
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def get_giocatori(self):
        try:
            return self._giocatori
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_giocatori(self, giocatori):
        try:
            assert self._col_carte_tavola is not None
            assert giocatori is not None
            self._giocatori.clear()
            self._col_carte_tavola.clear()

            for g in giocatori:
                self.add_giocatore(g)
                self._col_carte_tavola[g.get_position()] = []
                self._col_carte_scarti[g.get_position()] = []
                self._col_carte_mano[g.get_position()] = []
                self._col_carte_prese[g.get_position()] = []
                self._col_carte_rubate[g.get_position()] = []
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_mano(self, player):
        try:
            return self._col_carte_mano[player.get_position()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_rubate(self, player):
        try:
            return self._col_carte_rubate[player.get_position()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_fola(self, player):
        try:
            return self._col_carte_fola[player.get_position()]
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_mano(self, player):
        try:
            return len(self._col_carte_mano[player.get_position()])
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_fola(self, player):
        try:
            return len(self._col_carte_fola[player.get_position()])
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_gioco(self, g):
        try:
            assert g is not None
            self.gioco = g
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck(self, deck=DECK_MAZZO):
        try:
            if deck == DECK_MAZZO:
                return self._carte_mazzo
            elif deck == DECK_TAGLIO:
                return self._col_carte_taglio
            elif deck == DECK_FOLA:
                return self._col_carte_fola
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
                self._delegate_set_fronte(c, FRONTE_SCOPERTA)
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
                self._col_carte_taglio.append(self._carte_mazzo.pop(0))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ricomponi_taglio(self):
        try:
            while len(self._col_carte_taglio) != 0:
                c = self._col_carte_taglio.pop(-1)
                self._delegate_set_fronte(c, FRONTE_COPERTA)
                self._carte_mazzo.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sort_mazzo(self, player):
        try:
            if self.get_num_carte_mano(player) > 1:
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

    def raddrizza_mazzo(self):
        try:
            if self._mazzo_scoperto is True:
                self._mazzo_scoperto = False
                self._carte_mazzo.reverse()
                for c in self._carte_mazzo:
                    self._delegate_set_fronte(c, FRONTE_COPERTA)
                self.update_z(self._carte_mazzo)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self):
        try:
            i = 0
            if self._mazzo_scoperto is False:
                self._mazzo_scoperto = True
                self._carte_mazzo.reverse()
                for c in self._carte_mazzo:
                    self._delegate_set_fronte(c, FRONTE_SCOPERTA)
                    i = i + 1
                self.update_z(self._carte_mazzo)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def taglia_mazzo(self, cid):
        try:
            echo_message(_("Taglia il mazzo..."))
            self.split_mazzo_cid(cid)
            i = 0
            for c in self._col_carte_taglio:
                self._delegate_set_fronte(c, FRONTE_SCOPERTA)
                self._delegate_update_z(c, i)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ricomponi_mazzo(self, cid):
        try:
            echo_message(_("Ricompone il mazzo..."))
            self.split_mazzo_cid(cid)
            i = 0
            for c in self._col_carte_taglio:
                self._delegate_set_fronte(c, FRONTE_SCOPERTA)
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

    def restore_mazzo(self):
        try:
            assert self._carte_mazzo is not None
            self._delegate_restore_mazzo()
            self._mazzo.ripristina()
            self._carte_mazzo = self._mazzo.get_carte()
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

    def remove_tavola(self, c):
        try:
            for key, posto in self._col_carte_tavola.items():
                for car in posto:
                    if car == c:
                        self._col_carte_tavola[key].remove(c)
                        self._col_carte_prese[key].append(c)
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

    def pulisci_giocatori(self):
        try:
            if self._giocatori is not None:
                for g in self._giocatori:
                    g.reset()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_giocatori(self):
        try:
            if self._giocatori is not None:
                self.pulisci_giocatori()
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

    def update_game(self):
        try:
            if self.gioco_carta is not None:
                self.gioco_carta.update_game()
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

    def get_carte_in_tavola(self, posizione):
        try:
            if posizione is not None and self._col_carte_tavola is not None:
                if posizione in self._col_carte_tavola:
                    return self._col_carte_tavola[posizione]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def prendi_tavola(self):
        try:
            list = []
            for key, vect in self._col_carte_tavola.items():
                if len(vect) > 0:
                    for c in vect:
                        list.append(c)
                        vect.remove(c)
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
            self.gioco_carta = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def read_carta(self, i, deck):
        try:
            if deck == DECK_MAZZO:
                if len(self._carte_mazzo) != 0:
                    return self._carte_mazzo[i]
            elif deck == DECK_TAGLIO:
                if len(self._col_carte_taglio) != 0:
                    return self._col_carte_taglio[i]
            elif deck == DECK_FOLA:
                if len(self._col_carte_fola) != 0:
                    return self._col_carte_fola[i]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop_carta(self, i, deck):
        try:
            if deck == DECK_MAZZO:
                if len(self._carte_mazzo) != 0:
                    return self._carte_mazzo.pop(i)
            elif deck == DECK_TAGLIO:
                if len(self._col_carte_taglio) != 0:
                    return self._col_carte_taglio.pop(i)
            elif deck == DECK_FOLA:
                if len(self._col_carte_fola) != 0:
                    return self._col_carte_fola.pop(i)
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def read_carta_mazzo(self, i, m=DECK_MAZZO):
        try:
            return self.read_carta(i, m)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def read_ultima_carta(self):
        try:
            if len(self._carte_mazzo) != 0:
                return self._carte_mazzo[-1]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_rubate_giocatore(self, player, c):
        try:
            print(str(player) + " ruba " + str(c))
            self._col_carte_rubate[player.get_position()].append(c)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_mano_giocatore(self, player, c):
        try:
            print(str(player) + " riceve " + str(c))
            player.assegna_carta(c)
            self._col_carte_mano[player.get_position()].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_carta(self, player, cid):
        try:
            for c in self._col_carte_mano[player.get_position()]:
                if cid == c.get_id():
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_seme(self, seed):
        try:
            for c in self.cards_mano:
                if get_seme(c.get_id()) == seed:
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return False

    def piglia_da_fola(self, player):
        ca = []
        try:
            for c in self._col_carte_fola:
                if c.get_id() in punti_ger:
                    print(str(player) + " piglia " + str(c))
                    ca.append(c)
                    self._col_carte_fola.remove(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def preleva_dal_mazzo(self, n):
        ca = []
        try:
            for i in range(n):
                c = self._carte_mazzo.pop()
                if c is None:
                    break
                ca.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def pesca_dal_mazzo(self, player):
        c = None
        try:
            ca = self.general_man.preleva_dal_mazzo(1)
            if c != None:
                if player is not None:
                    echo_message(player._name + " pesca " + str(c))
                    player.assegna_carta(c)
            else:
                raise Exception(_("No card in the deck"))

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def sposta_in_tavola(self, player, c):
        try:
            self._col_carte_mano[player.get_position()].remove(c)
            self._col_carte_tavola[player.get_position()].insert(0, c)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_in_fola(self, c):
        try:
            self._col_carte_fola[self._mazziere()].append(c)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scarta(player, n):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carta_obj(self, player, cid):
        c = None
        try:
            x = self.get_carte_mano(player)
            for c in x:
                if c.get_id() == cid:
                    break
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

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

    def show_mazzo(self):
        try:
            for c in self._carte_mazzo:
                self._delegate_set_fronte(c, FRONTE_COPERTA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_restore_mazzo(self, f):
        try:
            self._delegate_restore_mazzo = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_update_z(self, f):
        try:
            self._delegate_update_z = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

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
