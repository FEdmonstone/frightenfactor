import pygame
import random
from event_types import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from health import Health
from main_menu import Main_menu
from help_menu import Help_menu
from game_over import Game_Over
from basic_zombie import BasicZombie
from flying_zombie import FlyingZombie
from drawing_manager import *
from sound_manager import *

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
timer_font = pygame.font.SysFont('Courier', 32)

# Event definitions
events = {PLAYERS_CAN_SHOOT: {"interval": 400, "count": 0},
          BASIC_ZOMBIE_SPAWN: {"interval": 500, "count": 0},
          FLYING_ZOMBIE_SPAWN: {"interval": 5000, "count": 0},
          FLYING_ZOMBIES_CAN_SHOOT: {"interval": 4000, "count":0 }}

# Window settings
WIDTH = 1280
HEIGHT = 720

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Frighten Factor")

main_loop = True

# Keyboard

pygame.key.set_repeat(1, 1)

# Keybindings

keybindings = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'fire': pygame.K_SPACE,
    'left2': pygame.K_a,
    'right2': pygame.K_d,
    'up2': pygame.K_w,
    'down2': pygame.K_s,
    'acidspit' : pygame.K_RETURN
}

# Font setup
debug_font = pygame.font.SysFont("Courier", 12)

# Sprite setup
main_menu = Main_menu(WIDTH, HEIGHT)

# Game initialisation ends


# Event timers
# Generate time-based events
def generate_time_based_events(time_elapsed_ms):

    # Check whether we should trigger any of the events
    for event_type, event_props in events.items():
        if time_elapsed_ms / event_props["interval"] > event_props["count"]:
            new_event = pygame.event.Event(pygame.USEREVENT, {"subtype": event_type})
            pygame.event.post(new_event)
            event_props["count"] += 1

frozen = True

# Main menu loop

def main_menu_screen():

    global current_state
    menu_loop = True

    def button(x,y,w,h,button_type):
        global frozen
        global current_state
        if menu_loop:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                if click[0] == 1:
                    frozen = False
                    if button_type == 'singleplayer':
                        current_state = screen_states['singleplayer']
                        return False
                    elif button_type == 'multiplayer':
                        current_state = screen_states['multiplayer']
                        return False
                    elif button_type == 'help':
                        current_state = screen_states['help']
                        return False
                    elif button_type == 'quit':
                        current_state = screen_states['quit']
                        return False
            return True

    #while frozen:
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            pygame.quit()
    #            quit()
    #        button(0, HEIGHT/2 - 100, WIDTH, HEIGHT/4)
    #    pygame.display.flip()
    #    clock.tick(60)

    while menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_state = screen_states['quit']
                menu_loop = False
            menu_loop = button(WIDTH / 2 - 128, HEIGHT / 2 - 32, 256, 64, 'singleplayer')
            menu_loop = button(WIDTH / 2 - 128, HEIGHT / 2 + 64, 256, 64, 'multiplayer')
            menu_loop = button(WIDTH / 2 - 128, HEIGHT / 2 + 160, 256, 64, 'help')
            menu_loop = button(WIDTH / 2 - 128, HEIGHT / 2 + 256, 256, 64, 'quit')

        screen.blit(main_menu.background, (0, 0))
        main_menu.button_sprites_list.update()
        main_menu.button_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def singleplayer_screen():
    global current_state

    time_since_start_ms = 0
    for event in events:
        events[event]["count"] = 0

    stage_theme.play(loops=-1)
    player_sprites_list = pygame.sprite.Group()
    enemy_sprites_list = pygame.sprite.Group()
    bullet_sprites_list = pygame.sprite.Group()
    health_sprites_list = pygame.sprite.Group()
    dead_sprites_list = pygame.sprite.Group()

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

    invincible = False      # After-hit invincibility state
    running = True
    start_time = pygame.time.get_ticks()

    horizon = list(pygame.image.load("Assets/Backgrounds/horizonfull.png").get_rect().size)
    borders = [WIDTH, HEIGHT, horizon[1]]
    bck_image_width = horizon[0]

    background = pygame.image.load("Assets/Backgrounds/Background.png").convert_alpha()
    background_horizon = pygame.image.load("Assets/Backgrounds/horizonfull.png").convert_alpha()

    offset = 0
    offset2 = -bck_image_width
    
    game_loop = True
    while game_loop:

        print(time_since_start_ms)
        time_since_start_ms += clock.get_time()

        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_state = screen_states['quit']
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

                elif event.dict["subtype"] == FLYING_ZOMBIES_CAN_SHOOT:
                    for enemy in enemy_sprites_list:
                        if isinstance(enemy, FlyingZombie):
                            enemy.can_shoot = True

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

        if keys[keybindings['fire']]:
            bullet = main_player.shoot()
            if bullet:
                bullet.direction = main_player.last_direction
                bullet_sprites_list.add(bullet)

        counting_time = pygame.time.get_ticks() - start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = 5 - (counting_time / 60000)
        counting_seconds = int(60 - (counting_time % 60000) / 1000)

        counting_string = "%d:%d" % (counting_minutes, counting_seconds)

        #counting_rect = counting_text.get_rect(midtop=screen.get_rect().midtop)
        counting_text = debug_font.render(str(counting_string), 1, (255, 255, 255))
        counting_rect = counting_text.get_rect(midtop=screen.get_rect().midtop)

        #screen.blit(counting_text, counting_rect)
        if int(counting_minutes) == 4 and counting_seconds == 0:
            current_state = screen_states['congrats']
            game_loop = False
        #screen.blit(counting_text, counting_rect)
        #pygame.display.update()


        # Game logic
        

        for enemy in pygame.sprite.groupcollide(bullet_sprites_list, enemy_sprites_list, 1, 0).values():
            bullet_hit_sound.play()
            zombie_hit_sound.play()
            dead_sprites_list.add(enemy[0])
            enemy[0].dead = True
            enemy_sprites_list.remove(enemy[0])

        # Kills player when they collide with enemy
        for player in pygame.sprite.groupcollide(player_sprites_list, enemy_sprites_list, 0, 0).keys():
            if not invincible:
                zombie_attack_melee_sound.play()
                player_hit.play()
                current = hearts[-1]
                current.kill()
                del hearts[-1]
                invincible = True
                player.hit = True
                pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)

        for player in pygame.sprite.groupcollide(player_sprites_list, spit_sprites, 0, 1).keys():
            if not invincible:
                bullet_hit_sound.play()
                player_hit.play()
                current = hearts[-1]
                current.kill()
                del hearts[-1]
                invincible = True
                player.hit = True
                pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)

        if not hearts:
            pygame.sprite.groupcollide(player_sprites_list, enemy_sprites_list, 1, 0)
            current_state = screen_states['game_over']
            game_loop = False

        player_sprites_list.update()
        enemy_sprites_list.update()
        bullet_sprites_list.update()
        health_sprites_list.update()
        spit_sprites.update()
        dead_sprites_list.update()

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

        dead_sprites_list.draw(screen)
        player_sprites_list.draw(screen)
        enemy_sprites_list.draw(screen)
        bullet_sprites_list.draw(screen)
        health_sprites_list.draw(screen)
        spit_sprites.draw(screen)

        # Timer counter
        counting_text = timer_font.render(str(counting_string), True, WHITE)
        screen.blit(counting_text, (WIDTH / 2 - 40, 10))

        # FPS counter
        fps_str = "".join(["FPS: ", str(int(clock.get_fps()))])
        fps = debug_font.render(fps_str, True, WHITE)
        screen.blit(fps, (WIDTH - 80, 20))

        # Screen update
        pygame.display.flip()
        clock.tick(60)

        # Timer updates
        generate_time_based_events(time_since_start_ms)

def multiplayer_screen():

    global current_state

    time_since_start_ms = 0
    for event in events:
        events[event]["count"] = 0

    stage_theme.play(loops=-1)
    player_sprites_list = pygame.sprite.Group()
    player2_sprites_list = pygame.sprite.Group()
    enemy_sprites_list = pygame.sprite.Group()
    bullet_sprites_list = pygame.sprite.Group()
    health_sprites_list = pygame.sprite.Group()
    dead_sprites_list = pygame.sprite.Group()

    num_health = 3
    num_health2 = 6
    hearts = []
    hearts2 = []

    for count in range(num_health):
        elem = Health(WHITE, 20, 20)
        health_sprites_list.add(elem)
        elem.rect.x = count * 64
        elem.rect.y = 0
        hearts.append(elem)

    for count in range(num_health2):
        elem = Health(WHITE, 20, 20)
        health_sprites_list.add(elem)
        elem.rect.x = 1280 - (count * 64)
        elem.rect.y = 0
        hearts2.append(elem)

    main_player = Player(RED, 64, 64)
    player2 = Player(RED, 80, 80)

    player_sprites_list.add(main_player)
    player2_sprites_list.add(player2)

    main_player.rect.x = 20
    main_player.rect.y = HEIGHT / 2

    player2.rect.x = 1280 - 40
    player2.rect.y = HEIGHT / 2

    invincible = False  # After-hit invincibility state
    running = True
    start_time = pygame.time.get_ticks()

    horizon = list(pygame.image.load("Assets/Backgrounds/horizonfull.png").get_rect().size)
    borders = [WIDTH, HEIGHT, horizon[1]]
    bck_image_width = horizon[0]

    background = pygame.image.load("Assets/Backgrounds/Background.png").convert_alpha()
    background_horizon = pygame.image.load("Assets/Backgrounds/horizonfull.png").convert_alpha()

    offset = 0
    offset2 = -bck_image_width

    game_loop = True
    while game_loop:

        time_since_start_ms += clock.get_time()

        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                current_state = screen_states['quit']
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
                    new_enemy.rect.y = random.randint(64, borders[1] - 64)
                    enemy_sprites_list.add(new_enemy)

                elif event.dict["subtype"] == FLYING_ZOMBIE_SPAWN:
                    new_enemy = FlyingZombie(64, 64)
                    new_enemy.rect.x = WIDTH - 64
                    new_enemy.rect.y = random.randint(0, borders[2] - 64)
                    enemy_sprites_list.add(new_enemy)

                elif event.dict["subtype"] == FLYING_ZOMBIES_CAN_SHOOT:
                    for enemy in enemy_sprites_list:
                        if isinstance(enemy, FlyingZombie):
                            enemy.can_shoot = True

        keys = pygame.key.get_pressed()
        # Movement event
        if keys[keybindings['left']]:
            player2.moveLeft()
        if keys[keybindings['right']]:
            player2.moveRight(borders)
        if keys[keybindings['up']]:
            player2.moveUp(borders)
        if keys[keybindings['down']]:
            player2.moveDown(borders)

        if keys[keybindings['left2']]:
            main_player.moveLeft()
        if keys[keybindings['right2']]:
            main_player.moveRight(borders)
        if keys[keybindings['up2']]:
            main_player.moveUp(borders)
        if keys[keybindings['down2']]:
            main_player.moveDown(borders)

        # Fire event
        if keys[keybindings['fire']]:
            bullet = main_player.shoot()
            if bullet:
                bullet.direction = main_player.last_direction
                bullet_sprites_list.add(bullet)

        counting_time = pygame.time.get_ticks() - start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = 3 - (counting_time / 60000)
        counting_seconds = int(60 - (counting_time % 60000) / 1000)

        counting_string = "%d:%d" % (counting_minutes, counting_seconds)

        # counting_rect = counting_text.get_rect(midtop=screen.get_rect().midtop)
        counting_text = debug_font.render(str(counting_string), 1, (255, 255, 255))
        counting_rect = counting_text.get_rect(midtop=screen.get_rect().midtop)

        screen.blit(counting_text, counting_rect)
        if int(counting_minutes) == 0 and counting_seconds == 0:
            current_state = screen_states['congrats']
            game_loop = False
        # screen.blit(counting_text, counting_rect)
        # pygame.display.update()

        # Game logic
        # Kills enemy when they collide with player
        for enemy in pygame.sprite.groupcollide(bullet_sprites_list, enemy_sprites_list, 1, 0).values():
            bullet_hit_sound.play()
            zombie_hit_sound.play()
            dead_sprites_list.add(enemy[0])
            enemy[0].dead = True
            enemy_sprites_list.remove(enemy[0])

        for enemy in pygame.sprite.groupcollide(bullet_sprites_list, player2_sprites_list, 1, 0):
            if not invincible:
                current = hearts2[-1]
                current.kill()
                del hearts2[-1]
                invincible = True
                pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)
        if not hearts2:
            #global current_state
            current_state = screen_states['game_over']
            game_loop = False

        for player in pygame.sprite.groupcollide(player_sprites_list, enemy_sprites_list, 0, 0):
            if not invincible:
                zombie_attack_melee_sound.play()
                player_hit.play()
                current = hearts[-1]
                current.kill()
                del hearts[-1]
                invincible = True
                pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)

        for player in pygame.sprite.groupcollide(player_sprites_list, player2_sprites_list, 0, 0):
            if not invincible:
                zombie_attack_melee_sound.play()
                player_hit.play()
                current = hearts[-1]
                current.kill()
                del hearts[-1]
                invincible = True
                pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)
        if not hearts:
            #global current_state
            current_state = screen_states['game_over']
            game_loop = False

        for player in pygame.sprite.groupcollide(player2_sprites_list, player_sprites_list, 0, 0):
            if not invincible:
                bullet_hit_sound.play()
                zombie_hit_sound.play()
                current = hearts[-1]
                current.kill()
                del hearts[-1]
                invincible = True
                pygame.time.set_timer(INVINCIBILITY_END, INVINCIBILITY_DURATION)

        if not hearts:
            pygame.sprite.groupcollide(player_sprites_list, enemy_sprites_list, 1, 0)

        if not hearts2:
            pygame.sprite.groupcollide(player2_sprites_list, player_sprites_list, 1, 0)

        player_sprites_list.update()
        player2_sprites_list.update()
        enemy_sprites_list.update()
        bullet_sprites_list.update()
        health_sprites_list.update()
        spit_sprites.update()
        dead_sprites_list.update()

        # Drawing logic
        offset += 1
        offset2 += 1
        screen.blit(background, (-offset, 0))
        screen.blit(background_horizon, (-offset, 0))

        screen.blit(background, (-offset2, 0))
        screen.blit(background_horizon, (-offset2, 0))

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

        dead_sprites_list.draw(screen)
        player_sprites_list.draw(screen)
        player2_sprites_list.draw(screen)
        enemy_sprites_list.draw(screen)
        bullet_sprites_list.draw(screen)
        health_sprites_list.draw(screen)
        spit_sprites.draw(screen)

        # Screen update
        pygame.display.flip()
        clock.tick(60)

        # Timer updates
        generate_time_based_events(time_since_start_ms)

def help_screen():

    help_menu = Help_menu(WIDTH, HEIGHT)

    global current_state
    help_loop = True

    def button(x,y,w,h,button_type):
        global frozen
        global current_state
        if help_loop:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                if click[0] == 1:
                    frozen = False
                    if button_type == 'back':
                        current_state = screen_states['mainmenu']
                        return False
            return True

    while help_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_state = screen_states['quit']
                help_loop = False

            help_loop = button(WIDTH - 256, HEIGHT - 64, 256, 64, 'back')
        
        screen.blit(help_menu.background, (0, 0))
        help_menu.button_sprites_list.update()
        help_menu.button_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def congrats_screen():

    congrats = Game_Over(WIDTH, HEIGHT)

    global current_state
    congrats_loop = True

    def button(x,y,w,h,button_type):
        global frozen
        global current_state
        if congrats_loop:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                if click[0] == 1:
                    frozen = False
                    if button_type == 'back':
                        current_state = screen_states['mainmenu']
                        return False
                    if button_type == 'quit':
                        current_state = screen_states['quit']
                        return False
            return True

    while congrats_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_state = screen_states['quit']
                congrats_loop = False
            
                
        congrats_loop = button(WIDTH / 2 - 128, HEIGHT / 2 - 32, 254,  64, 'back')
        congrats_loop = button(WIDTH / 2 - 128, HEIGHT / 2 + 35, 256, 64, 'quit')
        go_background = pygame.image.load("Assets/Backgrounds/congratulations.png").convert_alpha()
            
        screen.blit(go_background, (0, HEIGHT/3-100))
        congrats.button_sprites_list.update()
        congrats.button_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def game_over_screen():

    game_over = Game_Over(WIDTH, HEIGHT)

    global current_state
    game_over_loop = True

    def button(x,y,w,h,button_type):
        global frozen
        global current_state
        if game_over_loop:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                if click[0] == 1:
                    frozen = False
                    if button_type == 'back':
                        current_state = screen_states['mainmenu']
                        return False
                    if button_type == 'quit':
                        current_state = screen_states['quit']
                        return False
            return True

    while game_over_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_state = screen_states['quit']
                game_over_loop = False
            
                
        game_over_loop = button(WIDTH / 2 - 128, HEIGHT / 2 - 32, 254,  64, 'back')
        game_over_loop = button(WIDTH / 2 - 128, HEIGHT / 2 + 35, 256, 64, 'quit')
        go_background = pygame.image.load("Assets/Backgrounds/game_over.png").convert_alpha()
            
        screen.blit(go_background, (0, HEIGHT/3-100))
        game_over.button_sprites_list.update()
        game_over.button_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)



screen_states = {
    'mainmenu': 0,
    'singleplayer': 1,
    'multiplayer': 2,
    'help': 3,
    'congrats': 7,
    'game_over': 8,
    'quit': 9
}

current_state = screen_states['mainmenu']
while main_loop:
    if current_state == screen_states['mainmenu']:
        main_menu_screen()
    elif current_state == screen_states['singleplayer']:
        singleplayer_screen()
    elif current_state == screen_states['multiplayer']:
        multiplayer_screen()
    elif current_state == screen_states['help']:
        help_screen()
    elif current_state == screen_states['congrats']:
        congrats_screen()
    elif current_state == screen_states['game_over']:
        game_over_screen()
    elif current_state == screen_states['quit']:
        main_loop = False

pygame.quit()

