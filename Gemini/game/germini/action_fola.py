#   '''
#  Created on 16 2 2022
#  @author: david
#  '''

from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia, is_sopraventi, count_seme, Seme, seme_name
from game.germini.action import Action
from game.germini.punteggi import punti_ger
from main.exception_man import ExceptionMan
from main.globals import echo_message
from oggetti.posizioni import DECK_MAZZO, DECK_FOLA

'''
(5). Il mazziere conta ora il tallone delle carte rimaste che, a meno di errori, consiste di 14 carte  meno le carte
 rubate. Nell'improbabile caso che siano state rubate più di 14 carte, il mazziere avrà inizialmente meno di 21
 carte, in attesa che il "ladro" scarti le sue carte in eccesso. In caso contrario scopre la sua ventunesima carta
 segnando il suo eventuale valore.

(6). A questo punto passa quindi al suo compagno il resto della fola, questi la guarda e comunica agli avversari
 il numero di carte di ogni seme (per esempio: due Coppe, due Bastoni, una Spade, zero Denari) omettendo di
 comunicare il numero dei tarocchi. Attenzione: se sono state rubate o pigliate alcune carte, ne devono essere
 scartate altrettante. Queste carte vengono poste coperte sul tavolo, davanti al giocatore, finché non viene giocata
 la prima carta. Finalmente, ogni giocatore dovrebbe ora avere 21 carte e quello che siede alla destra del mazziere
 può giocare la sua prima carta.

(7). La fola resta sul tavolo alla destra del mazziere. Questi può consultarla in qualsiasi momento mentre ogni
 giocatore ha il diritto di chiedergli cosa contiene. La fola viene comunicata nel modo già descritto, menzionando
 sempre i semi in ordine decrescente ovvero cominciando sempre da quello più numeroso.
Se due o più semi hanno lo stesso numero di carte, si dice per sorte; per esempio:
 quattro coppe e una per sorte significa che denari, spade e bastoni hanno una carta ciascuno.
 Le carte della fola possono essere raggruppate anche in rosse e lunghe; ad esempio: quattro rosse, una lunga
 indica quattro di coppe, quattro di denari, una di spade e una di bastoni. Infine, se i quattro semi hanno un
 numero di carte in ordine crescente, si può ad esempio annunciare semplicemente denari, "spade, coppe, bastoni"
 intendendo che c'è una sola carta di denari, due di spade, tre di coppe e quattro di bastoni.
'''
class ActionFola(Action):
    ACTSTATUS_FOLA_MARCA = "ACTSTATUS_FOLA_MARCA"
    ACTSTATUS_FOLA_PIGLIA = "ACTSTATUS_FOLA_PRENDI"
    ACTSTATUS_FOLA_VEDI = "ACTSTATUS_FOLA_VEDI"
    ACTSTATUS_FOLA_DESCRIVE = "ACTSTATUS_FOLA_DESCRIVE"
    ACTSTATUS_PASSA = "ACTSTATUS_PASSA"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"
    ACTSTATUS_SCARTA = "ACTSTATUS_SCARTA"

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionFola - Crea la fola"))
            self._status = self.ACTSTATUS_FOLA_MARCA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fola_descrive_sub(self, seme):
        try:
            txt = ""
            fo = self._fsm.get_deck(DECK_FOLA)
            n = count_seme(fo, seme)
            if n == 1:
                txt = "<br/>Una carta di " + seme_name[seme]
            elif n > 1:
                txt = "<br/>" + str(n) +" carte di " + seme_name[seme]
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fola_descrive(self):
        try:
            txt = "La fola contiene" +\
            self.fola_descrive_sub(Seme.DENARI) + self.fola_descrive_sub(Seme.COPPE) +\
            self.fola_descrive_sub(Seme.SPADE) + self.fola_descrive_sub(Seme.BASTONI)
            self.show_popup("<p>" + txt + "</p>")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            p = self._fsm.general_man.get_compagno_mazziere()
            if self._status == self.ACTSTATUS_FOLA_MARCA:
                c = self._fsm.game_man.get_prima(DECK_MAZZO)
                if (c is not None) and (c in self._fsm.get_deck(DECK_MAZZO)):
                    if is_sopraventi(c.get_id()) or c.get_id() in punti_ger:
                        c = self._fsm.game_man.pop_prima(DECK_MAZZO)
                        self._fsm.segna_punti_da_fola(self._fsm.game_man.get_mazziere(), c)
                        print("Marca i punti di " + str(c))
                    else:
                        self._fsm.fai_la_fola()
                        self._fsm.game_man.mostra_fola(self._fsm.get_winner())
                        #TODO: Vede le prime 13 carte
                        print("Finisce il rubare del mazziere")
                        self._status = self.ACTSTATUS_FOLA_VEDI
            elif self._status == self.ACTSTATUS_FOLA_DESCRIVE:
                if self._fsm.simulated(p):
                    self.fola_descrive()
                    self._status = self.ACTSTATUS_SCARTA
            elif self._status == self.ACTSTATUS_SCARTA:
                #if self._fsm.simulated(p):
                #    self._fsm.giocatore_scarta(p)
                #self._status = self.ACTSTATUS_END
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if self._status == self.ACTSTATUS_FOLA_MARCA:
                if not self._fsm.simulated(self._fsm._player) and\
                        self._fsm.general_man.has_carta(self._fsm._player, cid):
                    c = self._fsm.game_man.get_prima(DECK_MAZZO)
                    if (c is not None) and (c in self._fsm.get_deck(DECK_MAZZO)) and (str(cid) == c.get_name()):
                        if is_sopraventi(c.get_id()) or c.get_id() in punti_ger:
                            c = self._fsm.game_man.pop_prima(DECK_MAZZO)
                            self._fsm.segna_punti_da_fola(self._fsm.game_man.get_mazziere(), c)
                            print("Marca i punti di " + str(c))
                        else:
                            self._fsm.fai_la_fola()
                            self._fsm.game_man.mostra_fola(self._fsm.game_man.get_mazziere())
                            #TODO: Vede le prime 13 carte
                            print("Finisce il rubare del mazziere")
                            self._status = self.ACTSTATUS_FOLA_VEDI
            elif self._status == self.ACTSTATUS_FOLA_VEDI:
                if not self._fsm.simulated(self._fsm._player):
                    self._fsm.game_man.mostra_fola(self._fsm.game_man.get_mazziere())
                    self._status = self.ACTSTATUS_FOLA_PIGLIA
                    print("Piglia le carte di conto")
            elif self._status == self.ACTSTATUS_FOLA_PIGLIA:
                ca = self._fsm.piglia_da_fola(self._fsm.game_man.get_mazziere())
                for c in ca:
                    self._fsm.game_man.cala_in_tavola(self._fsm.game_man.get_mazziere(), c)
                self._status = self.ACTSTATUS_PASSA
                print("Passa la fola al compagno")
            elif self._status == self.ACTSTATUS_PASSA:
                p = self._fsm.general_man.get_compagno_mazziere()
                self._fsm.game_man.passa_fola(p)
                self._status = self.ACTSTATUS_FOLA_DESCRIVE
            elif self._status == self.ACTSTATUS_FOLA_DESCRIVE:
                p = self._fsm.general_man.get_compagno_mazziere()
                if not self._fsm.simulated(p):
                    self.fola_descrive()
                    self._status = self.ACTSTATUS_SCARTA
            elif self._status == self.ACTSTATUS_SCARTA:
                #p = self._fsm.game_man.get_next_player(self._fsm.game_man.get_mazziere(), False)
                #self._status = self.ACTSTATUS_END
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)