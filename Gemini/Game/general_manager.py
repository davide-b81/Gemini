'''
Created on 4 gen 2022

@author: david
'''

class GeneralManager(object):
    '''
    classdocs
    '''
    nomegiocatori = []
    giocatori = []
    coppia1 = []
    coppia2 = []
    posizioni = ["Nord", "Est", "Sud", "Ovest"]
    mazzo = None
    carte = {}
    mazziere = None
    tavola = {}

    def __init__(self, params = None):
        '''
        Constructor
        '''
        