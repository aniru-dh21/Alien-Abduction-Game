import pygame
import random
import sys

def start_screen(screen):
    
    WIDTH, HEIGHT = 800, 600
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FONT_SIZE = 30

    font = pygame.font.Font(None, FONT_SIZE)

    screen.fill(BLACK)

    intro_text = [
        "Welcome, Alien Abductor!",
        "You're behind on your weekly quota of abductions.",
        "Help the alien catch up by abducting targets on Earth!",
        "",
        "----------------------------------------------------------------------------------------------",
        "Move the UFO with ARROWS and", 
        "press SPACE to abduct cows with the track bean.",
        "----------------------------------------------------------------------------------------------",
        "",
        "Press any key to start the game...",
        "",
    ]

    y_position = HEIGHT // 4
    for line in intro_text:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        y_position += FONT_SIZE

    pygame.display.flip()

    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_text_on_screen(screen, text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, (255, 255, 255))
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)

def game_over_screen(screen):
    screen.fill((0, 0, 0))  
    show_text_on_screen(screen, "Game Over", 50, HEIGHT // 3)
    show_text_on_screen(screen, f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def victory_screen(screen):
    screen.fill((0, 0, 0))
    show_text_on_screen(screen, "Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(screen, f"You've completed all levels with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen(screen, "Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

ovni = pygame.image.load("ovni.png")
cow = pygame.image.load("cow.png")

ovni = pygame.transform.scale(ovni, (50, 50))
cow = pygame.transform.scale(cow, (40, 40))

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)  
SHIP_GREEN = (0, 255, 0)  
GRASS_GREEN = (0, 100, 0)  
STAR_COUNT = int(WIDTH * HEIGHT * 0.001)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Abduction Game")

clock = pygame.time.Clock()

player_rect = pygame.Rect(WIDTH // 2 - 25, 10, 50, 50)
player_speed = 5

targets = []

score = 0

font = pygame.font.Font(None, 36)

space_pressed = False

stars = [{'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'size': random.randint(1, 3),
          'color': LIGHT_BLUE} for _ in range(STAR_COUNT)]

grass_rect = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)

current_level = 1
abduction_target = 10  
countdown_timer = 60  
current_score = 0  

target_spawn_counter = 0
TARGET_SPAWN_RATE = max(30, 120 - (current_level * 90))

level_colors = [
    LIGHT_BLUE,
    ORANGE,
    RED,
    YELLOW,
    GRAY,
    (0, 255, 0),  
    (255, 0, 255),  
    (0, 255, 255),  
    (255, 165, 0),  
    (128, 0, 128),  
]

start_screen(screen)

running = True
game_started = False  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_started:
                game_started = True
                continue
            elif event.key == pygame.K_SPACE:
                space_pressed = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space_pressed = False

    keys = pygame.key.get_pressed()

    player_rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
    player_rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed

    player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, HEIGHT - player_rect.height))

    target_spawn_counter += 1
    if target_spawn_counter >= TARGET_SPAWN_RATE:
        target_rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT - 50, 50, 50)
        targets.append(target_rect)
        target_spawn_counter = 0

    for star in stars:
        star['size'] += 0.05
        if star['size'] > 3:
            star['size'] = 1
        star['color'] = level_colors[current_level - 1]

    screen.fill(BLACK)

    for star in stars:
        pygame.draw.circle(screen, star['color'], (star['x'], star['y']), int(star['size']))

    pygame.draw.rect(screen, GRASS_GREEN, grass_rect)

    screen.blit(ovni, player_rect)
    
    for target in targets:
        screen.blit(cow, target)

    if space_pressed:
        tractor_beam_rect = pygame.Rect(player_rect.centerx - 2, player_rect.centery, 4, HEIGHT - player_rect.centery)
        pygame.draw.line(screen, YELLOW, (player_rect.centerx, player_rect.centery),
                         (player_rect.centerx, HEIGHT), 2)

        for target in targets[:]:
            if tractor_beam_rect.colliderect(target):
                
                pygame.draw.line(screen, YELLOW, (player_rect.centerx, player_rect.centery),
                                 (player_rect.centerx, target.bottom), 2)
                
                pygame.draw.rect(screen, RED, target)
                targets.remove(target)
                current_score += 1
                score += 1

    info_line_y = 10  
    info_spacing = 75  

    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    timer_text = font.render(f"Time: {int(countdown_timer)}", True, WHITE)
    timer_rect = timer_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, RED, timer_rect.inflate(10, 5))
    screen.blit(timer_text, timer_rect)
    
    targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
    targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, GRAY, targets_rect.inflate(10, 5))
    screen.blit(targets_text, targets_rect)

    pygame.display.flip()

    clock.tick(FPS)

    countdown_timer -= 1 / FPS  
    if countdown_timer <= 0:
        
        if current_score < abduction_target:
            
            game_over_screen(screen)
            running = False
        else:

            current_level += 1
            if current_level <= 10:
                current_score = 0
                abduction_target = 10 * current_level
                countdown_timer = 60  
                
                targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
                targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))

    if current_score >= abduction_target:
        
        current_level += 1
        if current_level <= 10:
            current_score = 0
            abduction_target = 10 * current_level
            countdown_timer = 60  

            targets_text = font.render(f"Abductions: {current_score}/{abduction_target}", True, WHITE)
            targets_rect = targets_text.get_rect(topleft=(timer_rect.topright[0] + info_spacing, info_line_y))
        else:
            victory_screen(screen)
            running = False

pygame.quit()