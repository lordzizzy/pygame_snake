import sys
import pygame

pygame.init()

width = 1920
height = 1080
size = (width, height)
speed = [2, 2]
black = pygame.Color(0, 0, 0)
screen = pygame.display.set_mode(size)
ball = pygame.image.load("res/intro_ball.gif")
ball_rect = ball.get_rect()
keys = pygame.key.get_pressed()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
        elif event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    ball_rect = ball_rect.move(speed)

    if ball_rect.left < 0 or ball_rect.right > width:
        speed[0] *= -1
    if ball_rect.top < 0 or ball_rect.bottom > height:
        speed[1] *= -1

    screen.fill(black)
    screen.blit(ball, ball_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
