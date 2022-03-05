'''
Created on 3 gen 2022

@author: david
'''
from main.globals import *
from time import monotonic
from abc import ABCMeta, abstractmethod
from oggetti.stringhe import _
from main.exception_man import ExceptionMan



class FsmGioco(metaclass=ABCMeta):
    '''
    classdocs
    '''
    handlers = None
    _actions = None
    startState = None
    _running = None
    _status = None
    _sub_status = None
    _status_next = None
    _sub_status_next = None
    _status_prev = None
    _t_status = None
    general_man = None
    game_man = None
    _winner = None
    _player = None
    _delegate_append_html_text = None
    _delegate_show_popup = None
    _delegate_presa = None
    _delegate_update_turno = None
    _delegate_update_mazziere = None
    _delegate_update_caduto = None
    _delegate_update_fola = None
    _t_sub_status = None

    STATUS_INIZIO = "INIZIO"
    STATUS_FINE = "STATUS_FINE"
    STATUS_GIOCO_BEGIN = "STATUS_GIOCO_BEGIN"
    STATUS_SORTEGGIA = "STATUS_SORTEGGIA"
    STATUS_MESCOLA = "STATUS_MESCOLA"
    STATUS_TAGLIA = "STATUS_TAGLIA"
    STATUS_DICHIARA = "STATUS_DICHIARA"
    STATUS_MODAL_POPUP = "STATUS_MODAL_POPUP"

    def __init__(self, gamman=None, genman=None):
        '''
        Constructor
        '''
        self._globals = Globals()
        self.handlers = {}
        self._actions = {}
        self._running = False
        self._t_status = monotonic()
        self._t_sub_status = monotonic()
        self.general_man = genman
        self.game_man = gamman
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

    def add_action(self, name, action):
        self._actions[name] = action

    def add_state(self, name, handler):
        self.handlers[name] = handler

    def set_start_player(self, player):
        self._player = player

    def simulated(self, player):
        try:
            if player is not None:
                if player.get_position() != "Sud":
                    return True
            return False
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
            print("Impossibile elecnare carte")

    def distribuzione(self, n, coperta=True):
        check_locals(locals())
        try:
            if self._player == None:
                raise Exception("Giocatore non specificato")
            self.dai_al_giocatore(self._player, n, coperta)
            self.update_next_player(self._player, True)
            self.dai_al_giocatore(self._player, n, coperta)
            self.update_next_player(self._player, True)
            self.dai_al_giocatore(self._player, n, coperta)
            self.update_next_player(self._player, True)
            self.dai_al_giocatore(self._player, n, coperta)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_mazziere(self, player):
        try:
            self.game_man.set_mazziere(player)
            self.set_delegate_update_mazziere(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_player(self, player):
        try:
            self._player = player
            self._delegate_update_turno(player)
            return player
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_next_player(self, player, antior=True):
        try:
            player = self.game_man.get_next_player(player, antior)
            return self.set_player(player)
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

    def calata(self, player, c):
        try:
            if player == None:
                raise Exception("Giocatore non specificato")
            if c == None:
                raise Exception("Carta non specificata")

            self.game_man.cala_in_tavola(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def get_deck(self, deck):
        try:
            return self.general_man.get_deck(deck)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fai_la_fola(self):
        try:
            self.general_man.fai_la_fola()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def piglia_da_fola(self, player):
        try:
            return self.general_man.piglia_da_fola(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def segna_punti_da_fola(self, player, c):
        try:
            assert self.general_man is not None
            assert player is not None
            if c is not None:
                self.game_man.cala_in_tavola(player, c)
                self.game_man.marca_punti(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def dai_al_giocatore(self, player, n, coperta=True):
        try:
            assert self.general_man is not None
            assert player is not None
            sim = self.simulated(self._player)
            ca = self.general_man.preleva_dal_mazzo(n)
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
                self.game_man.add_mano_giocatore(player, ca, coperta and sim)
            return ca
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_game(self):
        try:
            if self.game_man.get_draw_stable() and self._running:
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

    def step_ready(self):
        try:
            if self.game_man.get_draw_stable():
                return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_popup(self, txt, next_status):
        try:
            echo_message(txt)
            if self._globals.get_debug():
                self._status_next = next_status
            else:
                self._delegate_show_popup(txt)
                self._status_post = next_status
                self._status = self.STATUS_MODAL_POPUP
                self._status_next = self.STATUS_MODAL_POPUP
                self._sub_status = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_popup(self):
        try:
            self._delegate_show_popup(False, "")
            self._status = self._status_post
            self._sub_status_next = self._sub_status_post
            echo_message("Stato: " + str(self._status))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_termina(self):
        self._status = self.STATUS_FINE