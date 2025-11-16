import random
import pygame
from colorpalette import couleurs
import text

class RoomDraw:
    """Classe qui gère le système de tirage et de choix des pièces
    
    Attributes:
    - available_rooms : list
        Pool de salles disponibles
    - current_draw : list
        Les 3 salles actuellement tirées
    - room_weights : dict
        Poids des classes de pièces
    - weight_modifiers : dict
        Modifie les poids des classes de pièces 
    """
    
    def __init__(self):
        self.available_rooms = []
        self.current_draw = []  
        self.room_weights = {
            "blue": 2,
            "red": 1,
            "orange": 1,
            "purple": 1,
            "yellow": 1,
            "green": 1
        }
        # Modificateurs temporaires (ex: Greenhouse augmente les verts)
        self.weight_modifiers = {}
    
    def set_available_rooms(self, rooms_by_color):
        """Initialise le pool de salles disponibles
        
        Parameters:
        - rooms_by_color: dict {"blue": [Room1, Room2], "red": [...], ...}
        """
        self.available_rooms = []
        for color, rooms in rooms_by_color.items():
            for room in rooms:
                self.available_rooms.append({
                    "room": room,
                    "color": color,
                    "weight": self.room_weights.get(color, 1)
                })
    
    def add_temporary_rooms(self, rooms, color="special"):
        """Ajoute des salles temporaires au pool (ex: Chamber of Mirrors)
        
        Parameters:
        - rooms : list
            Liste de pièces
        - color : str
            Couleur de la pièce
        """
        for room in rooms:
            self.available_rooms.append({
                "room": room,
                "color": color,
                "weight": 1,
                "temporary": True
            })
    
    def modify_weights(self, color, modifier):
        """Modifie temporairement le poids d'une couleur (ex: Greenhouse)
        
        Parameters:
        - color: str
            couleur à modifier
        - modifier: int
            multiplicateur (ex: 2 pour doubler)
        """
        self.weight_modifiers[color] = modifier
    
    def reset_weight_modifiers(self):
        """Réinitialise les modificateurs de poids"""
        self.weight_modifiers = {}
    
    def draw_rooms(self, num_rooms=3):
        """Tire aléatoirement des salles selon les poids
        
        Parameters:
        - num_rooms : int
            Nombre de pièces tirées

        Returns:
        - drawn : list 
            Liste de 3 dictionnaires {"room": Room, "color": str}
        """
        if len(self.available_rooms) < num_rooms:
            print("Pas assez de salles disponibles!")
            return []
        
        # Calculer les poids effectifs
        weighted_rooms = []
        for room_data in self.available_rooms:
            color = room_data["color"]
            base_weight = room_data["weight"]
            modifier = self.weight_modifiers.get(color, 1)
            effective_weight = base_weight * modifier
            weighted_rooms.append((room_data, effective_weight))
        
        # Tirage sans remise
        drawn = []
        temp_pool = weighted_rooms.copy()
        
        for _ in range(num_rooms):
            if not temp_pool:
                break
            
            # Extraire les salles et poids
            rooms = [r[0] for r in temp_pool]
            weights = [r[1] for r in temp_pool]
            
            # Tirer une salle
            chosen = random.choices(rooms, weights=weights, k=1)[0]
            drawn.append(chosen)
            
            # Retirer du pool temporaire
            temp_pool = [(r, w) for r, w in temp_pool if r != chosen]
        
        self.current_draw = drawn
        
        # Retirer les salles temporaires après le tirage
        self.available_rooms = [r for r in self.available_rooms 
                               if not r.get("temporary", False)]
        
        return drawn
    
    def redraw(self, inventory):
        """Retire à nouveau les salles (coûte 1 dé)
        
        Parameters:
        - inventory: Inventory
            Inventaire du joueur

        Returns:
        - bool: 
            True si succès, False si pas assez de dés
        """

        if inventory.dice < 1:
            return False
        
        inventory.dice -= 1
        self.draw_rooms()
        return True
    
    def choose_room(self, choice_index, inventory, gem_cost=0):
        """Le joueur choisit une salle parmi les 3 tirées
        
        Parameters:
        - choice_index: int
            Indice des choix 0, 1 ou 2
        - inventory: Inventory
            Inventaire du joueur
        - gem_cost: int
            Coût en gemmes pour choisir cette salle spécifique
        
        Returns:
        - chosen_room : Room
            Renvoie la pièce choisie
        - None 
            si choix invalide
        """
        if choice_index < 0 or choice_index >= len(self.current_draw):
            return None
        
        # Vérifier le coût en gemmes
        if gem_cost > 0:
            if inventory.gems < gem_cost:
                print(f"Pas assez de gemmes! ({gem_cost} requises)")
                return None
            inventory.gems -= gem_cost
        
        chosen_data = self.current_draw[choice_index]
        chosen_room = chosen_data["room"]
        
        # Retirer la salle choisie du pool (on ne peut pas la retirer à nouveau)
        self.available_rooms = [r for r in self.available_rooms 
                               if r["room"] != chosen_room]
        
        self.current_draw = []
        return chosen_room
    
    def display_draw(self, surface, inventory):
        """Affiche l'interface de tirage des salles

        Parameters:
        - surface: Surface
            Surface de l'interface
        - inventory : Inventory
            Inventaire du joueur

        Returns:
        - choice :int
            Indice de la salle choisie
        - None
            Si pas de choix effectué
        """
        # Fond semi-transparent
        overlay = pygame.Surface(surface.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        surface.blit(overlay, (0, 0))
        
        centerx = surface.get_width() // 2
        centery = surface.get_height() // 2
        
        # Titre
        text.ligne_texte_centre("Choisissez une pièce", surface, 
                               offsety=-250, font=text.room_font, color="white")
        
        # Afficher les 3 salles
        card_width = 200
        card_height = 280
        card_spacing = 50
        start_x = centerx - (card_width * 3 + card_spacing * 2) // 2
        
        color_map = {
            "blue": couleurs["blue1"],
            "red": (200, 50, 50),
            "orange": (255, 150, 50),
            "purple": (150, 80, 180),
            "yellow": (220, 200, 50),
            "green": couleurs["green"]
        }
        
        for i, room_data in enumerate(self.current_draw):
            room = room_data["room"]
            color = room_data["color"]
            
            x = start_x + i * (card_width + card_spacing)
            y = centery - card_height // 2
            
            # Carte
            card_color = color_map.get(color, couleurs["grey"])
            pygame.draw.rect(surface, card_color, 
                           pygame.Rect(x, y, card_width, card_height))
            pygame.draw.rect(surface, couleurs["lightblue"], 
                           pygame.Rect(x, y, card_width, card_height), 5)
            
            # Numéro
            num_text = text.font2.render(f"{i+1}", True, "white")
            surface.blit(num_text, (x + 10, y + 10))
            
            # Nom de la salle (multiligne si nécessaire)
            room_name = room.name
            words = room_name.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) > 15:  # Limite de caractères par ligne
                    if current_line:
                        lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
            
            # Afficher le nom
            for j, line in enumerate(lines):
                line_text = text.inventory_font.render(line, True, "white")
                line_rect = line_text.get_rect(center=(x + card_width//2, 
                                                       y + 40 + j * 25))
                surface.blit(line_text, line_rect)
            
            # Couleur de la salle
            color_text = text.inventory_font.render(f"({color})", True, "white")
            color_rect = color_text.get_rect(center=(x + card_width//2, y + 120))
            surface.blit(color_text, color_rect)
        
        # Instructions
        text.ligne_texte_centre(f"Gemmes: {inventory.gems} | Dés: {inventory.dice}", 
                               surface, offsety=180, font=text.inventory_font, color="white")
        text.ligne_texte_centre("Appuyez sur 1, 2 ou 3 pour choisir", 
                               surface, offsety=210, font=text.inventory_font, color="white")
        text.ligne_texte_centre("Appuyez sur R pour retirer (1 dé) | ESC pour annuler", 
                               surface, offsety=240, font=text.inventory_font, color="white")
        
        pygame.display.flip()
        
        # Attendre le choix du joueur
        waiting = True
        choice = None
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        choice = 0
                        waiting = False
                    elif event.key == pygame.K_2:
                        choice = 1
                        waiting = False
                    elif event.key == pygame.K_3:
                        choice = 2
                        waiting = False
                    elif event.key == pygame.K_r:
                        if self.redraw(inventory):
                            return self.display_draw(surface, inventory)
                        else:
                            print("Pas assez de dés!")
                    elif event.key == pygame.K_ESCAPE:
                        return None
        
        return choice