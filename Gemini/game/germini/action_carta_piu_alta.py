#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from bisect import *
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message
from oggetti.posizioni import DECK_MAZZO

'''
    (). Se un giocatore non ha più tarocchi si dice che cade e può scoprire tutte le carte che gli restano; da ora in
     poi non giocherà più (come il morto nel Bridge), ma sarà il vincitore di ogni singola mano a scegliere la carta
     che deve giocare nella successiva, ovviamente rispettando l'obbligo di rispondere a seme, se possibile,
     altrimenti giocando una carta qualsiasi, non avendo, appunto, più tarocchi. Come è facile capire, si tratta di
     una scelta da non farsi se si possiedono ancora dei Re oppure il Matto.È importante ricordare che i giocatori
     possono in qualsiasi momento guardare tutte le carte prese dalla coppia di cui fanno parte.
'''


'''
(2). Il mazziere passa il mazzo al giocatore che si trova alla sua sinistra il quale taglia il mazzo   
'''
class ActionCartaPiuAlta(Action):

    ACTSTATUS_SUDPESCA = "SUB_SUDPESCA"
    ACTSTATUS_NORDPESCA = "SUB_NORDPESCA"
    ACTSTATUS_OVESTPESCA = "SUB_OVESTPESCA"
    ACTSTATUS_ESTPESCA = "SUB_ESTPESCA"
    ACTSTATUS_RISULTATO = "SUB_RISULTATO"

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("Action - Sorteggia il mazziere e le coppie"))
            self._status = self.ACTSTATUS_SUDPESCA
            self._fsm.game_man.mescola_mazzo()
            self._fsm.game_man.mostra_mazzo("Sud")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:

            if self._status == self.ACTSTATUS_OVESTPESCA:
                self.giocatore_pesca("Ovest")
                self._status = self.ACTSTATUS_NORDPESCA
                self.wait_seconds(1)
            elif self._status == self.ACTSTATUS_NORDPESCA:
                self.giocatore_pesca("Nord")
                self._status = self.ACTSTATUS_ESTPESCA
                self.wait_seconds(1)
            elif self._status == self.ACTSTATUS_ESTPESCA:
                self.giocatore_pesca("Est")
                self._status = self.ACTSTATUS_RISULTATO
                self.wait_seconds(1)
            elif self._status == self.ACTSTATUS_RISULTATO:
                c_s = self._fsm.general_man.get_carte_in_tavola("Sud")
                c_w = self._fsm.general_man.get_carte_in_tavola("Ovest")
                c_n = self._fsm.general_man.get_carte_in_tavola("Nord")
                c_e = self._fsm.general_man.get_carte_in_tavola("Est")
                c_win = max(c_s[0], c_w[0])
                c_win = max(c_win, c_n[0])
                c_win = max(c_win, c_e[0])

                classif = [(c_s, "Sud")]
                insort_right(classif, (c_w, "Ovest"))
                insort_right(classif, (c_e, "Est"))
                insort_right(classif, (c_n, "Nord"))

                print(classif)

                if (c_win == c_s[0]):
                    self.winner = self._fsm.general_man.get_player_at_pos("Sud")
                elif (c_win == c_w[0]):
                    self.winner = self._fsm.general_man.get_player_at_pos("Ovest")
                elif (c_win == c_n[0]):
                    self.winner = self._fsm.general_man.get_player_at_pos("Nord")
                elif (c_win == c_e[0]):
                    self.winner = self._fsm.general_man.get_player_at_pos("Est")
                else:
                    self.winner = None

                if self.winner is not None:
                    self._fsm._delegate_append_html_text("Vince " + str(self.winner) + " con " + str(c_win))
                    self.show_popup("<p>" + str(self.winner) + " vince con " + str(c_win) + " e sarà il mazziere</p>")
                    self._fsm.update_mazziere(self.winner)
                    self._status = self.ACTSTATUS_END
                else:
                    self._fsm._delegate_append_html_text("Nessun vincitore")
                    self.show_popup("<p>Nessun vincitore. Ripete il sorteggio</p>" + str(c_win))
                    self._status = self.ACTSTATUS_SUDPESCA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def giocatore_pesca(self, ppos):
        g = self._fsm.general_man.get_player_at_pos(ppos)
        ca = self._fsm.dai_al_giocatore(g, 1, False)
        c = ca[0]
        c = self._fsm.calata(g, c)
        self._fsm._delegate_append_html_text(str(g) + " ha pescato " + str(c))

    def on_carta_click(self, cid):
        try:
            if self._status == self.ACTSTATUS_SUDPESCA:
                self.giocatore_pesca("Sud")
                self._status = self.ACTSTATUS_OVESTPESCA
                self.wait_seconds(1)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)