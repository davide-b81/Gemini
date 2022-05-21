'''
Created on 7 gen 2022

@author: david
'''#
from time import monotonic
from importlib.resources import _
from main.globals import *
from main.exception_man import ExceptionMan
from game.germini.strategia import Strategia
from decks.carta import Carta
from decks.mazzo import Mazzo
from game.germini.action_distribuzione import ActionDistribuzione
from game.germini.action_fola import ActionFola
from game.germini.action_partita import ActionPartita
from game.germini.action_mescola import ActionMescola
from game.germini.action_punteggi import ActionPunteggi
from game.germini.action_taglia import ActionTaglia
from game.germini.versicole_manager import VersicoleManager
from game.fsm_gioco import FsmGioco

#from oggetti.posizioni import *
#from oggetti.stringhe import _
from decks.carta_id import *
from game.germini.punteggi import carte_conto, carte_sopraventi


def conteggia_mazzetti(deck):
    try:
        i = 0
        while len(deck) > 0 and i < 14:
            cartaP = deck.pop_carta(Qualita.CARTA_DICONTO)
            carta1 = deck.pop_carta(Qualita.CARTA_CONTO_0)
            carta2 = deck.pop_carta(Qualita.CARTA_CONTO_0)
            if carta2 is None or carta1 is None or cartaP is None:
                break
            else:
                i = i + 1

        return len(deck)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)


class FsmGermini(FsmGioco):
    '''
    classdocs
    '''
    _strategia = None
    _versicole = {}
    STATUS_PUNTEGGI = "STATUS_PUNTEGGI"
    STATUS_DISTRIBUZIONE = "STATUS_DISTRIBUZIONE"
    STATUS_CADE = "STATUS_CADE"
    STATUS_FOLA = "STATUS_FOLA"
    STATUS_PARTITA = "STATUS_PARTITA"
    STATUS_PRESA = "STATUS_PRESA"

    def __init__(self, gamman=None, genman=None):
        try:
            '''
            Constructor
            '''
            super().__init__(gamman, genman)

            # Actions
            self.add_action(self.STATUS_MESCOLA, ActionMescola(self))
            self.add_action(self.STATUS_TAGLIA, ActionTaglia(self))
            self.add_action(self.STATUS_DISTRIBUZIONE, ActionDistribuzione(self))
            self.add_action(self.STATUS_FOLA, ActionFola(self))
            self.add_action(self.STATUS_PARTITA, ActionPartita(self))
            self.add_action(self.STATUS_PUNTEGGI, ActionPunteggi(self))

            self.add_state(self.STATUS_GIOCO_BEGIN, self.gioco_begin)
            self.add_state(self.STATUS_MESCOLA, self.mescola)
            self.add_state(self.STATUS_TAGLIA, self.taglia)
            self.add_state(self.STATUS_DISTRIBUZIONE, self.distribuisci)
            self.add_state(self.STATUS_FOLA, self.fola)
            self.add_state(self.STATUS_PARTITA, self.partita)
            self.add_state(self.STATUS_PUNTEGGI, self.punteggio)
            self.set_postazioni([POSTAZIONE_NORD, POSTAZIONE_EST, POSTAZIONE_SUD, POSTAZIONE_OVEST])
            self._t_sub_status = monotonic()

            self._strategia = Strategia(self, self._game_man)
            for ppos in self._game_man.get_postazioni():
                self._versicole[ppos] = VersicoleManager()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_game(self):
        try:
            super().update_game()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def start_game(self):
        try:
            super().start_game()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gioco_begin(self):
        try:
            if self.step_ready():
                echo_message("================ INIZIO =================")
                self._append_html_text("<p>================ INIZIO =================</p>")
                self._game_man.pulisci_tavola()
                self.new_status = FsmGioco.STATUS_DISTRIBUZIONE
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizio(self):
        try:
            if self.step_ready():
                self._cid_apertura = None
                self._status_next = FsmGioco.STATUS_GIRO
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def exe_status_update(self, status, next):
        try:
            if self.step_ready():
                self._actions[status].update()
                if self._actions[status].finished():
                    self._status_next = next
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def mescola(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_MESCOLA, FsmGermini.STATUS_TAGLIA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def taglia(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_TAGLIA, FsmGermini.STATUS_DISTRIBUZIONE)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuisci(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_DISTRIBUZIONE, FsmGermini.STATUS_FOLA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def giocatore_scarta_carta(self, c, player=None):
        try:
            if player is None:
                player = self.get_player()
            self.sposta_e_nascondi(c, DeckId.DECK_MANO, DeckId.DECK_SCARTO, FRONTE_COPERTA, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def scarta_sub(self, player, c):
        try:
            rubate = self.get_list_ca(DeckId.DECK_RUBATE, player.get_position())
            if self.player_has_carta(player, c):
                self.giocatore_scarta_carta(c, player)
                self.sposta_e_stendi(rubate[0], DeckId.DECK_RUBATE, DeckId.DECK_MANO, None, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def giocatore_scarta(self, player=None):
        try:
            if player is None:
                player = self.get_player()
            c = Strategia.scarta_carta(player)
            echo_message(_(str(player) + " scarta " + str(c)))
            self.scarta_sub(player, c)
            return c
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_coppie(self, c1, c2, mazziere):
        try:
            if not c1[0].get_simulated():
                c1[0].set_position(POSTAZIONE_SUD)
                c1[1].set_position(POSTAZIONE_NORD)
                c2[0].set_position(POSTAZIONE_EST)
                c2[1].set_position(POSTAZIONE_OVEST)
            elif not c1[1].get_simulated():
                c1[1].set_position(POSTAZIONE_SUD)
                c1[0].set_position(POSTAZIONE_NORD)
                c2[0].set_position(POSTAZIONE_EST)
                c2[1].set_position(POSTAZIONE_OVEST)
            elif not c2[0].get_simulated():
                c2[0].set_position(POSTAZIONE_SUD)
                c2[1].set_position(POSTAZIONE_NORD)
                c1[0].set_position(POSTAZIONE_EST)
                c1[1].set_position(POSTAZIONE_OVEST)
            elif not c2[1].get_simulated():
                c2[1].set_position(POSTAZIONE_SUD)
                c2[0].set_position(POSTAZIONE_NORD)
                c1[0].set_position(POSTAZIONE_EST)
                c1[1].set_position(POSTAZIONE_OVEST)
            else:
                # Demo mode
                c1[0].set_position(POSTAZIONE_NORD)
                c1[1].set_position(POSTAZIONE_SUD)
                c2[0].set_position(POSTAZIONE_EST)
                c2[1].set_position(POSTAZIONE_OVEST)
            self.update_mazziere(mazziere)
            self._delegate_update_players()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_apertura(self, c):
        try:
            self._cid_apertura = c.get_id()
            s = get_seme(self._cid_apertura)
            Strategia.on_prima(c)
            self._delegate_append_html_text("<p>Palo di apertura " + seme_name[s] + " </p>")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def partita(self):
        """
         (). Le carte vengono giocate in senso antiorario, iniziando dal giocatore seduto alla destra del mazziere.
          Subito dopo aver giocato la loro prima carta, i giocatori che possiedono una o più versicole devono mostrarle
          per poterne segnare il valore. Non appena viene raccolta la prima mano, non è più possibile segnare versicole.
        """
        try:
            self.exe_status_update(FsmGermini.STATUS_PARTITA, FsmGermini.STATUS_GIRO)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fola(self):
        """
         (). Al termine della prima mano, le carte precedentemente scartate (a causa dei rubati o dei pigliati)
          devono essere mostrate. Il compagno del mazziere deve annunciarle a voce alta, specificando chi le ha
          scartate e ponendole nella fola. Dopodiché comunica di nuovo la fola nel modo precedentemente descritto
          e la passa al mazziere che la pone sul tavolo, alla sua destra.
        """
        try:
            self.exe_status_update(FsmGermini.STATUS_FOLA, FsmGermini.STATUS_PARTITA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
    (). Come in molti giochi, la carta più alta vince la mano. Il giocatore che l'ha giocata raccoglie le carte,
     le unisce a quelle della sua squadra (che vengono quindi tenute tutte assieme) e gioca la prima carta della
     mano successiva. Ogni volta che una carta di conto viene presa dalla coppia avversaria, questa ne segna subito
     il valore. Si dice che muore rispettivamente un 3, un 5 o un 10 in base al valore della carta. La perdita di una 
     carta di conto è quindi una perdita tripla: non se ne segnerà infatti alla fine il valore, valore che verrà invece
     segnato dagli avversari che in più segnano subito un bonus extra per la carta che muore. Se una carta viene
     catturata dal compagno, si dice che muore in casa e non vale come extra.
    '''

    def punteggio(self):
        try:
            pass #self.exe_status_update(FsmGermini.STATUS_CONTEGGIO, FsmGermini.STATUS_FINEMANO)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
    '''

Ogni coppia ha cinque “pesci” e cinque gettoni o monete con i quali viene segnato il punteggio conseguito
durante il gioco. Un gettone () vale un punto, un pesce () dieci mentre due gettoni posti uno sull'altro
() indicano cinque punti. I gettoni posti alla sinistra di un pesce devono essere sommati al punteggio
mentre quelli posti a destra di un pesce devono essere sottratti come mostrano i seguenti esempi:
 indica 7 punti
 8 punti (si può anche segnare con: )
 34 punti
 48 punti
 26 punti
Attenzione: come già detto le coppie non segnano il punteggio effettivamente conseguito ma solo la
differenza con quello degli avversari. In particolare il punteggio minore viene sottratto dal maggiore e
viene segnata solo la differenza. Se, per esempio, la coppia A ha segnato 15 punti e ora la coppia B segna
32 punti, questa ultima segnerà solo 17 mentre la coppia A non segnerà niente.
    '''

    '''
    (). Se il mazziere commette un errore nella distribuzione delle carte, l'errore può essere corretto fintantoché gli
     altri giocatori non hanno preso le carte e la ventunesima non è stata ancora distribuita. In caso contrario si
     applica una penalità di 10 punti più 10 punti per carta che vengono segnati a vantaggio degli avversari
     del mazziere. Dopodiché, prima che il mazziere possa scoprire o pigliare, un giocatore che ha meno carte del
     previsto prende dalla fola le carte mancanti senza guardarle né mostrarle. Al contrario, un giocatore che ha
     ricevuto troppe carte può scartare quelle in eccesso ma non può in questo modo farsi un fallio
     (restare scoperto in un seme). Le carte dimenticate (ad esempio in un angolo o sotto il tavolo) fanno parte della
     fola, indipendentemente dal fatto che siano o meno delle carte di conto; in questo caso non è prevista la penalità.
     Se nella fola vi sono ora troppe carte, quelle in eccesso vengono prese dal mazziere.
    '''

    '''
  Se un giocatore ha troppe - o troppe poche - carte e si rende conto di questo solo durante il gioco, lui e il suo
  compagno possono segnare solo le carte e l'ultima oltre a quanto era stato segnato durante il gioco. Se non viene
  risposto a seme oppure non viene tagliato con un tarocco, al momento che viene rilevato l'errore il giocatore deve
  pagare due resti a ciascuno dei giocatori avversari ma la mano resta valida e non viene rigiocata. È questo il solo
  caso in cui il compagno del giocatore che commette l'errore può risultare avvantaggiato dall'errore stesso.
    '''
    def gioca_carta(self, player):
        try:
            return Strategia.gioca_carta(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gioca_carta_caduto(self, player, caduto):
        try:
            return Strategia.gioca_carta_caduto(player, caduto)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_fallio(self, seme, player):
        try:
            ca = self._game_man.get_carte_mano(player)
            for c in ca:
                if seme_carta(c) == seme:
                    return False
            return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    # TODO: Nel caso un seme venga giocato la prima volta e tagliato, il giocatore di seguito che ha il Re lo deve giocare
    def is_giocabile(self, cid):
        """
         (). Prendere una mano: Finché è possibile si deve rispondere a ciascun seme, tarocchi inclusi; nel caso non si
          possiedano carte del seme giocato è necessario giocare un tarocco (ma non è obbligatorio surtagliare,
          ovvero superare il tarocco precedente). Nel caso un seme venga giocato per la prima volta e tagliato
          con un tarocco, un successivo giocatore che abbia il Re è obbligato a giocarlo, ed è una regola
          peculiare delle Minchiate. Ad un secondo giro può invece giocare una carta più bassa o il Matto.
        """
        try:
            player = self.get_player()
            if self._cid_apertura == None:
                if cid == CartaId.MATTO_0:
                    if self.get_num_carte_prese(player) > 0:
                        return True
                    else:
                        return False
                return True

            elif cid == CartaId.MATTO_0:
                if self.get_num_carte_prese(player) > 0:
                    return True
                else:
                    return False

            elif is_tarocco(self._cid_apertura):
                if is_tarocco(cid):
                    return True
                elif not self._game_man.has_seme(player, Palo.TRIONFO):
                    return True
                else:
                    return False

            elif seme_carta(cid) == seme_carta(self._cid_apertura):
                return True

            elif not self._game_man.has_seme(player, get_seme(self._cid_apertura)):
                if is_tarocco(cid):
                    return True
                else:
                    if self._game_man.has_seme(player, Palo.TRIONFO):
                        return False
                    else:
                        return True
            else:
                return False

            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_giocabile_caduto(self, cid):
        try:
            if self._cid_apertura == None:
                return True
            #elif self.giocatore_turno.get_caduto():
            #    self.show_popup(True, "<p>Cade " + str(self.giocatore_turno) + "</p>")
            #    return True

            elif cid == CartaId.MATTO_0:
                return True

            elif is_tarocco(self._cid_apertura):
                if is_tarocco(cid):
                    return True
                elif not self._game_man.has_seme(self.get_player(), Palo.TRIONFO):
                    return True
                else:
                    return False

            elif seme_carta(cid) == seme_carta(self._cid_apertura):
                return True

            elif not self._game_man.has_seme(self.get_player(), get_seme(self._cid_apertura)):
                if is_tarocco(cid):
                    return True
                else:
                    if self._game_man.has_seme(self.get_player(), Palo.TRIONFO):
                        return False
                    else:
                        if self.cascare_enabled(self.get_player()):
                            return True
                        else:
                            print("CADE " + str(self.get_player()))
                            #self.on_cade(self.get_player())
                        return True
            else:
                return False

        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
        return False

    def on_popup(self):
        try:
            if self._status in self._actions:
                self._actions[self._status].on_popup()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta(self, cid):
        try:
            if self._status in self._actions:
                self._actions[self._status].on_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_presa(self, winner, c_list):
        try:
            Strategia.on_presa(winner, c_list)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def metti_in_lista(self, lista, cc):
        try:
            if lista is None:
                lista = []
            for c in cc:
                lista.append(c)
            return lista
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def man_risultato_giro(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def ruba_da_mazzo(self, player):
        try:
            self._game_man.preleva_dal_mazzo(1)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_caduto(self, player=None):
        try:
            if player is None:
                player = self._game_man.get_player()
            return player.get_caduto()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def carte_da_conto_in_deck(self, deck):
        try:
            d = self.get_list_ca(deck)
            for c in d:
                if c.get_id() in carte_conto:
                    return False
            return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def cascare_enabled(self, player=None):
        try:
            if player is None:
                player = self._game_man.get_player()

            for c in self._game_man.get_carte_mano(player):
                if c.get_id() in tarocco:
                    return False

            for c in self._game_man.get_carte_mano(player):
                if c.get_id() in carte_conto:
                    return False
            return True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_compagno(self, player):
        try:
            return self._game_man.get_compagno(player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_coppia(self, ppos):
        try:
            if ppos == POSTAZIONE_SUD or ppos == POSTAZIONE_NORD:
                return (self.get_player_at_pos(POSTAZIONE_NORD), self.get_player_at_pos(POSTAZIONE_SUD))
            elif ppos == POSTAZIONE_EST or ppos == POSTAZIONE_OVEST:
                return (self.get_player_at_pos(POSTAZIONE_EST), self.get_player_at_pos(POSTAZIONE_OVEST))
            else:
                raise Exception("Coppia sconosciuta.")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_resti(self, diff):
        res = 0
        while diff > 0:
            if diff > 0:
                res = res + 1
            diff = diff - 60
        return res

    def get_resti_coppia(self):
        try:
            ptsNS = self.get_punti_coppia(POSTAZIONE_NORD)
            ptsEO = self.get_punti_coppia(POSTAZIONE_EST)

            rNS = 0
            rEO = 0
            diff = abs(ptsNS-ptsEO)
            r = self.get_num_resti(diff)
            if ptsNS == 0:
                # Nel caso in cui una coppia non abbia fatto neanche una presa
                rEO = max(14, r)
            elif ptsEO == 0:
                rNS = max(14, r)
            elif ptsNS >= ptsEO:
                rNS = self.get_num_resti(diff)
            else:
                rEO = self.get_num_resti(diff)
            return (rNS, rEO)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_punti_coppia(self, ppos):
        try:
            pts = 0
            (p1, p2) = self.get_coppia(ppos)
            if p1 is not None:
                pts = pts + p1.get_punti_mano()
            if p2 is not None:
                pts = pts + p2.get_punti_mano()
            return pts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_compagno_mazziere(self):
        try:
            if self._globals.get_debug():
                return self.get_player_at_pos(POSTAZIONE_SUD)

            pos = self._game_man.get_opposit_pos(self._game_man.get_mazziere().get_position())
            return self._game_man.get_player_at_pos(pos)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizializza_versicole(self, player=None):
        try:
            if player is None:
                player = self._game_man.get_player()

            self._versicole[player.get_position()].reset()
            ca = self.get_carte_mano(player)
            self._versicole[player.get_position()].riempi(ca)
            ca = self.get_carte_rubate(player)
            self._versicole[player.get_position()].riempi(ca)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gestisci_carte_versicola(self, ca, player=None):
        try:
            if player is None:
                player = self._game_man.get_player()
            if player.get_position() in self._versicole:
                self._versicole[player.get_position()].gestisci_carte(ca)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_versicole_dichiarazione(self, player=None):
        try:
            txt = ""
            if player is None:
                player = self._game_man.get_player()
            if player.get_position() in self._versicole:
                txt = self._versicole[player.get_position()].get_txt_description()
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def assegna_resti(self, ppos, resti):
        try:
            player = self._game_man.get_player_at_pos(ppos)
            player.add_resti(resti)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_restore_mano(self):
        try:
            for p in self._game_man.get_giocatori():
                p.on_fine_mano()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def conteggia_mazzetti_ns(self):
        try:
            lista = []
            d1 = self.get_deck(DeckId.DECK_PRESE, POSTAZIONE_NORD)
            d2 = self.get_deck(DeckId.DECK_PRESE, POSTAZIONE_SUD)
            lista.append(d1.get_carte())
            lista.append(d2.get_carte())
            return conteggia_mazzetti(lista)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def conteggia_mazzetti_eo(self):
        try:
            lista = []
            d1 = self.get_deck(DeckId.DECK_PRESE, POSTAZIONE_EST)
            d2 = self.get_deck(DeckId.DECK_PRESE, POSTAZIONE_OVEST)
            d1 <<= d2
            return conteggia_mazzetti(d1)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_fine_mano(self, winner):
        try:
            """
            (). La coppia che ha fatto l'ultima presa aggiungerà per questa dieci punti.
            """
            print(str(winner) + " + 10 punti per l'ultima presa")
            self._game_man.marca_punti(winner, 10)
            """
            (). Al termine di ognuna delle quattro partite che formano un giro, il punteggio viene così calcolato:
             Ogni coppia riunisce le prese fatte e pone sotto a ciascuna carta di conto due carte senza valore (cartiglie,
             tarocchini o sopraventi) creando così tanti mazzetti di tre carte ciascuno. A partire dal quattordicesimo mazzetto
             tutte le carte, anche quelle senza valore, valgono un punto. Supponiamo ad esempio che una coppia abbia preso 64
             carte, 17 delle quali sono carte di conto. Poiché i primi 14 mazzetti (dei 17 fatti) contengono 14x3=42 carte,
             la coppia guadagna 64-42=22 punti; Dopo questi punti vengono quindi calcolati quelli delle versicole;
             si ricordi che la coppia che ha preso il matto ne aggiunge il valore a tutte le versicole fatte. 
            """
            pts = self.conteggia_mazzetti_ns()
            if pts != 0:
                print("Coppia N-S " + str(pts) + " punti per le carte oltre i 14 mazzetti")
                self._game_man.marca_punti(self.get_player_at_pos(POSTAZIONE_NORD), pts)

            pts = self.conteggia_mazzetti_eo()
            if pts != 0:
                print("Coppia E-O " + str(pts) + " punti per le carte oltre i 14 mazzetti")
                self._game_man.marca_punti(self.get_player_at_pos(POSTAZIONE_SUD), pts)

            """
             Si contano poi le carte di conto, Matto incluso, iniziando
             di solito dai Papi e dai Re; si sommano a questo risultato i punti segnati durante il gioco e viene infine
             calcolata la differenza fra i punteggi conseguiti dalle due coppie. 60 punti di differenza costituiscono un resto.
             Un resto viene pagato immediatamente in base a quanto concordato prima dell'inizio del gioco.
             Al termine del gioco anche un solo punto costituisce un resto così da 61 a 120 punti valgono due resti,
             da 121 a 180 tre e così via. Nell'altamente improbabile caso che una coppia non effettui neppure una presa,
             la perdita viene raddoppiata e il punteggio del gioco è fissato a 2x7=14 resti oltre al punteggio già fatto che
             viene anch'esso raddoppiato. I resti in precedenza già realizzati e pagati non vengono invece raddoppiati.
            """
            (rNS, rEO) = self.get_resti_coppia()
            self.assegna_resti(POSTAZIONE_NORD, rNS)
            self.assegna_resti(POSTAZIONE_SUD, rNS)
            self.assegna_resti(POSTAZIONE_EST, rEO)
            self.assegna_resti(POSTAZIONE_OVEST, rEO)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def marca_punti_versicole(self, c, player=None):
        try:
            if player == None:
                player = self.get_player()
            pts = self._versicole[player.get_position()].get_punti_totali()
            self._game_man.marca_punti(player, pts)
            return pts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def da_pigliare(self, player=None):
        try:
            if player is None:
                player = self._game_man.get_player()
            d = self.get_list_ca(DeckId.DECK_FOLA, player.get_position())
            for c in d:
                if c.get_id() in carte_conto or c.get_id() in carte_sopraventi:
                    return True
            return False
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_num_scarti(self, player=None):
        try:
            if player is None:
                player = self._game_man.get_player()
            return self.get_deck_len(DeckId.DECK_RUBATE, player)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_resti(self):
        try:
            return self._game_man.get_text_resti()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_text_punti_mano(self):
        try:
            txt = "<p>Punteggi mano:<br/>"
            ptsNS = self.get_punti_coppia(POSTAZIONE_NORD)
            (pN, pS) = self.get_coppia(POSTAZIONE_NORD)
            if pN is not None and pS is not None:
                txt = txt + str(pN) + "-" + str(pS) + ": " + str(ptsNS) + "<br/>"
            ptsEO = self.get_punti_coppia(POSTAZIONE_EST)
            (pE, pO) = self.get_coppia(POSTAZIONE_EST)
            if pE is not None and pO is not None:
                txt = txt + str(pE) + "-" + str(pO) + ": " + str(ptsEO) + "<br/>"
            txt = txt + "</p>"
            return txt
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_winner(self):
        try:
            ca = self._game_man.get_deck_pos(DeckId.DECK_TAVOLA)
            c_s = ca[POSTAZIONE_SUD]
            c_n = ca[POSTAZIONE_NORD]
            c_w = ca[POSTAZIONE_OVEST]
            c_e = ca[POSTAZIONE_EST]

            c_win = get_greatest_card(self.get_carte_in_tavola())

            if c_win in c_s:
                winner = self.get_player_at_pos(POSTAZIONE_SUD)
            elif c_win in c_w:
                winner = self.get_player_at_pos(POSTAZIONE_OVEST)
            elif c_win in c_n:
                winner = self.get_player_at_pos(POSTAZIONE_NORD)
            elif c_win in c_e:
                winner = self.get_player_at_pos(POSTAZIONE_EST)
            else:
                echo_message("Warning no winner")
                return (None, None)
            return (winner, c_win)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reprJSON(self):
        return "PPPP"

if __name__ == '__main__':
    man = FsmGermini()
    try:
        print(man.reprJSON())
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
