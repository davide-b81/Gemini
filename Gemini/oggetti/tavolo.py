'''
Created on 2 gen 2022

@author: david
'''
from oggetti import posizioni

class TavoloArea(object):
    '''
    classdocs
    '''
    pos_man = None
    
    _posizioni = ["Nord", "Est", "Sud", "Ovest"]

    def __init__(self, pos):
        '''
        Constructor
        '''
        self.pos_man = pos

    def get_posizioni(self):
        return self._posizioni

    def get_next_pos(self, pos, antior = True):
        i = self._posizioni.index(pos)
        if i > 0:
            i = (i - 1) % len(self._posizioni)
        else:
            i = len(self._posizioni) - 1
            
        return self._posizioni[i]
        
    def draw(self, screen):
        try:
            self.pos_man.desk_area.fill((0, 148, 135))
            screen.blit(self.pos_man.desk_area, self.pos_man.desk_pos)

        except Exception as e:
                print("draw: An error occurred:", e.args[0])
        