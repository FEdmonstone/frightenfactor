import pygame
WHITE = (255, 255, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.speed = 10
        self.direction = 'right'
        self.image = pygame.image.load("Assets/Sprites/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()


    def update(self):
        self.move()

    def move(self):
        if(self.direction == 'right'):
            self.rect.x += self.speed
        if(self.direction == 'left'):
            self.rect.x -= self.speed
        if(self.direction == 'up'):
            self.rect.y -= self.speed
        if(self.direction == 'down'):
            self.rect.y += self.speed

    def change_speed(self, speed):
        self.speed = speed
