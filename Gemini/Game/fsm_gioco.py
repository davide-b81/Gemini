'''
Created on 3 gen 2022

@author: david
'''

class FsmGioco(object):
    '''
    classdocs
    '''
    running = None

    def __init__(self, params = None):
        '''
        Constructor
        '''
        running = False
        
    def running(self):
        return self.running()
    
    def start_game(self):
        self.running = True

    def end_game(self):
        self.running = False

    def update_game(self):
        self.running = False