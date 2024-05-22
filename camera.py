import pygame


class Camera:
    def __init__(self, screen_size, canvas_size, block_size):
        self.width, self.height = screen_size
        self.c_width, self.c_height = canvas_size
        self.block_size = block_size
        self.pos = {'x': self.c_width, 'y': self.c_height}
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = None
        self.update_rect()
        self.get_camera_block()

    def update_rect(self):
        temp_x = self.pos['x'] - self.width/2
        temp_y = self.pos['y'] - self.height/2

        # Ograniczenie x
        if temp_x < 0:
            x = 0
        elif temp_x > (self.c_width - self.width):
            x = max(self.c_width - self.width, 0)
        else:
            x = temp_x

        # Ograniczenie y
        if temp_y < 0:
            y = 0
        elif temp_y > (self.c_height - self.height):
            y = max(self.c_height - self.height, 0)
        else:
            y = temp_y

        w = min(self.c_width, self.width)
        h = min(self.c_height, self.height)

        self.rect = pygame.Rect(x, y, w, h)

    def get_camera_block(self):
        x = int(self.rect.x / self.block_size)
        y = int(self.rect.y / self.block_size)
        return x, y
