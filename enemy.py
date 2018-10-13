import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.speed = 2
        self.image = pygame.image.load("Assets/Sprites/enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.move()

    def move(self):
        self.rect.x -= self.speed

    def change_speed(self, speed):
        self.speed = speed