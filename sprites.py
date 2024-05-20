import pygame


class Sprite:
    def __init__(self):
        self.sprites = {}
        self.path = 'assets/'

    def get_sprite(self, name, flipped=False):
        if (name, flipped) not in self.sprites.keys():
            path = self.path + name + ".png"
            try:
                image = pygame.image.load(path)
                image = image if not flipped else pygame.transform.flip(image, True, False)
                self.sprites[(name, flipped)] = image
            except FileNotFoundError:
                raise
        return self.sprites[(name, flipped)]


sprite = Sprite()
