from enum import Enum
from decks.carta import CartaId

class Tokens(Enum):
    TOKEN_UNO = 1
    TOKEN_BIS = 5
    TOKEN_PESCE = 10
'''
Carte di conto punti
'''
carte_conto = {
    CartaId.MATTO_0: 5,
    CartaId.PAPA_I: 5,
    CartaId.PAPA_II: 3,
    CartaId.PAPA_III: 3,
    CartaId.PAPA_IV: 3,
    CartaId.PAPA_V: 3,
    CartaId.CARRO_X: 5,
    CartaId.MORTE_XIII: 5,
    CartaId.FUOCO_XX: 5,
    CartaId.CAPRIC_XXVIII: 5,
    CartaId.CANCRO_XXX: 5,
    CartaId.PESCI_XXXI: 5,
    CartaId.ACQUARIO_XXXII: 5,
    CartaId.LEONE_XXXIII: 5,
    CartaId.TORO_XXXIV: 5,
    CartaId.GEMINI_XXXV: 5,
    CartaId.STELLA_XXXVI: 10,
    CartaId.LUNA_XXXVII: 10,
    CartaId.SOLE_XXXVIII: 10,
    CartaId.MONDO_XXXIX: 10,
    CartaId.TROMBA_XL: 10,
    CartaId.DANAR_R: 5,
    CartaId.SPADE_R: 5,
    CartaId.COPPE_R: 5,
    CartaId.BASTO_R: 5
}

carte_sopraventi = {
    CartaId.ACQUA_XXI: 0,
    CartaId.TERRA_XXII: 0,
    CartaId.ARIA_XXIII: 0,
    CartaId.BILANCIA_XXIV: 0,
    CartaId.VERGINE_XXV: 0,
    CartaId.SCORP_XXVI: 0,
    CartaId.ARIETE_XXVII: 0,
    CartaId.CAPRIC_XXVIII: 5,
    CartaId.SAGITT_XXIX: 0,
    CartaId.CANCRO_XXX: 5,
    CartaId.PESCI_XXXI: 5,
    CartaId.ACQUARIO_XXXII: 5,
    CartaId.LEONE_XXXIII: 5,
    CartaId.TORO_XXXIV: 5,
    CartaId.GEMINI_XXXV: 5,
    CartaId.STELLA_XXXVI: 10,
    CartaId.LUNA_XXXVII: 10,
    CartaId.SOLE_XXXVIII: 10,
    CartaId.MONDO_XXXIX: 10,
    CartaId.TROMBA_XL: 10
}

def is_conto(c):
    global carte_conto
    return c.get_id in carte_conto

def get_punti_carta(c):
    global carte_conto
    if c.get_id in carte_conto:
        return carte_conto[c.get_id]
    else:
        return 0

punti_vers = {
    CartaId.MATTO_0: 5,
    CartaId.PAPA_I: 5,
    CartaId.PAPA_II: 3,
    CartaId.PAPA_III: 3,
    CartaId.PAPA_IV: 3,
    CartaId.PAPA_V: 3,
    CartaId.CARRO_X: 5,
    CartaId.MORTE_XIII: 5,
    CartaId.DIAVOLO_XIV: 5,
    CartaId.FUOCO_XX: 5,
    CartaId.CAPRIC_XXVIII: 5,
    CartaId.SAGITT_XXIX: 5,
    CartaId.CANCRO_XXX: 5,
    CartaId.PESCI_XXXI: 5,
    CartaId.ACQUARIO_XXXII: 5,
    CartaId.LEONE_XXXIII: 5,
    CartaId.TORO_XXXIV: 5,
    CartaId.GEMINI_XXXV: 5,
    CartaId.STELLA_XXXVI: 10,
    CartaId.LUNA_XXXVII: 10,
    CartaId.SOLE_XXXVIII: 10,
    CartaId.MONDO_XXXIX: 10,
    CartaId.TROMBA_XL: 10,
    CartaId.DANAR_R: 5,
    CartaId.SPADE_R: 5,
    CartaId.COPPE_R: 5,
    CartaId.BASTO_R: 5
}
