import pygame
from constants import *
from player import Player

pygame.init()


class Game:
    def __init__(self):
        self.width = 1080
        self.height = 1080
        self.fullscreen = False
        font_path = 'fonts/Pixellari.ttf'
        font_size = 16
        self.max_fps = 60
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, font_size)
        fullscreen = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_type = fullscreen if self.fullscreen else pygame.NOFRAME
        self.screen = pygame.display.set_mode((self.width, self.height), screen_type)
        self.start_x, self.start_y, self.y_speed, self.x_speed = 100, 100, 0, 0
        self.player = Player(self.start_x, self.start_y, 32, 32)
        self.running = True
        self.delay = 0

    def start(self):
        while self.running:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()

            self.player.keyboard(pygame.key.get_pressed())
            self.player.update(self.delay)
            self.player.draw(screen=self.screen)
            pygame.display.update()
            self.delay = self.clock.tick(60) / 1000

    def restart(self):
        self.player.x = self.start_x
        self.player.y = self.start_y
        self.player.x_speed = self.x_speed
        self.player.y_speed = self.y_speed


instance = Game()
