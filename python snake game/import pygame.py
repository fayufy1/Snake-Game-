import pygame
import time
import random

# Initialize the game
pygame.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (138, 43, 226)
ORANGE = (255, 165, 0)

# Game window size
width, height = 600, 400
game_window = pygame.display.set_mode((width, height))

# Game title
pygame.display.set_caption('Snake Game')

# Frame rate control
clock = pygame.time.Clock()

# Snake block size
snake_block = 20  # Increased for better visuals
snake_speed = 10  # Reduced initial speed for smoother gameplay

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Sound effects
eat_sound = pygame.mixer.Sound('snake-hiss-95241.mp3')  # The hissing sound for food
pygame.mixer.music.load('Snake.io Music.mp3')  # Background music

# Function to display the score
def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    game_window.blit(value, [0, 0])

# Function to display the high score
def high_score_display(high_score):
    value = font_style.render("High Score: " + str(high_score), True, WHITE)
    game_window.blit(value, [400, 0])

# Snake function with rounded visuals
def our_snake(snake_block, snake_list):
    for i, pos in enumerate(snake_list):
        # Gradient/alternating colors
        color = (255 - (i * 5) % 255, 153, (213 + i * 5) % 255)  # Dynamic color change
        pygame.draw.circle(game_window, color, [int(pos[0] + snake_block // 2), int(pos[1] + snake_block // 2)], snake_block // 2)

# Display message function
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_window.blit(mesg, [width / 6, height / 3])

# Starting screen
def start_screen():
    game_window.fill(BLACK)
    message("Welcome to Snake Game! Press S to Start or Q to Quit", YELLOW)
    pygame.display.update()

    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start = True
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main game loop
def gameLoop():
    game_over = False
    game_close = False
    high_score = 0

    # Starting screen before the game starts
    start_screen()

    pygame.mixer.music.play(-1)  # Loop background music

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close == True:
            game_window.fill(BLACK)
            message("Game Over! Press C to Play Again or Q to Quit", RED)
            your_score(length_of_snake - 1)
            high_score_display(high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        game_window.fill(GREEN)

        pygame.draw.rect(game_window, RED, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        # Update high score
        if length_of_snake - 1 > high_score:
            high_score = length_of_snake - 1
        high_score_display(high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            length_of_snake += 1
            eat_sound.play()

        clock.tick(snake_speed + length_of_snake // 4)  # Increase speed with length

    pygame.quit()
    quit()

# Pause functionality
def pause_game():
    paused = True
    message("Game Paused. Press P to Resume", YELLOW)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

gameLoop()
