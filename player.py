import pygame
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.max_speed = 5

        pygame.draw.rect(self.image, colour, [0, 0, width, height])

        # Example car sprite load
        # self.image = pygame.image.load("car.png").convert_alpha()

        self.rect = self.image.get_rect()

    def moveRight(self):
        self.rect.x += self.max_speed

    def moveLeft(self):
        self.rect.x -= self.max_speed

    def moveUp(self):
        self.rect.y -= self.max_speed

    def moveDown(self):
        self.rect.y += self.max_speed