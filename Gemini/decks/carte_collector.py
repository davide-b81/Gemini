#   '''
#  Created on 25 1 2022
#  @author: david
#  '''
from main.exception_man import ExceptionMan

class CarteCollector(object):
    _carte = None


    def __init__(self, man):
        try:
            self._carte = []
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def insert(self, c):
        try:
            self._carte.append(c)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def delete(self, c):
        try:
            self._carte.clear()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)


    def __str__(self):
        try:
            return self.name
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)