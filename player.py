import pygame
from constants import *
import sprites


class Player:
    def __init__(self, x, y, width, height, block_size, blocks):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.sprite = S_IDLE
        self.x_speed, self.y_speed = 0, 0
        self.delay = 0
        self.block_size = block_size
        self.blocks = blocks
        self.right_pressed = False
        self.left_pressed = False

        self.status = Status(S_IDLE, self)

    def keyboard(self, keys):
        self.status.keyboard(self=self.status, player=self, keys=keys)
        self.right_pressed = bool(keys[pygame.K_RIGHT])
        self.left_pressed = bool(keys[pygame.K_LEFT])
        if self.left_pressed:
            self.x_speed = -MOVE_SPEED
        if self.right_pressed:
            self.x_speed = MOVE_SPEED
        if not self.left_pressed and not self.right_pressed:
            self.x_speed = 0

    def update(self, delay):
        self.delay = delay
        self.x += self.x_speed * delay
        self.y += self.y_speed * delay
        self.status.update(self, self.delay)
        moves = []
        if self.x_speed > 0:
            moves.append('right')
        elif self.x_speed < 0:
            moves.append('left')
        elif self.y_speed < 0:
            moves.append('up')
        elif self.y_speed > 0:
            moves.append('down')
        self.get_possible_collision_blocks()



    def draw(self, screen):
        new_index = self.status.index % self.status.count
        sprite_name = self.sprite + str(new_index)
        sprite = sprites.sprite.get_sprite(sprite_name)
        screen.blit(sprite, (self.x, self.y))

    def get_player_cols(self):
        x = int(self.x / self.block_size)
        w = int(self.width / self.block_size) + 1
        col_min = x - 1
        col_max = x + w + 1
        return col_min, col_max

    def get_possible_collision_blocks(self):
        col_min, col_max = self.get_player_cols()
        blocks = []
        for key in self.blocks.keys():
            if col_min <= key <= col_max:
                for block in self.blocks[key]:
                    blocks.append(block)
        return blocks

    def update_blocks(self, blocks):
        self.blocks = blocks

    def get_player_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Status:
    def __init__(self, status_name: str, player: Player):
        self.name = status_name
        self.player = player
        self.block_size = player.block_size
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
        self.block_under_player = [0, -1]
        self.block_right_player = [-1, 0]
        self.block_up_player = [0, 1]
        self.block_left_player = [1, 0]

    def check_collision(self, side_b):

        blocks = self.player.get_possible_collision_blocks()
        bs = self.block_size
        for block in blocks:
            block_rect = pygame.Rect(block[-2]*bs + side_b[0],
                                     block[-1] * bs + side_b[1],
                                     bs,
                                     bs)
            p_rect = self.player.get_player_rect()
            if p_rect.colliderect(block_rect):
                return True, block
                break
        return False, None

    def common_update_left(self):
        if self.player.left_pressed:
            collision, block = self.check_collision(self.block_left_player)
            if collision:
                self.player.x_speed = 0
                self.player.x = block[-2] * self.block_size + self.block_size
                return block

    def common_update_right(self):
        if self.player.right_pressed:
            collision, block = self.check_collision(self.block_right_player)
            if collision:
                self.player.x_speed = 0
                self.player.x = block[-2] * self.block_size - self.player.width
                return block

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
        self.common_update_left()
        self.common_update_right()
        player.x_speed = 0
        player.y_speed = 0
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0

        collision, block = self.check_collision(self.block_under_player)

        if not collision:
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
        self.common_update_left()
        self.common_update_right()
        self.player.y_speed += (GRAVITY + self.add_gravity) * delay
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0

        collision, block = self.check_collision(self.block_under_player)

        if collision:
            player.y_speed = 0
            player.status = Status(S_IDLE, player)
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
        self.common_update_left()
        self.common_update_right()
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
        self.common_update_left()
        self.common_update_right()
        self.elapsed += delay
        if self.elapsed > 0.05:
            self.index += 1
            self.elapsed = 0
        player.y_speed = -JUMP_SPEED
        collision, block = self.check_collision(self.block_up_player)
        if collision:
            player.y_speed = 0
            player.status = Status(S_FALL, player)
