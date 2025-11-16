import pygame
import json
import os
import random
from tile import Tile
from door import Door, RoomNode
from Chambres import Room, Yellow, Green, Red, Blue, Orange, Purple

class Map:
    """Classe qui définit la carte de jeu.

    Attributes:
    - tiles : list[Tile]
        Liste des tuiles du jeu
    - tile_size : int
        Taille de chaque tuile
    - room_nodes : dict[RoomNode]
        Graphe de salles avec leurs connexions
    - asset_folders : dict[str, str]
        Dossier avec less pièces   
    - room_images : dict
        Images des pièces disponibles dans le jeu
    - map_grid : list[str]
        Grille de la carte 
    """
    
    def __init__(self):
        self.tiles = []
        self.tile_size = 128    
        
        # Graphe des salles avec leurs connexions
        self.room_nodes = {}  # {(x, y): RoomNode}

        # dossiers
        self.asset_folders = {
            "start": "assets/start_rooms",
            "end": "assets/end_rooms",
            "blue": "assets/blue_rooms",
            "red": "assets/red_rooms",
            "orange": "assets/orange_rooms",
            "purple": "assets/purple_rooms",
            "yellow": "assets/yellow_rooms",
            "green": "assets/green_rooms"
        }

        # chargement des images pour chaque catégorie
        self.room_images = {key: self._load_room_images(folder) 
                            for key, folder in self.asset_folders.items()}

        self.map_grid = []

    def _clean_name(self, name):
        """Nettoie le nom d'une salle pour correspondre aux fichiers.
        
        Parameters:
        - name : str
            Nom de la pièce

        Returns:
        - name : str
            Renvoie une version nettoyée du nom de la pièce
        """

        return name.strip().replace(" ", "_").lower()

    def _load_room_images(self, folder):
        """Charge les images .jpg depuis un dossier donné.
        
        Parameters:
        - folder 
            Fichier où se trouvent les images

        Returns:
        - images : dict
            Renvoie l'image de la pièce
        """

        images = {}
        if not os.path.exists(folder):
            print(f"Dossier introuvable : {folder}")
            return images
        for filename in os.listdir(folder):
            if filename.lower().endswith(".jpg"):
                room_name = self._clean_name(os.path.splitext(filename)[0])
                path = os.path.join(folder, filename)
                try:
                    image = pygame.image.load(path).convert()
                    image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
                    images[room_name] = image
                except Exception as e:
                    print(f"Erreur chargement {filename}: {e}")
        print(f"{len(images)} images chargées depuis {folder}")
        return images

    def load_from_json(self, path="map_layout.json"):
        """Ouvre le template de la carte principale depuis le JSON.
        
        Parameters:
        - path : str
            Chemin du fichier "map_layout.json"
        """

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.map_grid = data["map"][0]

    def create_room_object(self, room_name, color):
        """Crée un objet Room approprié selon le type.
        
        Parameters:
        - room_name : str
            Nom de la pièce
        - color : str
            Couleur de la pièce

        Returns:
        - Room
            Renvoie la pièce approppriée
        """
        
        if color == "yellow":
            if room_name in Yellow.rooms:
                return Yellow(room_name)
        elif color == "green":
            if room_name in Green.rooms:
                return Green(room_name)
        elif color == "red":
            if room_name in Red.rooms:
                return Red(room_name)
        elif color == "orange":
            if room_name in Orange.rooms:
                return Orange(room_name)
        elif color == "purple":
            if room_name in Purple.rooms:
                return Purple(room_name) 
        elif color == "blue":
            if room_name in Blue.rooms:
                return Blue(room_name)   
        
        return Room(room_name, color)

    def generate_map(self):
        """Création de la carte à partir du layout avec génération des portes."""
        
        colors = ["blue", "red", "orange", "purple", "yellow", "green"]
        weights = {"blue": 2, "red": 1, "orange": 1, "purple": 1, "yellow": 1, "green": 1}

        # Phase 1: Créer toutes les tuiles et RoomNodes
        for y, row in enumerate(self.map_grid):
            for x, cell in enumerate(row):
                cell_name = self._clean_name(cell)

                # Départ
                if cell_name in self.room_images["start"]:
                    image = self.room_images["start"][cell_name]
                    room_color = "start"

                # Arrivée
                elif cell_name in self.room_images["end"]:
                    image = self.room_images["end"][cell_name]
                    room_color = "end"

                # Pour les salles random
                elif cell_name == "0":
                    # Choix de la couleur selon pondération
                    chosen_color = random.choices(colors, weights=[weights[c] for c in colors])[0]
                    available_rooms = list(self.room_images[chosen_color].keys())
                    if not available_rooms:
                        for c in colors:
                            if self.room_images[c]:
                                available_rooms = list(self.room_images[c].keys())
                                chosen_color = c
                                break
                    cell_name = random.choice(available_rooms)
                    image = self.room_images[chosen_color][cell_name]
                    room_color = chosen_color

                # Pour la sécurité
                else:
                    found = False
                    for c in colors + ["start", "end"]:
                        if cell_name in self.room_images[c]:
                            image = self.room_images[c][cell_name]
                            room_color = c
                            found = True
                            break
                    if not found:
                        fallback_color = "blue" if self.room_images["blue"] else next(iter(self.room_images))
                        available_rooms = list(self.room_images[fallback_color].keys())
                        cell_name = random.choice(available_rooms)
                        image = self.room_images[fallback_color][cell_name]
                        room_color = fallback_color

                # Créer la tuile
                tile = Tile(x * self.tile_size, y * self.tile_size, image, cell_name)
                self.tiles.append(tile)
                
                # Créer le RoomNode
                room_obj = self.create_room_object(cell_name, room_color)
                room_node = RoomNode(room_obj, (x, y))
                self.room_nodes[(x, y)] = room_node

        # Phase 2: Créer les portes entre salles adjacentes
        self.generate_doors()

    def generate_doors(self):
        """Génère les portes entre toutes les salles adjacentes."""

        directions = {
            'north': (0, -1),
            'south': (0, 1),
            'east': (1, 0),
            'west': (-1, 0)
        }
        
        for (x, y), room_node in self.room_nodes.items():
            for direction, (dx, dy) in directions.items():
                neighbor_pos = (x + dx, y + dy)
                
                # Vérifier si le voisin existe
                if neighbor_pos in self.room_nodes:
                    neighbor_node = self.room_nodes[neighbor_pos]
                    
                    # Éviter de créer la porte deux fois
                    opposite = {'north': 'south', 'south': 'north', 
                               'east': 'west', 'west': 'east'}
                    if neighbor_node.get_door(opposite[direction]) is None:
                        # Créer la porte
                        door = Door(room_node, neighbor_node)
                        room_node.add_door(direction, door)
                        neighbor_node.add_door(opposite[direction], door)

    def get_room_at(self, x, y):
        """Retourne le RoomNode à une position donnée.
        
        Parameters:
        - x : int
            Position en x 
        - y : str
            Position en y

        Returns:
        - RoomNode
            Renvoie le RoomNode à une position donnée
        """

        return self.room_nodes.get((x, y))

    def get_start_position(self):
        """Trouve la position de départ (première salle 'start').
        
        Returns:
        - tuple(int, int) 
            Renvoie la position de départ
        """
        for y, row in enumerate(self.map_grid):
            for x, cell in enumerate(row):
                cell_name = self._clean_name(cell)
                if cell_name in self.room_images.get("start", {}):
                    return (x, y)
        return (0, 0) 

    def draw(self, surface, camera_offset=(0, 0)):
        """Dessine la carte avec offset de caméra.
        
        Parameters:
        - surface : Surface
            Surface de la pièce
        - camera_offset : tuple(int, int)
            Offset de la caméra
        """

        for tile in self.tiles:
            tile.draw(surface, camera_offset)
    
    def draw_doors(self, surface, camera_offset=(0, 0)):
        """Dessine les indicateurs de portes (optionnel pour debug).
        
        Parameters:
        - surface : Surface
            Surface de la pièce
        - camera_offset : tuple(int, int)
            Offset de la caméra
        """
        
        for room_node in self.room_nodes.values():
            x, y = room_node.position
            pixel_x = x * self.tile_size - camera_offset[0]
            pixel_y = y * self.tile_size - camera_offset[1]
            
            # Dessiner des petits carrés pour indiquer les portes
            for direction, door in room_node.doors.items():
                if direction == 'north':
                    pos = (pixel_x + self.tile_size // 2, pixel_y + 5)
                elif direction == 'south':
                    pos = (pixel_x + self.tile_size // 2, pixel_y + self.tile_size - 5)
                elif direction == 'east':
                    pos = (pixel_x + self.tile_size - 5, pixel_y + self.tile_size // 2)
                else:  
                    pos = (pixel_x + 5, pixel_y + self.tile_size // 2)
                
                # Couleur selon verrouillage
                if door.locked:
                    color = (200, 50, 50) if door.lock_level > 1 else (200, 150, 50)
                else:
                    color = (50, 200, 50)
                
                pygame.draw.circle(surface, color, pos, 8)
                
                # Afficher le niveau de verrouillage
                if door.locked and door.lock_level > 0:
                    font = pygame.font.Font(None, 20)
                    text = font.render(str(door.lock_level), True, "white")
                    text_rect = text.get_rect(center=pos)
                    surface.blit(text, text_rect)
