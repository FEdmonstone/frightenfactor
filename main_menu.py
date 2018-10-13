import pygame
from button import Button

class Main_menu(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.background = pygame.image.load("Assets/Backgrounds/background.png").convert_alpha()
        self.WIDTH = width
        self.HEIGHT = height

        self.button_sprites_list = pygame.sprite.Group()

        self.singleplayer = self.create_button(self.WIDTH/2, self.HEIGHT/2, 256, 64, 'singleplayer')

    def create_button(self, x, y, width, height, button_type):
        tempbutton = Button(width, height, button_type)
        self.button_sprites_list.add(tempbutton)
        tempbutton.rect.x = x + width / 2
        tempbutton.rect.y = y + height / 2
        return tempbutton