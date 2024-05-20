import pygame
from constants import *
import sprites



class Player:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.sprite = S_IDLE
        self.x_speed, self.y_speed = 0, 0
        self.delay = 0

        self.status = Status(S_IDLE, self)

    def keyboard(self, keys):
        self.status.keyboard(self, keys)
        if keys.key == pygame.KLEFT:
            self.x_speed = -MOVE_SPEED
        if keys.key == pygame.K_RIGHT:
            self.x_speed = MOVE_SPEED

    def update(self, delay):
        self.delay = delay
        self.status.update(self, self.delay)

    def draw(self, screen):
        new_index = self.status.index % self.status.count
        sprite_name = self.sprite + str(new_index)
        sprite = sprites.sprite.get_sprite(sprite_name)
        screen.blit(sprite, (self.x, self.y))

class Status:
    def __init__(self, status_name: str, player: Player):
        self.name = status_name
        self.player = player
        if self.name == S_IDLE:
            self.index, self.count, self.elapsed = self.idle_props()
            self.player.sprite = S_IDLE
            self.keyboard = self.idle_keyboard
            self.update = self.idle_update

        self.elapsed = 0
    @staticmethod
    def idle_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def idle_keyboard(player: Player, keys=None):
        if keys is not None:
            if keys.key == pygame.K_UP:
                player.status = Status(S_JUMP, player)
                player.y_speed = -JUMP_SPEED
            if keys.key == pygame.K_LEFT or keys.key == pygame.K_RIGHT:
                player.status = Status(S_RUN, player)

    def idle_update(self, player: Player, delay):
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        is_falling = False
        # Collision with object
        if is_falling:
            player.y_speed = 10
            player.status = Status(S_FALL, player)

    @staticmethod
    def fall_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def death_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def run_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def jump_props():
        index, count, elapsed = 0, 5, 0
        return index, count, elapsed
