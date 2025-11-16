import pygame
from inventory import Inventory

class Player:
    """Classe qui gère le joueur, sa position et ses déplacements dans le manoir.

    Attributes
    - tile_x : int
        Position en x (en tuiles)
    - tile_y : int
        Position en y (en tuiles)
    - tile_size : int
        Taille de la tuile
    - inventory : Inventory
        Inventaire du joueur
    - pixel_x : int
        Position en x (en pixels)
    - pixel_y : int
        Position en y (en pixels)
    - target_x : int
        Position cible en x
    - target_y : int
        Position cible en y
    - is_moving : bool
        Indique si le joueur est en mouvement ou pas
    - move_speed : int
        Vitesse du mouvement du joueur (pixels par secondes)
    """

    def __init__(self, start_x, start_y, tile_size=128):
        self.tile_x = start_x 
        self.tile_y = start_y
        self.tile_size = tile_size
        self.inventory = Inventory()
        
        # Animation de déplacement
        self.pixel_x = start_x * tile_size
        self.pixel_y = start_y * tile_size
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.is_moving = False
        self.move_speed = 400  
        
        self.current_room = None
        
    def get_pixel_position(self):
        """Retourne la position en pixels pour l'affichage
        
        Returns:
        - tuple
            Retourne la position en pixels pour l'affichage
        """
        return (self.pixel_x, self.pixel_y)
    
    def get_tile_position(self):
        """Retourne la position en tuiles

        Returns:
        - tuple
            Retourne la position en tuiles pour l'affichage
        """
        return (self.tile_x, self.tile_y)
    
    def can_move_to(self, dx, dy, game_map):
        """Vérifie si le joueur peut se déplacer vers la case adjacente
        
        Parameters:
        - dx : int
            Déplacement en x du joueur
        - dy : int
            Déplacement en y du joueur
        - game_map : Map
            Carte du jeu

        Returns:
        - bool
            True si le joueur peut se déplacer vers la case adjacente, False sinon
        - str
            Message personnalisé
        """
        new_x = self.tile_x + dx
        new_y = self.tile_y + dy
        
        # Vérifier les limites de la carte
        if new_x < 0 or new_y < 0:
            return False, "Hors limites"
        if new_y >= len(game_map.map_grid) or new_x >= len(game_map.map_grid[0]):
            return False, "Hors limites"
        
        # Vérifier qu'il y a une salle (pas "0" ou vide)
        target_cell = game_map.map_grid[new_y][new_x]
        if target_cell == "0" or target_cell == "":
            return False, "Pas de salle ici"
        
        # Vérifier la porte (si elle existe)
        current_room = game_map.get_room_at(self.tile_x, self.tile_y)
        target_room = game_map.get_room_at(new_x, new_y)
        
        if current_room and target_room:
            door = current_room.get_door_to(target_room)
            if door:
                # Vérifier si la porte est verrouillée
                if door.locked:
                    if self.inventory.keys >= door.lock_level:
                        return True, f"Porte verrouillée (niveau {door.lock_level})"
                    else:
                        return False, f"Clés insuffisantes ({door.lock_level} requises)"
                return True, "Porte ouverte"
            else:
                return False, "Pas de porte ici"
        
        return True, "OK"
    
    def move(self, dx, dy, game_map):
        """Déplace le joueur d'une tuile (avec animation)
        
        Parameters:
        - dx : int
            Déplacement en x du joueur
        - dy : int
            Déplacement en y du joueur
        - game_map : Map
            Carte du jeu

        Returns:
        - bool
            False si le joueur est déjà en mouvement, True sinon
        """
        if self.is_moving:
            return False  # Déjà en mouvement
        
        can_move, message = self.can_move_to(dx, dy, game_map)
        
        if not can_move:
            return False
        
        # Si porte verrouillée, demander confirmation et dépenser clés
        if "verrouillée" in message:
            door = game_map.get_room_at(self.tile_x, self.tile_y).get_door_to(
                game_map.get_room_at(self.tile_x + dx, self.tile_y + dy)
            )
            # Ici vous pouvez ajouter une interface pour confirmer
            # Pour l'instant, on ouvre automatiquement si assez de clés
            if self.inventory.keys >= door.lock_level:
                # Option: utiliser kit de crochetage pour niveau 1
                if door.lock_level == 1 and self.inventory.lockpick_kit:
                    print(f"Porte ouverte avec le kit de crochetage !")
                else:
                    self.inventory.keys -= door.lock_level
                    print(f"Porte ouverte ! {self.inventory.keys} clés restantes")
                door.unlock()
        
        # Démarrer le mouvement
        self.tile_x += dx
        self.tile_y += dy
        self.target_x = self.tile_x * self.tile_size
        self.target_y = self.tile_y * self.tile_size
        self.is_moving = True
        
        # Décrémenter les pas
        self.inventory.move()
        
        return True
    
    def update(self, dt):
        """Met à jour l'animation de déplacement
        
        Parameters:
        - dt : int
            Temps 
        """
        if not self.is_moving:
            return
        
        # Interpolation vers la position cible
        move_distance = self.move_speed * dt
        
        # Déplacement X
        if abs(self.target_x - self.pixel_x) > move_distance:
            if self.target_x > self.pixel_x:
                self.pixel_x += move_distance
            else:
                self.pixel_x -= move_distance
        else:
            self.pixel_x = self.target_x
        
        # Déplacement Y
        if abs(self.target_y - self.pixel_y) > move_distance:
            if self.target_y > self.pixel_y:
                self.pixel_y += move_distance
            else:
                self.pixel_y -= move_distance
        else:
            self.pixel_y = self.target_y
        
        # Vérifier si arrivé
        if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
            self.is_moving = False
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Dessine le joueur
        
        Parameters:
        - surface: Surface
            Surface prise par le joueur
        - camera_offset: tuple
            Camera offset centré en (0, 0)
        """
        draw_x = self.pixel_x - camera_offset[0] + self.tile_size // 2
        draw_y = self.pixel_y - camera_offset[1] + self.tile_size // 2
        
        # Cercle bleu pour le joueur
        player_radius = self.tile_size // 3
        pygame.draw.circle(surface, (71, 182, 240), (int(draw_x), int(draw_y)), player_radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(draw_x), int(draw_y)), player_radius, 3)
