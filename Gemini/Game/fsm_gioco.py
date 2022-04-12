'''
Created on 3 gen 2022

@author: david
'''
import pygame

from decks.carta_id import get_seme, seme_name
from game.action_giro import ActionGiro
from main.globals import *
from time import monotonic
from abc import ABCMeta, abstractmethod

from oggetti.posizioni import DeckId
from oggetti.stringhe import _
from main.exception_man import ExceptionMan

posizioni = ["Nord", "Est", "Sud", "Ovest"]


class FsmGioco(metaclass=ABCMeta):
    '''
    classdocs
    '''
    handlers = None
    _actions = None
    _act_giro = None
    startState = None
    _running = None
    _status = None
    _sub_status = None
    _status_next = None
    _sub_status_next = None
    _status_prev = None
    _t_status = None
    _game_man = None
    _winner = None
    _delegate_append_html_text = None
    _delegate_show_popup = None
    _delegate_presa = None
    _delegate_update_turno = None
    _delegate_update_mazziere = None
    _delegate_update_caduto = None
    _delegate_update_fola = None
    _delegate_update_players = None
    _t_sub_status = None
    _cid_apertura = None

    STATUS_INIZIO = "INIZIO"
    STATUS_FINE = "STATUS_FINE"
    STATUS_GIOCO_BEGIN = "STATUS_GIOCO_BEGIN"
    STATUS_GIRO = "STATUS_GIRO"
    STATUS_MESCOLA = "STATUS_MESCOLA"
    STATUS_TAGLIA = "STATUS_TAGLIA"
    STATUS_DICHIARA = "STATUS_DICHIARA"
    STATUS_MODAL_POPUP = "STATUS_MODAL_POPUP"
    STATUS_RESUME = "STATUS_RESUME"

    def __init__(self, gamman=None, genman=None):
        '''
        Constructor
        '''
        self._globals = Globals()
        self.handlers = {}
        self._actions = {}
        self._act_giro = ActionGiro(self)
        self._running = False
        self._t_status = monotonic()
        self._t_sub_status = monotonic()
        self._game_man = gamman
        self.add_state(self.STATUS_INIZIO, self.inizio)
        self.add_state(self.STATUS_FINE, self.fine)
        self.add_state(self.STATUS_MODAL_POPUP, self.wait_user)
        self._status = self.STATUS_INIZIO
        self._sub_status = None
        self._sub_status_post = None
        self._status_next = self._status
        self._status_post = self._status
        self._winner = None
        self._status_prev = self.STATUS_INIZIO

    def set_delegate_presa(self, f):
        self._delegate_presa = f

    def set_delegate_show_popup(self, foo):
        self._delegate_show_popup = foo

    def set_delegate_append_html_text(self, foo):
        self._delegate_append_html_text = foo

    def set_delegate_update_turno(self, foo):
        self._delegate_update_turno = foo

    def set_delegate_update_mazziere(self, foo):
        self._delegate_update_mazziere = foo

    def set_delegate_update_caduto(self, foo):
        self._delegate_update_caduto = foo

    def set_delegate_update_fola(self, foo):
        self._delegate_update_fola = foo

    def set_delegate_update_players(self, foo):
        self._delegate_update_players = foo

    def add_action(self, name, action):
        self._actions[name] = action

    def add_state(self, name, handler):
        self.handlers[name] = handler

    def simulated(self, player=None):
        try:
            if self._globals.get_demo_mode():
                return True
            if player is None:
                player = self.get_player()
            if player.get_position() == "Sud":
                return False
            else:
                return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_running(self):
        return self._running

    def start_game(self):
        check_locals(locals())
        try:
            self._t_status = monotonic()
            self._t_sub_status = monotonic()
            self._running = True
            self._act_giro.start()
            self._status = self.STATUS_INIZIO
            self._status_next = self._status
            self._winner = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end_game(self):
        self._running = False

    def man_end(self):
        pass

    ''' Pure virtual function '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def inizio(self):
        pass

    def echo_mazzo(self, deck):
        try:
            print(str(deck) + " contiene:")
            for c in self.get_deck(deck):
                print(" - " + str(c))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuzione(self, n, coperta=True):
        check_locals(locals())
        try:
            for i in range(0, len(self._game_man.get_giocatori())):
                sim = self.simulated()
                if not sim or not coperta:
                    self.dai_al_giocatore(self._game_man.get_player(), n, FRONTE_SCOPERTA, not sim)
                else:
                    self.dai_al_giocatore(self._game_man.get_player(), n, FRONTE_COPERTA)
                self.update_next_player()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_mazziere(self, player):
        try:
            self._game_man.set_mazziere(player)
            self._delegate_update_mazziere(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_player(self):
        try:
            return self._game_man.get_player()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_player(self, player):
        try:
            assert player is not None
            self._game_man.set_player(player)
            self._delegate_update_turno(player)
            return player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_next_player(self, player, antior=True):
        try:
            return self._game_man.get_next_player(player, antior)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_next_player(self, antior=True):
        try:
            player = self.get_next_player(self.get_player(), antior)
            if player is None:
                raise Exception("Cannot set next player")
            else:
                print("Next player " + str(player))
            self.set_player(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def wait_user(self):
        pass

    def fine(self):
        pass

    def get_finished(self):
        return self._status == FsmGioco.STATUS_FINE

    def get_winner(self):
        return self._winner

    def get_action_status(self):
        return self._actions[self._status].get_status()

    def calata(self, c, player=None):
        try:
            if player == None:
                player = self.get_player()
            if c == None:
                raise Exception("Carta non specificata")

            self._game_man.cala_in_tavola(player, c, self._globals.get_instant())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def get_deck(self, deck, ppos=None):
        try:
            return self._game_man.get_deck(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti(self, c, player=None):
        try:
            if player == None:
                player = self.get_player()
            self._game_man.marca_punti(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def segna_punti_da_fola(self, player, c):
        try:
            assert player is not None
            if c is not None:
                self._game_man.cala_in_tavola(player, c, self._globals.get_instant())
                self._game_man.marca_punti(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def consegna_carta(self, c, coperta=FRONTE_COPERTA, player=None):
        try:
            if player == None:
                player = self.get_player()
            if coperta == False:
                echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve " + str(c) + " ."))
            else:
                echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve " + str(c) + "."))
            self.move_card_and_repos(c, None, DeckId.DECK_MANO, coperta, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def dai_al_giocatore(self, player, n, coperta=True, hoverable=False):
        try:
            assert player is not None

            ca = self._game_man.preleva_dal_mazzo(n)
            if ca is not None and len(ca) > 0:
                if len(ca) == 1:
                    if coperta == False:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve una carta scoperta"))
                    else:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve una carta"))
                else:
                    if coperta == False:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve ") + str(len(ca)) + " carte scoperte")
                    else:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve ") + str(len(ca)) + " carte")
                self._game_man.add_mano_giocatore(player, ca, coperta, hoverable)
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_game(self):
        try:
            if self._game_man.get_draw_stable():
                if self._status == self.STATUS_GIRO:
                    self._act_giro.update()
                    if self._act_giro.get_status() == self._act_giro.ACTSTATUS_PARTITA_1:
                        self._status = self.STATUS_MESCOLA
                        self._status_next = self.STATUS_MESCOLA
                        self._status_post = self.STATUS_MESCOLA
                        self._actions[self._status].start()
                    elif self._act_giro.get_status() == self._act_giro.ACTSTATUS_PARTITA_2:
                        self._status = self.STATUS_MESCOLA
                        self._status_next = self.STATUS_MESCOLA
                        self._status_post = self.STATUS_MESCOLA
                        self._actions[self._status].start()
                    elif self._act_giro.get_status() == self._act_giro.ACTSTATUS_PARTITA_3:
                        self._status = self.STATUS_MESCOLA
                        self._status_next = self.STATUS_MESCOLA
                        self._status_post = self.STATUS_MESCOLA
                        self._actions[self._status].start()
                elif self._running:
                    handler = self.handlers[self._status]

                    if handler != None:
                        handler()

                        if self._status != self._status_next:
                            self._status_prev = self._status
                            self._status = self._status_next
                            self._status_post = self._status
                            self._t_status = monotonic()
                            echo_message("Stato: " + str(self._status))
                            if self._status in self._actions:
                                self._actions[self._status].start()
                        if self._sub_status_next != self._sub_status:
                            self._sub_status = self._sub_status_next
                            self._t_sub_status = monotonic()
                            echo_message("Sotto stato: " + str(self._sub_status))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def raccogli_carte_calate(self, winner, player):
        return self._game_man.raccogli_carte_calate(winner, player)

    def step_ready(self):
        try:
            if self._globals.get_quick():
                return True
            elif self._game_man.get_draw_stable():
                return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_popup(self, txt):
        try:
            echo_message(txt)
            self._delegate_show_popup(txt)
            self._status = self.STATUS_MODAL_POPUP
            self._status_next = self.STATUS_MODAL_POPUP
            self._sub_status = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_popup(self):
        try:
            self._delegate_show_popup("")
            echo_message("Stato: " + str(self._status))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_termina(self):
        try:
            for key, act in self._actions.items():
                act.termina()
            self._act_giro.termina()
            self._status = self.STATUS_FINE
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_cade(self, player):
        try:
            self.scopri_carte(player)
            player.giocatore_cade()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
    Game manager wrappers
    '''
    def set_giocatori(self, giocatori):
        self._game_man.set_giocatori(giocatori)

    def get_giocatori(self):
        return self._game_man.get_giocatori()

    def get_carte_mano(self, player):
        return self._game_man.get_carte_mano(player)

    def set_lato_mazzo(self, deck, coperta):
        try:
            for c in self.get_deck(deck):
                self._game_man.set_fronte(c, coperta, self._globals.get_instant())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self):
        self._game_man.capovolgi_mazzo()

    def taglia_mazzo(self, cid):
        self._game_man.taglia_mazzo(cid)

    def ricomponi_taglio(self, player):
        self._game_man.ricomponi_taglio(player)

    def mostra_in_tavola(self, c, pos, inst):
        self._game_man.mostra_in_tavola(c, pos, inst)

    def mostra_taglio(self, ppos=None):
        self._game_man.mostra_taglio(ppos)

    def raddrizza_mazzo(self):
        self._game_man.raddrizza_mazzo()

    def get_prima(self, deck, player=None):
        return self._game_man.read_carta(0, deck, player)

    def get_ultima(self, deck, player=None):
        return self._game_man.read_carta(-1, deck, player)

    def read_carta(self, i, deck, player):
        return self._game_man.read_carta(i, deck, player)

    def set_mazzo_ultima(self):
        self._delegate_set_mazzo_ultima(self._game_man.get_deck())

    def clear_carte_in_tavola(self, posizione):
        return self._game_man.clear_carte_in_tavola(posizione)

    def pop_prima(self, deck=DeckId.DECK_TAGLIO, ppos=None):
         return self._game_man.pop_prima(deck, ppos)

    def has_seme(self, player, seed):
        return self._game_man.has_seme(player, seed)

    def add_rubate_giocatore(self, player, c):
        return self._game_man.add_rubate_giocatore(player, c)

    """ FOLA """
    def piglia_da_fola(self, player):
        return self._game_man.piglia_da_fola(player)

    def append_fola(self, c):
        return self._game_man.append_fola(c)

    def fai_la_fola(self):
        self._game_man.fai_la_fola()

    def inserisci_nel_mazzo(self, c, deck=DeckId.DECK_MAZZO, ppos=None):
        try:
            self._game_man.inserisci_nel_mazzo(c, deck, ppos)
            self.update_deck_display(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pesca_dal_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None):
        return self._game_man.pesca_dal_mazzo(deck, ppos)

    def preleva_dal_mazzo(self, n):
        return self._game_man.preleva_dal_mazzo(n)

    def deck_contains(self, cid, deck=DeckId.DECK_MAZZO, player=None):
        return self._game_man.deck_contains(cid, deck, player)

    def has_carta(self, player, cid):
        return self._game_man.has_carta(player, cid)

    def restore_manche(self):
        return self._game_man.restore_manche()

    def get_carte_rubate(self, player):
        return self._game_man.get_carte_rubate(player)

    def get_num_carte_mano(self, player):
        return self._game_man.get_num_carte_mano(player)

    def get_num_carte_prese(self, player):
        return self._game_man.get_num_carte_prese(player)

    def restore_manche(self):
        return self._game_man.restore_manche()

    def get_giocatori(self):
        return self._game_man.get_giocatori()

    def player_has_carta(self, player, cid):
        return self._game_man.has_carta(player, cid)

    def get_carta(self, cid):
        return self._game_man.cid_to_carta(cid)

    def get_carte_in_tavola(self):
        return self._game_man.get_carte_in_tavola()

    def get_carte_in_tavola_pos(self, posizione):
        return self._game_man.get_carte_in_tavola_pos(posizione)

    def get_carte_in_tavola_player(self, player):
        return self._game_man.get_carte_in_tavola_pos(player.get_position())

    def get_mazziere(self):
        return self._game_man.get_mazziere()

    def mostra_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None, n=None):
        return self._game_man.mostra_mazzo(deck, ppos, n)

    def get_position_turno(self, ppos=None, deck=DeckId.DECK_MAZZO):
        return self._game_man.get_position_turno(ppos, deck)

    def get_player_at_pos(self, pos):
        return self._game_man.get_player_at_pos(pos)

    def mostra_rubate(self, pos=None):
        return self._game_man.mostra_rubate(pos)

    def on_show_popup(self, txt):
        return self._game_man.on_show_popup(txt)

    def on_hide_popup(self):
        return self._game_man.on_hide_popup()

    def get_position_turno(self):
        return self._game_man.get_position_turno()

    def passa_fola(self, player):
        return self._game_man.passa_fola(player)

    def nascondi_fola(self, player):
        return self._game_man.nascondi_fola(player)

    def mostra_scarto(self, player):
        return self._game_man.mostra_scarto(player)

    def mostra_fola(self, player):
        return self._game_man.mostra_fola(player)

    def set_postazioni(self, ppos):
        self._game_man.set_postazioni(ppos)

    def get_postazioni(self):
        return self._game_man.get_postazioni()

    def mescola_mazzo(self):
        return self._game_man.mescola_mazzo()

    def split_mazzo_n(self, n):
        return self._game_man.split_mazzo_n(n)

    def scarta(self, player, c):
        try:
            self._game_man.scarta(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri_carte(self, player):
        return self._game_man.scopri_carte(player)

    def update_deck_display(self, deck_dst, ppos=None):
        try:
            self._game_man.stendi_deck(deck_dst, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def move_card_and_repos(self, c, deck_src, deck_dst, fronte=FRONTE_SCOPERTA, player=None):
        try:
            self._game_man.sposta_carta(c, deck_src, deck_dst, player)
            self._game_man.set_fronte(c, fronte, self._globals.get_instant())
            self.update_deck_display(deck_dst, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_carta(self, c, deck_src, deck_dst, player=None):
        try:
            self._game_man.sposta_carta(c, deck_src, deck_dst, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, evt):
        try:
            if self._status in self._actions:
                self._actions[self._status].on_event(evt)
            self._act_giro.on_event(evt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
