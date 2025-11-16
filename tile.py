import pygame

class Tile:
    """Représente une tuile de la carte (visuel d'une salle)
    
    Attributes
    - x : int
        La coordonnée x (horizontale) du sommet en haut à gauche de la tuile
    - y : int
        La coordonnée y (verticale) du sommet en haut à gauche de la tuile
    - image : Surface
        L'image pour la représenter dans l'interface graphique
    - name : str
        Le nom de la pièce
    - rect : Rectangle
        Représente la région qu'occupe la tuile sur l'interface graphique
    """
    
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

