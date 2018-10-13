import pygame
import random
from event_types import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from health import Health
from main_menu import Main_menu
from basic_zombie import BasicZombie
from flying_zombie import FlyingZombie

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
INVINCIBILITY_DURATION = 1500
invincible = False      # After-hit invincibility state
running = True
timer_font = pygame.font.SysFont('Courier', 32)
start_time = pygame.time.get_ticks()

# Event definitions
events = {PLAYERS_CAN_SHOOT: {"interval": 400, "count": 0},
          BASIC_ZOMBIE_SPAWN: {"interval": 10000, "count": 0},
          FLYING_ZOMBIE_SPAWN: {"interval": 450, "count": 0}}

# Window settings

WIDTH  = 1280
HEIGHT = 720

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Frighten Factor")

main_loop = True

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
main_menu = Main_menu(WIDTH, HEIGHT)

player_sprites_list = pygame.sprite.Group()
enemy_sprites_list = pygame.sprite.Group()
bullet_sprites_list = pygame.sprite.Group()
health_sprites_list = pygame.sprite.Group()

horizon = list(pygame.image.load("Assets/Backgrounds/horizon.png").get_rect().size)
borders = [WIDTH, HEIGHT, horizon[1]]
bck_image_width = horizon[0]

background = pygame.image.load("Assets/Backgrounds/background.png").convert_alpha()
background_horizon = pygame.image.load("Assets/Backgrounds/horizon.png").convert_alpha()
offset = 0
offset2 = -bck_image_width


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

# Game initialisation ends


# Event timers
# Generate time-based events
def generate_time_based_events():
    ms_elapsed = pygame.time.get_ticks()

    # Check whether we should trigger any of the events
    for event_type, event_props in events.items():
        if ms_elapsed / event_props["interval"] > event_props["count"]:
            new_event = pygame.event.Event(pygame.USEREVENT, {"subtype": event_type})
            pygame.event.post(new_event)
            event_props["count"] += 1
"""
WIP

# Add an event to a list, it will be performed every 'interval' amount of milliseconds
def add_time_based_event(event_type, interval):
    events[event_type] = {"interval": interval, "count": 0}
"""


# Main menu loop

def main_menu_screen():
    menu_loop = True
    while menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.blit(main_menu.background, (0, 0))
        main_menu.button_sprites_list.update()
        main_menu.button_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def singleplayer_screen():
    
    game_loop = True
    while game_loop:

        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
            elif event.type == INVINCIBILITY_END:
                invincible = False
                pygame.time.set_timer(INVINCIBILITY_END, 0)

            elif event.type == pygame.USEREVENT:
                if event.dict["subtype"] == PLAYERS_CAN_SHOOT:
                    for player in player_sprites_list:
                        player.can_shoot = True

                elif event.dict["subtype"] == BASIC_ZOMBIE_SPAWN:
                    new_enemy = BasicZombie(64, 64)
                    new_enemy.rect.x = WIDTH - 64
                    new_enemy.rect.y = random.randint(64, borders[1]-64)
                    enemy_sprites_list.add(new_enemy)

                elif event.dict["subtype"] == FLYING_ZOMBIE_SPAWN:
                    new_enemy = FlyingZombie(64, 64)
                    new_enemy.rect.x = WIDTH - 64
                    new_enemy.rect.y = random.randint(0, borders[2]-64)
                    enemy_sprites_list.add(new_enemy)

        keys = pygame.key.get_pressed()
        # Movement event
        if keys[keybindings['left']]:
            main_player.moveLeft()
        if keys[keybindings['right']]:
            main_player.moveRight(borders)
        if keys[keybindings['up']]:
            main_player.moveUp(borders)
        if keys[keybindings['down']]:
            main_player.moveDown(borders)

        # Fire event
        if keys[keybindings['fire']]:
            bullet = main_player.shoot()
            if bullet:
                bullet_sprites_list.add(bullet)

        counting_time = pygame.time.get_ticks() - start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = 5 - (counting_time / 60000)
        counting_seconds = int(60 - (counting_time % 60000) / 1000)

        counting_string = "%d:%d" % (counting_minutes, counting_seconds)

        #counting_rect = counting_text.get_rect(midtop=screen.get_rect().midtop)

        if int(counting_minutes) == 4 and counting_seconds == 0:
            game_loop = False
        #screen.blit(counting_text, counting_rect)
        #pygame.display.update()


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
        offset +=1
        offset2 += 1
        screen.blit(background, (-offset, 0))
        screen.blit(background_horizon, (-offset,0))

        screen.blit(background, (-offset2, 0))
        screen.blit(background_horizon, (-offset2,0))

        if offset > bck_image_width:
            offset = -bck_image_width
        if offset2 > bck_image_width:
            offset2 = -bck_image_width
            

        # FPS counter
        fps_str = "".join(["FPS: ", str(int(clock.get_fps()))])
        fps = debug_font.render(fps_str, True, WHITE)
        screen.blit(fps, (50, 50))

        # Timer counter
        counting_text = timer_font.render(str(counting_string), True, WHITE)
        screen.blit(counting_text, (WIDTH / 2, 10))

        player_sprites_list.draw(screen)
        enemy_sprites_list.draw(screen)
        bullet_sprites_list.draw(screen)
        health_sprites_list.draw(screen)

        # Screen update
        pygame.display.flip()
        clock.tick(60)

        # Timer updates
        generate_time_based_events()

    def multiplayer_screen():
        pass

    def options_screen():
        pass

    def help_screen():
        pass

screen_states = {
    'mainmenu' : 0,
    'singleplayer' : 1,
    'multiplayer' : 2,
    'options' : 3,
    'help' : 4
}

current_state = screen_states['mainmenu']
while main_loop:
    print(current_state)
    if current_state == screen_states['mainmenu']:
        main_menu_screen()
    elif current_state == screen_states['singleplayer']:
        singleplayer_screen()
    elif current_state == screen_states['multiplayer']:
        multiplayer_screen()
    elif current_state == screen_states['options']:
        options_screen()
    elif current_state == screen_states['help']:
        help_screen()

pygame.quit()
