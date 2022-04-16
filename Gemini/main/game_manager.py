'''
Created on 4 gen 2022

@author: david
'''
from copy import copy
from time import monotonic

import pygame

from decks.carta_id import CartaId
from game.germini.punteggi import carte_conto
from main.general_manager import GeneralManager
from main.globals import *
from game.germini.strategia import Strategia
from game.germini.fsm_germini import FsmGermini
from oggetti.posizioni import DeckId
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
    _draw_stable = None
    _posizioni = None
    # Gestione carta
    _delegate_show_carta = None
    _delegate_hide_carta = None
    _delegate_set_fronte = None
    # Gestione mazzi
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
            self._gen_manager = GeneralManager()
            self._gen_manager.set_delegate_restore_mazzo(self.restore_mazzo)
            self._gen_manager.set_delegate_update_z(self.set_z)
            self._gen_manager.set_delegate_hoverable(self.set_hoverable)
            self._gen_manager.set_delegate_set_fronte(self.set_fronte)
            self._gen_manager.set_delegate_is_coperta(self.is_coperta)
            self._gen_manager.set_delegate_rotate_pos_carta(self.rotate_pos_carta)
            self._fsmger = FsmGermini(self, self._gen_manager)
            self._fsmger.set_delegate_append_html_text(self.on_append_text_box)
            self._fsmger.set_delegate_show_popup(self.on_show_popup)
            self._fsmger.set_delegate_presa(self.on_presa)
            self._fsmger.set_delegate_update_turno(self.on_turno)
            self._fsmger.set_delegate_update_mazziere(self.on_mazziere)
            self._fsmger.set_delegate_update_players(self.on_players)
            self._fsmger.set_delegate_update_fola(self.on_fola)
            self._fsmger.set_delegate_update_caduto(self.on_cade)

            self._t_update = monotonic()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    ''' Initialize delegates '''

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

    def set_delegate_set_hoverable(self, f):
        self._delegate_set_hoverable = f

    def set_delegate_is_front(self, f):
        self._delegate_is_front = f

    def set_delegate_rotate_pos_carta(self, f):
        self._delegate_rotate_pos_carta = f

    def set_delegate_restore_mazzo(self, foo):
        self._delegate_restore_mazzo = foo

    def set_delegate_frame_show_popup(self, foo):
        self._delegate_show_popup = foo

    def set_delegate_append_text_box(self, foo):
        self._delegate_append_text_box = foo

    def set_delegate_draw_stable(self, f):
        self._delegate_draw_stable = f

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

    def set_delegete_on_players(self, f):
        self._delegete_on_players = f

    def set_delegate_fola(self, f):
        self._delegate_fola = f

    def set_delegate_cade(self, f):
        self._delegate_cade = f

    def get_posizioni(self):
        return self._posizioni

    def set_posizioni(self, pp):
        self._posizioni = pp

    def on_show_popup(self, txt):
        try:
            return self._delegate_show_popup(txt, True)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_hide_popup(self):
        try:
            return self._delegate_show_popup("", False)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_turno(self, player):
        try:
            if player is not None:
                self._delegate_turno(player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_mazziere(self, ppos):
        try:
            self._delegate_mazziere(ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_players(self):
        try:
            self._delegete_on_players()
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
            self._delegate_append_text_box(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti(self, player, pts):
        try:
            player.segna_punti(pts)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti_carta(self, player, c):
        try:
            if c.get_id() in carte_conto:
                pts = carte_conto[c.get_id()]
                if pts > 0:
                    player.mangia_carta(c, pts)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raccogli_carte_calate(self, winner, player):
        try:
            ca = self._gen_manager.get_carte_in_tavola_pos(player.get_position())
            for c in ca:
                if c.get_id() != CartaId.MATTO_0:
                    self.marca_punti_carta(winner, c)
                elif not self._gen_manager.is_ultima_mano():
                    pass
                else:
                    pass
                self.nascondi_carta(c)
                self._gen_manager.remove_tavola(winner, c)
            self._delegete_on_presa(winner, ca)
            self.on_redraw()
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_punti_mano(self):
        try:
            if self.game != None and self.game == self._fsmger:
                return self._fsmger.get_text_punti_mano()
            return ""
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_punti_totale(self):
        try:
            if self.game != None and self.game == self._fsmger:
                return self._fsmger.get_text_punti_totale()
            return ""
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_presa(self, player, c_list):
        try:
            self.update_carte()
            if self.game != None:
                self.game.on_presa(player, c_list)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gestisci_matto(self, cc):
        try:
            c_list = self.start_game().get_carte_in_tavola()
            pp = self.get_posizioni()
            for p in pp:
                for c in c_list[p]:
                    if c.get_id() == CartaId.MATTO_0:
                        player = self._game_man.get_player_at_pos(p)
                        self._delegate_presa(player, [c])
                        c_list[p].remove(c)
                        break
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_popup_click(self):
        try:
            if self.game:
                self.game.on_popup()
                self._fsmger.on_popup()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_click(self, cid):
        try:
            if cid is not None:
                print("Click su " + str(cid))
                if cid == "POPUP":
                    self.game.on_popup()
                elif self.game != None and self.game == self._fsmger:
                    self.on_carta_click(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if cid is not None:
                if self.game != None and self.game == self._fsmger:
                    self._fsmger.on_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_gioco(self, gioco):
        try:
            if self._fsmc.__class__.__name__ == gioco:
                self.game = self._fsmc
                self._fsmc.reset()
                echo_message(_("Who get greatest card will be the Dealer"))
            elif self._fsmger.__class__.__name__ == gioco:
                echo_message(_("Germini"))
                self.game = self._fsmger
            else:
                raise Exception("Unknown game " + gioco)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_giocatori_pos(self):
        try:
            res = []
            for pos in self.get_posizioni():
                res.append((self._gen_manager.get_player_at_pos(pos), pos))
            return res
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_reset(self):
        try:
            self.restore_mazzo()
            self._gen_manager.restore_tavola()
            self._gen_manager.restore_mazzo()
            self._gen_manager.termina_gioco()
            self.reset_giocatori()
            Strategia.reset()
            if self.game is not None:
                self.game.on_termina()
                self.game = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_mazzo(self):
        try:
            self._delegate_restore_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola_mazzo(self):
        try:
            self._gen_manager.mescola_mazzo()
            self._delegate_mescola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizia_gioco(self, giocatori, gioco):
        try:
            print("INIZIA")
            self.set_gioco(gioco)
            self.reset_tavola()
            self.reset_mazzo()
            self.game.winner = None
            self.set_giocatori(giocatori)
            self.set_postazioni(self.game.get_postazioni())
            self._gen_manager.start()
            self._gen_manager.mescola_mazzo()
            self.game.start_game()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            self._gen_manager.start()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_player(self):
        try:
            return self._gen_manager.get_player()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_position_turno(self):
        try:
            return self.get_player().get_position()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_mazziere(self):
        try:
            return self._gen_manager.get_mazziere()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_player(self, player):
        try:
            return self._gen_manager.set_player(player)
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
                                self._gen_manager.set_player(self.game.winner)
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
            pps = self.get_posizioni()
            for pos in pps:
                player = self._gen_manager.get_player_at_pos(pos)
                if player is not None:
                    cman = self._gen_manager.get_carte_mano(player)
                    if cman is not None and len(cman) > 0:
                        self._delegate_show_mano(pos, cman)

                ccal = self._gen_manager.get_carte_in_tavola_pos(pos)
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
                player = self.get_mazziere()
            
            #pp = self._gen_manager.get_giocatori()
            #if pp[0].get_position() is not None:
            #    print(str(pp[0]) + " - " + pp[0].get_position())
            #if pp[1].get_position() is not None:
            #    print(str(pp[1]) + " - " + pp[1].get_position())
            #if pp[2].get_position() is not None:
            #    print(str(pp[2]) + " - " + pp[2].get_position())
            #if pp[3].get_position() is not None:
            #    print(str(pp[3]) + " - " + pp[3].get_position())

            i = self._posizioni.index(player.get_position())
            if not antior:
                i = (i + 1) % len(self._posizioni)
            else:
                if i > 0:
                    i = (i - 1) % len(self._posizioni)
                else:
                    i = len(self._posizioni) - 1

            pos = self._posizioni[i]
            
            player = self._gen_manager.get_player_at_pos(pos)
            if player is not None:
                n = len(self.get_deck(DeckId.DECK_MANO, player.get_position()))
                echo_message("Turno di " + str(player) + " (" + player.get_position() + ") - " + str(n) + " carte in mano.")
            else:
                raise Exception("No player")
            return player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def passa_fola(self, player):
        try:
            self.copri_fola(player.get_position())
            self.raccogli_mazzo(player.get_position(), DeckId.DECK_FOLA)
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

    def reset_tavola(self):
        try:
            pps = self.get_posizioni()
            for pos in pps:
                cc = self._gen_manager.get_carte_in_tavola_pos(pos)
                self.rimuove_da_tavola(cc)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("Error", e, True)

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

    def get_fronte(self, c):
        try:
            self._gen_manager.get_fronte(c)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_fronte(self, c, coperta, inst):
        try:
            self._delegate_set_fronte(c, coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def is_coperta(self, c):
        try:
            self._delegate_is_coperta(c)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_hoverable(self, c, h):
        try:
            self._delegate_set_hoverable(c, h)
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
            mazzo = self._gen_manager.get_taglio()
            i = 0
            #if not self._globals.get_uncover():
            #    mazzo.reverse()
            for c in mazzo:
                self._delegate_show_carta(c)
                (x, y) = self._pos_man.get_area_taglio(ppos)
                pos = (int(x + (i / 2)), int(y + (i / 2)))
                self._delegate_posiziona_carta(c, pos, self._globals.get_instant())
                if not self._globals.get_uncover():
                    self._delegate_set_z(c, i + 1)
                self._delegate_rotate_pos_carta(c, ppos, self._globals.get_instant())
                i = i + 1
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def stendi_deck(self, deck, ppos, n=0):
        """
        Carte stese
        """
        try:
            mazzo = self._gen_manager.get_deck(deck, ppos)
            if mazzo != None:
                for c in mazzo:
                    z = n
                    pos = self._pos_man.get_pos_stesa(ppos, deck, n, len(mazzo), self._pos_man.get_card_size()[0] / 2)
                    self._delegate_posiziona_carta(c, pos, self._globals.get_instant())
                    self._delegate_rotate_pos_carta(c, ppos, self._globals.get_instant())
                    self._delegate_set_z(c, z)
                    coperto = FRONTE_SCOPERTA
                    if coperto == FRONTE_SCOPERTA:
                        if deck == DeckId.DECK_MANO:
                            self._delegate_set_hoverable(c, True)
                        else:
                            self._delegate_set_hoverable(c, False)
                    n = n + 1
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def raccogli_mazzo(self, ppos, deck=DeckId.DECK_MAZZO, n=None):
        """
        Carte raccolte in un mazzo
        """
        try:
            i = 0
            hoverable = True
            ca = self._gen_manager.get_deck(deck)
            if n is None:
                n = len(ca)

            for c in ca:
                if not self._globals.get_uncover():
                    index = i
                else:
                    index = n - i
                (x, y) = self._pos_man.get_area_mazzo(deck, ppos)
                pos = (int(x + (index / 2)), int(y + (index / 2)))
                self._delegate_show_carta(c, pos)
                self._delegate_posiziona_carta(c, pos, self._globals.get_instant())
                self._delegate_rotate_pos_carta(c, ppos, self._globals.get_instant())
                self._delegate_set_z(c, index + 1)

                self._delegate_set_hoverable(c, hoverable)
                hoverable = False

                i = i + 1
                if i >= n:
                    break
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_mazzo(self, deck, ppos=None, n=None):
        try:
            print("MOSTRA MAZZO " + ppos)
            self.raccogli_mazzo(ppos, deck, n)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_scarto(self, ppos=None):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)
        
    def mostra_rubate(self, ppos=None):
        try:
            z = 0
            player = self._gen_manager.get_player_at_pos(ppos)
            ca = self._gen_manager.get_carte_rubate(player)
            if ca != None:
                for c in ca:
                    pos = self._pos_man.get_pos_stesa(ppos, DeckId.DECK_RUBATE, len(ca) - z, len(ca),
                                                      self._pos_man.get_card_size()[0])
                    self._delegate_posiziona_carta(c, pos, self._globals.get_instant())
                    self._delegate_set_z(c, z + 1)
                    self._delegate_rotate_pos_carta(c, ppos, self._globals.get_instant())
                    self.set_fronte(c, FRONTE_SCOPERTA, self._globals.get_instant())
                    z = z + 1
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def sposta_carta(self, c, src_deck, dst_deck, player):
        try:
            if player is not None:
                ppos = player.get_position()
            else:
                ppos = None

            if src_deck is not None:
                src = self._gen_manager.get_deck(src_deck, ppos)
                dst = self._gen_manager.get_deck(dst_deck, ppos)
                src.remove(c)
                dst = self._gen_manager.get_deck(dst_deck, ppos)
                if dst is not None:
                    dst.append(c)
                self.on_redraw()
        except Exception as e:
            print(str(c))
            ExceptionMan.manage_exception("", e, True)

    def mostra_scarto(self, player):
        try:
            self.stendi_deck(DeckId.DECK_POZZO, player.get_position(), 12)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_fola(self, player):
        try:
            self.stendi_deck(DeckId.DECK_FOLA, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def nascondi_fola(self, player):
        try:
            self.nascondi_mazzo(DeckId.DECK_FOLA, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def copri_fola(self, ppos=None):
        try:
            print("Nascondi fola")
            ca = self._gen_manager.get_deck(DeckId.DECK_FOLA)
            i = 0
            for c in ca:
                self._delegate_set_fronte(c, FRONTE_COPERTA, self._globals.get_instant())
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def nascondi_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            ca = self._gen_manager.get_deck(deck, ppos)
            for c in ca:
                self._delegate_hide_carta(c)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def scarta(self, player, c):
        ca = []
        try:
            self.set_fronte(c, FRONTE_COPERTA, self._globals.get_instant())
            self._gen_manager.scarta(c, player)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def mostra_in_tavola(self, c, ppos, inst):
        try:
            self.set_fronte(c, FRONTE_SCOPERTA, inst)
            pos = self._pos_man.get_area_tavola(ppos)
            self._delegate_posiziona_carta(c, pos, self._globals.get_instant())
            self._delegate_rotate_pos_carta(c, pos, self._globals.get_instant())
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cala_in_tavola(self, player, c, inst):
        try:
            self._gen_manager.sposta_in_tavola(c, player.get_position())
            self.mostra_in_tavola(c, player.get_position(), inst)
            #self._gen_manager.update_z(self._gen_manager.get_carte_in_tavola_pos(pos))
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

    def add_mano_giocatore(self, player, ca, coperta=FRONTE_COPERTA, hoverable=False):
        try:
            if ca is not None:
                for c in ca:
                    self.set_fronte(c, coperta, self._globals.get_instant())
                    self.set_hoverable(c, hoverable)
                    pos = self._pos_man.get_area_mano(player.get_position())
                    self._delegate_posiziona_carta(c, pos, self._globals.get_instant())
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
            if self.game is not None:
                self.game.on_event(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri_carte(self, player):
        try:
            ca = self._gen_manager.get_carte_mano(player)
            for c in ca:
                self.set_fronte(c, FRONTE_SCOPERTA, self._globals.get_instant())
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
    Deletage manager
    '''

    def on_sort(self):
        try:
            res = []
            # for pos in self.get_posizioni():
            #    player = self._gen_manager.get_player_at_pos(pos)
            self._gen_manager.sort_mazzo(self._gen_manager.get_player_at_pos(POSTAZIONE_SUD))
            if len(res) > 0:
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_redraw(self):
        try:
            self._delegate_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_mano(self, player):
        try:
            return len(self._gen_manager.get_carte_mano(player))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_prese(self, player):
        try:
            return len(self._gen_manager.get_carte_prese(player))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_in_tavola(self):
        return self._gen_manager.get_carte_tavola()

    def get_compagno(self, player):
        try:
            pos = self.get_opposit_pos(player.get_position())
            return self.get_player_at_pos(pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
    General manager wrapper
    '''

    def set_postazioni(self, ppos):
        self.set_posizioni(ppos)
        self._gen_manager.set_postazioni(ppos)

    def get_postazioni(self):
        return self.get_posizioni()

    def set_giocatori(self, giocatori):
        self._gen_manager.set_giocatori(giocatori)

    def get_giocatori(self):
        return self._gen_manager.get_giocatori()

    def get_carte_mano(self, player):
        return self._gen_manager.get_carte_mano(player)

    def merge_deck(self, deck_src, ppos_src, deck_dst, ppos_dst):
        self._gen_manager.merge_deck(deck_src, ppos_src, deck_dst, ppos_dst)

    def taglia_mazzo(self, cid):
        self._gen_manager.taglia_mazzo(cid)

    def ricomponi_taglio(self, player):
        try:
            assert player is not None
            self.capovolgi_mazzo(DeckId.DECK_TAGLIO, player.get_position(), FRONTE_COPERTA)
            self.merge_deck(DeckId.DECK_TAGLIO, player.get_position(), DeckId.DECK_MAZZO, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None, fronte=FRONTE_SCOPERTA):
        self._gen_manager.capovolgi_mazzo(deck, ppos, fronte)

    def raddrizza_mazzo(self):
        self._gen_manager.capovolgi_mazzo(DeckId.DECK_MAZZO, None, FRONTE_COPERTA)

    def read_carta(self, i, deck, player):
        return self._gen_manager.read_carta(i, deck, player)

    def set_mazzo_ultima(self):
        self._delegate_set_mazzo_ultima(self._gen_manager.get_deck())

    def get_carte_in_tavola_pos(self, pos):
        return self._gen_manager.get_carte_in_tavola_pos(pos)

    def clear_carte_in_tavola(self, posizione):
        return self._gen_manager.clear_carte_in_tavola(posizione)

    def reset_giocatori(self):
        self._gen_manager.restore_giocatori()

    def pop_prima(self, deck=DeckId.DECK_TAGLIO, ppos=None):
        return self._gen_manager.pop_carta(0, deck, ppos)

    def has_seme(self, player, seed):
        return self._gen_manager.has_seme(player, seed)

    def add_rubate_giocatore(self, player, c):
        return self._gen_manager.add_rubate_giocatore(player, c)

    def get_deck(self, deck=DeckId.DECK_MAZZO, ppos=None):
        return self._gen_manager.get_deck(deck, ppos)

    def piglia_da_fola(self, player):
        return self._gen_manager.piglia_da_fola(player)

    def append_fola(self, c):
        return self._gen_manager.append_fola(c)

    def preleva_dal_mazzo(self, n):
        return self._gen_manager.preleva_dal_mazzo(n)

    def inserisci_nel_mazzo(self, c, deck, ppos):
        self._gen_manager.inserisci_nel_mazzo(c, deck, ppos)

    def pesca_dal_mazzo(self, deck, ppos):
        return self._gen_manager.pesca_dal_mazzo(deck, ppos)

    def get_carte_rubate(self, player):
        return self._gen_manager.get_carte_rubate(player)

    def split_mazzo_n(self, n):
        return self._gen_manager.split_mazzo_n(n)

    def deck_contains(self, cid, deck=DeckId.DECK_MAZZO, player=None):
        return self._gen_manager.deck_contains(cid, deck, player)

    def has_carta(self, player, cid):
        return self._gen_manager.has_carta(player, cid)

    def restore_manche(self):
        return self._gen_manager.restore_manche()

    def cid_to_carta(self, cid):
        return self._gen_manager.cid_to_carta(cid)

    def fai_la_fola(self):
        self._gen_manager.fai_la_fola()

    def get_opposit_pos(self, pos):
        return self._gen_manager.get_opposit_pos(pos)

    def get_draw_stable(self):
        return self._delegate_draw_stable()
