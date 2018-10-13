import pygame, os
from enemy import Enemy

class BasicZombie(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height)

        sprites_path = "Assets/Sprites/BasicZombie"
        sprites_paths = [os.path.join(sprites_path, loc) for loc in os.listdir(sprites_path)]

        self.move_sprites = [pygame.image.load(img) for img in sprites_paths]
        self.animation_counter = 0
        
        self.dead = False

    def move(self):
        if self.dead:
            self.image = pygame.transform.scale(pygame.image.load("Assets/Sprites/blood.png"), (64, 64))
        else:
            self.image = self.move_sprites[(self.animation_counter // 10) % len(self.move_sprites)]
            self.animation_counter += 1
        super().move()
