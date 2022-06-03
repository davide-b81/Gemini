'''
Created on 4 gen 2022

@author: david
'''
import json
from json import JSONDecoder, JSONEncoder

from decks import mazzo_97
from decks.carta import Carta
from decks.carta_id import get_seme
from decks.mazzo import Mazzo
from game.germini.punteggi import carte_conto
from game.germini.strategia import posizioni
from game.player import Player
from oggetti.stringhe import _
from main.globals import *
from main.exception_man import ExceptionMan

class GeneralManager(object):
    '''
    classdocs
    '''
    _giocatori = None

    _mazzo = None
    _pozzo = None
    _fola = None
    _taglio = None
    _set_ca_tavola = {}
    _set_ca_scarti = {}
    _set_ca_mano = {}
    _set_ca_prese = {}
    _set_ca_rubate = {}

    _curdeck = None

    _mazziere = None
    _player = None

    _delegate_restore_mazzo = None
    _delegate_get_sprite = None
    _globals = Globals()

    '''
    CONSTRUCTOR
    '''

    def __init__(self):
        try:
            '''
            Constructor
            '''
            self._mazziere = None
            self._giocatori = []
            self._player = None
            self._mazzo = Mazzo("Mazzo")
            self._taglio = Mazzo("Taglio")
            self._fola = Mazzo("Fola")
            self._pozzo = Mazzo("Pozzo")
            self._set_ca_tavola = {}
            self._set_ca_scarti = {}
            self._set_ca_mano = {}
            self._set_ca_prese = {}
            self._set_ca_rubate = {}
            self.restore_decks()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            self._player = None
            self._mazziere = None
            self._mazzo.append_carte(self._globals.get_carte())
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
            if Globals().get_force_mazziere():
                self._mazziere = self.get_player_at_pos(POSTAZIONE_SUD)
            return self._mazziere
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_sprite(self, c):
        try:
            self._delegate_get_sprite()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_mazziere(self, player):
        try:
            print("Mazziere " + str(player))
            self._mazziere = player
            self._player = player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_player(self, player):
        try:
            self._player = player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_cards_sprites(self):
        try:
            if self._delegate_get_sprite is not None:
                for c in self._globals.get_carte():
                    c.set_sprite(self._delegate_get_sprite(c.get_id()))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_get_sprite(self, f):
        try:
            self._delegate_get_sprite = f
            self.set_cards_sprites()
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

            for ppos in post:
                self._set_ca_tavola[ppos] = Mazzo("Tavola-" + str(ppos))
                self._set_ca_scarti[ppos] = Mazzo("Scarti-" + str(ppos))
                self._set_ca_mano[ppos] = Mazzo("Mano-" + str(ppos))
                self._set_ca_prese[ppos] = Mazzo("Prese-" + str(ppos))
                self._set_ca_rubate[ppos] = Mazzo("Rubate-" + str(ppos))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_giocatori(self, giocatori):
        try:
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
            if player.get_position() not in self._set_ca_mano:
                return None
            return self._set_ca_mano[player.get_position()].get_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_rubate(self, player):
        try:
            return self._set_ca_rubate[player.get_position()].get_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_fola(self):
        try:
            return self._fola.get_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_prese(self, player):
        try:
            return self._set_ca_prese[player.get_position()].get_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_merged(self, deck=DeckId.DECK_MAZZO):
        try:
            if deck == DeckId.DECK_MAZZO:
                return self._mazzo.get_carte()
            elif deck == DeckId.DECK_TAGLIO:
                return self._taglio.get_carte()
            elif deck == DeckId.DECK_FOLA:
                return self._fola.get_carte()
            elif deck == DeckId.DECK_POZZO:
                return self._pozzo.get_carte()
            elif deck == DeckId.DECK_MANO:
                return self.get_merged_list_ca(self._set_ca_mano)
            elif deck == DeckId.DECK_TAVOLA:
                return self.get_merged_list_ca(self._set_ca_tavola)
            elif deck == DeckId.DECK_RUBATE:
                return self.get_merged_list_ca(self._set_ca_rubate)
            elif DeckId.DECK_SCARTO:
                return self.get_merged_list_ca(self._set_ca_scarti)
            elif DeckId.DECK_PRESE:
                return self.get_merged_list_ca(self._set_ca_prese)
            else:
                raise Exception("Unknown deck " + str(deck))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_merged_list_ca(self, deck_list):
        try:
            list = []
            for key, vect in deck_list.items():
                if len(vect) > 0:
                    for c in vect:
                        list.append(c)
            return list
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_vect(self, deck=DeckId.DECK_MANO):
        try:
            if deck == DeckId.DECK_TAVOLA:
                return self._set_ca_tavola
            if deck == DeckId.DECK_RUBATE:
                return self._set_ca_rubate
            elif deck == DeckId.DECK_SCARTO:
                return self._set_ca_scarti
            elif deck == DeckId.DECK_PRESE:
                return self._set_ca_prese
            else:
                return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            if deck == DeckId.DECK_MAZZO:
                return self._mazzo
            elif deck == DeckId.DECK_TAGLIO:
                return self._taglio
            elif deck == DeckId.DECK_FOLA:
                return self._fola
            elif deck == DeckId.DECK_POZZO:
                return self._pozzo
            elif deck == DeckId.DECK_MANO:
                if ppos is not None:
                    if ppos in self._set_ca_mano:
                        return self._set_ca_mano[ppos]
            elif deck == DeckId.DECK_TAVOLA:
                if ppos is not None:
                    if ppos in self._set_ca_tavola:
                        return self._set_ca_tavola[ppos]
            if deck == DeckId.DECK_RUBATE:
                if ppos is not None:
                    if ppos in self._set_ca_rubate:
                        return self._set_ca_rubate[ppos]
            elif deck == DeckId.DECK_SCARTO:
                if ppos is not None:
                    if ppos in self._set_ca_scarti:
                        return self._set_ca_scarti[ppos]
            elif deck == DeckId.DECK_PRESE:
                if ppos is not None:
                    if ppos in self._set_ca_prese:
                        return self._set_ca_prese[ppos]
            raise Exception("Unknown deck " + str(deck))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_list_ca(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            if deck == DeckId.DECK_MAZZO or deck == DeckId.DECK_TAGLIO\
                    or deck == DeckId.DECK_FOLA or deck == DeckId.DECK_POZZO:
                return self.get_deck(deck).get_carte()
            elif deck == DeckId.DECK_MANO:
                if ppos is not None:
                    if ppos in self._set_ca_mano:
                        return self._set_ca_mano[ppos].get_carte()
            elif deck == DeckId.DECK_TAVOLA:
                if ppos is not None:
                    if ppos in self._set_ca_tavola:
                        return self._set_ca_tavola[ppos].get_carte()
            if deck == DeckId.DECK_RUBATE:
                if ppos is not None:
                    if ppos in self._set_ca_rubate:
                        return self._set_ca_rubate[ppos].get_carte()
            elif deck == DeckId.DECK_SCARTO:
                if ppos is not None:
                    if ppos in self._set_ca_scarti:
                        return self._set_ca_scarti[ppos].get_carte()
            elif deck == DeckId.DECK_PRESE:
                if ppos is not None:
                    if ppos in self._set_ca_prese:
                        return self._set_ca_prese[ppos].get_carte()
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_fola(self):
        try:
            return self._fola.get_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fai_la_fola(self):
        try:
            self._fola.flush_carte()
            self._fola <<= self._mazzo
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_taglio(self):
        try:
            return self._taglio
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def split_mazzo_n(self, n):
        try:
            i = 0
            c = None
            while i < len(self._mazzo) and i < n:
                c = self._mazzo.pop(0)
                self._taglio.append(c)

                c.set_coperta(FRONTE_SCOPERTA)
                c.set_z(i)
                i = i + 1
            #if c is not None:
            #    print("Taglio " + str(c))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def split_mazzo_cid(self, cid):
        try:
            while len(self._mazzo) != 0:
                if str(self._mazzo[0].get_id()) == str(cid):
                    print("Break taglio " + str(cid))
                    break
                c = self._mazzo.pop(0)
                self._taglio.insert(c)
                #print("Sposta in taglio " + str(c))
            self._mazzo.print_carte()
            self._taglio.print_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sort_mazzo_z(self, deck, ppos=None):
        try:
            ca = self.get_list_ca(deck, ppos)
            ca.sort(key=lambda x: x.get_id().value)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_z(self, ca):
        try:
            i = 0
            for c in ca:
                if not c.get_coperta():
                    c.set_z(i)
                i = i + 1

            for c in ca:
                if c.get_coperta():
                    c.set_z(i)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def merge_deck(self, deck_src, ppos_src, deck_dst, ppos_dst):
        try:
            src = self.get_list_ca(deck_src, ppos_src)
            dst = self.get_list_ca(deck_dst, ppos_dst)
            while len(src) > 0:
                c = self.pop_carta(-1, deck_src)
                dst.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raddrizza_mazzo(self):
        try:
            i = 0
            if self._mazzo.is_scoperto():
                self._mazzo.set_dorso()
                for c in self._mazzo:
                    c.set_coperta(FRONTE_SCOPERTA)
                    c.set_z(i)
                    if i == 0:
                        c.set_hoverable(True)
                    else:
                        c.set_hoverable(False)
                    i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None, fronte=FRONTE_SCOPERTA):
        try:
            mazzo = self.get_list_ca(deck, ppos)
            i = 0
            if self._mazzo.is_coperto() and fronte == FRONTE_SCOPERTA:
                mazzo.set_fronte()
            if self._mazzo.is_scoperto() and fronte == FRONTE_COPERTA:
                mazzo.set_dorso()

            for c in mazzo:
                c.set_coperta(fronte == FRONTE_COPERTA)
                c.set_z(i)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def taglia_mazzo(self, cid):
        try:
            echo_message(_("Taglia il mazzo..."))
            self.split_mazzo_cid(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola_mazzo(self):
        try:
            assert self._mazzo is not None
            self._mazzo.append_carte(self._globals.get_carte())
            self._mazzo.mescola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def svuota_mazzo(self, d):
        try:
            for col in d:
                d[col].flush_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_decks(self):
        try:
            assert self._globals.get_carte() is not None
            if self._delegate_restore_mazzo is not None:
                self._delegate_restore_mazzo()
            self._mazzo.flush_carte()
            self._pozzo.flush_carte()
            self._fola.flush_carte()
            self._taglio.flush_carte()
            self.svuota_mazzo(self._set_ca_mano)
            self.svuota_mazzo(self._set_ca_scarti)
            self.svuota_mazzo(self._set_ca_prese)
            self.svuota_mazzo(self._set_ca_rubate)
            #for p in posizioni:
            #    self._set_ca_mano[p] = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_manche(self):
        try:
            echo_message(_("Raccoglie tutte le carte..."))
            self.restore_tavola()
            self.restore_decks()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def remove_tavola(self, player, c):
        try:
            for key, elems in self._set_ca_tavola.items():
                for cc in elems.get_carte():
                    if cc == c:
                        self._set_ca_tavola[key].remove(c)
                        self._set_ca_prese[player.get_position()].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_tavola(self):
        try:
            assert self._set_ca_tavola is not None
            echo_message("Restore tavola")
            for key, posto in self._set_ca_tavola.items():
                posto.flush_carte()
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

    def restore_all(self):
        try:
            self.restore_manche()
            self.restore_tavola()
            self.restore_giocatori()
            self._fola.flush_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def carta_giocata(self, posizione):
        try:
            assert posizione is not None
            assert self._set_ca_tavola is not None
            cc = self._set_ca_tavola[posizione].get_carte()
            if cc is not None:
                if len(cc) > 0:
                    return cc[0]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def clear_carte_in_tavola(self, posizione):
        try:
            self._set_ca_tavola[posizione].flush_carte()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_in_tavola_pos(self, posizione):
        try:
            if posizione is not None and self._set_ca_tavola is not None:
                if posizione in self._set_ca_tavola:
                    return self._set_ca_tavola[posizione].get_carte()
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return None

    def get_all_tavola(self):
        try:
            ll = []
            for key, mm in self._set_ca_tavola.items():
                for c in mm.get_carte():
                    ll.append(c)
            return ll
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def rimuove_carta_in_tavola(self, c):
        try:
            for key, mm in self._set_ca_tavola.items():
                mm.remove(c)
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

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

            mazzo = self.get_list_ca(deck, ppos)
            if mazzo is not None:
                if len(mazzo) > i:
                    return mazzo[i]
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop(self, i, mazzo):
        try:
            return mazzo.pop(i)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop_carta(self, i, deck, ppos=None):
        try:
            return self.pop(i, self.get_list_ca(deck, ppos))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_ultima_mano(self):
        return len(self._set_ca_mano[self._player.get_position()]) == 1

    def read_ultima_carta(self):
        try:
            return self._mazzo.get_carta(-1)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_rubate_giocatore(self, player, c):
        try:
            return self._set_ca_rubate[player.get_position()].append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def deck_contains(self, cid, deck=DeckId.DECK_MAZZO, player=None):
        try:
            if player is not None:
                ppos = player.get_position()
            else:
                ppos = None
            d = self.get_list_ca(deck, ppos)
            if d is not None:
                for c in d:
                    if str(cid) == str(c.get_id()):
                        return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_carta(self, player, cid):
        try:
            for c in self._set_ca_mano[player.get_position()].get_carte():
                if str(cid) == str(c.get_id()):
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_seme(self, player, seed):
        try:
            for c in self._set_ca_mano[player.get_position()].get_carte():
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
                c = self._mazzo.pop()
                if c is None:
                    break
                ca.append(c)
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pesca_dal_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            d = self.get_list_ca(deck, ppos)
            if d is not None:
                if len(d) > 0:
                    return d.pop()
            else:
                raise Exception(_("No card in the deck"))
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inserisci_nel_mazzo(self, c, deck, ppos):
        try:
            assert ppos is not None
            d = self.get_list_ca(deck, ppos)
            if d is not None:
                d.insert(0, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_in_tavola(self, c, ppos):
        try:
            if c in self._set_ca_mano[ppos]:
                self._set_ca_mano[ppos].remove(c)
                self._set_ca_tavola[ppos].insert(c)
            elif c in self._set_ca_rubate[ppos]:
                self._set_ca_rubate[ppos].remove(c)
                self._set_ca_tavola[ppos].insert(c)
            else:
                raise Exception("Carta non trovata!")
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def piglia_da_fola(self, player):
        ca = []
        try:
            for c in self._fola:
                if c.get_id() in carte_conto:
                    print(str(player) + " piglia " + str(c))
                    ca.append(c)
                    self._fola.remove(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def append_fola(self, c):
        try:
            self._fola[self._mazziere()].append(c)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scarta(self, c, player=None):
        try:
            if player is None:
                player = self._player
            assert c in self._set_ca_mano[player.get_position()].get_carte()
            self._set_ca_mano[player.get_position()].remove(c)
            self._set_ca_scarti[player.get_position()].append(c)
        except Exception as e:
            print(str(c))
            ExceptionMan.manage_exception("", e, True)

    def cid_to_carta(self, cid):
        try:
            for c in self._globals.get_carte():
                if str(c.get_id()) == str(cid):
                    return c
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_deck_visible(self, deck, ppos, enable=True):
        try:
            deck_obj = self.get_deck(deck, ppos)
            deck_obj.set_visible(enable)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_carta(self, player, c):
        try:
            echo_message(player._name + " (" + player.get_position() + ") mostra " + str(c))
            self._set_ca_tavola[player.get_position()].insert(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def set_delegate_restore_mazzo(self, f):
        try:
            self._delegate_restore_mazzo = f
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_coperta(self, c):
        return c.get_coperta()

    def get_scoperte(self, deck, ppos):
        try:
            lissc = []
            ca = self.get_list_ca(deck, ppos)
            for c in ca:
                if not c.get_coperta():
                    lissc.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def count_seme_in_deck(self, palo, deck, ppos):
        """ Utilità per strategia """
        try:
            i = 0
            ca = self.get_list_ca(deck, ppos)
            for c in ca:
                if c.get_seme() == palo:
                    i = i + 1
            return i
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_lista_seme(self, palo, deck, ppos):
        try:
            i = 0
            ca = self.get_list_ca(deck, ppos)
            lista = []
            for c in ca:
                if c.get_seme() == palo:
                    lista.append(c)
            return Carta.sort(lista)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_deserialize_complete(self):
        try:
            print(str(self._mazzo))
            print(str(self._taglio))
            print(str(self._fola))
            print(str(self._pozzo))
            print(str(self._set_ca_tavola))
            print(str(self._set_ca_scarti))
            print(str(self._set_ca_mano))
            print(str(self._set_ca_prese))
            print(str(self._set_ca_rubate))

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reprJSON(self):
        return dict(
                    _id_gen_man=type(self).__name__,
                    _giocatori=self._giocatori,
                    _mazziere=str(self._mazziere),
                    _player=self._player,
                    _mazzo=self._mazzo,
                    _taglio=self._taglio,
                    _fola=self._fola,
                    _pozzo=self._pozzo,
                    _set_ca_tavola=self._set_ca_tavola,
                    _set_ca_scarti=self._set_ca_scarti,
                    _set_ca_mano=self._set_ca_mano,
                    _set_ca_prese=self._set_ca_prese,
                    _set_ca_rubate=self._set_ca_rubate
               )

    def fromJSON(self, json_object):
        try:
            if '_id_fsm' in json_object.keys():
                self._curdeck = self._mazzo
            elif '_id_vers' in json_object.keys():
                print(json_object['_id_vers'])
            elif '_cardset' in json_object.keys():
                print(json_object['_cardset'])
            elif '_id_deck' in json_object.keys():
                _id_deck = json_object['_id_deck']
                if _id_deck == self._mazzo.get_id():
                    self._curdeck = self._mazzo
                    self._mazzo.fromJSON(json_object)
                elif _id_deck == self._taglio.get_id():
                    self._curdeck = self._taglio
                    self._taglio.fromJSON(json_object)
                    self._curdeck = self._fola
                elif _id_deck == self._fola.get_id():
                    self._curdeck = self._fola
                    self._fola.fromJSON(json_object)
                    self._curdeck = self._pozzo
                elif _id_deck == self._pozzo.get_id():
                    self._curdeck = self._pozzo
                    self._pozzo.fromJSON(json_object)
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_NORD]
                elif _id_deck == self._set_ca_tavola[POSTAZIONE_NORD].get_id():
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_NORD]
                    self._set_ca_tavola[POSTAZIONE_NORD].fromJSON(json_object)
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_EST]
                elif _id_deck == self._set_ca_tavola[POSTAZIONE_EST].get_id():
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_EST]
                    self._set_ca_tavola[POSTAZIONE_EST].fromJSON(json_object)
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_SUD]
                elif _id_deck == self._set_ca_tavola[POSTAZIONE_SUD].get_id():
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_SUD]
                    self._set_ca_tavola[POSTAZIONE_SUD].fromJSON(json_object)
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_OVEST]
                elif _id_deck == self._set_ca_tavola[POSTAZIONE_OVEST].get_id():
                    self._curdeck = self._set_ca_tavola[POSTAZIONE_OVEST]
                    self._set_ca_tavola[POSTAZIONE_OVEST].fromJSON(json_object)
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_NORD]

                elif _id_deck == self._set_ca_scarti[POSTAZIONE_NORD].get_id():
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_NORD]
                    self._set_ca_scarti[POSTAZIONE_NORD].fromJSON(json_object)
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_EST]
                elif _id_deck == self._set_ca_scarti[POSTAZIONE_EST].get_id():
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_EST]
                    self._set_ca_scarti[POSTAZIONE_EST].fromJSON(json_object)
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_SUD]
                elif _id_deck == self._set_ca_scarti[POSTAZIONE_SUD].get_id():
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_SUD]
                    self._set_ca_scarti[POSTAZIONE_SUD].fromJSON(json_object)
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_OVEST]
                elif _id_deck == self._set_ca_scarti[POSTAZIONE_OVEST].get_id():
                    self._curdeck = self._set_ca_scarti[POSTAZIONE_OVEST]
                    self._set_ca_scarti[POSTAZIONE_OVEST].fromJSON(json_object)

                    self._curdeck = self._set_ca_mano[POSTAZIONE_NORD]
                elif _id_deck == self._set_ca_mano[POSTAZIONE_NORD].get_id():
                    self._curdeck = self._set_ca_mano[POSTAZIONE_NORD]
                    self._set_ca_mano[POSTAZIONE_NORD].fromJSON(json_object)
                    self._curdeck = self._set_ca_mano[POSTAZIONE_EST]
                elif _id_deck == self._set_ca_mano[POSTAZIONE_EST].get_id():
                    self._curdeck = self._set_ca_mano[POSTAZIONE_EST]
                    self._set_ca_mano[POSTAZIONE_EST].fromJSON(json_object)
                    self._curdeck = self._set_ca_mano[POSTAZIONE_SUD]
                elif _id_deck == self._set_ca_mano[POSTAZIONE_SUD].get_id():
                    self._curdeck = self._set_ca_mano[POSTAZIONE_SUD]
                    self._set_ca_mano[POSTAZIONE_SUD].fromJSON(json_object)
                    self._curdeck = self._set_ca_mano[POSTAZIONE_OVEST]
                elif _id_deck == self._set_ca_mano[POSTAZIONE_OVEST].get_id():
                    self._curdeck = self._set_ca_mano[POSTAZIONE_OVEST]
                    self._set_ca_mano[POSTAZIONE_OVEST].fromJSON(json_object)

                    self._curdeck = self._set_ca_prese[POSTAZIONE_NORD]
                elif _id_deck == self._set_ca_prese[POSTAZIONE_NORD].get_id():
                    self._curdeck = self._set_ca_prese[POSTAZIONE_NORD]
                    self._set_ca_prese[POSTAZIONE_NORD].fromJSON(json_object)
                    self._curdeck = self._set_ca_prese[POSTAZIONE_EST]
                elif _id_deck == self._set_ca_prese[POSTAZIONE_EST].get_id():
                    self._curdeck = self._set_ca_prese[POSTAZIONE_EST]
                    self._set_ca_prese[POSTAZIONE_EST].fromJSON(json_object)
                    self._curdeck = self._set_ca_prese[POSTAZIONE_SUD]
                elif _id_deck == self._set_ca_prese[POSTAZIONE_SUD].get_id():
                    self._curdeck = self._set_ca_prese[POSTAZIONE_SUD]
                    self._set_ca_prese[POSTAZIONE_SUD].fromJSON(json_object)
                    self._curdeck = self._set_ca_prese[POSTAZIONE_OVEST]
                elif _id_deck == self._set_ca_prese[POSTAZIONE_OVEST].get_id():
                    self._curdeck = self._set_ca_prese[POSTAZIONE_OVEST]
                    self._set_ca_prese[POSTAZIONE_OVEST].fromJSON(json_object)

                    self._curdeck = self._set_ca_rubate[POSTAZIONE_NORD]
                elif _id_deck == self._set_ca_rubate[POSTAZIONE_NORD].get_id():
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_NORD]
                    self._set_ca_rubate[POSTAZIONE_NORD].fromJSON(json_object)
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_EST]
                elif _id_deck == self._set_ca_rubate[POSTAZIONE_EST].get_id():
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_EST]
                    self._set_ca_rubate[POSTAZIONE_EST].fromJSON(json_object)
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_SUD]
                elif _id_deck == self._set_ca_rubate[POSTAZIONE_SUD].get_id():
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_SUD]
                    self._set_ca_rubate[POSTAZIONE_SUD].fromJSON(json_object)
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_OVEST]
                elif _id_deck == self._set_ca_rubate[POSTAZIONE_OVEST].get_id():
                    self._curdeck = self._set_ca_rubate[POSTAZIONE_OVEST]
                    self._set_ca_rubate[POSTAZIONE_OVEST].fromJSON(json_object)
                    self._curdeck = self._mazzo

            elif '_id_carta' in json_object.keys():
                self._curdeck.fromJSON(json_object)

            elif '_id_player' in json_object.keys():
                _player = json_object['_id_player']

            elif '_giocatori' in json_object.keys():
                #self.set_giocatori(_giocatori)
                _list = json_object['_giocatori']
                _mazziere = json_object['_mazziere']
                self.set_giocatori(_list)
                m = json_object['_mazziere']
                for p in self.get_giocatori():
                    if str(p) == m:
                        self.set_mazziere(p)
            else:
                return json_object
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

if __name__ == '__main__':
    man = GeneralManager()
    try:
        _players = []
        _players.append(Player("Davide", POSTAZIONE_SUD))
        _players.append(Player("Tizio", POSTAZIONE_EST))
        _players.append(Player("Caio", POSTAZIONE_NORD))
        _players.append(Player("Sempronio", POSTAZIONE_OVEST))
        man.set_giocatori(_players)
        man.set_mazziere(man.get_player_at_pos(POSTAZIONE_SUD))
        man.set_player(man.get_player_at_pos(POSTAZIONE_OVEST))
        man.set_postazioni([POSTAZIONE_NORD, POSTAZIONE_EST, POSTAZIONE_SUD, POSTAZIONE_OVEST])

        src = man.get_list_ca(DeckId.DECK_MAZZO)
        c = src.pop()
        dst = man.get_list_ca(DeckId.DECK_MANO, POSTAZIONE_OVEST)
        if dst is not None:
            dst.append(c)
        cc = json.dumps(man.reprJSON(), cls=ComplexEncoder)
        f = JSONDecoder(object_hook=GeneralManager.fromJSON).decode(cc)
        d = f.get_deck(DeckId.DECK_MANO, POSTAZIONE_OVEST)
        print(f.get_player_at_pos(POSTAZIONE_SUD))
        print(f.get_mazziere())
        print(str(d))
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)