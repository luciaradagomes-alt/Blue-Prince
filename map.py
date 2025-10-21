import pygame
import json
import os
import random
from tile import Tile

class Map:
    def __init__(self):
        self.tiles = []
        self.tile_size = 96

        # dossiers
        self.asset_folders = {
            "start": "assets/start_rooms",
            "end": "assets/end_rooms",
            "blue": "assets/blue_rooms",
            "red": "assets/red_rooms",
            "orange": "assets/orange_rooms",
            "purple": "assets/purple_rooms",
            "yellow": "assets/yellow_rooms"
        }

        # chargement des images pour chaque catégorie
        self.room_images = {key: self._load_room_images(folder) 
                            for key, folder in self.asset_folders.items()}

        self.map_grid = []

    def _clean_name(self, name):
        """Nettoie le nom d'une salle pour correspondre aux fichiers."""
        return name.strip().replace(" ", "_").lower()

    def _load_room_images(self, folder):
        """Charge les images .jpg depuis un dossier donné"""
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
        #ouvre le template de la carte principale depuis le JSON
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.map_grid = data["map"][0]

    def generate_map(self):
        #creation de la carte à partir du layout
        colors = ["blue", "red", "orange", "purple", "yellow"]
        weights = {"blue": 2, "red": 1, "orange": 1, "purple": 1, "yellow": 1}

        for y, row in enumerate(self.map_grid):
            for x, cell in enumerate(row):
                cell_name = self._clean_name(cell)

                # depart
                if cell_name in self.room_images["start"]:
                    image = self.room_images["start"][cell_name]

                # arrivée
                elif cell_name in self.room_images["end"]:
                    image = self.room_images["end"][cell_name]

                # pour les salles random
                elif cell_name == "0":
                    # choix de la couleur selon pondération
                    chosen_color = random.choices(colors, weights=[weights[c] for c in colors])[0]
                    available_rooms = list(self.room_images[chosen_color].keys())
                    if not available_rooms:
                        # fallback sur une couleur avec images
                        for c in colors:
                            if self.room_images[c]:
                                available_rooms = list(self.room_images[c].keys())
                                break
                    cell_name = random.choice(available_rooms)
                    image = self.room_images[chosen_color][cell_name]

                # pour la sécurité
                else:
                    found = False
                    for c in colors:
                        if cell_name in self.room_images[c]:
                            image = self.room_images[c][cell_name]
                            found = True
                            break
                    if not found:
                        # fallback
                        fallback_color = "blue" if self.room_images["blue"] else next(iter(self.room_images))
                        available_rooms = list(self.room_images[fallback_color].keys())
                        cell_name = random.choice(available_rooms)
                        image = self.room_images[fallback_color][cell_name]

                tile = Tile(x * self.tile_size, y * self.tile_size, image, cell_name)
                self.tiles.append(tile)

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
