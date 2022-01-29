'''
Created on 3 gen 2022

@author: david
'''
from time import monotonic
from abc import ABCMeta, abstractmethod
from oggetti.stringhe import _
from main.globals import *
from main.exception_man import ExceptionMan

class FsmGioco(metaclass=ABCMeta):
    '''
    classdocs
    '''
    handlers = None
    startState = None
    running = None
    txt = ""
    status = None
    new_status = None
    t_status = None
    general_man = None
    game_man = None
    _winner = None
    giocatore_turno = None
    delay = 0.3

    STATUS_INIZIO = "INIZIO"
    STATUS_FINE = "FINE"
    STATUS_GIOCO_BEGIN = "GIOCOBEGIN"
    STATUS_DISTRIBUZIONE1 = "DISTRIBUZIONE1"
    STATUS_DISTRIBUZIONE2 = "DISTRIBUZIONE2"
    STATUS_MESCOLA = "MESCOLA"
    STATUS_TAGLIA = "TAGLIA"
    STATUS_DICHIARA = "DICHIARAZIONE"

    def __init__(self, gamman = None, genman = None):
        '''
        Constructor
        '''
        self.handlers = {}
        self.running = False
        self.t_status = monotonic()
        self.general_man = genman
        self.game_man = gamman
        self.add_state(self.STATUS_INIZIO, self.inizio)
        self.add_state(self.STATUS_FINE, self.fine)
        self.status = self.STATUS_INIZIO.upper()
        self.new_status = self.status
        self._winner = None
    
    def add_state(self, name, handler):
        name = name.upper()
        self.handlers[name] = handler

    def set_start_player(self, player):
        self.giocatore_turno = player
            
    def is_running(self):
        return self.running
    
    def start_game(self):
        self.t_status = monotonic()
        self.running = True
        self.status = self.STATUS_INIZIO.upper()
        self.new_status = self.status
        self.winner = None
        self.txt = _("Start")

    def end_game(self):
        self.running = False
    
    def man_end(self):
        pass
    
    def get_text(self):
        return self.txt
    
    ''' Pure virtual function '''
    __metaclass__=ABCMeta
    @abstractmethod
    def inizio(self):
        pass

    def distribuzione(self, n, fronte=True):
        check_locals(locals())
        try:
            if self.giocatore_turno == None:
                raise Exception("Giocatore non specificato")
            self.dai_al_giocatore(self.giocatore_turno, n, fronte or self.giocatore_turno.get_position() == "Sud")
            self.giocatore_turno = self.game_man.get_next_player(self.giocatore_turno, True)
            self.dai_al_giocatore(self.giocatore_turno, n, fronte or self.giocatore_turno.get_position() == "Sud")
            self.giocatore_turno = self.game_man.get_next_player(self.giocatore_turno, True)
            self.dai_al_giocatore(self.giocatore_turno, n, fronte or self.giocatore_turno.get_position() == "Sud")
            self.giocatore_turno = self.game_man.get_next_player(self.giocatore_turno, True)
            self.dai_al_giocatore(self.giocatore_turno, n, fronte or self.giocatore_turno.get_position() == "Sud")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def fine(self):
        pass


    def get_finished(self):
        return self.t_status == FsmGioco.STATUS_FINE


    def get_winner(self):
        return self.winner


    def calata(self, player, c):
        try:
            if player == None:
                raise Exception("Giocatore non specificato")
            if c == None:
                raise Exception("Carta non specificata")

            player.cala_carta(c)
            c = self.game_man.cala_in_tavola(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return c

    def dai_al_giocatore(self, player, n, fronte = True):
        try:
            assert self.general_man is not None
            assert player is not None
            ca = self.general_man.preleva_dal_mazzo(n)
            if ca is not None and len(ca) > 0:
                echo_message(str(player) + " (" + player.get_position() + ")" + _(" riceve ") + str(len(ca)) + " carte:")
                #pm = self.game_man.get_position_manager()
                for c in ca:
                    player.assegna_carta(c, fronte)
                    self.game_man.gira_carta(c, fronte)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_delegate_incamera(self, foo):
        self._delegate_incamera = foo

    def update_game(self):
        try:
            if self.running:
                handler = self.handlers[self.status]

                if handler != None:
                    try:
                        handler()
                    except Exception as e:
                        ExceptionMan.manage_exception("", e, True)
                    if self.status != self.new_status.upper():
                        self.status = self.new_status.upper()
                        self.new_status = self.status
                        self.t_status = monotonic()
                        handler = self.handlers[self.status]
                        echo_message("Stato: " + str(self.status))

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

            