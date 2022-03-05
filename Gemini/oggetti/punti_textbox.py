'''
Created on 8 gen 2022

@author: david
'''
import pygame

class PuntiTextBox:

    COLOR_INACTIVE = None
    FONT = None
    COLOR_INACTIVE = None
    text = ""
    input_active = True

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 32)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.active = False

    def append_text(self, str):
        self.text +=  str

    def set_text(self, str):
        self.text =  str

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.input_active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def on_draw(self, screen):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)