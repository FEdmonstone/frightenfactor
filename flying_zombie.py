import pygame, os
from enemy import Enemy


class FlyingZombie(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height)

        sprites_path = "Assets/Sprites/FlyingZombie"
        sprites_paths = [os.path.join(sprites_path, loc) for loc in os.listdir(sprites_path)]

        self.move_sprites = [pygame.image.load(img) for img in sprites_paths]
        self.animation_counter = 0

    def move(self):
        self.image = self.move_sprites[(self.animation_counter // 10) % len(self.move_sprites)]
        self.animation_counter += 1
        super().move()
