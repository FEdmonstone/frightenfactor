import pygame
WHITE = (255, 255, 255)

class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, button_type):
        super().__init__()

        self.speed = 10
        self.button_type = button_type
        self.width = width
        self.height = height

        self.image = pygame.image.load("Assets/Buttons/" + button_type +".png").convert_alpha()

        self.rect = self.image.get_rect()
