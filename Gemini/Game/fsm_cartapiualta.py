'''
Created on 4 gen 2022

@author: david
'''
from game.fsm_gioco import FsmGioco
from time import monotonic
from game.carta import get_greater
from main.exception_man import ExceptionMan

class FsmCartaPiuAlta(FsmGioco):

    '''
    classdocs
    '''
    def __init__(self, gamman = None, genman = None):
        '''
        Constructor
        '''
        super().__init__(gamman, genman)
        self.add_state("IoPesco", self.io_pesco)
        self.add_state("OvestPesca", self.ovest_pesca)
        self.add_state("NordPesca", self.nord_pesca)
        self.add_state("EstPesca", self.est_pesca)
        self.add_state("Risultato", self.risultato)
        self.txt = "Inizia"
    
    def update_game(self):
        try:
            super().update_game()        
        except Exception as e:
            print(type(self).__name__ + ".update_game: An error occurred:", e.args[0])
    
    def start_game(self):
        super().start_game()
     
    def inizio(self):      
        self.new_status = "IoPesco"
            
    def io_pesco(self):
        if self.t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Sud")
                c = self.general_man.pesca_dal_mazzo(g)
                c = self.game_man.cala_in_tavola(g, c)
                self.txt = "Sud ha pescato " + str(c)
            except Exception as e:
                print(type(self).__name__ + ".io_pesco: An error occurred:", e.args[0])            
            self.new_status = "OvestPesca"
        
    def ovest_pesca(self):                
        if self.t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Ovest")
                c = self.general_man.pesca_dal_mazzo(g)
                c = self.game_man.cala_in_tavola(g, c)
                self.txt = "Ovest ha pescato " + str(c)
            except Exception as e:
                print(type(self).__name__ + ".ovest_pesca: An error occurred:", e.args[0])
            self.new_status = "NordPesca"
    
    def nord_pesca(self):                
        if self.t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Nord")
                c = self.general_man.pesca_dal_mazzo(g)
                c = self.game_man.cala_in_tavola(g, c)
                self.txt = "Nord ha pescato " + str(c)
            except Exception as e:
                print(type(self).__name__ + ".nord_pesca: An error occurred:", e.args[0])
            self.new_status = "EstPesca"

    def est_pesca(self):                
        if self.t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Est")
                c = self.general_man.pesca_dal_mazzo(g)
                c = self.game_man.cala_in_tavola(g, c)
                self.txt = "Est ha pescato " + str(c)
            except Exception as e:
                print(type(self).__name__ + ".est_pesca: An error occurred:", e.args[0])
            self.new_status = "Risultato"

    def risultato(self):
        if self.t_status + self.delay < monotonic():
            # Prende la carta di ogni posizione
            c_s = self.general_man.carte_in_tavola("Sud")
            c_w = self.general_man.carte_in_tavola("Ovest")
            c_n = self.general_man.carte_in_tavola("Nord")
            c_e = self.general_man.carte_in_tavola("Est")

            # TODO: Gestire il caso di pari (si rifa la distribuzione)
            c_win = get_greater(c_s[0], c_w[0])
            c_win = get_greater(c_win, c_n[0])
            c_win = get_greater(c_win, c_e[0])
            
            if (c_win == c_s[0]):
                self.winner = "Sud"
            elif (c_win == c_w[0]):
                self.winner = "Ovest"
            elif (c_win == c_n[0]):
                self.winner = "Nord"
            elif (c_win == c_e[0]):
                self.winner = "Est"
            else:
                raise Exception(type(self).__name__ + ".FsmCartaPiuAlta.fine: Impossibile determinare il vincitore")
            
            self.txt = "Vince " + self.winner + " con " + str(c_win)
            self.new_status = FsmGioco.STATUS_FINE

    def fine(self):
        pass
