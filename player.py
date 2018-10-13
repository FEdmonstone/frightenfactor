import pygame
from bullet import Bullet
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.change_size(width, height)

        self.speed = 5

        #pygame.draw.rect(self.image, colour, [0, 0, width, height])
        
        self.image = pygame.image.load(".temp_images/player.png").convert_alpha()

        self.rect = self.image.get_rect()

    def change_size(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

    def shoot(self):
        bullet = Bullet(64, 64)
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y
        return bullet

    def moveRight(self):
        self.rect.x += self.speed

    def moveLeft(self):
        self.rect.x -= self.speed

    def moveUp(self):
        self.rect.y -= self.speed

    def moveDown(self):
        self.rect.y += self.speed