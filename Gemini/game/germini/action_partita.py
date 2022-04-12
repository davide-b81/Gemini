#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from copy import copy
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia, get_greater, seme_name, get_seme
from game.germini.action import Action
from game.germini.punteggi import is_conto
from game.germini.strategia import Strategia
from main.exception_man import ExceptionMan
from main.globals import echo_message, POSTAZIONE_SUD, POSTAZIONE_NORD, POSTAZIONE_EST, POSTAZIONE_OVEST, \
    FRONTE_SCOPERTA
from oggetti.posizioni import DeckId


class ActionPartita(Action):
    ACTSTATUS_PRIMA_CARTA_1 = "ACTSTATUS_PRIMA_CARTA_1"
    ACTSTATUS_PRIMA_CARTA_2 = "ACTSTATUS_PRIMA_CARTA_2"
    ACTSTATUS_PRIMA_CARTA_3 = "ACTSTATUS_PRIMA_CARTA_3"
    ACTSTATUS_PRIMA_CARTA_4 = "ACTSTATUS_PRIMA_CARTA_4"
    ACTSTATUS_SCARTA_CARTA_1 = "ACTSTATUS_SCARTA_CARTA_1"
    ACTSTATUS_SCARTA_CARTA_2 = "ACTSTATUS_SCARTA_CARTA_2"
    ACTSTATUS_SCARTA_CARTA_3 = "ACTSTATUS_SCARTA_CARTA_3"
    ACTSTATUS_SCARTA_CARTA_4 = "ACTSTATUS_SCARTA_CARTA_4"
    ACTSTATUS_DICHIARA_VERSICOLE_1 = "ACTSTATUS_DICHIARA_VERSICOLE_1"
    ACTSTATUS_DICHIARA_VERSICOLE_2 = "ACTSTATUS_DICHIARA_VERSICOLE_2"
    ACTSTATUS_DICHIARA_VERSICOLE_3 = "ACTSTATUS_DICHIARA_VERSICOLE_3"
    ACTSTATUS_DICHIARA_VERSICOLE_4 = "ACTSTATUS_DICHIARA_VERSICOLE_4"
    ACTSTATUS_GIOCO_CARTA_1 = "ACTSTATUS_GIOCO_CARTA_1"
    ACTSTATUS_GIOCO_CARTA_2 = "ACTSTATUS_GIOCO_CARTA_2"
    ACTSTATUS_GIOCO_CARTA_3 = "ACTSTATUS_GIOCO_CARTA_3"
    ACTSTATUS_GIOCO_CARTA_4 = "ACTSTATUS_GIOCO_CARTA_4"
    ACTSTATUS_PRESA = "ACTSTATUS_PRESA"
    ACTSTATUS_RITIRA_SCARTI = "ACTSTATUS_RITIRA_SCARTI"
    ACTSTATUS_FINAMANO = "ACTSTATUS_FINAMANO"
    ACTSTATUS_CHECK_CADUTO_1 = "ACTSTATUS_CHECK_CADUTO_1"
    ACTSTATUS_CHECK_CADUTO_2 = "ACTSTATUS_CHECK_CADUTO_2"
    ACTSTATUS_CHECK_CADUTO_3 = "ACTSTATUS_CHECK_CADUTO_3"
    ACTSTATUS_CHECK_CADUTO_4 = "ACTSTATUS_CHECK_CADUTO_4"

    _winner = None
    _scarto = None
    _tagliato = None
    _primo = {}

    def __init__(self, fsm):
        try:
            super().__init__(fsm)
            self._t_action = monotonic()
            self._scarto = False
            self._newsts = self.ACTSTATUS_PRIMA_CARTA_1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start(self):
        try:
            self.reset()
            # Posiziona mazzo e lo rende visibile
            echo_message(_("Action - Giro"))
            self._winner = None
            self._newsts = self.ACTSTATUS_PRIMA_CARTA_1
            self.reset_giro_singolo()
            self._primo[POSTAZIONE_SUD] = False
            self._primo[POSTAZIONE_NORD] = False
            self._primo[POSTAZIONE_EST] = False
            self._primo[POSTAZIONE_OVEST] = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_versicole(self, player, nextsts):
        try:
            txt = self._fsm.get_versicole().get_txt_description()
            self.show_timed_popup("<p>" + str(player) + ": " + txt + "</p>", 1.5)
            self._newsts = nextsts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_scarta(self, player, nextsts):
        try:
            n_sca = self._fsm.scartare()
            if n_sca > 0:
                self._fsm.giocatore_scarta(player)
            else:
                self._newsts = nextsts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_prima(self, player, nextsts1, nextsts2):
        try:
            self._fsm.inizializza_versicole(player)
            c = self._fsm.gioca_carta(player)
            n_sca = self._fsm.scartare()
            self._fsm.calata(c, player)
            if n_sca > 0:
                self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(n_sca) + " carte.")
                self._newsts = nextsts1
            else:
                self._newsts = nextsts2
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_play(self, player, nextsts):
        try:
            if self._fsm.is_caduto(player) and self._fsm.simulated(self._winner):
                c = self._fsm.gioca_carta_caduto(self._winner, player)
            else:
                c = self._fsm.gioca_carta(player)

            if self._status == self.ACTSTATUS_GIOCO_CARTA_1:
                self._fsm.set_apertura(c)
            self._fsm.calata(c, player)
            if nextsts != self.ACTSTATUS_PRESA:
                self._fsm.update_next_player()
            self._newsts = nextsts
            self.wait_seconds(0.1)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            '''            
            (12). Le carte vengono giocate in senso antiorario, iniziando dal giocatore seduto alla destra del mazziere.
              Subito dopo aver giocato la loro prima carta, i giocatori che possiedono una o più versicole devono mostrarle
              per poterne segnare il valore. Non appena viene raccolta la prima mano, non è più possibile segnare versicole.
             Prendere una mano: Finché è possibile si deve rispondere a ciascun seme, tarocchi inclusi; nel caso non si
             possiedano carte del seme giocato è necessario giocare un tarocco (ma non è obbligatorio surtagliare,
             ovvero superare il tarocco precedente). Nel caso un seme venga giocato per la prima volta e tagliato
             con un tarocco, un successivo giocatore che abbia il Re è obbligato a giocarlo, ed è una regola
             peculiare delle Minchiate. Ad un secondo giro può invece giocare una carta più bassa o il Matto.
            '''
            player = self._fsm.get_player()

            # First player
            if self._status == self.ACTSTATUS_PRIMA_CARTA_1:
                if self._fsm.simulated():
                    c = self.manage_prima(player, self.ACTSTATUS_SCARTA_CARTA_1, self.ACTSTATUS_DICHIARA_VERSICOLE_1)
                    self._fsm.set_apertura(c)
            elif self._status == self.ACTSTATUS_SCARTA_CARTA_1:
                if self._fsm.simulated():
                    self.manage_scarta(player, self.ACTSTATUS_DICHIARA_VERSICOLE_1)
            elif self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_1:
                self.manage_versicole(player, self.ACTSTATUS_PRIMA_CARTA_2)
                self._fsm.update_next_player()

            # Second player
            elif self._status == self.ACTSTATUS_PRIMA_CARTA_2:
                if self._fsm.simulated():
                    self.manage_prima(player, self.ACTSTATUS_SCARTA_CARTA_2, self.ACTSTATUS_DICHIARA_VERSICOLE_2)
            elif self._status == self.ACTSTATUS_SCARTA_CARTA_2:
                if self._fsm.simulated():
                    self.manage_scarta(player, self.ACTSTATUS_DICHIARA_VERSICOLE_2)
            elif self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_2:
                self.manage_versicole(player, self.ACTSTATUS_PRIMA_CARTA_3)
                self._fsm.update_next_player()

            # Third player
            elif self._status == self.ACTSTATUS_PRIMA_CARTA_3:
                if self._fsm.simulated():
                    self.manage_prima(player, self.ACTSTATUS_SCARTA_CARTA_3, self.ACTSTATUS_DICHIARA_VERSICOLE_3)
            elif self._status == self.ACTSTATUS_SCARTA_CARTA_3:
                if self._fsm.simulated():
                    self.manage_scarta(player, self.ACTSTATUS_DICHIARA_VERSICOLE_3)
            elif self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_3:
                self.manage_versicole(player, self.ACTSTATUS_PRIMA_CARTA_4)
                self._fsm.update_next_player()

            # Fourth player
            elif self._status == self.ACTSTATUS_PRIMA_CARTA_4:
                if self._fsm.simulated():
                    self.manage_prima(player, self.ACTSTATUS_SCARTA_CARTA_4, self.ACTSTATUS_DICHIARA_VERSICOLE_4)
            elif self._status == self.ACTSTATUS_SCARTA_CARTA_4:
                if self._fsm.simulated():
                    self.manage_scarta(player, self.ACTSTATUS_DICHIARA_VERSICOLE_4)
            elif self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_4:
                if self._fsm.simulated():
                    self.manage_versicole(player, self.ACTSTATUS_PRESA)

            # Regular
            elif self._status == self.ACTSTATUS_GIOCO_CARTA_1:
                if self._fsm.simulated() or self._fsm.is_caduto():
                    self.manage_play(player, self.ACTSTATUS_GIOCO_CARTA_2)
            elif self._status == self.ACTSTATUS_GIOCO_CARTA_2:
                if self._fsm.simulated() or self._fsm.is_caduto():
                    self.manage_play(player, self.ACTSTATUS_GIOCO_CARTA_3)
            elif self._status == self.ACTSTATUS_GIOCO_CARTA_3:
                if self._fsm.simulated() or self._fsm.is_caduto():
                    self.manage_play(player, self.ACTSTATUS_GIOCO_CARTA_4)
            elif self._status == self.ACTSTATUS_GIOCO_CARTA_4:
                if self._fsm.simulated() or self._fsm.is_caduto():
                    self.manage_play(player, self.ACTSTATUS_PRESA)
            elif self._status == self.ACTSTATUS_PRESA:
                self.presa()
                #if not self._scarto:
                #    self._newsts = self.ACTSTATUS_SCARTA
                #else:
                #    self._newsts = self.ACTSTATUS_END
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_1:
                self.check_caduto(self._winner)
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_2
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_2:
                self.check_caduto(self._fsm.get_next_player(self._winner))
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_3
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_3:
                player = self._fsm.get_next_player(self._winner)
                self.check_caduto(self._fsm.get_next_player(player))
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_4
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_4:
                player = self._fsm.get_next_player(self._winner)
                player = self._fsm.get_next_player(player)
                self.check_caduto(self._fsm.get_next_player(player))
                if self._fsm.get_num_carte_mano(self._winner) > 0:
                    self._newsts = self.ACTSTATUS_GIOCO_CARTA_1
                else:
                    self._newsts = self.ACTSTATUS_END
            elif self._status == self.ACTSTATUS_FINAMANO:
                    self._newsts = self.ACTSTATUS_END
            else:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def man_scarta_carta_click(self, c):
        try:
            player = self._fsm.get_player()
            rubate = self._fsm.get_deck(DeckId.DECK_RUBATE, player.get_position())
            if self._fsm.player_has_carta(self._fsm.get_player(), c.get_id()):
                self._fsm.giocatore_scarta_carta(c, player)
                self._fsm.move_card_and_repos(rubate[0], DeckId.DECK_RUBATE, DeckId.DECK_MANO, FRONTE_SCOPERTA, player)
            if self._fsm.scartare() <= 0:
                if self._status == self.ACTSTATUS_SCARTA_CARTA_1:
                    self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_1
                elif self._status == self.ACTSTATUS_SCARTA_CARTA_2:
                    self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_2
                elif self._status == self.ACTSTATUS_SCARTA_CARTA_3:
                    self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_3
                elif self._status == self.ACTSTATUS_SCARTA_CARTA_4:
                    self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_4
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def man_prima_carta_click(self, c):
        try:
            if self._fsm.player_has_carta(self._fsm.get_player(), c.get_id()) and self._fsm.is_giocabile(c.get_id()):
                if self._status == self.ACTSTATUS_PRIMA_CARTA_1:
                    self._fsm.set_apertura(c)
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.scartare() > 0:
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.scartare()) + " carte.")
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_1
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_1
                elif self._status == self.ACTSTATUS_PRIMA_CARTA_2:
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.scartare() > 0:
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.scartare()) + " carte.")
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_2
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_2
                elif self._status == self.ACTSTATUS_PRIMA_CARTA_3:
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.scartare() > 0:
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.scartare()) + " carte.")
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_3
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_3
                elif self._status == self.ACTSTATUS_PRIMA_CARTA_4:
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.scartare() > 0:
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.scartare()) + " carte.")
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_4
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_4
                else:
                    pass

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            c = self._fsm.get_carta(cid)

            if not self._fsm.simulated():
                if self._status == self.ACTSTATUS_PRIMA_CARTA_1 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_2 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_3 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_4:
                    self.man_prima_carta_click(c)

                elif self._status == self.ACTSTATUS_SCARTA_CARTA_1 or\
                   self._status == self.ACTSTATUS_SCARTA_CARTA_2 or\
                   self._status == self.ACTSTATUS_SCARTA_CARTA_3 or\
                   self._status == self.ACTSTATUS_SCARTA_CARTA_4:
                    self.man_scarta_carta_click(c)

                elif self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_1 or\
                   self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_2 or\
                   self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_3 or\
                   self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_4:
                    # Gestito in automatico
                    pass

                elif self._status == self.ACTSTATUS_GIOCO_CARTA_1 or\
                   self._status == self.ACTSTATUS_GIOCO_CARTA_2 or\
                   self._status == self.ACTSTATUS_GIOCO_CARTA_3 or\
                   self._status == self.ACTSTATUS_GIOCO_CARTA_4 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_1 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_2 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_3 or\
                   self._status == self.ACTSTATUS_PRIMA_CARTA_4:
                    if not self._fsm.simulated() and (self._fsm.get_player() == self._winner or not self._fsm.is_caduto()):
                        if self._fsm.player_has_carta(self._fsm.get_player(), cid) and self._fsm.is_giocabile(cid):
                            if self._status == self.ACTSTATUS_GIOCO_CARTA_1:
                                self._fsm.set_apertura(c)
                                self._newsts = self.ACTSTATUS_GIOCO_CARTA_2
                            elif self._status == self.ACTSTATUS_GIOCO_CARTA_2:
                                self._newsts = self.ACTSTATUS_GIOCO_CARTA_3
                            elif self._status == self.ACTSTATUS_GIOCO_CARTA_3:
                                self._newsts = self.ACTSTATUS_GIOCO_CARTA_4
                            elif self._status == self.ACTSTATUS_GIOCO_CARTA_4:
                                self._newsts = self.ACTSTATUS_PRESA
                            elif self._status == self.ACTSTATUS_SCARTA:
                                pass
                            else:
                                raise Exception("Error in FSM")

                            self._fsm.calata(c)
                            self._fsm.update_next_player()
                            self._fsm._delegate_append_html_text("Tocca a " +\
                            str(self._fsm.get_player()) + " (" + self._fsm.get_player().get_position() + ") tirare ")
                elif self._fsm.is_caduto() and not self._fsm.simulated(self._winner):
                    if self._fsm.is_giocabile_caduto(cid):
                        self._fsm.calata(c)
                        self._fsm.update_next_player()
                        self._fsm._delegate_append_html_text("Tocca a " +\
                        str(self._fsm.get_player()) + " (" + self._fsm.get_player().get_position() + ") tirare ")

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scarto(self):
        try:
            for p in self._game_man.get_giocatori():
                if self._fsm.simulated():
                    self._fsm.giocatore_scarta(p.get_position())
                    self._fsm.mostra_mazzo(DeckId.DECK_POZZO, p.get_position())
            self._scarto = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ritira_scarti(self):
        """
        (13). Al termine della prima mano, le carte precedentemente scartate (a causa dei rubati o dei pigliati)
            devono essere mostrate. Il compagno del mazziere deve annunciarle a voce alta, specificando chi le ha
            scartate e ponendole nella fola. Dopodiché comunica di nuovo la fola nel modo precedentemente descritto
            e la passa al mazziere che la pone sul tavolo, alla sua destra. Come in molti giochi, la carta più alta
            vince la mano. Il giocatore che l'ha giocata raccoglie le carte, le unisce a quelle della sua squadra
            (che vengono quindi tenute tutte assieme) e gioca la prima carta della mano successiva.
        """
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def presa_avversari(self, player1):
        try:
            player2 = self._fsm.get_compagno(player1)

            c1 = self._fsm.get_carte_in_tavola_player(player1)
            c2 = self._fsm.get_carte_in_tavola_player(player2)
            assert len(c1) == 1
            assert len(c2) == 1
            if is_conto(c1[0]):
                echo_message("Cade " + str(c1[0]))
            if is_conto(c2[0]):
                echo_message("Cade " + str(c2[0]))
            self._fsm.raccogli_carte_calate(self._winner, player1)
            self._fsm.raccogli_carte_calate(self._winner, player2)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def presa_coppia(self, player1):
        try:
            player2 = self._fsm.get_compagno(player1)
            self._fsm.raccogli_carte_calate(self._winner, player1)
            self._fsm.raccogli_carte_calate(self._winner, player2)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def presa(self):
        try:
            '''().  Ogni volta che una carta di conto viene presa dalla coppia avversaria, questa ne segna subito
     il valore. Si dice che muore rispettivamente un 3, un 5 o un 10 in base al valore della carta. La perdita di una
     carta di conto è quindi una perdita tripla: non se ne segnerà infatti alla fine il valore, valore che verrà invece
     segnato dagli avversari che in più segnano subito un bonus extra per la carta che muore. Se una carta viene
     catturata dal compagno, si dice che muore in casa e non vale come extra.
            '''
            c_list = self._fsm.get_carte_in_tavola()
            (self._winner, c_win) = self.get_winner(c_list)
            assert self._winner is not None
            self._fsm._delegate_append_html_text("Mano a " + str(self._winner) + " con " + str(c_win))

            self.presa_coppia(self._winner)
            self.presa_avversari(self._fsm.get_next_player(self._winner))

            self._fsm.set_player(self._winner)
            self._fsm._delegate_presa(self._winner)

            '''
            (). Se un giocatore non ha più tarocchi si dice che cade e può scoprire tutte le carte che gli restano; da ora in
             poi non giocherà più (come il morto nel Bridge), ma sarà il vincitore di ogni singola mano a scegliere la carta
             che deve giocare nella successiva, ovviamente rispettando l'obbligo di rispondere a seme, se possibile,
             altrimenti giocando una carta qualsiasi, non avendo, appunto, più tarocchi. Come è facile capire, si tratta di
             una scelta da non farsi se si possiedono ancora dei Re oppure il Matto.È importante ricordare che i giocatori
             possono in qualsiasi momento guardare tutte le carte prese dalla coppia di cui fanno parte.
            '''
            self._fsm._cid_apertura = None
            if self._fsm.get_num_carte_mano(self._winner) > 0:
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_1
            else:
                txt = self._fsm.get_text_punti_mano()
                for p in self._fsm.get_giocatori():
                    p.on_fine_mano()
                txt = txt + self._fsm.get_text_punti_totale()
                self.show_timed_popup(txt)
                self._newsts = self.ACTSTATUS_FINAMANO
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_giro_singolo(self):
        try:
            self._fsm._cid_apertura = None
            self._tagliato = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def check_caduto(self, player):
        try:
            # First event
            if not self._fsm.is_caduto(player) and self._fsm.cascare_enabled(player):
                self.show_timed_popup("<p>Cade " + str(player) + " e scopre le sue carte</p>", 1)
                self._fsm.on_cade(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_winner(self, clist):
        try:
            winner = None
            c_s = copy(self._fsm.get_carte_in_tavola_pos("Sud"))
            c_w = copy(self._fsm.get_carte_in_tavola_pos("Ovest"))
            c_n = copy(self._fsm.get_carte_in_tavola_pos("Nord"))
            c_e = copy(self._fsm.get_carte_in_tavola_pos("Est"))

            c_win = get_greater(clist)

            if c_win in c_s:
                winner = self._fsm.get_player_at_pos("Sud")
            elif c_win in c_w:
                winner = self._fsm.get_player_at_pos("Ovest")
            elif c_win in c_n:
                winner = self._fsm.get_player_at_pos("Nord")
            elif c_win in c_e:
                winner = self._fsm.get_player_at_pos("Est")
            else:
                echo_message("Warning no winner")
                assert True
            return (winner, c_win)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
