'''
Created on 4 gen 2022

@author: david
'''
from game.fsm_gioco import FsmGioco
from time import monotonic
from decks.carta_id import get_greater
from main.exception_man import ExceptionMan


class FsmTest(FsmGioco):
    '''
    classdocs
    '''

    delay = 0.3

    def __init__(self, gamman=None, genman=None):
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
            ExceptionMan.manage_exception("", e, True)

    def start_game(self):
        super().start_game()

    def inizio(self):
        self._status_next = "IoPesco"

    def io_pesco(self):
        if self._t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Nord")

                c = self.general_man.pesca_dal_mazzo(g)
                while c != None:
                    self.game_man.set_fronte(c, FRONT_SCOPERTA)
                    c = self.general_man.pesca_dal_mazzo(g)

                #c = self.calata(g, c)
                self.txt = "Ho pescato " + str(c)
            except Exception as e:
                ExceptionMan.manage_exception("", e, True)
            self._status_next = "OvestPesca"

    def ovest_pesca(self):
        if self._t_status + self.delay < monotonic():
            try:
                #g = self.general_man.get_player_at_pos("Ovest")
                #c = self.general_man.pesca_dal_mazzo(g)
                #g.assegna_carta(c)
                #c = self.calata(g, c)
                #self.txt = "Ovest ha pescato " + str(c)
                pass
            except Exception as e:
                ExceptionMan.manage_exception("", e, True)
            #self.new_status = "NordPesca"

    def nord_pesca(self):
        if self._t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Nord")
                c = self.general_man.pesca_dal_mazzo(g)
                c = self.calata(g, c)
                self.txt = "Nord ha pescato " + str(c)
            except Exception as e:
                ExceptionMan.manage_exception("", e, True)
            self._status_next = "EstPesca"

    def est_pesca(self):
        if self._t_status + self.delay < monotonic():
            try:
                g = self.general_man.get_player_at_pos("Est")
                c = self.general_man.pesca_dal_mazzo(g)
                c = self.calata(g, c)
                self.txt = "Est ha pescato " + str(c)
            except Exception as e:
                ExceptionMan.manage_exception("", e, True)
            self._status_next = "Risultato"

    def risultato(self):
        if self._t_status + self.delay < monotonic():
            # Prende la carta di ogni posizione
            c_s = self.general_man.get_carte_in_tavola("Sud")
            c_w = self.general_man.get_carte_in_tavola("Ovest")
            c_n = self.general_man.get_carte_in_tavola("Nord")
            c_e = self.general_man.get_carte_in_tavola("Est")
            clist = self.general_man.prendi_tavola()
            # TODO: Gestire il caso di pari (si rifa la distribuzione)

            c_win = get_greater(clist)

            if c_win in c_s:
                self.winner = "Sud"
            elif c_win in c_w:
                self.winner = "Ovest"
            elif c_win in c_n:
                self.winner = "Nord"
            elif c_win in c_e:
                self.winner = "Est"
            else:
                assert False

            self.txt = "Vince " + self.winner + " con " + str(c_win)
            self._status_next = FsmGioco.STATUS_FINE

    def fine(self):
        pass
