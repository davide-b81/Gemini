#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from copy import copy
from importlib.resources import _
from time import monotonic

from game.germini.action import Action
from game.germini.punteggi import is_conto
from game.germini.strategia import Strategia
from main.exception_man import ExceptionMan
from oggetti.posizioni import *
from main.globals import echo_message, FRONTE_COPERTA


class ActionPartita(Action):
    ACTSTATUS_PRIMA_CARTA_1 = "ACTSTATUS_PRIMA_CARTA_1"
    ACTSTATUS_PRIMA_CARTA_2 = "ACTSTATUS_PRIMA_CARTA_2"
    ACTSTATUS_PRIMA_CARTA_3 = "ACTSTATUS_PRIMA_CARTA_3"
    ACTSTATUS_PRIMA_CARTA_4 = "ACTSTATUS_PRIMA_CARTA_4"
    ACTSTATUS_SCARTA_CARTA_1 = "ACTSTATUS_SCARTA_CARTA_1"
    ACTSTATUS_SCARTA_CARTA_2 = "ACTSTATUS_SCARTA_CARTA_2"
    ACTSTATUS_SCARTA_CARTA_3 = "ACTSTATUS_SCARTA_CARTA_3"
    ACTSTATUS_SCARTA_CARTA_4 = "ACTSTATUS_SCARTA_CARTA_4"
    ACTSTATUS_INTEGRA = "ACTSTATUS_INTEGRA"
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
    ACTSTATUS_FINEMANO = "ACTSTATUS_FINEMANO"
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

    def set_primo(self):
        '''
        (12a). Le carte vengono giocate in senso antiorario, iniziando dal giocatore seduto alla destra del mazziere.
        '''
        try:
            assert self._fsm.get_mazziere() is not None
            player = self._fsm.get_mazziere()
            player = self._fsm.get_next_player(player, True)
            self._fsm.set_player(player)
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
            self.set_primo()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_versicole(self, player, nextsts):
        try:
            print("Gestisce versicole di " + str(player))
            txt = ""
            ca = self._fsm.get_carte_mano(player)

            self._fsm.gestisci_carte_versicola(ca, player)
            pts = self._fsm.marca_punti_versicole(player)

            if pts > 0:
                self.show_timed_popup("<p>" + str(player) + ": " + self._fsm.get_versicole_dichiarazione() + "</p><br/>")
            self._newsts = nextsts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_scarta(self, player, nextsts):
        try:
            n_sca = self._fsm.get_num_scarti()
            if n_sca > 0:
                cc = Strategia.scarta_carte(player, n_sca)
                for c in cc:
                    self.man_scarta_carta(player, c)
            else:
                self._newsts = nextsts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_prima(self, player, nextsts1, nextsts2):
        try:
            self._fsm.inizializza_versicole(player)
            c = self._fsm.gioca_carta(player)
            n_sca = self._fsm.get_num_scarti()
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
            #Strategia.on_carta(player, c)
            self._fsm.calata(c, player)
            if nextsts != self.ACTSTATUS_PRESA:
                self._fsm.update_next_player()
            self._newsts = nextsts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def manage_fine_mano(self, player):
        try:
            self._fsm.on_fine_mano(player)
            txt = self._fsm.get_text_punti_mano()
            txt = txt + self._fsm.get_text_resti()
            self.show_timed_popup(txt)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            '''
            (12b).  Subito dopo aver giocato la loro prima carta, i giocatori che possiedono una o più versicole devono mostrarle
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
                    #self._fsm.set_deck_visible(DeckId.DECK_SCARTO, player.get_position(), False)
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
                    # Sono state prese tutte le carte della fola, dopo lo scarto preleva la ventunesima
                    """
                    (6b). Attenzione: se sono state rubate o pigliate alcune carte, ne devono essere scartate altrettante.
                    Queste carte vengono poste coperte sul tavolo, davanti al giocatore, finché non viene giocata la prima carta.
                    Finalmente, ogni giocatore dovrebbe ora avere 21 carte e quello che siede alla destra del mazziere può giocare
                    la sua prima carta.
                    -- Prende la prima delle scartate?? --
                    """
                    if self._fsm.get_deck_len(DeckId.DECK_MANO, player) < 21:
                        p = self._fsm.get_carte(DeckId.DECK_POZZO)
                        self._fsm.sposta_carta(p[0], DeckId.DECK_POZZO, DeckId.DECK_MANO, player)
                    # ----------------
                    self.manage_prima(player, self.ACTSTATUS_SCARTA_CARTA_4, self.ACTSTATUS_DICHIARA_VERSICOLE_4)
            elif self._status == self.ACTSTATUS_SCARTA_CARTA_4:
                if self._fsm.simulated():
                    self.manage_scarta(player, self.ACTSTATUS_DICHIARA_VERSICOLE_4)
            elif self._status == self.ACTSTATUS_DICHIARA_VERSICOLE_4:
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
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_1:
                self.check_caduto(self._winner)
                self._fsm.update_next_player()
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_2
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_2:
                self.check_caduto(self._fsm.get_player())
                self._fsm.update_next_player()
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_3
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_3:
                self.check_caduto(self._fsm.get_player())
                self._fsm.update_next_player()
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_4
            elif self._status == self.ACTSTATUS_CHECK_CADUTO_4:
                self.check_caduto(self._fsm.get_player())
                self._fsm.update_next_player()
                if self._fsm.get_deck_len(DeckId.DECK_MANO, self._winner) > 0:
                    self._newsts = self.ACTSTATUS_GIOCO_CARTA_1
                else:
                    self._newsts = self.ACTSTATUS_END
            elif self._status == self.ACTSTATUS_FINEMANO:
                self._fsm.on_restore_mano()
                self._newsts = self.ACTSTATUS_END
            else:
                pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def man_scarta_carta(self, player, c):
        try:
            self._fsm.scarta_sub(player, c)

            if self._fsm.get_num_scarti() <= 0:
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
            if self._fsm.is_giocabile(c.get_id()) and self._fsm.player_has_carta(self._fsm.get_player(), c):
                if self._status == self.ACTSTATUS_PRIMA_CARTA_1:
                    self._fsm.set_apertura(c)
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.get_num_scarti() > 0:
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_1
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.get_num_scarti()) + " carte.")
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_1
                elif self._status == self.ACTSTATUS_PRIMA_CARTA_2:
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.get_num_scarti() > 0:
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_2
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.get_num_scarti()) + " carte.")
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_2
                elif self._status == self.ACTSTATUS_PRIMA_CARTA_3:
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.get_num_scarti() > 0:
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_3
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.get_num_scarti()) + " carte.")
                    else:
                        self._newsts = self.ACTSTATUS_DICHIARA_VERSICOLE_3
                elif self._status == self.ACTSTATUS_PRIMA_CARTA_4:
                    self._fsm.inizializza_versicole()
                    self._fsm.calata(c)
                    if self._fsm.get_num_scarti() > 0:
                        self._newsts = self.ACTSTATUS_SCARTA_CARTA_4
                        self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.get_num_scarti()) + " carte.")
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
                    self.man_scarta_carta(self._fsm.get_player(), c)

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
                        if self._fsm.player_has_carta(self._fsm.get_player(), c) and self._fsm.is_giocabile(cid):
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
                    self._fsm.show_deck_packed(DeckId.DECK_POZZO, p.get_position())
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
            '''().  Ogni volta che una carta di conto viene presa dalla coppia avversaria, questa ne segna subito
                il valore. Si dice che muore rispettivamente un 3, un 5 o un 10 in base al valore della carta.
                 La perdita di una carta di conto è quindi una perdita tripla: non se ne segnerà infatti alla fine
                il valore, valore che verrà invece segnato dagli avversari che in più segnano subito un bonus extra
                per la carta che muore. Se una carta viene catturata dal compagno, si dice che muore in casa e
                non vale come extra.
            '''
            if is_conto(c1[0]):
                # I punti persi dagli avversari si contano due volte, alla presa e nel conto finale
                self._fsm.marca_punti(c1[0], self._winner)
                echo_message("Cade " + str(c1[0]))
            if is_conto(c2[0]):
                # I punti persi dagli avversari si contano due volte, alla presa e nel conto finale
                self._fsm.marca_punti(c2[0], self._winner)
                echo_message("Cade " + str(c2[0]))
            self._fsm.raccogli_carte(self._winner, player1, True)
            self._fsm.raccogli_carte(self._winner, player2, True)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def presa_coppia(self, player1):
        try:
            player2 = self._fsm.get_compagno(player1)
            self._fsm.raccogli_carte(self._winner, player1)
            self._fsm.raccogli_carte(self._winner, player2)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def presa(self):
        try:
            (self._winner, c_win) = self._fsm.get_winner()
            assert self._winner is not None
            echo_message("Mano a " + str(self._winner) + " con " + str(c_win))

            self.presa_coppia(self._winner)
            self.presa_avversari(self._fsm.get_next_player(self._winner))

            self._fsm.set_player(self._winner)
            #self._fsm._delegate_presa(self._winner, c_list)

            '''
            (). Se un giocatore non ha più tarocchi si dice che cade e può scoprire tutte le carte che gli restano;
             da ora in poi non giocherà più (come il morto nel Bridge), ma sarà il vincitore di ogni singola mano a
              scegliere la carta che deve giocare nella successiva, ovviamente rispettando l'obbligo di rispondere a seme, se possibile,
             altrimenti giocando una carta qualsiasi, non avendo, appunto, più tarocchi. Come è facile capire, si tratta di
             una scelta da non farsi se si possiedono ancora dei Re oppure il Matto.È importante ricordare che i giocatori
             possono in qualsiasi momento guardare tutte le carte prese dalla coppia di cui fanno parte.
            '''
            self._fsm._cid_apertura = None
            if self._fsm.get_deck_len(DeckId.DECK_MANO, self._winner) > 0:
                self._newsts = self.ACTSTATUS_CHECK_CADUTO_1
            else:
                self._fsm._delegate_append_html_text("Ultima presa: +10 punti")
                self.manage_fine_mano(self._winner)
                self._newsts = self.ACTSTATUS_FINEMANO
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset_giro_singolo(self):
        try:
            self._fsm._cid_apertura = None
            self._tagliato = False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def check_caduto(self, player=None):
        try:
            # First event
            if not self._fsm.is_caduto(player) and self._fsm.cascare_enabled(player):
                self.show_timed_popup("<p>Cade " + str(player) + " e scopre le sue carte</p>", 1)
                self._fsm.on_cade(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
