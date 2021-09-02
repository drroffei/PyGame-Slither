import pygame
import random

import pygame.examples.vgrade

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

# pygame.display.flip() update the whole screen
# pygame.display.update() update a given surface, if null the whole surface

clock = pygame.time.Clock()

block_size = 20
FPS = 10
direction = "right"

font = pygame.font.SysFont(None, 25)

img = pygame.image.load('snakehead.png')


def snake(block_size, snake_list):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)

    if direction == "left":
        head = pygame.transform.rotate(img, 90)

    if direction == "up":
        head = img

    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))

    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])
        # [x-pos, y-pos, width, height] - This is the "snake"


def text_objects(text, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color):
    text_surface, text_rect = text_objects(msg, color)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    text_rect.center = (display_width/2), (display_height/2)
    gameDisplay.blit(text_surface, text_rect)


def game_loop():
    global direction
    game_exit = False
    game_over = False

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 2
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    rand_apple_x = random.randrange(0, display_width-block_size)#, block_size)
    rand_apple_y = random.randrange(0, display_height-block_size)#, block_size)

    while not game_exit:
        while game_over:
            gameDisplay.fill(white)
            message_to_screen("Game over, press 'c' to play again or 'q' to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change -= block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change += block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change -= block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change += block_size
                    lead_x_change = 0

        if lead_x < 0 or lead_x > 790 or lead_y < 0 or lead_y > 590:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)
        apple_thickness = 30
        pygame.draw.rect(gameDisplay, red, [rand_apple_x, rand_apple_y, apple_thickness, apple_thickness])
        # [x-pos, y-pos, width, height] - This is the apple

        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for eachSegment in snake_list[:-1]:
            if eachSegment == snake_head:
                game_over = True

        snake(block_size, snake_list)

        pygame.display.update()

        # Collision
        # if rand_apple_x <= lead_x <= rand_apple_x + (apple_thickness - block_size):
        #     if rand_apple_y <= lead_y <= rand_apple_y + (apple_thickness - block_size):
        #         rand_apple_x = random.randrange(0, display_width - block_size)#, block_size)
        #         rand_apple_y = random.randrange(0, display_height - block_size)#, block_size)
        #         snake_length += 1

        if lead_x > rand_apple_x and lead_x < rand_apple_x + apple_thickness or lead_x + block_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_thickness:
            if lead_y > rand_apple_y and lead_y < rand_apple_y + apple_thickness:
                print("x and y crossover")
                rand_apple_x = random.randrange(0, display_width - block_size)
                rand_apple_y = random.randrange(0, display_height - block_size)
                snake_length += 1

            elif lead_y + block_size > rand_apple_y and lead_y + block_size < rand_apple_y + apple_thickness:
                print("x and y cross over")
                rand_apple_x = random.randrange(0, display_width - block_size)
                rand_apple_y = random.randrange(0, display_height - block_size)
                snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()


game_loop()
