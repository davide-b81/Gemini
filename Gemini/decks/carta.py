'''
Created on 31 dic 2021

@author: david
'''
#   '''
#  Created on 25 1 2022
#  @author: david
#  '''

from decks.carta_id import *

class Carta(object):
    id = None

    def __init__(self, id):
        '''
        Constructor
        '''
        self.id = id

    def get_seme(self):
        try:
            return get_seme(self.id)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_numerale(self):
        try:
            return get_numerale(self.id)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def is_tarocco(self):
        try:
            return is_tarocco(self.id)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_name(self):
        return str(self.id)

    def get_id(self):
        assert self.id is not None
        return self.id

    def get_short_name(self):
        return get_short_name(self.id)

    def __name__(self):
        return get_card_name(self.id)

    def __str__(self):
        return get_card_name(self.id)

    def __gt__(self, other):
        try:
            if (self.is_tarocco()):
                if other.is_tarocco():
                    return self.get_numerale() > other.get_numerale()
                else:
                    return True
            else:
                if other.is_tarocco():
                    return False
                elif self.get_seme() != other.get_seme():
                    return True
                else:
                    return self.get_numerale() > other.get_numerale()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __lt__(self, other):
        if (other):
            return not self.__gt__(other) and self.id != other.id
        else:
            return False

    def __le__(self, other):
        if (other):
            return not self.__gt__(other)
        else:
            return False

    def __eq__(self, other):
        if (other):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        if (other):
            return self.id != other.id
        else:
            return True

    def __ge__(self, other):
        if (other):
            return self.__gt__(other) or self.id == other.id
        else:
            return False
