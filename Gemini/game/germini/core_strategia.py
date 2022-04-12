
#   '''
#  Created on 14 3 2022
#  @author: david
#  '''

from decks.carta_id import is_cartiglia, is_sopraventi, count_seme, Palo, seme_name
from main.exception_man import ExceptionMan
from main.general_manager import GeneralManager
from decks import mazzo_97

class CoreStrategia(object):

    def __init__(self):
        pass

    def riceve(self, ca, ppos):
        pass

if __name__ == '__main__':
    """ Main test """
    c = CoreStrategia()
    man = GeneralManager()
    ca = man.preleva_dal_mazzo(21)
    ca = man.preleva_dal_mazzo(21)
    ca = man.preleva_dal_mazzo(21)
    ca = man.preleva_dal_mazzo(21)

