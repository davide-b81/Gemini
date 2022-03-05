'''
Created on 4 gen 2022

@author: david
'''
from copy import copy
from time import monotonic

import pygame

from game.germini.punteggi import punti_ger
from main.globals import *
from game.germini.strategia import Strategia
from main.general_manager import *
from game.germini.fsm_germini import FsmGermini
from oggetti.posizioni import DECK_RUBATE
from oggetti.tavolo import TavoloArea
from oggetti.stringhe import _
from main.exception_man import ExceptionMan


class GiocoManager(object):
    '''
    classdocs
    '''
    _globals = None
    game = None
    _fsmc = None
    _fsmger = None
    _gen_manager = None
    _pos_man = None
    _tavolo = None
    _strategia = None
    _draw_stable = None

    # Gestione carta
    _delegate_show_carta = None
    _delegate_hide_carta = None
    _delegate_set_fronte = None
    # Gestione mazzi
    _delegate_show_mazzo = None
    _delegate_hide_mazzo = None
    _delegate_is_coperta = None
    _delegate_set_mazzo_ultima = None
    _delegate_show_pozzo = None
    _delegate_hide_pozzo = None
    _delegate_show_fola = None
    _delegate_hide_fola = None
    _delegate_show_presa = None
    _delegate_hide_presa = None
    _delegate_show_mano = None
    _delegate_hide_mano = None

    _delegate_show_tavola = None
    _delegate_hide_tavola = None

    _delegate_mescola = None
    _delegate_posiziona_carta = None

    _delegate_set_z = None
    _delegate_is_front = None
    _delegate_rotate_pos_carta = None
    _delegate_sort = None
    _delegate_incamera = None
    _delegate_restore_mazzo = None
    _delegate_draw_stable = None
    _delegate_show_popup = None
    _delegete_on_presa = None
    _delegate_redraw = None
    _delegate_turno = None
    _delegate_mazziere = None
    _delegate_cade = None
    _delegate_fola = None
    _t_update = None

    def __init__(self, pos_man):
        '''
        Constructor
        '''
        try:
            self._globals = Globals()
            self._pos_man = pos_man
            self._gen_manager = GeneralManager(self)
            self._gen_manager.set_delegate_restore_mazzo(self.restore_mazzo)
            self._gen_manager.set_delegate_update_z(self.set_z)
            self._gen_manager.set_delegate_set_fronte(self.set_fronte)
            self._gen_manager.set_delegate_is_coperta(self.is_coperta)
            self._gen_manager.set_delegate_rotate_pos_carta(self.rotate_pos_carta)

            self._tavolo = TavoloArea(self._pos_man)
            self._strategia = Strategia(self._gen_manager)

            self._fsmger = FsmGermini(self, self._gen_manager)
            self._fsmger.set_delegate_append_html_text(self.on_append_text_box)
            self._fsmger.set_delegate_show_popup(self.on_show_popup)
            self._fsmger.set_delegate_presa(self.on_incamera)
            self._fsmger.set_delegate_update_turno(self.on_turno)
            self._fsmger.set_delegate_update_mazziere(self.on_mazziere)
            self._fsmger.set_delegate_update_fola(self.on_fola)
            self._fsmger.set_delegate_update_caduto(self.on_cade)

            self._t_update = monotonic()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_show_mazzo(self, f):
        self._delegate_show_mazzo = f

    def set_delegate_hide_mazzo(self, f):
        self._delegate_hide_mazzo = f

    def set_delegate_set_mazzo_ultima(self, f):
        self._delegate_set_mazzo_ultima = f

    def set_delegate_show_pozzo(self, f):
        self._delegate_show_pozzo = f

    def set_delegate_hide_pozzo(self, f):
        self._delegate_hide_pozzo = f

    def set_delegate_show_fola(self, f):
        self._delegate_show_fola = f

    def set_delegate_hide_fola(self, f):
        self._delegate_hide_fola = f

    def set_delegate_show_presa(self, f):
        self._delegate_show_presa = f

    def set_delegate_hide_presa(self, f):
        self._delegate_hide_presa = f

    def set_delegate_show_mano(self, foo):
        self._delegate_show_mano = foo

    def set_delegate_hide_mano(self, foo):
        self._delegate_hide_mano = foo

    def set_delegate_show_tavola(self, foo):
        self._delegate_show_tavola = foo

    def set_delegate_hide_tavola(self, foo):
        self._delegate_hide_tavola = foo

    def set_delegate_show_carta(self, f):
        self._delegate_show_carta = f

    def set_delegate_hide_carta(self, f):
        self._delegate_hide_carta = f

    def set_delegate_set_fronte(self, f):
        self._delegate_set_fronte = f

    def set_delegate_is_coperta(self, f):
        self._delegate_is_coperta = f

    def set_delegate_card_move(self, f):
        self._delegate_posiziona_carta = f

    def set_delegate_set_z(self, f):
        self._delegate_set_z = f

    def set_delegate_is_front(self, f):
        self._delegate_is_front = f

    def set_delegate_rotate_pos_carta(self, f):
        self._delegate_rotate_pos_carta = f

    def set_delegate_restore(self, foo):
        self._delegate_restore_mazzo = foo

    def set_delegate_frame_show_popup(self, foo):
        self._delegate_show_popup = foo

    def set_delegate_append_text_box(self, foo):
        self._delegate_append_text_box = foo

    def set_delegate_draw_stable(self, foo):
        self._delegate_draw_stable = foo

    def set_delegete_presa(self, f):
        self._delegete_on_presa = f

    def set_delegate_mescola(self, foo):
        self._delegate_mescola = foo

    def set_delegate_redraw(self, f):
        self._delegate_redraw = f

    def set_delegate_turno(self, f):
        self._delegate_turno = f

    def set_delegate_mazziere(self, f):
        self._delegate_mazziere = f

    def set_delegate_fola(self, f):
        self._delegate_fola = f

    def set_delegate_cade(self, f):
        self._delegate_cade = f

    def get_draw_stable(self):
        try:
            if self._delegate_draw_stable is not None:
                 return self._delegate_draw_stable
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_show_popup(self, txt, visible=True):
        try:
            self._delegate_show_popup(txt, visible)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_turno(self, player):
        try:
            self._delegate_turno(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_mazziere(self, player):
        try:
            self._delegate_mazziere(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_fola(self, player):
        try:
            self._delegate_fola(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_cade(self, player):
        try:
            self._delegate_cade(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_append_text_box(self, txt):
        try:
            print("Message box output: " + txt)
            self._delegate_append_text_box(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti(self, player, c):
        try:
            if c.get_id() in punti_ger:
                pts = punti_ger[c.get_id()]
                if pts > 0:
                    player.mangia_carta(c, pts)
                ca = [c]
                self._delegete_on_presa(player, ca)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_incamera(self, player, cc):
        try:
            pts = 0
            for c in cc:
                self.nascondi_carta(c)
                self.marca_punti(player, c)
                self._gen_manager.remove_tavola(c)
            self._delegete_on_presa(player, cc)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_popup_click(self):
        try:
            if self.game:
                self.game.on_popup()
                self._fsmger.on_popup()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if cid is not None:
                print("Click su " + str(cid))
                if cid == "POPUP":
                    self.game.on_popup()
                elif self.game != None and self.game == self._fsmger:
                    self._fsmger.on_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_gioco(self, gioco):
        try:
            if self._fsmc.__class__.__name__ == gioco:
                self.game = self._fsmc
                echo_message(_("Who get greatest card will be the Dealer"))
            elif self._fsmger.__class__.__name__ == gioco:
                echo_message(_("Germini"))
                self.game = self._fsmger
            else:
                raise Exception("Unknown game " + gioco)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_giocatori(self, giocatori):
        try:
            self._gen_manager.set_giocatori(giocatori)
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_giocatori(self):
        try:
            return self._gen_manager.get_giocatori()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_giocatori_pos(self):
        try:
            res = []
            for pos in self._tavolo.get_posizioni():
                res.append((self._gen_manager.get_player_at_pos(pos), pos))
            return res
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_reset(self):
        try:
            # self.restore_mazzo()
            # self.gen_manager.restore_tavola()
            # self.gen_manager.restore_mazzo()
            self.game.on_termina()
            self.game.winner = None
            self._gen_manager.termina_gioco()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_mazzo(self):
        try:
            self._delegate_restore_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self):
        try:
            self._gen_manager.capovolgi_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def taglia_mazzo(self, cid):
        try:
            self._gen_manager.taglia_mazzo(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ricomponi_taglio(self):
        try:
            self._gen_manager.ricomponi_taglio()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raddrizza_mazzo(self):
        try:
            self._gen_manager.raddrizza_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola_mazzo(self):
        try:
            self._gen_manager.mescola_mazzo()
            self._delegate_mescola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def read_last(self):
        try:
            return self._gen_manager.read_ultima_carta()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizia_gioco(self, giocatori, gioco):
        try:
            print("INIZIA")
            self.set_gioco(gioco)
            self.reset_giocatori()
            self.reset_tavola()
            self.reset_mazzo()
            self.game.winner = None
            self.set_giocatori(giocatori)
            self._gen_manager.mescola_mazzo()
            self.set_gioco(gioco)
            self.game.start_game()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_mazziere(self):
        try:
            return self._gen_manager.get_mazziere()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_mazziere(self, player):
        try:
            self._gen_manager.set_mazziere(player)
            self._delegate_mazziere(player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def termina_gioco(self):
        try:
            self.restore()
            if self.game is not None:
                self.game.winner = None
                self.game.on_termina()
            self._gen_manager.termina_gioco()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_gioco(self, screen):
        try:
            if self._delegate_draw_stable():
                if self.game != None:
                    self.update_carte()

                    if self.game == self._fsmc:
                        if self.game.get_finished():
                            if self.game.winner is not None:
                                self._gen_manager.set_mazziere(self.game.winner)
                                self.giocatore_turno = self.game.winner
                                echo_message(_("Il mazziere sara' " + str(self.game.winner)))
                                self.game = self._fsmger
                                # I giocatori sono gli stessi
                                players = copy(self._gen_manager._giocatori)
                                self.inizia_gioco(players, "FsmGermini")
                        else:
                            self.game.update_game()
                    elif self.game == self._fsmger:
                        if not self.game.get_finished():
                            self.game.update_game()
                Strategia.update_mano()

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_carte(self):
        try:
            pps = self._tavolo.get_posizioni()
            for pos in pps:
                player = self._gen_manager.get_player_at_pos(pos)
                if player is not None:
                    cman = self._gen_manager.get_carte_mano(player)
                    if cman is not None and len(cman) > 0:
                        self._delegate_show_mano(pos, cman)

                ccal = self._gen_manager.get_carte_in_tavola(pos)
                if ccal is not None and len(ccal) > 0:
                    if self._delegate_show_tavola is not None:
                        # TODO: Prende solo la sotto-lista costituita dal primo elemento. Gestire il caso in cui il giocatore cala più carte
                        self._delegate_show_tavola(pos, ccal[:1])
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_running(self):
        try:
            if self.game is not None:
                return self.game.is_running()
            else:
                return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_player_at_pos(self, pos):
        try:
            return self._gen_manager.get_player_at_pos(pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_opposit_player(self, player):
        try:
            pos = self._gen_manager.get_opposit_pos(player.get_position())
            return self.get_player_at_pos(pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_next_player(self, player, antior=True):
        try:
            if player is None:
                if self._globals.get_debug():
                    player = self._gen_manager.get_player_at_pos("Sud")
                else:
                    assert player is None
            pos = self._tavolo.get_next_pos(player.get_position(), antior)
            player = self._gen_manager.get_player_at_pos(pos)
            if player is not None:
                echo_message("Turno di " + str(player) + " (" + player.get_position() + ")")
            return player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def passa_fola(self, player):
        try:
            self.copri_fola(player.get_position())
            self.raccogli_mazzo(player.get_position(), DECK_FOLA)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def carte_calate(self, posizione):
        try:
            return self._gen_manager.get_carte_in_tavola(posizione)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_mazzo(self):
        try:
            self._gen_manager.restore_mazzo()
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_giocatori(self):
        try:
            self._gen_manager.pulisci_giocatori()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_tavola(self):
        try:
            pps = self._tavolo.get_posizioni()
            for pos in pps:
                cc = self._gen_manager.get_carte_in_tavola(pos)
                self.rimuove_da_tavola(cc)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("Error", e, True)

    def mostra_in_tavola(self, player, c):
        try:
            self.cala_in_tavola(player, c)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore(self):
        try:
            print("Restore")
            self._gen_manager.restore_all()
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_carta(self, c):
        try:
            self._delegate_show_carta(c)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def nascondi_carta(self, c):
        try:
            self._delegate_hide_carta(c)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_fronte(self, c, coperta=FRONTE_COPERTA):
        try:
            self._delegate_set_fronte(c, coperta)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def is_coperta(self, c):
        try:
            self._delegate_is_coperta(c)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_z(self, c, z):
        try:
            self._delegate_set_z(c, z)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def rotate_pos_carta(self, c, ppos=None):
        try:
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_taglio(self, ppos=None):
        try:
            ca = self._gen_manager.get_taglio()
            i = 0
            for c in ca:
                self._delegate_show_carta(c)
                (x, y) = self._pos_man.get_area_taglio(ppos)
                pos = (int(x + (i / 2)), int(y + (i / 2)))
                self._delegate_posiziona_carta(c, pos, True)
                self._delegate_set_z(c, i)
                self._delegate_rotate_pos_carta(c, ppos, True)
                i = i + 1
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def raccogli_mazzo(self, ppos, deck=DECK_MAZZO):
        try:
            i = 0
            ca = self._gen_manager.get_deck(deck)
            for c in ca:
                self._delegate_show_carta(c)
                (x, y) = self._pos_man.get_area_mazzo(ppos)
                pos = (int(x + (i / 2)), int(y + (i / 2)))
                self._delegate_posiziona_carta(c, pos, True)
                self._delegate_set_z(c, i)
                self._delegate_rotate_pos_carta(c, ppos)
                i = i + 1
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_mazzo(self, ppos=None, deck=DECK_MAZZO):
        try:
            self.raccogli_mazzo(ppos, deck)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_rubate(self, ppos=None):
        try:
            z = 0
            player = self._gen_manager.get_player_at_pos(ppos)
            ca = self._gen_manager.get_carte_rubate(player)
            if ca != None:
                for c in ca:
                    pos = self._pos_man.get_pos_stesa(ppos, DECK_RUBATE, z, len(ca), self._pos_man.get_card_size()[0])
                    self._delegate_posiziona_carta(c, pos, True)
                    self._delegate_set_z(c, z)
                    self._delegate_rotate_pos_carta(c, ppos)
                    self.set_fronte(c, FRONTE_SCOPERTA)
                    z = z + 1
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def copri_fola(self, ppos=None):
        try:
            print("Nascondi fola")
            ca = self._gen_manager.get_deck(DECK_FOLA)
            i = 0
            for c in ca:
                self._delegate_set_fronte(c, FRONTE_COPERTA)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def sposta_carte(self, src, dest_deck):
        try:
            deck = self._gen_manager.get_deck(dest_deck)
            deck.append(src)
            src.clear()
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def stendi_deck(self, ppos, deck, coperto=FRONTE_SCOPERTA):
        try:
            z = 0
            mazzo = self._gen_manager.get_deck(deck)
            if mazzo != None:
                for c in mazzo:
                    pos = self._pos_man.get_pos_stesa(ppos, DECK_FOLA, z, len(mazzo), self._pos_man.get_card_size()[0])
                    self._delegate_posiziona_carta(c, pos, True)
                    self._delegate_set_z(c, z)
                    self._delegate_rotate_pos_carta(c, ppos)
                    self.set_fronte(c, coperto)
                    z = z + 1
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_fola(self, player):
        try:
            self.stendi_deck(player.get_position(), DECK_FOLA)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def nascondi_mazzo(self):
        try:
            # self._delegate_hide_mazzo(self._gen_manager.get_mazzo())
            ca = self._gen_manager.get_deck()
            for c in ca:
                self._delegate_hide_carta(c)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def pop_prima(self, deck=DECK_TAGLIO):
        try:
            return self._gen_manager.pop_carta(0, deck)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def get_prima(self, deck=DECK_TAGLIO):
        try:
            return self._gen_manager.read_carta(0, deck)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def get_ultima(self, deck=DECK_TAGLIO):
        try:
            return self._gen_manager.read_carta(-1, deck)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def get_ultima_carta(self):
        try:
            return self._gen_manager.read_ultima_carta()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def get_carta_mazzo(self, i=0, deck=DECK_MAZZO):
        try:
            return self._gen_manager.read_carta(i, deck)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_mazzo_ultima(self):
        try:
            self._delegate_set_mazzo_ultima(self._gen_manager.get_deck())
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def scarta(self, player):
        ca = []
        try:
            ca = self._gen_manager.get_carte_rubate(player)
            self._gen_manager.scarta(player, len(ca))
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def cala_in_tavola(self, player, c):
        try:
            self.set_fronte(c, FRONTE_SCOPERTA)
            c = self._gen_manager.sposta_in_tavola(player, c)
            pos = self._pos_man.get_area_tavola(player.get_position())
            self._delegate_posiziona_carta(c, pos, False)
            self._delegate_rotate_pos_carta(c, pos)
            self._gen_manager.update_z(self._gen_manager.get_carte_in_tavola(player.get_position()))
            self.on_redraw()
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def rimuove_da_tavola(self, ca):
        try:
            if ca is not None:
                for c in ca:
                    self._delegate_hide_carta(c)
                    self._gen_manager.rimuove_carta_in_tavola(c)
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_mano_giocatore(self, player, ca, coperta=FRONTE_COPERTA):
        try:
            if ca is not None:
                for c in ca:
                    self.set_fronte(c, coperta)
                    pos = self._pos_man.get_area_tavola(player.get_position())
                    self._delegate_posiziona_carta(c, pos, False)
                    self._gen_manager.add_mano_giocatore(player, c)
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position_manager(self):
        try:
            return self._pos_man
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, evt):
        try:
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_r:
                    self.on_sort()
                    self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri_carte(self, player):
        try:
            ca = self._gen_manager.get_carte_mano(player)
            for c in ca:
                self.set_fronte(c, FRONTE_SCOPERTA)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_sort(self):
        try:
            res = []
            for pos in self._tavolo.get_posizioni():
                player = self._gen_manager.get_player_at_pos(pos)
                self._gen_manager.sort_mazzo(player)
            if len(res) > 0:
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_redraw(self):
        try:
            self._delegate_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
