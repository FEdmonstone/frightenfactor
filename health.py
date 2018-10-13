import pygame
WHITE = (255, 255, 255)

class Health(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        heart = pygame.image.load("Assets/Sprites/health.png").convert_alpha()
        self.image = pygame.transform.scale(heart, (64, 64))

        self.rect = self.image.get_rect()

    def change_size(self, width, height):
            self.width = width
            self.height = height
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
