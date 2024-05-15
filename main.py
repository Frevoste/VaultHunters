#TO DO
#1.Player Movement
#2.Level Loader
#3.Level Creator
#4.Main Menu
#5.Leaderboard
#6.Communication with Server*
#BDragon1727 - https://bdragon1727.itch.io/16x16-pixel-adventures-character
#analogStudios_ - https://analogstudios.itch.io/four-seasons-platformer-tileset
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()