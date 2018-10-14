import pygame
from button import Button

class Help_menu(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.background = pygame.image.load("Assets/Backgrounds/helpbg.png").convert_alpha()
        self.WIDTH = width
        self.HEIGHT = height

        self.button_sprites_list = pygame.sprite.Group()

        self.back = self.create_button(self.WIDTH - 256, self.HEIGHT - 64, 256, 64, 'back')

    def create_button(self, x, y, width, height, button_type):
        tempbutton = Button(width, height, button_type)
        self.button_sprites_list.add(tempbutton)
        tempbutton.rect.x = x
        tempbutton.rect.y = y
        return tempbutton