import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 480, 640
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

# Load images
player_car = pygame.image.load("car.png")
enemy_car = pygame.image.load("enemy_car.png")
road = pygame.image.load("road.png")
road = pygame.transform.scale(road, (WIDTH, HEIGHT))

# Resize cars
player_car = pygame.transform.scale(player_car, (50, 90))
enemy_car = pygame.transform.scale(enemy_car, (50, 90))

# Fonts
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()
FPS = 60

def draw_text(text, font, color, surface, x, y):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y))
    surface.blit(txt, rect)

# Buttons
def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = (200, 200, 200) if x+w > mouse[0] > x and y+h > mouse[1] > y else (150, 150, 150)
    pygame.draw.rect(win, color, (x, y, w, h))
    draw_text(text, small_font, (0, 0, 0), win, x + w//2, y + h//2)
    if x+w > mouse[0] > x and y+h > mouse[1] > y and click[0] == 1 and action:
        pygame.time.delay(200)
        action()

# Game states
game_active = False
game_over = False

# Game variables
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120
player_speed = 5

enemy_speed = 5
enemy_timer = 0
enemies = []

def reset_game():
    global enemies, player_x, game_active, game_over
    enemies = []
    player_x = WIDTH // 2 - 25
    game_active = True
    game_over = False

def show_start_screen():
    win.blit(road, (0, 0))
    draw_text("Racing Game", font, (255, 255, 255), win, WIDTH//2, HEIGHT//3)
    draw_button("Start", WIDTH//2 - 60, HEIGHT//2, 120, 50, reset_game)

def show_game_over():
    win.blit(road, (0, 0))
    draw_text("Game Over", font, (255, 0, 0), win, WIDTH//2, HEIGHT//3)
    draw_button("Restart", WIDTH//2 - 60, HEIGHT//2, 120, 50, reset_game)

# Main loop
run = True
while run:
    clock.tick(FPS)
    win.blit(road, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_active and not game_over:
        show_start_screen()
    elif game_over:
        show_game_over()
    else:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed

        # Spawn enemies
        enemy_timer += 1
        if enemy_timer > 50:
            enemy_x = random.randint(0, WIDTH - 50)
            enemies.append(pygame.Rect(enemy_x, -100, 50, 90))
            enemy_timer = 0

        # Move enemies
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.colliderect(pygame.Rect(player_x, player_y, 50, 90)):
                game_over = True
                game_active = False

        # Draw player
        win.blit(player_car, (player_x, player_y))

        # Draw enemies
        for enemy in enemies:
            win.blit(enemy_car, (enemy.x, enemy.y))

    pygame.display.update()

pygame.quit()
sys.exit()

