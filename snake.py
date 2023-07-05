import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")

# Load the background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

# Set the snake and food size
SNAKE_SIZE = 20
FOOD_SIZE = 20

# Set the eye and tongue size
EYE_SIZE = 5
TONGUE_SIZE = 5

# Set the game clock
clock = pygame.time.Clock()

# Set the font for displaying score
font_style = pygame.font.SysFont(None, 50)


def display_score(score, game_over_flag):
    """Display the score on the game window"""
    if game_over_flag:
        score_text = font_style.render("Score: " + str(score), True, WHITE)
        window.blit(score_text, [10, 10])


def draw_snake(snake_body):
    """Draw the snake on the game window"""
    for snake_part in snake_body:
        pygame.draw.rect(window, GREEN, [snake_part[0], snake_part[1], SNAKE_SIZE, SNAKE_SIZE])
        pygame.draw.circle(window, BLACK, [snake_part[0] + SNAKE_SIZE // 4, snake_part[1] + SNAKE_SIZE // 4], EYE_SIZE)
        pygame.draw.circle(window, BLACK, [snake_part[0] + SNAKE_SIZE // 4 * 3, snake_part[1] + SNAKE_SIZE // 4], EYE_SIZE)
        pygame.draw.rect(window, RED, [snake_part[0] + SNAKE_SIZE // 2 - TONGUE_SIZE // 2,
                                        snake_part[1] + SNAKE_SIZE, TONGUE_SIZE, SNAKE_SIZE // 2])


def draw_food(food_position):
    """Draw the food on the game window"""
    pygame.draw.rect(window, RED, [food_position[0], food_position[1], FOOD_SIZE, FOOD_SIZE])


def draw_border():
    """Draw the border around the game window"""
    pygame.draw.rect(window, WHITE, [0, 0, WINDOW_WIDTH, SNAKE_SIZE])
    pygame.draw.rect(window, WHITE, [0, 0, SNAKE_SIZE, WINDOW_HEIGHT])
    pygame.draw.rect(window, WHITE, [0, WINDOW_HEIGHT - SNAKE_SIZE, WINDOW_WIDTH, SNAKE_SIZE])
    pygame.draw.rect(window, WHITE, [WINDOW_WIDTH - SNAKE_SIZE, 0, SNAKE_SIZE, WINDOW_HEIGHT])


def game_over(score):
    """Display the game over message and restart or quit the game"""
    while True:
        window.fill(BLACK)
        window.blit(background_image, (0, 0))
        message("Game Over!", RED)
        display_score(score, True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()


def message(msg, color):
    """Display a message on the game window"""
    text = font_style.render(msg, True, color)
    window.blit(text, [WINDOW_WIDTH / 6, WINDOW_HEIGHT / 3])


def game_loop():
    """The main game loop"""
    # Set the initial position and direction of the snake
    x = WINDOW_WIDTH / 2
    y = WINDOW_HEIGHT / 2
    x_change = 0
    y_change = 0

    # Set the initial length and speed of the snake
    snake_body = []
    snake_length = 1
    snake_speed = 15

    # Set the initial food position
    food_position = [random.randrange(1, (WINDOW_WIDTH // FOOD_SIZE)) * FOOD_SIZE,
                     random.randrange(1, (WINDOW_HEIGHT // FOOD_SIZE)) * FOOD_SIZE]

    # Set the game over flag and score
    game_over_flag = False
    score = 0

    while not game_over_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_SIZE
                    x_change = 0

        # Update the snake position
        x += x_change
        y += y_change

        # Check for collision with the boundaries of the game window
        if x >= WINDOW_WIDTH or x < 0 or y >= WINDOW_HEIGHT or y < 0:
            game_over(score)

        # Update the game window
        window.blit(background_image, (0, 0))
        draw_border()
        draw_snake(snake_body)
        draw_food(food_position)
        display_score(score, False)

        # Update the snake body
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check for collision with the snake's body
        for part in snake_body[:-1]:
            if part == snake_head:
                game_over(score)

        # Check for collision with the food
        if x == food_position[0] and y == food_position[1]:
            food_position = [random.randrange(1, (WINDOW_WIDTH // FOOD_SIZE)) * FOOD_SIZE,
                             random.randrange(1, (WINDOW_HEIGHT // FOOD_SIZE)) * FOOD_SIZE]
            snake_length += 1
            score += 1

        # Update the game display
        pygame.display.update()

        # Set the game speed
        clock.tick(snake_speed)


def start_menu():
    """Display the start menu and handle options"""
    while True:
        window.fill(BLACK)
        window.blit(background_image, (0, 0))
        message("Snake Game", GREEN)
        display_score(0, False)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return


# Start the game
start_menu()