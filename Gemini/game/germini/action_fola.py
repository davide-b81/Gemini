#   '''
#  Created on 16 2 2022
#  @author: david
#  '''

from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia, is_sopraventi, count_seme, Palo, seme_name
from game.germini.action import Action
from game.germini.punteggi import carte_conto, carte_sopraventi
from game.germini.strategia import Strategia
from main.exception_man import ExceptionMan
from main.globals import echo_message, FRONTE_SCOPERTA
from oggetti.posizioni import DeckId


class ActionFola(Action):
    ACTSTATUS_FOLA_MARCA = "ACTSTATUS_FOLA_MARCA"
    ACTSTATUS_FOLA_PIGLIA = "ACTSTATUS_FOLA_PIGLIA"
    ACTSTATUS_FOLA_VEDI = "ACTSTATUS_FOLA_VEDI"
    ACTSTATUS_SCARTA_ANNUNCIA = "ACTSTATUS_SCARTA_ANNUNCIA"
    ACTSTATUS_SCARTA = "ACTSTATUS_SCARTA"
    ACTSTATUS_FOLA_DESCRIVE = "ACTSTATUS_FOLA_DESCRIVE"
    ACTSTATUS_PASSA = "ACTSTATUS_PASSA"
    ACTSTATUS_SHOWULTIMA = "ACTSTATUS_SHOWULTIMA"

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            self.reset()
            # Posiziona mazzo e lo rende visibile
            echo_message(_("ActionFola - Crea la fola"))
            '''
            (5). Il mazziere conta ora il tallone delle carte rimaste che, a meno di errori, consiste di 14 carte
              meno le carte rubate. Nell'improbabile caso che siano state rubate più di 14 carte,
              il mazziere avrà inizialmente meno di 21 carte, in attesa che il "ladro" scarti le sue carte in eccesso.
              In caso contrario scopre la sua ventunesima carta segnando il suo eventuale valore.
             '''
            self._fsm.set_player(self._fsm.get_mazziere())
            self._fsm.fai_la_fola()
            self._fsm.mostra_mazzo(DeckId.DECK_MAZZO, self._fsm.get_mazziere().get_position())
            self._fsm.set_lato_mazzo(DeckId.DECK_FOLA, FRONTE_SCOPERTA)
            self._newsts = self.ACTSTATUS_FOLA_MARCA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fola_descrive_sub(self, seme):
        """
        (7). La fola resta sul tavolo alla destra del mazziere. Questi può consultarla in qualsiasi momento mentre ogni
         giocatore ha il diritto di chiedergli cosa contiene. La fola viene comunicata nel modo già descritto, menzionando
         sempre i semi in ordine decrescente ovvero cominciando sempre da quello più numeroso.
        Se due o più semi hanno lo stesso numero di carte, si dice per sorte; per esempio:
         quattro coppe e una per sorte significa che denari, spade e bastoni hanno una carta ciascuno.
         Le carte della fola possono essere raggruppate anche in rosse e lunghe; ad esempio: quattro rosse, una lunga
         indica quattro di coppe, quattro di denari, una di spade e una di bastoni. Infine, se i quattro semi hanno un
         numero di carte in ordine crescente, si può ad esempio annunciare semplicemente denari, "spade, coppe, bastoni"
         intendendo che c'è una sola carta di denari, due di spade, tre di coppe e quattro di bastoni.
        """
        try:
            txt = ""
            fo = self._fsm.get_deck(DeckId.DECK_FOLA)
            n = count_seme(fo, seme)
            if n == 1:
                txt = "<br/>Una carta di " + seme_name[seme]
            elif n > 1:
                txt = "<br/>" + str(n) +" carte di " + seme_name[seme]
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fola_descrive(self):
        """
        (6). A questo punto passa quindi al suo compagno il resto della fola, questi la guarda e comunica agli avversari
          il numero di carte di ogni seme (per esempio: due Coppe, due Bastoni, una Spade, zero Denari) omettendo di
          comunicare il numero dei tarocchi.
        """
        try:
            txt = "La fola contiene" + \
                  self.fola_descrive_sub(Palo.DENARI) + self.fola_descrive_sub(Palo.COPPE) + \
                  self.fola_descrive_sub(Palo.SPADE) + self.fola_descrive_sub(Palo.BASTONI)
            self.show_timed_popup("<p>" + txt + "</p>", 0.05)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            if self._status == self.ACTSTATUS_FOLA_MARCA:
                if self._fsm.simulated():
                    c = self._fsm.get_prima(DeckId.DECK_FOLA, self._fsm.get_player())
                    if c is not None:
                        if is_sopraventi(c.get_id()) or c.get_id() in carte_conto:
                            self._fsm.move_card_and_repos(c, DeckId.DECK_FOLA, DeckId.DECK_RUBATE, FRONTE_SCOPERTA, self._fsm.get_player())
                            self._fsm.mostra_rubate(self._fsm.get_position_turno())
                            if c.get_id() in carte_conto:
                                print(str(self._fsm.get_player()) + " prende " + str(c) + " e marca " + str(carte_conto[c.get_id()]) + "punti")
                        else:
                            self._fsm.mostra_fola(self._fsm.get_mazziere())
                            print("Finisce il rubare di " + str(self._fsm.get_player()))
                            self._newsts = self.ACTSTATUS_FOLA_DESCRIVE
                    else:
                        raise NotImplemented("Sono state rubate tutte le 13 carte...")
            elif self._status == self.ACTSTATUS_FOLA_VEDI:
                #if not self._fsm.simulated():
                #    self._fsm.mostra_fola(self._fsm.get_player())
                self._newsts = self.ACTSTATUS_FOLA_PIGLIA
                print(str(self._fsm.get_player()) + " piglia le carte di conto")

            elif self._status == self.ACTSTATUS_FOLA_PIGLIA:
                if self._fsm.simulated():
                    if not self._fsm.da_pigliare():
                        player = self._fsm.get_compagno_mazziere()
                        self._fsm.set_player(player)
                        self._fsm.passa_fola(player)
                        self._newsts = self.ACTSTATUS_FOLA_DESCRIVE
                        print("Passa la fola al compagno")
                    else:
                        c = Strategia.manager.get_piglia()
                        assert c is not None
                        assert self._fsm.deck_contains(c.get_id(), DeckId.DECK_FOLA)
                        self._fsm.sposta_carta(c, DeckId.DECK_FOLA, DeckId.DECK_RUBATE, self._fsm.get_player())
                        self._fsm.mostra_rubate(self._fsm.get_position_turno())
                        print(str(self._fsm.get_player()) + " piglia " + str(c))

            elif self._status == self.ACTSTATUS_FOLA_DESCRIVE:
                if not self._wait_popup:
                    print(str(self._fsm.get_player()) + " guarda le carte rimaste nella fola e le comunica agli altri")
                    self.fola_descrive()
                    """
                    (6b). Attenzione: se sono state rubate o pigliate alcune carte, ne devono essere scartate altrettante. 
                    Queste carte vengono poste coperte sul tavolo, davanti al giocatore, finché non viene giocata la prima carta.
                    Finalmente, ogni giocatore dovrebbe ora avere 21 carte e quello che siede alla destra del mazziere può giocare
                    la sua prima carta.
                    """
                    player = self._fsm.get_mazziere()
                    self._fsm.set_player(player)
                    self._fsm.nascondi_fola(player)
                    if self._fsm.scartare(player):
                        self._newsts = self.ACTSTATUS_SCARTA_ANNUNCIA
                    else:
                        self._newsts = self.ACTSTATUS_END
            elif self._status == self.ACTSTATUS_SCARTA_ANNUNCIA:
                if not self._wait_popup:
                    self.show_timed_popup(str(self._fsm.get_player()) + " scarta n=" + str(self._fsm.scartare()) + " carte.")
                    self._newsts = self.ACTSTATUS_SCARTA
            elif self._status == self.ACTSTATUS_SCARTA:
                if not self._wait_popup:
                    if self._fsm.simulated():
                        rubate = self._fsm.get_deck(DeckId.DECK_RUBATE, self._fsm.get_position_turno())
                        self._fsm.giocatore_scarta(self._fsm.get_player())
                        self._newsts = self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def man_scarta_carta_click(self, c):
        try:
            pass
                #self._fsm.mostra_scarto(self._fsm.get_player())
                #self._game_man.stendi_deck(DeckId.DECK_MANO, player.get_position())
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            if self._status == self.ACTSTATUS_FOLA_MARCA:
                if not self._fsm.simulated(self._fsm.get_player()) and self._fsm.deck_contains(cid, DeckId.DECK_FOLA):
                    c = self._fsm.get_prima(DeckId.DECK_FOLA, self._fsm.get_player())
                    if (c is not None) and (str(cid) == c.get_name()):
                        if is_sopraventi(c.get_id()):
                            self._fsm.move_card_and_repos(c, DeckId.DECK_FOLA, DeckId.DECK_RUBATE, FRONTE_SCOPERTA, self._fsm.get_player())
                        elif c.get_id() in carte_conto:
                            self._fsm.move_card_and_repos(c, DeckId.DECK_FOLA, DeckId.DECK_RUBATE, FRONTE_SCOPERTA, self._fsm.get_player())
                            print(str(self._fsm.get_player()) + " marca i punti di " + str(c) + ": " + str(carte_conto[c.get_id()]) + " punti.")
                        else:
                            self._fsm.mostra_fola(self._fsm.get_player())
                            #TODO: Vede le prime 13 carte
                            print("Finisce il rubare del mazziere")
                            self._newsts = self.ACTSTATUS_FOLA_VEDI
                    else:
                        self._fsm.mostra_fola(self._fsm.get_player())
                        #TODO: Vede le prime 13 carte
                        print("Finisce il rubare del mazziere")
                        self._newsts = self.ACTSTATUS_FOLA_VEDI
            elif self._status == self.ACTSTATUS_FOLA_VEDI:
                pass
            elif self._status == self.ACTSTATUS_FOLA_PIGLIA:
                c = self._fsm.get_carta(cid)
                if not self._fsm.simulated() and self._fsm.deck_contains(c.get_id(), DeckId.DECK_FOLA):
                    if c.get_id() in carte_conto or c.get_id() in carte_sopraventi:
                        self._fsm.move_card_and_repos(c, DeckId.DECK_FOLA, DeckId.DECK_RUBATE, FRONTE_SCOPERTA, self._fsm.get_player())
                        self._fsm.mostra_rubate(self._fsm.get_position_turno())
                        print(str(self._fsm.get_player()) + " piglia " + str(c))
                    if not self._fsm.da_pigliare():
                        player = self._fsm.get_compagno_mazziere()
                        self._fsm.set_player(player)
                        self._fsm.passa_fola(player)
                        self._newsts = self.ACTSTATUS_FOLA_DESCRIVE
                        print("Passa la fola al compagno")
            elif self._status == self.ACTSTATUS_PASSA:
                pass
            elif self._status == self.ACTSTATUS_FOLA_DESCRIVE:
                pass
            elif self._status == self.ACTSTATUS_SCARTA_ANNUNCIA:
                pass
            elif self._status == self.ACTSTATUS_SCARTA:
                if not self._fsm.simulated() and self._fsm.player_has_carta(self._fsm.get_player(), cid):
                    self._fsm.scarta_sub(cid)
                    if not self._fsm.scartare(self._fsm.get_player()):
                        self._newsts = self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
