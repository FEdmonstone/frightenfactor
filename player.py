import pygame
from bullet import Bullet
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.change_size(width, height)
        self.image = pygame.image.load("Assets/Sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.speed = 5
        self.can_shoot = True

        #pygame.draw.rect(self.image, colour, [0, 0, width, height])


    def change_size(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

    def shoot(self):
        if not self.can_shoot: return None
        else:
            bullet = Bullet(64, 64)
            bullet.rect.x = self.rect.x
            bullet.rect.y = self.rect.y

            self.can_shoot = False

            return bullet


    def moveRight(self, borders):
        if self.rect.x != (borders[0] - self.width) and self.rect.x < (borders[0] - self.width):
            self.rect.x += self.speed

    def moveLeft(self, borders):
        if self.rect.x != 0 and self.rect.x > 0:
            self.rect.x -= self.speed

    def moveUp(self, borders):
        if self.rect.y != borders[2] and self.rect.y > borders[2]:
         self.rect.y -= self.speed

    def moveDown(self, borders):
        if self.rect.y != (borders[1] - self.height) and self.rect.y < (borders[1] - self.height):
         self.rect.y += self.speed
