'''
Created on 2 gen 2022

@author: david
'''
from importlib import resources

import pygame

class ButtonPygame:
    gui_font = None
    screen = None
    elevation = 5
    hndl = None

    def __init__(self, screen, text, width, height, pos, hndl=None):
        #Core attributes 
        self.pressed = False
        self.hndl = hndl
        self.dynamic_elecation = self.elevation
        self.original_y_pos = pos[1]
 
        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'
        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        self.text = text
        path = resources.path("fonts", "cmr8.ttf")
        self.gui_font = pygame.font.Font(path, 20)

        self.text_surf = self.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.screen = screen

    '''
    '''     
    def change_text(self, newtext):
        self.text_surf = self.gui_font.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
 
    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 
 
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
 
        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                #self.change_text(f"{self.translation}")
            else:
                self.dynamic_elecation = self.elevation
                    #self.change_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                #self.change_text(f"{self.translation}")
            else:
                if self.pressed == True:
                    if (self.hndl):
                        self.hndl()
                    self.pressed = False
                    #self.change_text(self.text)
        