import pygame
from player import Player

pygame.init()
clock = pygame.time.Clock()

# Colour Definitions
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0,   255, 0)
RED   = (255, 0,   0)

# Window settings

WIDTH  = 640
HEIGHT = 720

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Frighten Factory")
all_sprites_list = pygame.sprite.Group()

game_loop = True


# Sprite setup
main_player = Player(RED, 20, 20)
all_sprites_list.add(main_player)
main_player.rect.x = WIDTH / 2
main_player.rect.y = HEIGHT / 2

# Keyboard

pygame.key.set_repeat(16, 16)

# keybindings

keybindings          = {}
keybindings['left']  = pygame.K_LEFT
keybindings['right'] = pygame.K_RIGHT
keybindings['up']    = pygame.K_UP
keybindings['down']  = pygame.K_DOWN

# Main game loop
while game_loop:

    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        # Movement event handlerspygame.key.set_repeat()
        keys = pygame.key.get_pressed()
        if keys[keybindings['left']]:
            main_player.moveLeft()
        if keys[keybindings['right']]:
            main_player.moveRight()
        if keys[keybindings['up']]:
            main_player.moveUp()
        if keys[keybindings['down']]:
            main_player.moveDown()


    # Game logic

    all_sprites_list.update()

    # Drawing logic

    screen.fill(WHITE)

    all_sprites_list.draw(screen)

    #pygame.draw.rect(screen, RED, [55, 200, 100, 70], 0)
    #pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    #pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)

    # Screen update
    pygame.display.flip()
    clock.tick(60)

pygame.quit()