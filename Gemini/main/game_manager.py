'''
Created on 4 gen 2022

@author: david
'''
from copy import copy
from time import monotonic

from decks.carta_id import CartaId
from game.germini.punteggi import carte_conto
from game.player import Player
from main.general_manager import GeneralManager
from main.globals import *
from game.germini.strategia import Strategia
from game.germini.fsm_germini import FsmGermini
from oggetti.posizioni import *
from oggetti.stringhe import _
from main.exception_man import ExceptionMan


class GiocoManager(object):
    '''
    classdocs
    '''
    _globals = None
    #
    _game = None
    _fsmc = None
    _fsmger = None
    _gen_manager = None
    _pos_man = None
    _draw_stable = None
    _posizioni = None
    # Gestione carta
    _delegate_show_carta = None
    _delegate_hide_carta = None
    _delegate_set_fronte = None
    # Gestione mazzi
    _delegate_is_coperta = None
    _delegate_mescola = None

    _delegate_set_z = None
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
    _delegate_get_sprite = None
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

    def set_delegate_get_sprite(self, f):
        try:
            self._delegate_get_sprite = f
            self._gen_manager.set_delegate_get_sprite(self._delegate_get_sprite)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_show_pozzo(self, f):
        self._delegate_show_pozzo = f

    def set_delegate_hide_pozzo(self, f):
        self._delegate_hide_pozzo = f

    def set_delegate_show_presa(self, f):
        self._delegate_show_presa = f

    def set_delegate_hide_presa(self, f):
        self._delegate_hide_presa = f

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

    def set_delegate_set_z(self, f):
        self._delegate_set_z = f

    def set_delegate_set_hoverable(self, f):
        self._delegate_set_hoverable = f

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
            if c is None:
                return
            elif c.get_id() in carte_conto:
                pts = carte_conto[c.get_id()]
                if pts > 0:
                    player.segna_punti(pts)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti_matto(self, player, c):
        """ (). Il Matto non può quindi essere perso tranne nell'improbabile caso che la coppia che lo possiede
        non effettui neppure una presa ovvero si dimentichi di giocarlo prima dell'ultima mano.
        Gli avversari segnaranno 5 punti immediati più altri 5 per la morte del Matto.
        """
        try:
            pts = carte_conto[c.get_id()]
            echo_message("Punti extra:")
            player.segna_punti(pts)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raccogli_carte_casa(self, winner, player):
        try:
            ca = self._gen_manager.get_carte_in_tavola_pos(player.get_position())
            for c in ca:
                if c.get_id() != CartaId.MATTO_0:
                    self._gen_manager.remove_tavola(winner, c)
                elif not self._gen_manager.is_ultima_mano():
                    self._gen_manager.remove_tavola(player, c)
                else:
                    p2 = self.get_next_player(player)
                    self._gen_manager.remove_tavola(p2, c)
                self.nascondi_carta(c)
            self._delegete_on_presa(winner, ca)
            self.on_redraw()
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raccogli_carte_avversari(self, winner, player):
        try:
            ca = self._gen_manager.get_carte_in_tavola_pos(player.get_position())
            for c in ca:
                if c.get_id() != CartaId.MATTO_0:
                    self.marca_punti_carta(winner, c)
                    self._gen_manager.remove_tavola(winner, c)
                elif not self._gen_manager.is_ultima_mano():
                    self.marca_punti_carta(player, c)
                    self._gen_manager.remove_tavola(player, c)
                else:
                    p2 = self.get_next_player(player)
                    self.marca_punti_matto(p2, c)
                    self._gen_manager.remove_tavola(p2, c)
                self.nascondi_carta(c)
            self._delegete_on_presa(winner, ca)
            self.on_redraw()
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_punti_mano(self):
        try:
            if self._game != None and self._game == self._fsmger:
                return self._fsmger.get_text_punti_mano()
            return ""
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_punti_totale(self):
        try:
            if self._game != None and self._game == self._fsmger:
                return self._fsmger.get_text_resti()
            return ""
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_presa(self, player, c_list):
        try:
            if self._game != None:
                self._game.on_presa(player, c_list)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gestisci_matto(self, cc):
        try:
            c_list = self.start_game().get_all_tavola()
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
            if self._game:
                self._game.on_popup()
                self._fsmger.on_popup()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_click(self, cid):
        try:
            if cid is not None:
                print("Click su " + str(cid))
                if cid == "POPUP":
                    self._game.on_popup()
                elif self._game != None and self._game == self._fsmger:
                    self.on_carta_click(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if cid is not None:
                if self._game != None and self._game == self._fsmger:
                    self._fsmger.on_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def dump_gioco(self, file):
        try:
            json.dump(self.reprJSON(), file, cls=ComplexEncoder, indent=4)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_gioco(self, gioco):
        try:
            if self._fsmc.__class__.__name__ == gioco:
                self._game = self._fsmc
                self._fsmc.reset()
                echo_message(_("Who get greatest card will be the Dealer"))
            elif self._fsmger.__class__.__name__ == gioco:
                echo_message(_("Germini"))
                self._game = self._fsmger
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
            self._gen_manager.restore_decks()
            self._gen_manager.termina_gioco()
            self.reset_giocatori()
            Strategia.reset()
            if self._game is not None:
                self._game.on_termina()
                self._game = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_mazzo(self):
        try:
            if self._delegate_restore_mazzo is not None:
                self._delegate_restore_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola_mazzo(self):
        try:
            self._gen_manager.mescola_mazzo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizia_gioco(self, giocatori, gioco):
        try:
            print("INIZIA")
            self.set_gioco(gioco)
            self.reset_tavola()
            self.reset_mazzo()
            self._game.winner = None
            self.set_giocatori(giocatori)
            self.set_postazioni(self._game.get_postazioni())
            self._gen_manager.start()
            self._gen_manager.mescola_mazzo()
            self._game.start_game()
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
            if self._game is not None:
                self._game.winner = None
                self._game.on_termina()
            self._gen_manager.termina_gioco()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_gioco(self, screen):
        try:
            if self._delegate_draw_stable():
                if self._game != None:

                    if self._game == self._fsmc:
                        if self._game.get_finished():
                            if self._game.winner is not None:
                                self._gen_manager.set_mazziere(self._game.winner)
                                self._gen_manager.set_player(self._game.winner)
                                echo_message(_("Il mazziere sara' " + str(self._game.winner)))
                                self._game = self._fsmger
                                # I giocatori sono gli stessi
                                players = copy(self._gen_manager._giocatori)
                                self.inizia_gioco(players, "FsmGermini")
                        else:
                            self._game.update_game()
                    elif self._game == self._fsmger:
                        self._game.update_game()
                Strategia.update_mano()

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_running(self):
        try:
            if self._game is not None:
                return self._game.is_running()
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

            # pp = self._gen_manager.get_giocatori()
            # if pp[0].get_position() is not None:
            #    print(str(pp[0]) + " - " + pp[0].get_position())
            # if pp[1].get_position() is not None:
            #    print(str(pp[1]) + " - " + pp[1].get_position())
            # if pp[2].get_position() is not None:
            #    print(str(pp[2]) + " - " + pp[2].get_position())
            # if pp[3].get_position() is not None:
            #    print(str(pp[3]) + " - " + pp[3].get_position())

            assert self._posizioni is not None
            assert len(self._posizioni) > 0
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
                n = len(self.get_list_ca(DeckId.DECK_MANO, player.get_position()))
                echo_message(
                    "Turno di " + str(player) + " (" + player.get_position() + ") - " + str(n) + " carte in mano.")
            else:
                raise Exception("No player at pos " + str(pos))
            return player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def passa_fola(self, player, fronte):
        try:
            self.copri_fola(player.get_position())
            self.show_deck_packed(DeckId.DECK_FOLA, player.get_position(), fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def carte_calate(self, posizione):
        try:
            return self._gen_manager.get_carte_in_tavola(posizione)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_mazzo(self):
        try:
            self._gen_manager.restore_decks()
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

    def set_deck_visible(self, deck, ppos, enable=True):
        try:
            self._gen_manager.set_deck_visible(deck, ppos, enable)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_carta(self, c):
        try:
            c.set_visible(True)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def nascondi_carta(self, c):
        try:
            c.set_visible(False)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_fronte(self, c, coperta, inst):
        try:
            c.set_coperta(coperta, inst)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def is_coperta(self, c):
        try:
            self._delegate_is_coperta(c)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_hoverable(self, c, h):
        try:
            print("Set hoverable " + str(c) + " " + str(h))
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
            self.show_deck_plain(DeckId.DECK_TAGLIO, ppos)

            # mazzo = self._gen_manager.get_taglio()
            # i = 0
            # print("Mostra taglio call " + ppos)
            # if not self._globals.get_uncover():
            #    mazzo.reverse()
            # (x, y) = self._pos_man.get_pos_deck(DeckId.DECK_TAGLIO, ppos)
            # for c in mazzo:
            #    pos = (int(x + (i / 2)), int(y + (i / 2)))
            #    self.posiziona_carta(c, pos, ppos, i, FRONTE_SCOPERTA, True)
            #    i = i + 1
            # self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def set_deck_enabled(self, deck, ppos):
        try:
            mazzo = self._gen_manager.get_list_ca(deck, ppos)
            if mazzo != None:
                for c in mazzo:
                    c.set_hoverable()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def show_deck_plain(self, deck, ppos, fronte=None):
        """
        Carte stese
        """
        try:
            #print("Stendi mazzo " + str(deck) + " (" + ppos + ")")
            ca = self._gen_manager.get_list_ca(deck, ppos)
            n = len(ca)
            if ca != None and n > 0:
                for c in ca:
                    pos = self._pos_man.get_pos_stesa(deck, ppos, n, len(ca))
                    self.posiziona_carta(c, pos, ppos, len(ca) - n + 1, fronte, True)
                    n = n - 1
                self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def show_deck_packed(self, deck, ppos, fronte=None, n=None):
        """
        Carte raccolte in un mazzo
        """
        try:
            i = 0
            hoverable = False
            ca = self._gen_manager.get_list_ca(deck)
            if ca is not None:
                if n is None:
                    n = len(ca)
                for c in ca:
                    if not self._globals.get_uncover():
                        index = i
                    else:
                        index = n - i
                    (x, y) = self._pos_man.get_pos_deck(deck, ppos)
                    pos = (int(x + (index / 2)), int(y + (index / 2)))
                    self.posiziona_carta(c, pos, ppos, index + 1, fronte, True)

                    self._delegate_set_hoverable(c, hoverable)

                    i = i + 1
                    if i >= n:
                        break
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
                    pos = self._pos_man.get_pos_stesa(DeckId.DECK_RUBATE, ppos, len(ca) - z, len(ca))
                    z = z + 1
                    self.posiziona_carta(c, pos, ppos, z, FRONTE_SCOPERTA, True)
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
                src = self._gen_manager.get_list_ca(src_deck, ppos)
                src.remove(c)
                dst = self._gen_manager.get_list_ca(dst_deck, ppos)
                if dst is not None:
                    dst.append(c)
            else:
                # Es. Carta già estratta
                self.on_redraw()
        except Exception as e:
            print(str(c))
            ExceptionMan.manage_exception(str(c) + " not found in " + str(src_deck), e, True)

    def mostra_pozzo(self):
        try:
            pass#self.show_deck_packed(None, DeckId.DECK_POZZO)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_scarto(self, player):
        try:
            self.show_deck_plain(DeckId.DECK_POZZO, player.get_position(), FRONTE_SCOPERTA)
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def mostra_fola(self, player, fronte=FRONTE_SCOPERTA):
        try:
            self.show_deck_plain(DeckId.DECK_FOLA, player.get_position(), fronte)
            if fronte == FRONTE_SCOPERTA:
                self.set_deck_enabled(DeckId.DECK_FOLA, player.get_position())
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
            ca = self._gen_manager.get_list_ca(DeckId.DECK_FOLA)
            i = 0
            for c in ca:
                c.set_coperta(FRONTE_COPERTA)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def nascondi_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            ca = self._gen_manager.get_list_ca(deck, ppos)
            for c in ca:
                self._delegate_hide_carta(c)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception(".", e, True)

    def scarta(self, player, c):
        ca = []
        try:
            c.set_coperta(FRONTE_COPERTA, self._globals.get_instant())
            self._gen_manager.scarta(c, player)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return ca

    def mostra_in_tavola(self, c, ppos, inst):
        try:
            pos = self._pos_man.get_area_tavola(ppos)
            # Metto SUD in modo che le carte siano diritte
            self.posiziona_carta(c, pos, POSTAZIONE_SUD, 0, FRONTE_SCOPERTA, True)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cala_in_tavola(self, player, c, inst):
        try:
            self._gen_manager.sposta_in_tavola(c, player.get_position())
            self.mostra_in_tavola(c, player.get_position(), inst)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def rimuove_da_tavola(self, ca):
        try:
            if ca is not None:
                for c in ca:
                    # self._delegate_hide_carta(c)
                    c.set_visible(False)
                    self._gen_manager.rimuove_carta_in_tavola(c)
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
            if self._game is not None:
                self._game.on_event(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri_carta(self, c):
        try:
            self.set_fronte(c, FRONTE_SCOPERTA, self._globals.get_instant_flip())
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri_carte(self, player):
        try:
            ca = self._gen_manager.get_carte_mano(player)
            for c in ca:
                self.set_fronte(c, FRONTE_SCOPERTA, self._globals.get_instant_flip())
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_sort(self):
        try:
            self._gen_manager.sort_mazzo_z(DeckId.DECK_MANO, POSTAZIONE_SUD)
            self.show_deck_plain(DeckId.DECK_MANO,POSTAZIONE_SUD)
            self._gen_manager.sort_mazzo_z(DeckId.DECK_FOLA)
            self.on_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_redraw(self):
        try:
            if self._delegate_redraw is not None:
                self._delegate_redraw()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_len(self, deck=DeckId.DECK_MANO, player=None):
        try:
            mazzo = self._gen_manager.get_list_ca(deck, player.get_position())
            return len(mazzo)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_prese(self, player):
        try:
            return len(self._gen_manager.get_carte_prese(player))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

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
        try:
            self.set_posizioni(ppos)
            self._gen_manager.set_postazioni(ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_postazioni(self):
        try:
            return self.get_posizioni()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_giocatori(self, giocatori):
        try:
            self._gen_manager.set_giocatori(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_giocatori(self):
        try:
            return self._gen_manager.get_giocatori()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_mano(self, player):
        try:
            return self._gen_manager.get_carte_mano(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_scoperte(self, deck, ppos):
        try:
            return self._gen_manager.get_scoperte(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def change_deck(self, deck_src, ppos_src, deck_dst, ppos_dst):
        try:
            self.merge_deck(deck_src, ppos_src, deck_dst, ppos_dst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def merge_deck(self, deck_src, ppos_src, deck_dst, ppos_dst):
        try:
            self._gen_manager.merge_deck(deck_src, ppos_src, deck_dst, ppos_dst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def taglia_mazzo(self, cid):
        try:
            self._gen_manager.taglia_mazzo(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ricomponi_taglio(self, player):
        try:
            assert player is not None
            self.capovolgi_mazzo(DeckId.DECK_TAGLIO, player.get_position(), FRONTE_COPERTA)
            self.merge_deck(DeckId.DECK_TAGLIO, player.get_position(), DeckId.DECK_MAZZO, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None, fronte=FRONTE_SCOPERTA):
        try:
            self._gen_manager.capovolgi_mazzo(deck, ppos, fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raddrizza_mazzo(self):
        try:
            self._gen_manager.capovolgi_mazzo(DeckId.DECK_MAZZO, None, FRONTE_COPERTA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def read_carta(self, i, deck, player):
        try:
            return self._gen_manager.read_carta(i, deck, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_all_tavola(self):
        try:
            return self._gen_manager.get_all_tavola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_in_tavola_pos(self, pos):
        try:
            return self._gen_manager.get_carte_in_tavola_pos(pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def clear_carte_in_tavola(self, posizione):
        try:
            return self._gen_manager.clear_carte_in_tavola(posizione)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_giocatori(self):
        try:
            self._gen_manager.restore_giocatori()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pop_prima(self, deck=DeckId.DECK_TAGLIO, ppos=None):
        try:
            return self._gen_manager.pop_carta(0, deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_seme(self, player, seed):
        try:
            return self._gen_manager.has_seme(player, seed)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_rubate_giocatore(self, player, c):
        try:
            return self._gen_manager.add_rubate_giocatore(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_merged(self, deck=DeckId.DECK_MAZZO):
        try:
            return self._gen_manager.get_deck_merged(deck)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_list_ca(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            return self._gen_manager.get_list_ca(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_pos(self, deck=DeckId.DECK_MAZZO):
        try:
            return self._gen_manager.get_deck_vect(deck)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck(self, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            return self._gen_manager.get_deck(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def piglia_da_fola(self, player):
        try:
            return self._gen_manager.piglia_da_fola(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def append_fola(self, c):
        try:
            return self._gen_manager.append_fola(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def preleva_dal_mazzo(self, n):
        try:
            return self._gen_manager.preleva_dal_mazzo(n)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inserisci_nel_mazzo(self, c, deck, fronte, ppos):
        try:
            c.set_coperta(fronte)
            self._gen_manager.inserisci_nel_mazzo(c, deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pesca_dal_mazzo(self, deck, ppos):
        try:
            return self._gen_manager.pesca_dal_mazzo(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_rubate(self, player):
        try:
            return self._gen_manager.get_carte_rubate(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def split_mazzo_n(self, n):
        try:
            return self._gen_manager.split_mazzo_n(n)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def deck_contains(self, cid, deck=DeckId.DECK_MAZZO, player=None):
        try:
            return self._gen_manager.deck_contains(cid, deck, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def has_carta(self, player, cid):
        try:
            return self._gen_manager.has_carta(player, cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def restore_manche(self):
        try:
            return self._gen_manager.restore_manche()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cid_to_carta(self, cid):
        try:
            return self._gen_manager.cid_to_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fai_la_fola(self):
        try:
            self._gen_manager.fai_la_fola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_opposit_pos(self, pos):
        try:
            return self._gen_manager.get_opposit_pos(pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_draw_stable(self):
        try:
            return self._delegate_draw_stable()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_resti(self):
        try:
            txt = "<p>Resti:<br/>"
            for p in self.get_giocatori():
                txt = txt + str(p) + ": " + str(p.get_resti()) + "<br/>"
            txt = txt + "</p>"
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def posiziona_carta(self, c, pos, ppos, z, fronte=None, visible=True):
        try:
            c.set_pos(pos, self._globals.get_instant_pos())
            c.set_deg_from_ppos(ppos, self._globals.get_instant_rot())
            if visible is not None:
                c.set_visible(visible)
                if z is not None and visible:
                    c.set_z(z)
            if fronte is not None:
                c.set_coperta(fronte, self._globals.get_instant_flip())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __dict__(self):
        return dict(
            _game=str(self._game),
            #_fsmc,
            #_fsmger,
            _gen_manager=self._gen_manager,
            #_pos_man = self._pos_man,
            #_pos_man = self._draw_stable,
            _posizioni=self._posizioni)

    def reprJSON(self):
        return self.__dict__()

if __name__ == '__main__':
    man = GiocoManager(Globals().get_positions())
    _players = []
    _players.append(Player("Davide", POSTAZIONE_SUD))
    _players.append(Player("Tizio", POSTAZIONE_EST))
    _players.append(Player("Caio", POSTAZIONE_NORD))
    man.inizia_gioco(_players, "FsmGermini")
    try:
        cc = json.dumps(man.reprJSON(), cls=ComplexEncoder)
        print(cc)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)