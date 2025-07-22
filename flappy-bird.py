import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)

# Game settings
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 150

# Bird
bird = pygame.Rect(100, 250, 30, 30)
bird_velocity = 0

# Pipes
pipe_width = 60
pipes = []

def spawn_pipe():
    height = random.randint(100, 400)
    top = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom = pygame.Rect(WIDTH, height + PIPE_GAP, pipe_width, HEIGHT - height - PIPE_GAP)
    pipes.append((top, bottom))

# Score
score = 0
font = pygame.font.SysFont(None, 48)

# Clock
clock = pygame.time.Clock()

# Spawn first pipe
spawn_pipe()
frame_count = 0

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLUE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = FLAP_STRENGTH

    # Bird physics
    bird_velocity += GRAVITY
    bird.y += int(bird_velocity)

    # Draw bird
    pygame.draw.ellipse(screen, WHITE, bird)

    # Pipes
    new_pipes = []
    for top, bottom in pipes:
        top.x -= PIPE_SPEED
        bottom.x -= PIPE_SPEED

        pygame.draw.rect(screen, GREEN, top)
        pygame.draw.rect(screen, GREEN, bottom)

        if top.right > 0:
            new_pipes.append((top, bottom))

        # Score check
        if top.right == bird.left:
            score += 1

        # Collision check
        if bird.colliderect(top) or bird.colliderect(bottom):
            running = False

    pipes = new_pipes

    # Add new pipe every 90 frames
    frame_count += 1
    if frame_count % 90 == 0:
        spawn_pipe()

    # Floor/ceiling collision
    if bird.top < 0 or bird.bottom > HEIGHT:
        running = False

    # Display score
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Game over screen
screen.fill((0, 0, 0))
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
score_text = font.render(f"Score: {score}", True, WHITE)
screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
sys.exit()

