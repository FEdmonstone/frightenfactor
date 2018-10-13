import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

gun_sound = pygame.mixer.Sound("Assets/Sounds/gun_fire.ogg")
bullet_hit_sound = pygame.mixer.Sound("Assets/Sounds/bullet_impact.wav")
zombie_hit_sound = pygame.mixer.Sound("Assets/Sounds/zombie_hit.wav")
zombie_attack_melee_sound = pygame.mixer.Sound("Assets/Sounds/zombie_melee_attack.wav")
zombie_spit_sound = pygame.mixer.Sound("Assets/Sounds/zombie_spit.wav")
player_hit = pygame.mixer.Sound("Assets/Sounds/player_hit.wav")