import pygame

class Tile:
    """Représente une tuile de la carte (visuel d'une salle)"""
    
    def __init__(self, x, y, image, name):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Dessine la tuile sur la surface avec offset de caméra"""
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - camera_offset[1]
        surface.blit(self.image, (draw_x, draw_y))
    
    def __str__(self):
        return f"Tile({self.name} at {self.x}, {self.y})"

