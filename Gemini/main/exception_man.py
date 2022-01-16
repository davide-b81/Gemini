'''
Created on 9 gen 2022

@author: david
'''
import traceback

from oggetti.stringhe import Stringhe, _

class ExceptionMan(Exception):

    @staticmethod
    def manage_exception(s, e, retrow = False):
        stringa = "Exception in " + traceback.extract_stack(None, 2)[0][2] + ": " + _(s) + e.args[0]
        print(stringa)
        if (retrow):
            raise Exception("Throw exception", e)