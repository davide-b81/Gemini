'''
Created on 9 gen 2022

@author: david
'''
import sys, os
from logging import critical
import traceback

# debug()
# info()
# warning()
# error()
# critical()

class ExceptionMan(Exception):

    @staticmethod
    def manage_exception(s, e, retrow=False):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        if len(s) == 0:
            stringa = " Exception in " + e.__class__.__name__ + "." + traceback.extract_stack(None, 2)[0][2] + "(" + fname + ", line " + str(exc_tb.tb_lineno) + "): " + str(e.args[0])
        else:
            stringa = " Exception in " + e.__class__.__name__ + "." + traceback.extract_stack(None, 2)[0][2] + "(" + fname + ", line " + str(exc_tb.tb_lineno) + "): " + s + " " + str(e.args[0])
        critical(stringa)
        if retrow:
            raise Exception("Re-trow ", str(e.args[0]))
