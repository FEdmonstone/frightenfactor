import pygame
import random
from event_types import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from health import Health

# Game initialisation begins

pygame.init()
clock = pygame.time.Clock()

# Colour Definitions
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (0,   0,   255)
GREEN = (0,   255, 0)
RED   = (255, 0,   0)

# Game settings (intervals in milliseconds)
PLAYER_SHOOTING_INTERVAL = 400
ENEMY_SPAWN_INTERVAL = 1000
INVINCIBILITY_DURATION = 1500
invincible = False

# Window settings

WIDTH  = 1280
HEIGHT = 720

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Frighten Factor")

game_loop = True

# Keyboard

pygame.key.set_repeat(1, 1)

# Keybindings

keybindings = {
    'left'  : pygame.K_LEFT,
    'right' : pygame.K_RIGHT,
    'up'    : pygame.K_UP,
    'down'  : pygame.K_DOWN,
    'fire'  : pygame.K_SPACE
}

# Font setup
debug_font = pygame.font.SysFont("Courier", 12)

# Sprite setup
player_sprites_list = pygame.sprite.Group()
enemy_sprites_list = pygame.sprite.Group()
bullet_sprites_list = pygame.sprite.Group()
health_sprites_list = pygame.sprite.Group()

background = pygame.image.load("Assets/Backgrounds/background.png").convert_alpha()

num_health = 3
hearts = []
for count in range(num_health):
    elem = Health(WHITE, 20, 20)
    health_sprites_list.add(elem)
    elem.rect.x = count * 64
    elem.rect.y = 0
    hearts.append(elem)

main_player = Player(RED, 64, 64)
player_sprites_list.add(main_player)
main_player.rect.x = 20
main_player.rect.y = HEIGHT / 2

temp_enemy1 = Enemy(BLUE, 64, 64)
enemy_sprites_list.add(temp_enemy1)
temp_enemy1.rect.x = WIDTH - (temp_enemy1.width + 20)
temp_enemy1.rect.y = HEIGHT / 3 * 2

temp_enemy2 = Enemy(BLUE, 64, 64)
enemy_sprites_list.add(temp_enemy2)
temp_enemy2.rect.x = WIDTH - (temp_enemy2.width + 20)
temp_enemy2.rect.y = HEIGHT / 3

# Event timers
pygame.time.set_timer(PLAYERS_CAN_SHOOT, PLAYER_SHOOTING_INTERVAL)
pygame.time.set_timer(ENEMY_SPAWN, ENEMY_SPAWN_INTERVAL)


# Game initialisation ends

# Main game loop
while game_loop:

    # Main event loop
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            game_loop = False
        elif event.type == PLAYERS_CAN_SHOOT:
            for player in player_sprites_list:
                player.can_shoot = True
        elif event.type == ENEMY_SPAWN:
            new_enemy = Enemy(BLUE, 64, 64)
            new_enemy.rect.x = WIDTH - 64
            new_enemy.rect.y = random.randint(64, HEIGHT-64)
            enemy_sprites_list.add(new_enemy)
        elif event.type == INVINCIBILITY_END:
            invincible = False
            pygame.time.set_timer(INVINCIBILITY_END, 0)

    keys = pygame.key.get_pressed()
    # Movement event
    if keys[keybindings['left']]:
        main_player.moveLeft()
    if keys[keybindings['right']]:
        main_player.moveRight()
    if keys[keybindings['up']]:
        main_player.moveUp()
    if keys[keybindings['down']]:
        main_player.moveDown()

    # Fire event
    if keys[keybindings['fire']]:
        bullet = main_player.shoot()
        if bullet:
            bullet_sprites_list.add(bullet)


    # Game logic

    # Kills enemy when they collide with player
    for enemy in pygame.sprite.groupcollide(bullet_sprites_list, enemy_sprites_list, 1, 1):
        pass

    for player in pygame.sprite.groupcollide(player_sprites_list, enemy_sprites_list, 0, 0):
        if not invincible:
            current = hearts[-1]
            current.kill()
            del hearts[-1]
            invincible = True
            pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)
            
    if not hearts:
        pygame.sprite.groupcollide(player_sprites_list, enemy_sprites_list, 1, 0)

    player_sprites_list.update()
    enemy_sprites_list.update()
    bullet_sprites_list.update()
    health_sprites_list.update()

    # Drawing logic

    screen.blit(background, (0, 0))

    # FPS counter
    fps_str = "".join(["FPS: ", str(int(clock.get_fps()))])
    fps = debug_font.render(fps_str, True, WHITE)
    screen.blit(fps, (50, 50))

    player_sprites_list.draw(screen)
    enemy_sprites_list.draw(screen)
    bullet_sprites_list.draw(screen)
    health_sprites_list.draw(screen)

    # Screen update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
