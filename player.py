import pygame
from bullet import Bullet
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        self.change_size(width, height)

        self.stationary_sprite_left = pygame.image.load("Assets/Sprites/mc_stationary_left.png")
        self.stationary_sprite_right = pygame.image.load("Assets/Sprites/mc_stationary_right.png")

        self.left_walking_sprites = [pygame.image.load("Assets/Sprites/mc_left_leftstep.png"),
                                     self.stationary_sprite_left,
                                     pygame.image.load("Assets/Sprites/mc_left_rightstep.png")]
        self.right_walking_sprites = [pygame.image.load("Assets/Sprites/mc_right_leftstep.png"),
                                      self.stationary_sprite_right,
                                      pygame.image.load("Assets/Sprites/mc_right_rightstep.png")]

        self.rect = self.image.get_rect()
        self.image = self.stationary_sprite_right

        self.speed = 5
        self.faces_right = True
        self.can_shoot = True

        self.counter = 0

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
            bullet.rect.x = self.rect.x + 45
            bullet.rect.y = self.rect.y + 35

            self.can_shoot = False

            return bullet

    def moveRight(self, borders):
        if self.rect.x != (borders[0] - self.width) and self.rect.x < (borders[0] - self.width):
            self.rect.x += self.speed

            self.image = self.right_walking_sprites[(self.counter // 10) % len(self.right_walking_sprites)]
            self.counter += 1
            self.faces_right = True

    def moveLeft(self):
        if self.rect.x != 0 and self.rect.x > 0:
            self.rect.x -= self.speed

            self.image = self.left_walking_sprites[(self.counter // 10) % len(self.left_walking_sprites)]
            self.counter += 1
            self.faces_right = False

    def moveUp(self, borders):
        if self.rect.y != borders[2] and self.rect.y > borders[2]:
            self.rect.y -= self.speed
            if self.faces_right:
                self.image = self.right_walking_sprites[(self.counter // 10) % len(self.right_walking_sprites)]
            else:
                self.image = self.left_walking_sprites[(self.counter // 10) % len(self.left_walking_sprites)]
            self.counter += 1

    def moveDown(self, borders):
        if self.rect.y != (borders[1] - self.height) and self.rect.y < (borders[1] - self.height):
            self.rect.y += self.speed
            if self.faces_right:
                self.image = self.right_walking_sprites[(self.counter // 10) % len(self.right_walking_sprites)]
            else:
                self.image = self.left_walking_sprites[(self.counter // 10) % len(self.left_walking_sprites)]

            self.counter += 1

