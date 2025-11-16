import random

class Door:
    """Classe abstraite qui définit la porte entre deux pièces.

    Attributes
    - room_a : Room
        Pièce A se trouvant liée à la porte
    - room_b : Room
        Pièce B se trouvant liée à la porte
    - lock_level : int
        Indique le niveau de verrouillage de la porte
    - locked : bool
        Indique si la porte est verrouillée ou pas
    - discovered : bool
        Indique si la porte a été découverte ou pas 
    """
    def __init__(self, room_a, room_b, lock_level=None):
        self.room_a = room_a
        self.room_b = room_b
        
        # Niveau de verrouillage (0 = ouvert, 1-3 = nombre de clés nécessaires)
        if lock_level is None:
            self.lock_level = self.generate_lock_level()
        else:
            self.lock_level = lock_level
        
        self.locked = (self.lock_level > 0)
        self.discovered = False  # Le joueur a-t-il vu cette porte ?
    
    def generate_lock_level(self):
        """Génère aléatoirement le niveau de verrouillage
        
        Returns:
        - int
            Renvoie le niveau de verrouillage
        """
        # Probabilités : 49% ouvert, 35% niveau 1, 15% niveau 2, 1% niveau 3
        rand = random.random()
        if rand < 0.49:
            return 0
        elif rand < 0.84:
            return 1
        elif rand < 0.99:
            return 2
        else:
            return 3
    
    def unlock(self):
        """Déverrouille la porte"""
        self.locked = False
    
    def get_other_room(self, current_room):
        """Retourne l'autre salle connectée par cette porte
        
        Parameters:
        - current_room: Room
            Pièce ou le joueur se retrouve

        Returns:
        - room_b: Room
            Renvoie la pièce B si le joueur se trouve dans la pièce A
        - room_a: Room
            Renvoie la pièce A si le joueur se trouve dans la pièce B
        - None
            Ne renvoie rien si le joueur se trouve ailleurs

        """

        if current_room == self.room_a:
            return self.room_b
        elif current_room == self.room_b:
            return self.room_a
        return None
    
    def __str__(self):
        status = "ouverte" if not self.locked else f"verrouillée (niveau {self.lock_level})"
        return f"Porte {status} entre {self.room_a.room.name} et {self.room_b.room.name}"


class RoomNode:
    """Représente une salle dans le graphe du manoir avec ses connexions
    
    Attributes
    - room : Room
        Indique la pièce où se trouve le joueur
    - position : Room
        Indique la position du joueur
    - doors : dict
        Indique les portes de la pièce et leurs positions
    """
    
    def __init__(self, room, position):
        self.room = room  
        self.position = position  
        self.doors = {} 
    
    def add_door(self, direction, door):
        """Ajoute une porte dans une direction
        
        Parameters:
        - direction
            Indique la direction où la porte va être ajoutée
        - door: Door
            Indique la porte qui sera ajoutée
        """

        self.doors[direction] = door
    
    def get_door(self, direction):
        """Récupère la porte dans une direction

        Parameters:
        - direction
            Indique la direction où de la porte cible

        Returns:
        - tuple
            Renvoie la direction de la porte
        """
        return self.doors.get(direction)
    
    def get_door_to(self, target_room_node):
        """Trouve la porte menant à une salle spécifique
        
        Parameters:
        - target_room_node: RoomNode
            Indique la porte menant à une salle spécifique

        Returns:
        - door: Door
            Renvoie la porte cible
        """

        for door in self.doors.values():
            if door.get_other_room(self) == target_room_node:
                return door
        return None
    
    def get_adjacent_rooms(self):
        """Retourne toutes les salles adjacentes accessibles
        
        Returns:
        - list
            Renvoie la liste de pièces adjacentes

        """
        adjacent = []
        for direction, door in self.doors.items():
            other_room = door.get_other_room(self)
            if other_room:
                adjacent.append((direction, other_room, door))
        return adjacent
    
    def __str__(self):
        return f"RoomNode({self.room.name} at {self.position})"