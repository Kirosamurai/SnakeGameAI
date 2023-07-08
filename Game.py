import pygame
import time
import random

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

def game_over():
    font = pygame.font.SysFont('comic sans', 20)
    game_over_surface = font.render("Final Score: " + str(score), True, red)
    game_over_rect = game_over_surface.get()
    game_over_rect.center = (screen_height//4, screen_width//4)

    screen.blit(game_over_surface, game_over_rect)
    pygame.display.update()


#width and height of window
screen_width = 720
screen_height = screen_width * 0.8

#colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#snake speed
speed = 5

pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
fps = pygame.time.Clock() 

#snake position
position = [screen_width/2, screen_height/2]

#snake body
body = [[(screen_width/2), screen_height/2], [(screen_width/2)-10, screen_height/2], [(screen_width/2)-20, screen_height/2], [(screen_width/2)-30, screen_height/2]]

#fruit spawn location and boolean
fruit_spawn = [360, 120]
fruit = True

#initial direction
direction = 'UP'
change = direction

score = 0

#Main Function
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        

        if event.type == pygame.K_UP:
            change = 'UP'
        elif event.type == pygame.K_LEFT:
            change = 'LEFT'
        elif event.type == pygame.K_RIGHT:
            change = 'RIGHT'
        elif event.type == pygame.K_DOWN:
            change = 'DOWN'


    if change == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        position[1] -= 10
    if direction == 'DOWN':
        position[1] += 10
    if direction == 'LEFT':
        position[0] -= 10
    if direction == 'RIGHT':
        position[0] += 10
        
    body.insert(0, list(position))

    if position[0] == fruit_spawn[0] and position[1] == fruit_spawn[1]:
        score += 1
        fruit = False
    else:
        body.pop()

    if not fruit:
        fruit_spawn = fruit_spawn = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10))*10]

        fruit = True
    
    screen.fill(black)

    for it in body:
        pygame.draw.rect(screen, green, pygame.Rect(it[0], it[1], 10, 10))

    pygame.draw.rect(screen, red, pygame.Rect(fruit_spawn[0], fruit_spawn[1], 10, 10))

    if position[0] < 0 or position[1] > screen_width:
        game_over()
        run = False
        pygame.QUIT()
    
    if position[1] < 0 or position[1] > screen_height:
        game_over()
        run = False
        pygame.QUIT()
    
    for it in body[1::1]:
        if position[0] == it[0] and position[1] == it[1]:
            game_over()
            run = False
            pygame.QUIT()
    
    show_score(1, white, 'comic sans', 20)

    pygame.display.update()

    fps.tick(speed)