import json

import pygame
from constants import *
from camera import Camera
from player import Player

pygame.init()


class Game:
    def __init__(self):
        with open("config/conf.json", "r") as file:
            config = json.load(file)
        self.width = config["screen"]["width"]
        self.height = config["screen"]["height"]
        self.fullscreen = config["screen"]["fullscreen"]
        font_path = config["font"]["path"]
        font_size = config["font"]["size"]
        self.max_fps = config["max_fps"]

        self.level_cols = None
        self.level_rows = None
        self.level_block_size = None
        self.canvas = None
        self.camera = None
        self.player = None

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, font_size)
        fullscreen = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_type = fullscreen if self.fullscreen else pygame.NOFRAME
        self.screen = pygame.display.set_mode((self.width, self.height), screen_type)
        self.start_x, self.start_y, self.y_speed, self.x_speed = 100, 100, 0, 0
        self.running = True
        self.delay = 0

        self.load(config["entry_level"])

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

            camera_x = self.follow(self.camera.pos['x'], self.player.x, 10 * self.delay)
            camera_y = self.follow(self.camera.pos['y'], self.player.y, 10 * self.delay)

            self.camera.pos["x"] = camera_x
            self.camera.pos["y"] = camera_y
            self.camera.update_rect()

            self.player.keyboard(pygame.key.get_pressed())
            self.player.update(self.delay)
            self.player.draw(screen=self.canvas)

            self.camera.surface.blit(self.canvas.subsurface(self.camera.rect), (0, 0))
            self.screen.blit(pygame.transform.smoothscale(self.camera.surface, (self.width, self.height)), (0, 0))

            pygame.display.update()

            pygame.draw.rect(self.canvas, RED, self.camera.rect, 0)
            self.delay = self.clock.tick(self.max_fps) / 1000

    def load(self, level_str):
        with open(f"levels/{level_str}.json", "r") as file:
            level = json.load(file)
        self.level_cols = level["cols"]
        self.level_rows = level["rows"]
        self.level_block_size = level["block_size"]
        self.start_x, self.start_y = level["start"]["x"], level["start"]["y"]
        level_width = self.level_cols * self.level_block_size
        level_height = self.level_rows * self.level_block_size
        self.canvas = pygame.Surface((level_width, level_height))
        self.player = Player(self.start_x, self.start_y, 32, 32)
        self.camera = Camera(self.screen.get_size(),self.canvas.get_size(), self.level_block_size)

        self.camera.update_rect()
        self.camera.pos["x"] = self.player.x
        self.camera.pos["x"] = self.player.y
        self.blocks = dict()

    @staticmethod
    def follow(camera_pos, player_pos, speed):
        return camera_pos + (player_pos - camera_pos) * speed


    def restart(self):
        self.player.x = self.start_x
        self.player.y = self.start_y
        self.player.x_speed = self.x_speed
        self.player.y_speed = self.y_speed


instance = Game()
