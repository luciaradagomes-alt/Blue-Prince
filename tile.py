import pygame

class Tile:
    def __init__(self, x, y, image, name):
        self.x = x
        self.y = y
        self.image = image
        self.name = name

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
