import pygame
import time
import random

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

# Initializing pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('AlBot Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

# defining first blocks of snake body
snake_body = [[100, 50],
              [90, 50]]

# fruit position
food_position = [random.randrange(1, (window_x // 10)) * 10,
                 random.randrange(1, (window_y // 10)) * 10]
food_spawn = True

# power-up food position
godmode_position = None
godmode_spawn = False
godmode_eaten = False
betterApple_position = None
betterApple_spawn = False
betterApple_eaten = False

# setting initial snake direction randomly
direction = random.choice(['RIGHT', 'LEFT', 'UP', 'DOWN'])
change_to = direction

# initial score
score = 0

# Power-Ups state and timer
godmode = False
godmode_start_time = 0
betterApple = False
betterApple_start_time = 0

# Font settings
font = pygame.font.SysFont('times new roman', 30)

# displaying Score function
def show_score(color):
    score_surface = font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect(center=(window_x // 2, 30))
    game_window.blit(score_surface, score_rect)

# displaying GODMODE timer function
def show_godmode_timer(remaining_time):
    timer_surface = font.render('GODMODE: ' + str(round(remaining_time, 1)) + 's', True, white)
    timer_rect = timer_surface.get_rect(center=(window_x // 2, 60))
    game_window.blit(timer_surface, timer_rect)

# displaying BetterApple timer function
def show_betterApple_timer(remaining_time):
    timer_surface = font.render('BetterApple: ' + str(round(remaining_time, 1)) + 's', True, white)
    timer_rect = timer_surface.get_rect(center=(window_x // 2, 60))
    game_window.blit(timer_surface, timer_rect)

# game over function
def game_over():
    game_over_surface = font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect(center=(window_x // 2, window_y // 2))
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Start screen function
def start_screen():
    game_title = font.render('AlBot Snake Game', True, white)
    title_rect = game_title.get_rect(center=(window_x // 2, window_y // 4))
    game_window.blit(game_title, title_rect)

    start_text = font.render('Click to Start', True, white)
    start_rect = start_text.get_rect(center=(window_x // 2, window_y // 2))
    game_window.blit(start_text, start_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Pause screen Function
def show_pause_screen():
    pause_text = font.render('Paused', True, white)
    pause_rect = pause_text.get_rect(center=(window_x // 2, window_y // 2))
    game_window.blit(pause_text, pause_rect)
    pygame.display.flip()

# Main Function
def main():
    global direction, change_to, snake_position, snake_body, food_position, food_spawn, score
    global godmode_position, godmode_spawn, godmode_eaten, godmode, godmode_start_time
    global betterApple_position, betterApple_spawn, betterApple_eaten, betterApple, betterApple_start_time


    start_screen()

    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    change_to = 'UP'
                if event.key == pygame.K_s:
                    change_to = 'DOWN'
                if event.key == pygame.K_a:
                    change_to = 'LEFT'
                if event.key == pygame.K_d:
                    change_to = 'RIGHT'
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_m:
                    score += 10
                if event.key == pygame.K_u:
                    if len(snake_body) > 2:
                        snake_body.pop()

        if paused:
            show_pause_screen()
            continue

        # If two keys pressed simultaneously
        # we don't want snake to move into two 
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if godmode:
            if direction == 'UP':
                snake_position[1] -= 10
                if snake_position[1] < 0:
                    snake_position[1] = window_y - 10
            if direction == 'DOWN':
                snake_position[1] += 10
                if snake_position[1] >= window_y:
                    snake_position[1] = 0
            if direction == 'LEFT':
                snake_position[0] -= 10
                if snake_position[0] < 0:
                    snake_position[0] = window_x - 10
            if direction == 'RIGHT':
                snake_position[0] += 10
                if snake_position[0] >= window_x:
                    snake_position[0] = 0
        else:
            # Default movement logic without wrap-around behavior
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            if betterApple:
                score += 20  # Increment score by 20 for betterApple
                snake_body.append(list(snake_body[-1]))  # Add two segments
            else:
                score += 10  # Increment score by 10 for regular food
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn and not godmode_spawn and not betterApple_spawn:
            food_position = [random.randrange(1, (window_x // 10)) * 10,
                            random.randrange(1, (window_y // 10)) * 10]
            food_spawn = True

        # Spawn power-up foods
        if score >= 200 and not godmode_spawn and not godmode_eaten:
            godmode_position = [random.randrange(1, (window_x // 10)) * 10,
                                random.randrange(1, (window_y // 10)) * 10]
            godmode_spawn = True
            food_spawn = False  # Ensure normal food doesn't spawn with power-up food

        if score >= 450 and not betterApple_spawn and not betterApple_eaten:
            betterApple_position = [random.randrange(1, (window_x // 10)) * 10,
                                    random.randrange(1, (window_y // 10)) * 10]
            betterApple_spawn = True
            food_spawn = False  # Ensure normal food doesn't spawn with power-up food


        # Check if snake has eaten power-up foods
        if godmode_spawn and snake_position[0] == godmode_position[0] and snake_position[1] == godmode_position[1]:
            godmode = True
            godmode_start_time = time.time()
            godmode_spawn = False
            godmode_eaten = True
            snake_body.append(list(snake_body[-1]))
            score += 10

        if betterApple_spawn and snake_position[0] == betterApple_position[0] and snake_position[1] == betterApple_position[1]:
            betterApple = True
            betterApple_start_time = time.time()
            betterApple_spawn = False
            betterApple_eaten = True
            snake_body.append(list(snake_body[-1]))
            score += 10

        # Disable GODMODE after 20 seconds
        if godmode and time.time() - godmode_start_time > 20:
            godmode = False

        # Disable Better Apple after 15 seconds
        if betterApple and time.time() - betterApple_start_time > 15:
            betterApple = False

        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        if food_spawn:
            pygame.draw.rect(game_window, red, pygame.Rect(food_position[0], food_position[1], 10, 10))

        if godmode_spawn:
            pygame.draw.rect(game_window, blue, pygame.Rect(godmode_position[0], godmode_position[1], 10, 10))

        if betterApple_spawn:
            pygame.draw.rect(game_window, yellow, pygame.Rect(betterApple_position[0], betterApple_position[1], 10, 10))

        # Game Over conditions
        if not godmode:
            if snake_position[0] < 0 or snake_position[0] > window_x - 10:
                game_over()
            if snake_position[1] < 0 or snake_position[1] > window_y - 10:
                game_over()

            # Touching the snake body
            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over()

        # displaying score continuously
        show_score(white)

        # displaying GODMODE timer
        if godmode:
            remaining_time = 20 - (time.time() - godmode_start_time)
            show_godmode_timer(remaining_time)

        # displaying Better Apple timer
        if betterApple:
            remaining_time = 20 - (time.time() - betterApple_start_time)
            show_betterApple_timer(remaining_time)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(15)


if __name__ == "__main__":
    main()