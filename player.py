import pygame, os
from bullet import Bullet
from sound_manager import *
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        super().__init__()

        move_left_sprites_path = "Assets/Sprites/Player/Left"
        move_right_sprites_path = "Assets/Sprites/Player/Right"
        move_up_sprites_path = "Assets/Sprites/Player/Up"
        move_down_sprites_path = "Assets/Sprites/Player/Down"

        self.left_sprites = [pygame.image.load(os.path.join(move_left_sprites_path, img)) for img in os.listdir(move_left_sprites_path)]
        self.right_sprites = [pygame.image.load(os.path.join(move_right_sprites_path, img)) for img in os.listdir(move_right_sprites_path)]
        self.up_sprites = [pygame.image.load(os.path.join(move_up_sprites_path, img)) for img in os.listdir(move_up_sprites_path)]
        self.down_sprites = [pygame.image.load(os.path.join(move_down_sprites_path, img)) for img in os.listdir(move_down_sprites_path)]

        self.image = self.right_sprites[1]
        self.rect = self.image.get_rect()
        self.height = height
        self.width = width

        self.speed = 5
        self.faces_right = True
        self.can_shoot = True

        self.counter = 0
        self.last_direction = 'right'

    def shoot(self):
        if not self.can_shoot:
            return None
        else:
            bullet = Bullet(64, 64)
            if(self.last_direction == 'right'):
                bullet.rect.x = self.rect.x + 45
                bullet.rect.y = self.rect.y + 35
            elif(self.last_direction == 'left'):
                bullet.rect.y = self.rect.y + 35
                bullet.rect.x = self.rect.x + 10
            elif(self.last_direction == 'up'):
                bullet.rect.x = self.rect.x + 28
                bullet.rect.y = self.rect.y
            elif(self.last_direction == 'down'):
                bullet.rect.x = self.rect.x + 28
                bullet.rect.y = self.rect.y + 50


            self.can_shoot = False

            gun_sound.play()

            return bullet

    def moveRight(self, borders):
        self.last_direction = 'right'
        if self.rect.x != (borders[0] - self.width) and self.rect.x < (borders[0] - self.width):
            self.rect.x += self.speed

            self.image = self.right_sprites[(self.counter // 10) % len(self.right_sprites)]
            self.counter += 1
            self.faces_right = True

    def moveLeft(self):
        self.last_direction = 'left'
        if self.rect.x != 0 and self.rect.x > 0:
            self.rect.x -= self.speed

            self.image = self.left_sprites[(self.counter // 10) % len(self.left_sprites)]
            self.counter += 1
            self.faces_right = False

    def moveUp(self, borders):
        self.last_direction = 'up'
        if self.rect.y != borders[2] and self.rect.y > borders[2]:
            self.rect.y -= self.speed

            self.image = self.up_sprites[(self.counter // 10) % len(self.up_sprites)]
            self.counter += 1

    def moveDown(self, borders):
        self.last_direction = 'down'
        if self.rect.y != (borders[1] - self.height) and self.rect.y < (borders[1] - self.height):
            self.rect.y += self.speed

            self.image = self.down_sprites[(self.counter // 10) % len(self.down_sprites)]
            self.counter += 1