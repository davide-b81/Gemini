'''
Created on 3 gen 2022

@author: david
'''
from time import monotonic
from abc import ABCMeta, abstractmethod
from oggetti.stringhe import _

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
    winner = None
    giocatore_turno = None

    STATUS_INIZIO = "Inizio"
    STATUS_FINE = "Fine"
    STATUS_DISTRIBUZIONE1 = "Distribuzione1"
    STATUS_DISTRIBUZIONE2 = "Distribuzione2"
    STATUS_MESCOLA = "Mescola"
    STATUS_TAGLIA = "Taglia"

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
        self.winner = None
    
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

    def fine(self):
        self.game_man.res
        pass

    def get_finished(self):
        return self.t_status == FsmGioco.STATUS_FINE

    def get_winner(self):
        return self.winner
    
    def update_game(self):

        if self.running:
            handler = self.handlers[self.status]
            
            try:
                if self.running:
                    handler()
                    if self.status != self.new_status.upper():
                        self.status = self.new_status.upper()
                        self.new_status = self.status
                        self.t_status = monotonic()
                        handler = self.handlers[self.status]
                        print("update_game set status: " + str(self.status))

            except Exception as e:
                print("FsmGioco.update_game: An error occurred:", e.args[0])  

            