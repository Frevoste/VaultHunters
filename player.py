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
        self.status.keyboard(self=self.status, player=self, keys=keys)
        if keys[pygame.K_LEFT]:
            self.x_speed = -MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.x_speed = MOVE_SPEED

    def update(self, delay):
        self.delay = delay
        self.x += self.x_speed * delay
        self.y += self.y_speed * delay
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
        if self.name == S_FALL:
            self.index, self.count, self.elapsed = self.fall_props()
            self.player.sprite = S_FALL
            self.keyboard = self.fall_keyboard
            self.update = self.fall_update
            self.add_gravity = 0
        if self.name == S_RUN:
            self.index, self.count, self.elapsed = self.run_props()
            self.player.sprite = S_RUN
            self.keyboard = self.run_keyboard
            self.update = self.run_update
        if self.name == S_JUMP:
            self.index, self.count, self.elapsed = self.jump_props()
            self.player.sprite = S_JUMP
            self.keyboard = self.jump_keyboard
            self.update = self.jump_update
        self.elapsed = 0

    # IDLE
    @staticmethod
    def idle_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def idle_keyboard(self, player: Player, keys):
        if keys[pygame.K_UP]:
            player.status = Status(S_JUMP, player)
            player.y_speed = -JUMP_SPEED
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                player.status = Status(S_RUN, player)

    def idle_update(self, player: Player, delay):
        player.x_speed = 0
        player.y_speed = 0
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        is_falling = False
        # Collision with object
        if is_falling:
            player.y_speed = 10
            player.status = Status(S_FALL, player)

    # FALL

    @staticmethod
    def fall_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed
    @staticmethod
    def fall_keyboard(self, player: Player, keys):
        if keys[pygame.K_DOWN]:
            self.add_gravity = 100

    def fall_update(self, player: Player, delay):
        self.player.y_speed += (GRAVITY + self.add_gravity) * delay
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        # Collision check

    # DEATH

    @staticmethod
    def death_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    # RUN

    @staticmethod
    def run_props():
        index, count, elapsed = 0, 4, 0
        return index, count, elapsed

    @staticmethod
    def run_keyboard(self, player: Player, keys):
        if keys[pygame.K_UP]:
            player.status = Status(S_JUMP, player)
            player.y_speed = -JUMP_SPEED
        if not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.status = Status(S_IDLE, player)

    def run_update(self, player: Player, delay):
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        # collision check

    # JUMP

    @staticmethod
    def jump_props():
        index, count, elapsed = 0, 5, 0
        return index, count, elapsed

    @staticmethod
    def jump_keyboard(self, player: Player, keys):
        if keys[pygame.K_DOWN]:
            player.status = Status(S_FALL, player)

    def jump_update(self, player: Player, delay):
        # Collision check
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        player.y_speed = -JUMP_SPEED
