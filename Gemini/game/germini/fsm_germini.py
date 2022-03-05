'''
Created on 7 gen 2022

@author: david
'''
from game.germini.action_carta_piu_alta import ActionCartaPiuAlta
from game.germini.action_dichiara import ActionDichiara
from game.germini.action_distribuzione import ActionDistribuzione
from game.germini.action_fola import ActionFola
from game.germini.action_giro import ActionGiro
from game.germini.action_mescola import ActionMescola
from game.germini.action_piglia import ActionPiglia
from game.germini.action_conteggio import ActionConteggio
from game.germini.action_taglia import ActionTaglia
from main.globals import *
from game.fsm_gioco import FsmGioco
from time import monotonic
from game.germini.strategia import Strategia
from oggetti.stringhe import _
from decks.carta_id import *
from game.germini.punteggi import punti_ger

class FsmGermini(FsmGioco):
    mostrata = None

    numero_giocatori = 4
    cid_apertura = None
    STATUS_GIRO = "GIRO"
    STATUS_PIGLIA = "PIGLIA"
    STATUS_RUBA = "RUBA"
    STATUS_FINEMANO = "FINEMANO"
    STATUS_SHOW_ULTIMA = "STATUS_SHOW_ULTIMA"
    STATUS_DISTRIBUZIONE = "STATUS_DISTRIBUZIONE"

    STATUS_CADE = "STATUS_CADE"
    STATUS_FOLA = "STATUS_FOLA"
    STATUS_GIRO = "STATUS_GIRO"
    STATUS_PIGLIA = "STATUS_PIGLIA"
    STATUS_PRESA = "STATUS_PRESA"
    STATUS_CONTEGGIO = "STATUS_PUNTEGGI"


    '''
    classdocs
    '''
    def __init__(self, gamman=None, genman=None):
        try:
            '''
            Constructor
            '''
            super().__init__(gamman, genman)
            # Actions
            self.add_action(self.STATUS_SORTEGGIA, ActionCartaPiuAlta(self))
            self.add_action(self.STATUS_MESCOLA, ActionMescola(self))
            self.add_action(self.STATUS_MESCOLA, ActionMescola(self))
            self.add_action(self.STATUS_TAGLIA, ActionTaglia(self))
            self.add_action(FsmGermini.STATUS_DISTRIBUZIONE, ActionDistribuzione(self))
            self.add_action(FsmGermini.STATUS_FOLA, ActionFola(self))
            self.add_action(FsmGermini.STATUS_PIGLIA, ActionPiglia(self))
            self.add_action(self.STATUS_DICHIARA, ActionDichiara(self))
            self.add_action(FsmGermini.STATUS_GIRO, ActionGiro(self))
            self.add_action(FsmGermini.STATUS_CONTEGGIO, ActionConteggio(self))

            self.add_state(self.STATUS_GIOCO_BEGIN, self.gioco_begin)
            self.add_state(self.STATUS_SORTEGGIA, self.sorteggia)
            self.add_state(self.STATUS_MESCOLA, self.mescola)
            self.add_state(self.STATUS_TAGLIA, self.taglia)
            self.add_state(FsmGermini.STATUS_DISTRIBUZIONE, self.distribuisci)
            self.add_state(self.STATUS_FOLA, self.fola)
            self.add_state(self.STATUS_PIGLIA, self.piglia)
            self.add_state(self.STATUS_DICHIARA, self.dichiara)
            self.add_state(self.STATUS_GIRO, self.giro)
            self.add_state(self.STATUS_CONTEGGIO, self.conteggio())
            self.add_state(self.STATUS_FINEMANO, self.man_risultato_giro)
            self.mostrata = None
            self._t_sub_status = monotonic()
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
            self.giocatore_turno = self.general_man.get_mazziere()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gioco_begin(self):
        try:
            if self.step_ready():
                echo_message("================ INIZIO =================")
                self._append_html_text("<p>================ INIZIO =================</p>")
                self.mostrata = None
                self.game_man.pulisci_tavola()
                self.new_status = FsmGioco.STATUS_DISTRIBUZIONE1
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def inizio(self):
        try:
            if self.step_ready():
                self.cid_apertura = None
                self._status_next = FsmGioco.STATUS_SORTEGGIA
                self.giocatore_turno = self.game_man.get_mazziere()
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

    def sorteggia(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_SORTEGGIA, FsmGermini.STATUS_MESCOLA)
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

    def dichiara(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_DICHIARA, FsmGermini.STATUS_GIRO)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def piglia(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_PIGLIA, FsmGermini.STATUS_PIGLIA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def distribuisci(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_DISTRIBUZIONE, FsmGermini.STATUS_FOLA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def giocatore_scarta(self, player, n):
        try:
            cc = Strategia.scarta_carte(player, n)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def fola(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_FOLA, FsmGermini.STATUS_DICHIARA)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
     (). Le carte vengono giocate in senso antiorario, iniziando dal giocatore seduto alla destra del mazziere.
      Subito dopo aver giocato la loro prima carta, i giocatori che possiedono una o più versicole devono mostrarle
      per poterne segnare il valore. Non appena viene raccolta la prima mano, non è più possibile segnare versicole.
    '''
    def giro(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_GIRO, FsmGermini.STATUS_CONTEGGIO)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    '''
     (). Al termine della prima mano, le carte precedentemente scartate (a causa dei rubati o dei pigliati)
      devono essere mostrate. Il compagno del mazziere deve annunciarle a voce alta, specificando chi le ha
      scartate e ponendole nella fola. Dopodiché comunica di nuovo la fola nel modo precedentemente descritto
      e la passa al mazziere che la pone sul tavolo, alla sua destra.
    '''

    '''
     (). Prendere una mano: Finché è possibile si deve rispondere a ciascun seme, tarocchi inclusi; nel caso non si
      possiedano carte del seme giocato è necessario giocare un tarocco (ma non è obbligatorio surtagliare,
      ovvero superare il tarocco precedente). Nel caso un seme venga giocato per la prima volta e tagliato
      con un tarocco, un successivo giocatore che abbia il Re è obbligato a giocarlo, ed è una regola
      peculiare delle Minchiate. Ad un secondo giro può invece giocare una carta più bassa o il Matto.
    '''

    '''
    (). Come in molti giochi, la carta più alta vince la mano. Il giocatore che l'ha giocata raccoglie le carte,
     le unisce a quelle della sua squadra (che vengono quindi tenute tutte assieme) e gioca la prima carta della
     mano successiva. Ogni volta che una carta di conto viene presa dalla coppia avversaria, questa ne segna subito
     il valore. Si dice che muore rispettivamente un 3, un 5 o un 10 in base al valore della carta. La perdita di una 
     carta di conto è quindi una perdita tripla: non se ne segnerà infatti alla fine il valore, valore che verrà invece
     segnato dagli avversari che in più segnano subito un bonus extra per la carta che muore. Se una carta viene
     catturata dal compagno, si dice che muore in casa e non vale come extra.
    '''

    '''
    (). Se un giocatore non ha più tarocchi si dice che cade e può scoprire tutte le carte che gli restano; da ora in
     poi non giocherà più (come il morto nel Bridge), ma sarà il vincitore di ogni singola mano a scegliere la carta
     che deve giocare nella successiva, ovviamente rispettando l'obbligo di rispondere a seme, se possibile,
     altrimenti giocando una carta qualsiasi, non avendo, appunto, più tarocchi. Come è facile capire, si tratta di
     una scelta da non farsi se si possiedono ancora dei Re oppure il Matto.È importante ricordare che i giocatori
     possono in qualsiasi momento guardare tutte le carte prese dalla coppia di cui fanno parte.
    '''

    '''
    (). Al termine di ognuna delle quattro partite che formano un giro, il punteggio viene così calcolato:
     Ogni coppia riunisce le prese fatte e pone sotto a ciascuna carta di conto due carte senza valore (cartiglie,
     tarocchini o sopraventi) creando così tanti mazzetti di tre carte ciascuno. A partire dal quattordicesimo mazzetto
     tutte le carte, anche quelle senza valore, valgono un punto. Supponiamo ad esempio che una coppia abbia preso 64
     carte, 17 delle quali sono carte di conto. Poiché i primi 14 mazzetti (dei 17 fatti) contengono 14x3=42 carte,
     la coppia guadagna 64-42=22 punti; Dopo questi punti vengono quindi calcolati quelli delle versicole;
     si ricordi che la coppia che ha preso il matto ne aggiunge il valore a tutte le versicole fatte. La coppia che ha
     fatto l'ultima presa aggiungerà per questa dieci punti. Si contano poi le carte di conto, Matto incluso, iniziando
     di solito dai Papi e dai Re; si sommano a questo risultato i punti segnati durante il gioco e viene infine
     calcolata la differenza fra i punteggi conseguiti dalle due coppie. 60 punti di differenza costituiscono un resto.
     Un resto viene pagato immediatamente in base a quanto concordato prima dell'inizio del gioco.
     Al termine del gioco anche un solo punto costituisce un resto così da 61 a 120 punti valgono due resti,
     da 121 a 180 tre e così via. Nell'altamente improbabile caso che una coppia non effettui neppure una presa,
     la perdita viene raddoppiata e il punteggio del gioco è fissato a 2x7=14 resti oltre al punteggio già fatto che
     viene anch'esso raddoppiato. I resti in precedenza già realizzati e pagati non vengono invece raddoppiati.
    '''
    def conteggio(self):
        try:
            self.exe_status_update(FsmGermini.STATUS_CONTEGGIO, FsmGermini.STATUS_FINEMANO)
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

    def is_fallio(self):
        try:
            return self.giocatore_turno.get_caduto()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_giocabile(self, cid):
        try:
            if self.cid_apertura == None:
                # TODO: Matto
                return True

            #elif self.giocatore_turno.get_caduto():
            #    self.show_popup(True, "<p>Cade " + str(self.giocatore_turno) + "</p>")
            #    return True

            elif cid == CartaId.MATTO_0:
                if len(self.giocatore_turno.cards_mangiate) > 0:
                    return True
                else:
                    return False

            elif is_tarocco(self.cid_apertura):
                if is_tarocco(cid):
                    return True
                elif not self.general_man.has_seme(self.giocatore_turno, get_seme(Seme.TRIONFO)):
                    return True
                else:
                    return False

            elif seme_carta(cid) == seme_carta(self.cid_apertura):
                return True

            elif not self.giocatore_turno.has_seme(get_seme(self.cid_apertura)):
                if is_tarocco(cid):
                    return True
                else:
                    if self.giocatore_turno.has_seme(Seme.TRIONFO):
                        return False
                    else:
                        #if self.giocatore_turno.get_caduto():
                        #    return True
                        #else:
                        #    self.giocatore_turno.giocatore_cade()
                        #    self.show_popup(True, "<p>Cade " + self.giocatore_turno._name + " e scopre le sue carte</p>")
                        #    self.game_man.scopri_carte(self.giocatore_turno)
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
            self._actions[self._status].on_carta(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gestisci_presa(self, winner):
        try:
            c_list = []
            self.gestisci_matto()
            tav = self.general_man.get_carte_in_tavola()

            for p in self._fsm.game_man.get_posizioni():
                player = self.general_man.get_player_at_pos(p)
                tav[p].clear()
                self._delegate_presa(player, tav[p])
            return c_list
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def gestisci_matto(self):
        try:
            c_list = self.general_man.get_carte_in_tavola()
            pp = self._fsm.game_man.get_posizioni()
            for p in pp:
                for c in c_list[p]:
                    if c.get_id() == CartaId.MATTO_0:
                        player = self.general_man.get_player_at_pos(p)
                        self._delegate_presa(player, [c])
                        c_list[p].remove(c)
                        break
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
            self._delegate_append_html_text("Fine giro")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def add_rubate_giocatore(self, player, c):
        try:
            self.general_man.add_rubate_giocatore(player, c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
'''
    def show_ultima(self):
        try:
            if self.step_ready():
                if is_cartiglia(self.mostrata.get_id()):
                    self._delegate_append_html_text(_("Trovata: ") + str(self.mostrata) + _(". Carte mescolate."))
                    self.giocatore_turno = self.game_man.get_next_player(self.giocatore_turno, True)
                    self.show_popup("<p>" + _("La carta in fondo al mazzo &egrave: ") + str(self.mostrata) + _(".<br/> Carte mescolate correttamente.") + "</p>", FsmGioco.STATUS_GIOCO_BEGIN)
                    self.game_man.nascondi_carta(self.mostrata)
                    self.game_man.reset_tavola()
                else:
                    self._delegate_append_html_text(_("Trovata: ") + str(self.mostrata) + _(". Mescola di nuovo."))
                    echo_message(_("Trovata: ") + str(self.mostrata) + _(". Mescola di nuovo."))
                    self._status_next = FsmGioco.STATUS_MESCOLA
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)
'''