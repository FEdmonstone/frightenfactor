import pygame
import random
from player import Player
from enemy import Enemy

# Game initialisation begins

pygame.init()
clock = pygame.time.Clock()

# Colour Definitions
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (0,   0,   255)
GREEN = (0,   255, 0)
RED   = (255, 0,   0)

# Window settings

WIDTH  = 1280
HEIGHT = 720

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Frighten Factory")
all_sprites_list = pygame.sprite.Group()

game_loop = True

# Keyboard

pygame.key.set_repeat(1, 1)

# Keybindings

keybindings = {
    'left'  : pygame.K_LEFT,
    'right' : pygame.K_RIGHT,
    'up'    : pygame.K_UP,
    'down'  : pygame.K_DOWN
}

# Font setup
debug_font = pygame.font.SysFont("Courier", 12)

# Sprite setup
background = pygame.image.load(".temp_images/background.png").convert_alpha()

main_player = Player(RED, 64, 64)
all_sprites_list.add(main_player)
main_player.rect.x = 20
main_player.rect.y = HEIGHT / 2

temp_enemy = Enemy(BLUE, 64, 64)
all_sprites_list.add(temp_enemy)
temp_enemy.rect.x = WIDTH - (temp_enemy.width + 20)
temp_enemy.rect.y = HEIGHT / 2

# Game initialisation ends

# Main game loop
while game_loop:

    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        # Movement event
        keys = pygame.key.get_pressed()
        if keys[keybindings['left']]:
            print("Left")
            main_player.moveLeft()
        if keys[keybindings['right']]:
            print("Right")
            main_player.moveRight()
        if keys[keybindings['up']]:
            print("Up")
            main_player.moveUp()
        if keys[keybindings['down']]:
            print("Down")
            main_player.moveDown()


    # Game logic

    temp_enemy.update()
    all_sprites_list.update()

    # Drawing logic

    screen.blit(background, (0, 0))

    # FPS counter
    fps_str = "".join(["FPS: ", str(int(clock.get_fps()))])
    fps = debug_font.render(fps_str, True, BLACK)
    screen.blit(fps, (50, 50))

    all_sprites_list.draw(screen)

    #pygame.draw.rect(screen, RED, [55, 200, 100, 70], 0)
    #pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    #pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)

    # Screen update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()