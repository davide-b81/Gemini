'''
Created on 22 gen 2022

@author: david
'''
from typing import Dict, Union

import pygame
from pygame_gui.core import IContainerLikeInterface, UIElement, ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UITextBox
from oggetti.stringhe import _
from main.globals import *
from main.exception_man import ExceptionMan


class TextBox(UITextBox):
    def __init__(self,
                 html_text: str,
                 relative_rect: pygame.Rect,
                 manager: IUIManagerInterface,
                 wrap_to_height: bool = False,
                 layer_starting_height: int = 1,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 object_id: Union[ObjectID, str, None] = None,
                 anchors: Dict[str, str] = None,
                 visible: int = 1):

            super().__init__(html_text,
                 relative_rect,
                 manager,
                 wrap_to_height,
                 layer_starting_height,
                 container,
                 parent_element,
                 object_id,
                 anchors,
                 visible)


    def set_text(self, txt):
        print(txt)
        self.append_html_text(_(txt))