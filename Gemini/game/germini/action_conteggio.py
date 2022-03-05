#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from importlib.resources import _
from time import monotonic

from decks.carta_id import is_cartiglia
from game.germini.action import Action
from main.exception_man import ExceptionMan
from main.globals import echo_message
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

 È possibile, per quanto improbabile, fare più di 700 punti (ovvero 12 resti) in una sola mano.
 Come esempi si consideri che:
 Se alla fine della mano una coppia possiede tutte e tre le versicole che richiedono il Papa Uno - ovvero
 uno/Matto/Tromba, uno/tredici/ventotto e i cinque Papi - il punteggio è il così detto 74 dell’uno (dove i
 Papi 2, 3, 4, 5 sono tutti già contati come versicola e anche da soli). Infatti uno/Matto/Tromba valgono 20,
 uno/tredici/ventotto con il Matto sono altri 20 punti, i quattro Papi minori contati due volte fanno altri 24
 punti più Uno e Matto ancora 10 punti per un totale complessivo di 74 punti.
 Se mancano uno/Matto/Tromba o uno/tredici/ventotto, abbiamo il 54 dell’uno. Se invece manca il solo
 Papa 5, abbiamo il 68 dell’uno. Se invece mancano i Papi 5 e 4 si ha il 62 dell’uno. Se infine manca tutta la
 versicola dei Papi, abbiamo il 40 dell’uno.
 Se alla fine della mano entrambe le coppie hanno preso due Re o due Papi, non realizzando alcuna
 versicola, nessuna coppia conta i propri e si dice “senza re” ovvero “senza papi” (in questo caso si esclude
 naturalmente il Papa Uno). Se entrambe le coppie hanno preso due Re e due Papi si dice “senza questi,
 senza quelli”.
'''
class ActionConteggio(Action):

    def __init__(self, fsm):
        super().__init__(fsm)
        self._t_action = monotonic()

    def start(self):
        try:
            # Posiziona mazzo e lo rende visibile
            echo_message(_("Action - I"))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def end(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update_sub(self):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta_click(self, cid):
        try:
            pass
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)