import pygame, os, random
from enemy import Enemy
from bullet import Bullet
from drawing_manager import *
from sound_manager import *


class FlyingZombie(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height)

        sprites_path = "Assets/Sprites/FlyingZombie"
        sprites_paths = [os.path.join(sprites_path, loc) for loc in os.listdir(sprites_path)]

        self.move_sprites = [pygame.image.load(img) for img in sprites_paths]
        self.animation_counter = 0
        self.can_shoot = False
        self.spitting_interval = random.randint(2000, 3500)
        
        self.dead = False


    def move(self):
        if self.dead:
            self.kill()
        else:
            self.image = self.move_sprites[(self.animation_counter // 10) % len(self.move_sprites)]
            self.animation_counter += 1
        super().move()

        if self.can_shoot:
            self.shoot()

    def shoot(self):
        if self.can_shoot:
            bullet = Bullet(64, 64, is_spit=True)
            bullet.rect.x = self.rect.x
            bullet.rect.y = self.rect.y
            bullet.direction = "down"
            spit_sprites.add(bullet)

            zombie_spit_sound.play()

            self.can_shoot = False
