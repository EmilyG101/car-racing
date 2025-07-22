import pygame
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Game variables
gravity = 0.5
flap_power = -10
pipe_gap = 150
pipe_width = 70
pipe_velocity = 3

# Load bird
bird_img = pygame.Surface((34, 24))
bird_img.fill((255, 255, 0))

# Button
def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = (200, 200, 200) if x < mouse[0] < x + w and y < mouse[1] < y + h else (180, 180, 180)
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = small_font.render(text, True, BLACK)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel = 0

    def update(self):
        self.vel += gravity
        self.y += self.vel

    def flap(self):
        self.vel = flap_power

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.top = random.randint(50, HEIGHT - pipe_gap - 50)
        self.passed = False

    def update(self):
        self.x -= pipe_velocity

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, pipe_width, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, self.top + pipe_gap, pipe_width, HEIGHT))

def reset_game():
    global bird, pipes, score, game_active
    bird = Bird()
    pipes = []
    score = 0
    game_active = True

def show_start_screen():
    while True:
        screen.fill(SKY_BLUE)
        title = font.render("Flappy Bird", True, BLACK)
        screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 3))
        draw_button("Start", WIDTH // 2 - 50, HEIGHT // 2, 100, 40, reset_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
        if game_active:
            break

def show_game_over():
    while True:
        screen.fill(SKY_BLUE)
        over = font.render("Game Over", True, BLACK)
        score_label = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(over, ((WIDTH - over.get_width()) // 2, HEIGHT // 3))
        screen.blit(score_label, ((WIDTH - score_label.get_width()) // 2, HEIGHT // 3 + 50))
        draw_button("Restart", WIDTH // 2 - 60, HEIGHT // 2, 120, 40, reset_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
        if game_active:
            break

# Start game
game_active = False
show_start_screen()

reset_game()

# Game loop
while True:
    screen.fill(SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()

    if game_active:
        bird.update()
        bird.draw()

        # Pipe logic
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes[:]:
            pipe.update()
            pipe.draw()
            # Collision
            if bird.y < pipe.top or bird.y > pipe.top + pipe_gap:
                if pipe.x < bird.x + 34 < pipe.x + pipe_width:
                    game_active = False

            if pipe.x + pipe_width < 0:
                pipes.remove(pipe)

            # Score
            if not pipe.passed and pipe.x + pipe_width < bird.x:
                pipe.passed = True
                score += 1

        if bird.y > HEIGHT:
            game_active = False

        # Display score
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (WIDTH // 2, 20))
    else:
        show_game_over()

    pygame.display.update()
    clock.tick(60)
