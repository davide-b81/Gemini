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
from oggetti.posizioni import *
from oggetti.stringhe import _
from main.exception_man import ExceptionMan

class FsmGioco(metaclass=ABCMeta):
    '''
    classdocs
    '''
    _id_fsm = None
    _status = None
    _sub_status = None
    _status_next = None
    _sub_status_next = None
    _status_prev = None
    _cid_apertura = None
    _winner = None
    _globals = Globals()

    handlers = None
    _actions = None
    _act_giro = None
    startState = None
    _t_status = None
    _game_man = None
    _t_sub_status = None

    _delegate_append_html_text = None
    _delegate_show_popup = None
    _delegate_presa = None
    _delegate_update_turno = None
    _delegate_update_mazziere = None
    _delegate_update_caduto = None
    _delegate_update_fola = None
    _delegate_update_players = None

    STATUS_INIZIO = "INIZIO"
    STATUS_FINE = "STATUS_FINE"
    STATUS_GIOCO_BEGIN = "STATUS_GIOCO_BEGIN"
    STATUS_GIRO = "STATUS_GIRO"
    STATUS_MESCOLA = "STATUS_MESCOLA"
    STATUS_TAGLIA = "STATUS_TAGLIA"
    STATUS_DICHIARA = "STATUS_DICHIARA"
    STATUS_MODAL_POPUP = "STATUS_MODAL_POPUP"
    STATUS_RESUME = "STATUS_RESUME"


    def __init__(self, gamman=None):
        '''
        Constructor
        '''
        self.running = False
        self._id_fsm = str(self)
        self._globals = Globals()
        self.handlers = {}
        self._actions = {}
        self._act_giro = ActionGiro(self)
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

    def __str__(self):
        return type(self).__name__

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
            if player.get_position() == POSTAZIONE_SUD:
                return False
            else:
                return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start_game(self):
        check_locals(locals())
        try:
            self._t_status = monotonic()
            self._t_sub_status = monotonic()
            self.running = True
            self._act_giro.start()
            self._status = self.STATUS_INIZIO
            self._status_next = self._status
            self._winner = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end_game(self):
        self.running = False

    def man_end(self):
        pass

    ''' Pure virtual function '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def inizio(self):
        pass

    @abstractmethod
    def get_text_punti_mano(self):
        pass

    @abstractmethod
    def on_presa(self, winner):
        pass

    def echo_mazzo(self, deck, ppos):
        try:
            print(str(deck) + " contiene:")
            for c in self.get_list_ca(deck, ppos):
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
                player = self.get_next_player(self.get_mazziere(), antior)
            if player is None:
                raise Exception("Cannot set next player")
            self.set_player(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def wait_user(self):
        pass

    def fine(self):
        pass

    def get_finished(self):
        return self._status == FsmGioco.STATUS_FINE

    def calata(self, c, player=None):
        try:
            if player == None:
                player = self.get_player()
            if c == None:
                raise Exception("Carta non specificata")

            self._game_man.cala_in_tavola(player, c, self._globals.get_instant_pos())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def get_deck(self, deck, ppos=None):
        try:
            return self._game_man.get_deck(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_list_ca(self, deck, ppos=None):
        try:
            return self._game_man.get_list_ca(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti(self, c, player=None):
        try:
            if player == None:
                player = self.get_player()
            self._game_man.marca_punti_carta(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def segna_punti_da_fola(self, player, c):
        try:
            assert player is not None
            if c is not None:
                self._game_man.cala_in_tavola(player, c, self._globals.get_instant_pos())
                self._game_man.marca_punti_carta(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def consegna_carta(self, c, coperta=FRONTE_COPERTA, player=None):
        try:
            if player == None:
                player = self.get_player()
            #if coperta == False:
            #    echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve " + str(c) + " ."))
            #else:
            #    echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve " + str(c) + "."))
            self.sposta_e_stendi(c, None, DeckId.DECK_MANO, coperta, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def dai_al_giocatore(self, player, n, fronte=FRONTE_COPERTA, hoverable=False):
        try:
            assert player is not None

            ca = self._game_man.preleva_dal_mazzo(n)
            if ca is not None and len(ca) > 0:
                if len(ca) == 1:
                    if fronte == FRONTE_SCOPERTA:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve una carta scoperta"))
                    else:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve una carta"))
                else:
                    if fronte == FRONTE_SCOPERTA:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve ") + str(len(ca)) + " carte scoperte")
                    else:
                        echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve ") + str(len(ca)) + " carte")

                for c in ca:
                    c.set_hoverable(hoverable)
                    self.inserisci_nel_mazzo(c, DeckId.DECK_MANO, fronte, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_action_status(self):
        try:
            if self._status in self._actions:
                return self._actions[self._status].get_status()
            elif self._status == self.STATUS_GIRO:
                return self._act_giro.get_status()
            return None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_action_new_status(self):
        try:
            if self._status in self._actions:
                return self._actions[self._status].get_new_status()
            return None
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
                        self._actions[self._status].start_partita()
                    elif self._act_giro.get_status() == self._act_giro.ACTSTATUS_PARTITA_3:
                        self._status = self.STATUS_MESCOLA
                        self._status_next = self.STATUS_MESCOLA
                        self._status_post = self.STATUS_MESCOLA
                        self._actions[self._status].start_partita()
                elif self.running:
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

    def raccogli_carte(self, winner, player, bonus=False):
        try:
            if bonus:
                return self._game_man.raccogli_carte_avversari(winner, player)
            else:
                return self._game_man.raccogli_carte_casa(winner, player)

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

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
            if player is None:
                player = self._game_man.get_player()
            self.scopri_carte(player)
            player.giocatore_cade()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
    Game manager wrappers
    '''
    def set_giocatori(self, giocatori):
        try:
            self._game_man.set_giocatori(giocatori)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_giocatori(self):
        try:
            return self._game_man.get_giocatori()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_mano(self, player):
        return self._game_man.get_carte_mano(player)

    @property
    def posizioni(self):
        return self._game_man.get_posizioni()

    def set_lato_mazzo(self, deck, coperta):
        try:
            for c in self.get_list_ca(deck):
                self._game_man.set_fronte(c, coperta, self._globals.get_instant_pos())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def capovolgi_mazzo(self):
        self._game_man.capovolgi_mazzo()

    def taglia_mazzo(self, cid):
        self._game_man.taglia_mazzo(cid)

    def ricomponi_taglio(self, player):
        self._game_man.ricomponi_taglio(player)

    def raddrizza_mazzo(self):
        self._game_man.raddrizza_mazzo()

    def get_prima(self, deck, player=None):
        return self._game_man.read_carta(0, deck, player)

    def get_ultima(self, deck, player=None):
        return self._game_man.read_carta(-1, deck, player)

    def read_carta(self, i, deck, player):
        return self._game_man.read_carta(i, deck, player)

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

    def change_deck(self, deck_src, ppos_src, deck_dst, ppos_dst):
        try:
            self._game_man.change_deck(deck_src, ppos_src, deck_dst, ppos_dst)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inserisci_nel_mazzo(self, c, deck=DeckId.DECK_MAZZO, fronte=FRONTE_COPERTA, ppos=None):
        try:
            self._game_man.inserisci_nel_mazzo(c, deck, fronte, ppos)
            self._game_man.show_deck_plain(deck, ppos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def pesca_dal_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None):
        return self._game_man.pesca_dal_mazzo(deck, ppos)

    def preleva_dal_mazzo(self, n):
        return self._game_man.preleva_dal_mazzo(n)

    def deck_contains(self, c, deck=DeckId.DECK_MAZZO, player=None):
        return self._game_man.deck_contains(c.get_id(), deck, player)

    def has_carta(self, player, cid):
        return self._game_man.has_carta(player, cid)

    def restore_manche(self):
        return self._game_man.restore_manche()

    def get_carte(self, deck, player=None):
        try:
            if player is None:
                player = self.get_player()
            return self._game_man.get_list_ca(deck, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_carte_rubate(self, player):
        try:
            if player is None:
                player = self.get_player()
            return self.get_carte(DeckId.DECK_RUBATE, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_merged(self, deck=DeckId.DECK_MAZZO):
        try:
            return self._game_man.get_deck_merged(deck)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_deck_len(self, deck=DeckId.DECK_MANO, player=None):
        try:
            if player is None:
                player = self.get_player()
            return self._game_man.get_deck_len(deck, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def deck_contains(self, deck, c, player=None):
        try:
            return self._game_man.deck_contains(c.get_id(), deck, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_carte_prese(self, player):
        return self._game_man.get_num_carte_prese(player)

    def restore_manche(self):
        return self._game_man.restore_manche()

    def player_has_carta(self, player, c):
        return self.deck_contains(DeckId.DECK_MANO, c, player) or\
               self.deck_contains(DeckId.DECK_RUBATE, c, player)

    def get_carta(self, cid):
        return self._game_man.cid_to_carta(cid)

    def get_carte_in_tavola(self):
        return self._game_man.get_all_tavola()

    def get_carte_in_tavola_pos(self, posizione):
        return self._game_man.get_carte_in_tavola_pos(posizione)

    def get_carte_in_tavola_player(self, player):
        return self._game_man.get_carte_in_tavola_pos(player.get_position())

    def get_mazziere(self):
        return self._game_man.get_mazziere()

    def set_mazziere(self, player):
        self._game_man.set_mazziere(player)

    def update_mazziere(self, player):
        try:
            self.set_mazziere(player)
            self._delegate_update_mazziere(player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mostra_mazzo(self, deck=DeckId.DECK_MAZZO, ppos=None, n=None):
        return self._game_man.show_deck_packed(deck, ppos, n)

    def set_deck_visible(self, deck=DeckId.DECK_MAZZO, ppos=None, enable=True):
        return self._game_man.set_deck_visible(deck, ppos, enable)

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

    def passa_fola(self, player, fronte=FRONTE_SCOPERTA):
        if not self.simulated():
            self.mostra_fola(player, fronte)
        else:
            self.mostra_fola(player, FRONTE_COPERTA)
        return self._game_man.passa_fola(player, fronte)

    def nascondi_fola(self, player):
        return self._game_man.nascondi_fola(player)

    def mostra_scarto(self, player):
        return self._game_man.mostra_scarto(player)

    def mostra_pozzo(self, player):
        return self._game_man.mostra_pozzo(player)

    def mostra_fola(self, player, fronte=FRONTE_SCOPERTA):
        try:
            return self._game_man.mostra_fola(player, fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    @abstractmethod
    def get_postazioni(self):
        pass

    def mescola_mazzo(self):
        return self._game_man.mescola_mazzo()

    def split_mazzo_n(self, n):
        return self._game_man.split_mazzo_n(n)

    def scarta(self, player, c):
        try:
            self._game_man.scarta(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scopri_carta(self, c):
        return self._game_man.scopri_carta(c)

    def scopri_carte(self, player):
        return self._game_man.scopri_carte(player)

    def attiva_carte(self, deck, player=None):
        try:
            self._game_man.set_deck_enabled(deck, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_deck_packed(self, deck=DeckId.DECK_MAZZO, fronte=FRONTE_SCOPERTA, player=None):
        try:
            assert fronte==FRONTE_SCOPERTA or fronte==FRONTE_COPERTA
            if player is None:
                player = self.get_player()
            self._game_man.show_deck_packed(deck, player.get_position(), fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_deck_plain(self, deck=DeckId.DECK_MAZZO, fronte=FRONTE_SCOPERTA, player=None):
        try:
            if player is None:
                player = self.get_player()
            self._game_man.show_deck_plain(deck, player.get_position(), fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_e_stendi(self, c, deck_src, deck_dst, fronte=FRONTE_SCOPERTA, player=None):
        try:
            self._game_man.sposta_carta(c, deck_src, deck_dst, player)
            self._game_man.set_fronte(c, fronte, self._globals.get_instant_pos())
            self._game_man.show_deck_plain(deck_dst, player.get_position(), fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_e_raccogli(self, c, deck_src, deck_dst, fronte=FRONTE_SCOPERTA, player=None):
        try:
            self._game_man.sposta_carta(c, deck_src, deck_dst, player)
            self._game_man.set_fronte(c, fronte, self._globals.get_instant_pos())
            self._game_man.show_deck_packed(deck_dst, player.get_position(), fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def sposta_e_nascondi(self, c, deck_src, deck_dst, fronte=FRONTE_SCOPERTA, player=None):
        try:
            self._game_man.sposta_carta(c, deck_src, deck_dst, player)
            self._game_man.set_fronte(c, fronte, self._globals.get_instant_pos())
            c.set_visible(False)
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

    def __dict__(self):
        try:
            return dict(
                _status=self._status,
                _sub_status=self._sub_status,
                _status_next=self._status_next,
                _sub_status_next=self._sub_status_next,
                _status_prev=self._status_prev,
                _cid_apertura=self._cid_apertura,
                _winner=self._winner)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reprJSON(self):
        try:
            return dict(
                _id_fsm=self.__class__.__name__,
                _status=self._status,
                _action_status=self.get_action_status(),
                _action_new_status=self.get_action_new_status(),
                _sub_status=self._sub_status,
                _status_next=self._status_next,
                _sub_status_next=self._sub_status_next,
                _status_prev=self._status_prev,
                _cid_apertura=self._cid_apertura,
                _mazziere=str(self.get_mazziere()),
                _winner=self._winner)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fromJSON(self, json_object):
        try:
            if '_id_fsm' in json_object.keys():
                print("De-Serialize Fsm")
                self._status = json_object['_status']
                self._sub_status = json_object['_sub_status']
                self._status_next = json_object['_status_next']
                self._sub_status_next = json_object['_sub_status_next']
                self._status_prev = json_object['_status_prev']
                self._cid_apertura = json_object['_cid_apertura']
                self._winner = json_object['_winner']
                if self._status is self._actions:
                    self._actions[self._status].set_status(json_object['_action_status'])
                    self._actions[self._status].set_new_status(json_object['_action_new_status'])
                elif self._status == self.STATUS_GIRO:
                    self._act_giro.set_status(json_object['_action_status'])
                    self._act_giro.set_new_status(json_object['_action_new_status'])
            else:
                return json_object
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)