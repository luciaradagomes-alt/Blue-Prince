import pygame

class Tile:
    """Classe qui représente une tuile de la carte (visuel d'une salle).
    
    Attributes:
    - x : int
    - y : int
    - image : image
        Image de la tuile
    - name : str
        Nom de la tuile
    - rect : Rect
        Rectangle représentant la tuile
    """
    
    def __init__(self, x, y, image, name):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Dessine la tuile sur la surface avec offset de caméra.
        
        Parameters:
        - surface: Surface
            Surface choisie pour dessiner la tuile
        - camera_offset : tuple(int, int)
            Offset de la caméra
        """
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - camera_offset[1]
        surface.blit(self.image, (draw_x, draw_y))
    
    def __str__(self):
        return f"Tile({self.name} at {self.x}, {self.y})"

