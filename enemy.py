import pygame
WHITE = (255, 255, 255)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.change_size(width, height)

        self.speed = 2

        #pygame.draw.rect(self.image, colour, [0, 0, width, height])

        self.image = pygame.image.load("Assets/Sprites/enemy.png").convert_alpha()

        self.rect = self.image.get_rect()

    def change_size(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

    def update(self):
        self.move()

    def move(self):
        self.rect.x -= self.speed

    def change_speed(self, speed):
        self.speed = speed