import json

import pygame
from constants import *
from camera import Camera
from player import Player
import sprites

pygame.init()
pygame.font.init()
pygame.mixer.init()

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
        self.blocks = dict()
        self.bg_sprite = sprites.sprite.get_sprite('BG')
        self.bg_width, self.bg_height = self.bg_sprite.get_size()
        self.how_many_bgs = 1
        self.current_level = 1
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
        self.time = 9999
        self.level_time = 9999

        self.load(config["entry_level"])
        music_path = "music/music.mp3"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

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

            self.draw_blocks()

            self.player.keyboard(pygame.key.get_pressed())
            self.player.update(self.delay)
            self.player.draw(screen=self.canvas)

            self.camera.surface.blit(self.canvas.subsurface(self.camera.rect), (0, 0))
            textsurface = self.font.render(f'Time left: {self.time:.1f}', True, RED)
            self.camera.surface.blit(textsurface, (self.width/2 - 50, 200))
            self.screen.blit(pygame.transform.smoothscale(self.camera.surface, (self.width, self.height)), (0, 0))

            pygame.display.update()

            for i in range(self.how_many_bgs):
                self.canvas.blit(self.bg_sprite, (i*self.bg_width, 0))
            # pygame.draw.rect(self.canvas, RED, self.camera.rect, 0)
            self.delay = self.clock.tick(self.max_fps) / 1000
            self.time -= self.delay
            if self.time < 0:
                self.restart
            self.check_player_position()

    def load(self, level_str):
        self.blocks = dict()
        with open(f"levels/{level_str}.json", "r") as file:
            level = json.load(file)
        self.level_cols = level["cols"]
        self.level_rows = level["rows"]
        self.level_block_size = level["block_size"]
        self.start_x, self.start_y = level["start"]["x"], level["start"]["y"]
        self.level_time = self.time = level["time"]
        level_width = self.level_cols * self.level_block_size
        level_height = self.level_rows * self.level_block_size
        self.canvas = pygame.Surface((level_width, level_height))
        self.how_many_bgs = level_width // self.bg_width + 1
        self.camera = Camera(self.screen.get_size(), self.canvas.get_size(), self.level_block_size)

        self.player = Player(self.start_x, self.start_y, 32, 32, block_size=self.level_block_size, blocks=None)

        self.camera.update_rect()
        self.camera.pos["x"] = self.player.x
        self.camera.pos["x"] = self.player.y
        json_blocks = level["blocks"]
        for block in json_blocks:
            self.add_block(block)

        self.player.update_blocks(self.blocks)



    def add_block(self, block):
        name, x, y, w, h = block["name"], block["x"], block["y"], block["w"], block["h"]
        collision = block["collision"] if "collision" in block else None
        if collision == "die":
            collision = self.restart
        if collision == "win":
            collision = self.level_up

        overflow_x = block["overflow_x"] if "overflow_x" in block else 0
        overflow_y = block["overflow_y"] if "overflow_y" in block else 0
        for row in range(h):
            for col in range(w):
                curr_x = x + col
                curr_y = y + row
                if curr_x not in self.blocks.keys():
                    self.blocks[curr_x] = list()
                self.blocks[curr_x].append((name, collision, overflow_x, overflow_y, curr_x, curr_y))

    def draw_blocks(self):
        for col in self.blocks.keys():
            for block_tuple in self.blocks[col]:
                name, collision, overflow_x, overflow_y, curr_x, curr_y = block_tuple
                x = curr_x * self.level_block_size + overflow_x
                y = curr_y * self.level_block_size + overflow_y
                block_sprite = sprites.sprite.get_sprite(name)
                self.canvas.blit(block_sprite, (x, y))
    @staticmethod
    def follow(camera_pos, player_pos, speed):
        return camera_pos + (player_pos - camera_pos) * speed

    def check_player_position(self):
        canvas_width, canvas_height = self.canvas.get_size()
        if self.player.x > canvas_width:
            self.restart()
        elif self.player.y > canvas_height:
            self.restart()
        elif self.player.x + self.player .width < 0:
            self.restart()

    def level_up(self):
        self.current_level += 1
        self.load('002')

    def restart(self):
        self.time = self.level_time
        self.player.x = self.start_x
        self.player.y = self.start_y
        self.player.x_speed = self.x_speed
        self.player.y_speed = self.y_speed


instance = Game()
