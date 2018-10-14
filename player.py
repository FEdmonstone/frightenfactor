import pygame, os
from bullet import Bullet
from sound_manager import *
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, is_zombie):
        super().__init__()

        move_left_sprites_path = "Assets/Sprites/Player/Left"
        move_right_sprites_path = "Assets/Sprites/Player/Right"
        move_up_sprites_path = "Assets/Sprites/Player/Up"
        move_down_sprites_path = "Assets/Sprites/Player/Down"

        zombie_left_sprites_path = "Assets/Sprites/ZombieLord/Left"
        zombie_right_sprites_path = "Assets/Sprites/ZombieLord/Right"

        self.left_sprites = [pygame.image.load(os.path.join(move_left_sprites_path, img)) for img in os.listdir(move_left_sprites_path)]
        self.right_sprites = [pygame.image.load(os.path.join(move_right_sprites_path, img)) for img in os.listdir(move_right_sprites_path)]
        self.up_sprites = [pygame.image.load(os.path.join(move_up_sprites_path, img)) for img in os.listdir(move_up_sprites_path)]
        self.down_sprites = [pygame.image.load(os.path.join(move_down_sprites_path, img)) for img in os.listdir(move_down_sprites_path)]

        self.left_zombie_sprites = [pygame.image.load(os.path.join(zombie_left_sprites_path, img)) for img in os.listdir(zombie_left_sprites_path) if os.path.isfile(os.path.join(zombie_left_sprites_path, img))]
        self.right_zombie_sprites = [pygame.image.load(os.path.join(zombie_right_sprites_path, img)) for img in os.listdir(zombie_right_sprites_path) if os.path.isfile(os.path.join(zombie_right_sprites_path, img))]

        self.image = self.right_sprites[1] if not is_zombie else self.left_zombie_sprites[0]
        self.rect = self.image.get_rect()
        self.height = height
        self.width = width

        self.speed = 5
        self.faces_right = True
        self.can_shoot = True
        self.is_zombie = is_zombie

        self.rect.inflate_ip(-20,-10)

        self.counter = 0
        self.last_direction = 'right'
        
        self.hit = False
        self.redFlash = 0
        
        self.rightRed = pygame.image.load("Assets/Sprites/Player/RedPlayer/mcright-red.png").convert_alpha()
        self.leftRed = pygame.image.load("Assets/Sprites/Player/RedPlayer/mcleft-red.png").convert_alpha()
        self.downRed = pygame.image.load("Assets/Sprites/Player/RedPlayer/mcdown-red.png").convert_alpha()
        self.upRed = pygame.image.load("Assets/Sprites/Player/RedPlayer/mcup-red.png").convert_alpha()

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

            if self.is_zombie:
                self.image = self.right_zombie_sprites[(self.counter // 10) % len(self.right_zombie_sprites)]
                self.counter += 1
            else:
                if self.hit:
                    self.image = self.rightRed
                    self.redFlash += 1
                    if self.redFlash == 10:
                        self.hit = False
                        self.redFlash = 0
                else:
                    self.image = self.right_sprites[(self.counter // 10) % len(self.right_sprites)]
                    self.counter += 1
            self.faces_right = True

    def moveLeft(self):
        self.last_direction = 'left'
        if self.rect.x != 0 and self.rect.x > 0:
            self.rect.x -= self.speed

            if self.is_zombie:
                self.image = self.left_zombie_sprites[(self.counter // 10) % len(self.left_zombie_sprites)]
                self.counter += 1
            else:
                if self.hit:
                    self.image = self.leftRed
                    self.redFlash += 1
                    if self.redFlash == 10:
                        self.hit = False
                        self.redFlash = 0
                else:
                    self.image = self.left_sprites[(self.counter // 10) % len(self.left_sprites)]
                    self.counter += 1
            self.faces_right = False

    def moveUp(self, borders):
        self.last_direction = 'up'
        if self.rect.y != borders[2] and self.rect.y > borders[2]:
            self.rect.y -= self.speed

            if self.is_zombie:
                if self.faces_right:
                    self.image = self.right_zombie_sprites[(self.counter // 10) % len(self.right_zombie_sprites)]
                else:
                    self.image = self.left_zombie_sprites[(self.counter // 10) % len(self.left_zombie_sprites)]
            else:
                if self.hit:
                    self.image = self.upRed
                    self.redFlash += 1
                    if self.redFlash == 10:
                        self.hit = False
                        self.redFlash = 0
                else:
                    self.image = self.up_sprites[(self.counter // 10) % len(self.up_sprites)]
                    self.counter += 1

    def moveDown(self, borders):
        self.last_direction = 'down'
        if self.rect.y != (borders[1] - self.height) and self.rect.y < (borders[1] - self.height):
            self.rect.y += self.speed

            if self.is_zombie:
                if self.faces_right:
                    self.image = self.right_zombie_sprites[(self.counter // 10) % len(self.right_zombie_sprites)]
                else:
                    self.image = self.left_zombie_sprites[(self.counter // 10) % len(self.left_zombie_sprites)]
            else:
                if self.hit:
                    self.image = self.downRed
                    self.redFlash += 1
                    if self.redFlash == 10:
                        self.hit = False
                        self.redFlash = 0
                else:
                    self.image = self.down_sprites[(self.counter // 10) % len(self.down_sprites)]
                    self.counter += 1
