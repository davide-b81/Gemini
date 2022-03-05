#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia, get_greater, seme_name, get_seme
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message
from oggetti.posizioni import DECK_SCARTO

'''
(12). Le carte vengono giocate in senso antiorario, iniziando dal giocatore seduto alla destra del mazziere.
  Subito dopo aver giocato la loro prima carta, i giocatori che possiedono una o più versicole devono mostrarle
  per poterne segnare il valore. Non appena viene raccolta la prima mano, non è più possibile segnare versicole.
 Prendere una mano: Finché è possibile si deve rispondere a ciascun seme, tarocchi inclusi; nel caso non si
 possiedano carte del seme giocato è necessario giocare un tarocco (ma non è obbligatorio surtagliare,
 ovvero superare il tarocco precedente). Nel caso un seme venga giocato per la prima volta e tagliato
 con un tarocco, un successivo giocatore che abbia il Re è obbligato a giocarlo, ed è una regola
 peculiare delle Minchiate. Ad un secondo giro può invece giocare una carta più bassa o il Matto.
(13). Al termine della prima mano, le carte precedentemente scartate (a causa dei rubati o dei pigliati)
  devono essere mostrate. Il compagno del mazziere deve annunciarle a voce alta, specificando chi le ha
  scartate e ponendole nella fola. Dopodiché comunica di nuovo la fola nel modo precedentemente descritto
  e la passa al mazziere che la pone sul tavolo, alla sua destra.
  Come in molti giochi, la carta più alta vince la mano. Il giocatore che l'ha giocata raccoglie le carte,
  le unisce a quelle della sua squadra (che vengono quindi tenute tutte assieme) e gioca la prima carta della
  mano successiva.
().  Ogni volta che una carta di conto viene presa dalla coppia avversaria, questa ne segna subito
     il valore. Si dice che muore rispettivamente un 3, un 5 o un 10 in base al valore della carta. La perdita di una
     carta di conto è quindi una perdita tripla: non se ne segnerà infatti alla fine il valore, valore che verrà invece
     segnato dagli avversari che in più segnano subito un bonus extra per la carta che muore. Se una carta viene
     catturata dal compagno, si dice che muore in casa e non vale come extra.
'''


class ActionGiro(Action):
    ACTION_APERTURA = "ACTION_APERTURA"
    ACTION_RISPOSTA_I = "ACTION_RISPOSTA_I"
    ACTION_RISPOSTA_II = "ACTION_RISPOSTA_II"
    ACTION_RISPOSTA_III = "ACTION_RISPOSTA_III"
    ACTION_PRESA = "ACTION_PRESA"
    ACTION_SCARTA = "ACTION_SCARTA"
    ACTION_FINAMANO = "ACTION_FINAMANO"

    _cid_apertura = None
    _winner = None
    _scarto = False

    def __init__(self, fsm):
        try:
            super().__init__(fsm)
            self._t_action = monotonic()
            echo_message(_("ActionGiro - Gioco delle carte"))
            self._scarto = False
            self._status = self.ACTION_APERTURA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("Action - Giro"))
            self.status = self.ACTION_APERTURA
            self._cid_apertura = None
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            if self._winner is not None:
                player = self._fsm._winner
                self._fsm._winner = None
            else:
                player = self._fsm._player

            if self._status == self.ACTION_APERTURA:
                if self._fsm.simulated(self._fsm._player):
                    c = self._fsm.gioca_carta(player)
                    self.cid_apertura = c.get_id()
                    self._fsm.calata(player, c)
                    self._fsm._delegate_append_html_text(
                        "<p>Seme di apertura " + seme_name[get_seme(self.cid_apertura)] + " </p>")
                    self._status = self.ACTION_RISPOSTA_I
                    self._fsm.update_next_player(self.giocatore_turno, True)
            elif self._status == self.ACTION_RISPOSTA_I:
                if self._fsm.simulated(self._fsm._player):
                    c = self._fsm.gioca_carta(player)
                    self._fsm.calata(player, c)
                    self._status = self.ACTION_RISPOSTA_II
                    self._fsm.update_next_player(self.giocatore_turno, True)
            elif self._status == self.ACTION_RISPOSTA_II:
                if self._fsm.simulated(self._fsm._player):
                    c = self._fsm.gioca_carta(player)
                    self._fsm.calata(player, c)
                    self._status = self.ACTION_RISPOSTA_III
                    self._fsm.update_next_player(self.giocatore_turno, True)
            elif self._status == self.ACTION_RISPOSTA_III:
                if self._fsm.simulated(self._fsm._player):
                    c = self._fsm.gioca_carta(player)
                    self._fsm.calata(player, c)
                    self._status = self.ACTION_PRESA
                    self._fsm.update_next_player(self.giocatore_turno, True)
            elif self._status == self.ACTION_PRESA:
                self.presa()
                if not self._scarto:
                    self._status = self.ACTION_SCARTA
                else:
                    self._status = self.ACTSTATUS_END
            elif self._status == self.ACTION_SCARTA:
                self.scarto()
            else:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if self._status == self.ACTION_APERTURA or self._status == self.ACTION_RISPOSTA_I or \
                    self._status == self.ACTION_RISPOSTA_II or self._status == self.ACTION_RISPOSTA_III:
                if not self._fsm.simulated(self._fsm._player) and \
                        self._fsm.general_man.has_carta(self._fsm._player, cid):
                    if self.is_giocabile(cid):
                        if self._sub_status == self.SUB_APERTURA:
                            self.cid_apertura = cid
                        cc = self._fsm.general_man.get_carta_obj(self._fsm._player, cid)
                        self.calata(self._fsm._player, cc)
                        # TODO: Aggiornare lo stato altrimenti si può cliccare più carte
                        self._delegate_append_html_text("Tocca a " + str(
                            self._fsm._player) + " (" + self._fsm._player.get_position() + ") tirare ")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def player_scarta(self, player):
        try:
            self._fsm.giocatore_scarta(player)
            self.game_man.stendi_deck(player.get_position(), DECK_SCARTO)
            self.wait_seconds(1)
            self._scarto = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scarto(self):
        try:
            self.player_scarta("Nord")
            self.player_scarta("Sud")
            self.player_scarta("Est")
            self.player_scarta("Ovest")
            self.wait_seconds(1)
            self._scarto = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def presa(self):
        try:
            c_list = []

            c_win = self.gestisci_winner()

            self._delegate_presa(self._winner, c_list)
            self._delegate_append_html_text("Mano a " + str(self._winner) + " con " + str(c_win))

            if self._fsm.general_man.get_num_carte_mano(self._winner) > 0:
                self._status = self.SUB_APERTURA
                for g in self._fsm.general_man.get_giocatori():
                    if g.is_caduto():
                        self.giocatore_turno.giocatore_cade()
                        self.show_popup("<p>Cade " + self.giocatore_turno._name + " e scopre le sue carte</p>")
                        self.game_man.scopri_carte(self.giocatore_turno)
                        self._status = self.STATUS_MODAL_POPUP
            else:
                self._status = self.STATUS_FINEMANO
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gestisci_winner(self):
        try:
            c_s = self._fsm.general_man.get_carte_in_tavola("Sud")
            c_w = self._fsm.general_man.get_carte_in_tavola("Ovest")
            c_n = self._fsm.general_man.get_carte_in_tavola("Nord")
            c_e = self._fsm.general_man.get_carte_in_tavola("Est")

            clist = self._fsm.general_man.prendi_tavola()

            c_win = get_greater(clist)
            # c_win = get_greater([c_s, c_w, c_n, c_e])

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
            return c_win
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
