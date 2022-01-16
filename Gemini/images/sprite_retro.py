'''
Created on 6 gen 2022

@author: david
'''
import pygame
from pygame.sprite import Sprite


class SpriteRetro(pygame.sprite.Sprite):
    '''
    classdocs
    '''
    rect = (0, 0)
    visible = False

    def __init__(self, img):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.visible = False

    def set_position(self, pos):
        self.rect.center = pos

    def set_visible(self, visible, pos=(0, 0)):
        self.visible = visible
        if self.visible:
            self.rect.center = pos

    def get_visible(self):
        return self.visible

    def update(self):
        pass
