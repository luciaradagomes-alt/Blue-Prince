import pygame
import os
from chambres import *

pygame.display.init()

asset_folders = {
            "start": "assets/start_rooms",
            "end": "assets/end_rooms",
            "blue": "assets/blue_rooms",
            "red": "assets/red_rooms",
            "orange": "assets/orange_rooms",
            "purple": "assets/purple_rooms",
            "yellow": "assets/yellow_rooms",
            "green": "assets/green_rooms",
            "vide": "assets/vide"
        }

def _clean_name(name):
    """Nettoie le nom d'une salle pour correspondre aux fichiers."""
    return name.strip().replace(" ", "_").lower()

def _load_room_images(folder):
        """Charge les images .jpg depuis un dossier donné"""
        images = {}
        if not os.path.exists(folder):
            print(f"Dossier introuvable : {folder}")
            return images
        for filename in os.listdir(folder):
            if filename.lower().endswith(".jpg"):
                room_name = _clean_name(os.path.splitext(filename)[0])
                path = os.path.join(folder, filename)
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (128, 128))
                    images[room_name] = image
                except Exception as e:
                    print(f"Erreur chargement {filename}: {e}")
        print(f"{len(images)} images chargées depuis {folder}")
        
        return images

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

    room_images = {key: _load_room_images(folder) 
                    for key, folder in asset_folders.items()}

    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,name):
        self.__name = name
        if name == "0":
            self.color = "vide"
            name = "tuile_vide"
        elif name == "Entrance Hall":
            self.color = "start"
        elif name == "Antechamber":
            self.color = "end"
        elif name in Blue.rooms:
            self.color = "blue"
        elif name in Green.rooms:
            self.color = "green"
        elif name in Purple.rooms:
            self.color = "purple"
        elif name in Red.rooms:
            self.color = "red"
        elif name in Yellow.rooms:
            self.color = "yellow"
        elif name in Orange.rooms:
            self.color = "orange"
        self.image = self.room_images[self.color][_clean_name(name)]  

    def _clean_name(self, name):
        """Nettoie le nom d'une salle pour correspondre aux fichiers."""
        return name.strip().replace(" ", "_").lower()

    def draw(self, surface, camera_offset=(0, 0)):
        """Dessine la tuile sur la surface avec offset de caméra"""
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - camera_offset[1]
        surface.blit(self.image, (draw_x, draw_y))
    
    def __str__(self):
        return f"Tile({self.name} at {self.x}, {self.y})"

