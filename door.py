import random

class Door:
    """Représente une porte entre deux salles"""
    
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
        """Génère aléatoirement le niveau de verrouillage"""
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
        """Retourne l'autre salle connectée par cette porte"""
        if current_room == self.room_a:
            return self.room_b
        elif current_room == self.room_b:
            return self.room_a
        return None
    
    def __str__(self):
        status = "ouverte" if not self.locked else f"verrouillée (niveau {self.lock_level})"
        return f"Porte {status} entre {self.room_a.room.name} et {self.room_b.room.name}"


class RoomNode:
    """Représente une salle dans le graphe du manoir avec ses connexions"""
    
    def __init__(self, room, position):
        self.room = room  # Objet Room (Yellow, Green, etc.)
        self.position = position  # (x, y) en tuiles
        self.doors = {}  # {direction: Door} où direction = 'north', 'south', 'east', 'west'
    
    def add_door(self, direction, door):
        """Ajoute une porte dans une direction"""
        self.doors[direction] = door
    
    def get_door(self, direction):
        """Récupère la porte dans une direction"""
        return self.doors.get(direction)
    
    def get_door_to(self, target_room_node):
        """Trouve la porte menant à une salle spécifique"""
        for door in self.doors.values():
            if door.get_other_room(self) == target_room_node:
                return door
        return None
    
    def get_adjacent_rooms(self):
        """Retourne toutes les salles adjacentes accessibles"""
        adjacent = []
        for direction, door in self.doors.items():
            other_room = door.get_other_room(self)
            if other_room:
                adjacent.append((direction, other_room, door))
        return adjacent
    
    def __str__(self):
        return f"RoomNode({self.room.name} at {self.position})"