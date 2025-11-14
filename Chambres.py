#%%
from inventory import Inventory
from objet import Objet
import pygame
import random

#%%
class RoomGrid:
    """Gère les grille 9x9 des pièces"""

    def __init__(self, room_name, entry_door):
        self.grid_size = 9
        self.tile_size = 64
        self.room_name = room_name
        self.entry_door = entry_door
        self.grid = [["empty" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player_position = self.get_player_init_position()
        self.apply_room_data()
        self.active = True
        
    def get_player_init_position(self) :
        """Récupère la position initiale du joueur, en fonction de la porte ouverte."""
        center = self.grid_size // 2

        if self.entry_door == "north":
            return [center, self.grid_size - 1]
        if self.entry_door == "south":
            return [center, 0] 
        if self.entry_door == "east":
            return [self.grid_size - 1, center] 
        if self.entry_door == "west":
            return [0, center] 
        # fallback par défaut
        return [center, center]

    def grid_init(self):
        """Initialisation de la grille de la pièce."""
        grid = [["empty" for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # dig spots
        for (x, y) in getattr(self.room, "dig_spots_position", []):
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                grid[y][x] = "dig"

        px, py = self.player_position
        grid[py][px] = "player"

        return grid

    def apply_room_data(self):
        """Gère les endroits à creuser, les coffres et les lockers."""
        dig_positions = getattr(self.room_name, "dig_spots_position", [])
        chest_position = getattr(self.room_name, "chest_spots_position", [])
        locker_position = getattr(self.room_name, "locker_spots_position", [])

        # Endroits pour creuser :
        for (x, y) in dig_positions:
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid[y][x] = "dig"

        # Coffres :
        for (x, y) in chest_position:
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid[y][x] = "chest"

        # Lockers :
        for (x, y) in locker_position:
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid[y][x] = "locker"

        # Player position
        px, py = self.player_pos
        self.grid[py][px] = "player"
    
    def move(self, dx, dy):
        """Gère le mouvement du joueur sur la grille."""
        px, py = self.player_pos
        nx, ny = px + dx, py + dy

        # limites de la pièce
        if not (0 <= nx < self.grid_size and 0 <= ny < self.grid_size):
            return

        
        self.grid[py][px] = "empty"
        self.grid[ny][nx] = "player"
        self.player_pos = [nx, ny]

    def draw(self, surface):
        """Dessine la grille, ou implémente la grille"""

    def player_is_on_door(self):
        """Gère la sortie de la pièce du joueur"""
        px, py = self.player_pos
        mid = self.GRID_SIZE // 2
        return (px, py) in [
            (mid, 0), (mid, self.GRID_SIZE-1),
            (0, mid), (self.GRID_SIZE-1, mid)
        ]

class Room :
    """Classe qui définit les pièces du jeu."""
    
    possible = ["Commissary", "Kitchen", "Locksmith", "Laundry Room", "Bookshop", "The Armory", "Showroom", "Mount Holly Gift Shop",
                "Terrace", "Patio", "Courtyard", "Cloister", "Veranda", "Greenhouse", "Morning Room", "Secret Garden",
                "Bedroom", "Boudoir", "Guest Bedroom", "Nursery", "Servant's Quarters", "Bunk Room", "Her Ladyship's Chamber", "Master Bedroom",
                "Hallway", "West Wing Hall", "East Wing Hall", "Corridor", "Passageway", "Secret Passage", "Foyer", "Great Hall",
                "Lavatory", "Chapel", "Maid's Chamber", "Archives", "Gymnasium", "Darkroom", "Weight Room", "Furnace",
                "The Foundation", "Entrance Hall", "Spare Room", "Rotunda", "Parlor", "Billiard Room", "Gallery", "Room 8", "Closet", "Walk-in Closet", "Attic", "Storeroom", "Nook", "Garage", "Music Room", "Locker Room", "Den", "Wine Cellar", "Trophy Room", "Ballroom", "Pantry", "Rumpus Room", "Vault", "Office", "Drawing Room", "Study", "Library", "Chamber of Mirrors", "The Pool", "Drafting Studio", "Utility Closet", "Boiler Room", "Pump Room", "Security", "Workshop", "Laboratory", "Sauna", "Coat Check", "Mail Room", "Freezer", "Dining Room", "Observatory", "Conference Room", "Aquarium", "Antechamber", "Room 46"]
    

    def __init__(self, name : str, color : str):
        self.name = name
        self.color = color
        self.visited = False # False si la pièce n'a pas encore été visité, True sinon
        self.doors = [] # Liste des pièces qui peuvent être accédées à travers la pièce actuelle

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        # MODIFICATION: rendre plus permissif pour les noms nettoyés
        if name not in Room.possible:
            # Essayer de trouver une correspondance approximative
            name_cleaned = name.replace("_", " ").title()
            if name_cleaned in Room.possible:
                self.__name = name_cleaned
                return
            # Si toujours pas trouvé, accepter quand même (pour le développement)
            print(f"Attention: '{name}' n'est pas dans la liste des salles possibles")
            self.__name = name
        else:
            self.__name = name

  
    def enter_room(self):
        """Ajoute des effets lorsque le joueur rentre dans la pièce"""
        print(f"Vous entrez dans {self.name}")
        self.visited = True
        return True
    
    def add_door(self, room):
        """Ajoute une porte vers une nouvelle pièce"""
        self.doors.append(room)
    
    def __str__(self):
        return f"{self.name} (pièce {self.color})"

class Yellow(Room) :
    """Ce sont des magasins dans lesquels il est possible d'échanger de l'or contre d'autres objets."""
    
    rooms = ["Commissary", "Kitchen", "Locksmith", "Laundry Room", "Bookshop", "The Armory", "Showroom", "Mount Holly Gift Shop"]
    
    def __init__(self, name:str):
        super().__init__(name, "jaune")
        self.items_for_sale = self.items()
        self.restock_days = 1
        
        # Services du laundry room
        self.services = {
            "Essorage" : {"cost" : 5, "action" : "exchange_all_gems_with_all_gold"},
            "Lavage et séchage" : {"cost" : 5, "action" : "exchange_all_keys_with_all_gems"},
            "Fluff and fold" : {"cost" : 5, "action" : "exchange_all_keys_with_all_gold"}
        }
            
    def items(self):
        """Renvoie la liste d'objets pour chacun des magasins"""

        if self.name == "Commissary" :
            items = {
                "gemme" : 3,
                "banane" : 3,
                "pelle" : 6, 
                "marteau" : 8,
                "détecteur de métal" : 10,
                "clé" : 10,
                "loupe" : 4,
                "salière" : 5,
                "compas" : 6,
                "masque pour dormir" : 8
            }
            self.items_for_sale = dict(random.sample(list(items.items()), 4)) 
            return self.items_for_sale
        
        elif self.name == "Kitchen" :
        
            special_items = {
                "repas" : 20,
                "bacon et oeufs" : 8,
                "salade" : 5,
                "soupe" : 5
            } # Chaque jour un item spécial est proposé d'après le wiki

            special_item = random.choice(list(special_items.keys())) # Choisit de façon aléatoire un seul de la liste 

            self.items_for_sale = {
                "banane" : 2,
                "sandwich" : 8,
                special_item : special_items[special_item]
            } # Les bananes et sandwichs sont toujours proposés
            return self.items_for_sale
        
        elif self.name == "Locksmith" :
            self.items_for_sale = {
                "clé" : 5,
                "kit de crochetage" : 10
            }
            return self.items_for_sale
        
        elif self.name == "Showroom" : # Pour l'instant vide car nous n'avons pas implémenté les objets du showroom
            self.items_for_sale = {}
            #items= { "moon pendant" : 20, "silver spoon" : 30, "chronograph" : 30, "ornate compass" : 50, "emerald bracelet" : 60, "master key" : 80, "trophy of wealth" : 100}
            #self.items_for_sale = dict(random.sample(list(items.items(), 4)))
            return self.items_for_sale
        
        elif self.name == "Bookshop" : # Pour l'instant vide car nous n'avons pas implémenté les objets de la bibliothèque
            self.items_for_sale = {}
            #self.items_for_sale = {
            #   "The History of Orindia (1st ed.)" : 50,
            #    "A New Clue" : 50,
            #    "The Curse of Black Bridge" : 40,
            #    "Realm & Rune" : 20,
            #    "Drafting Strategy Vol. 4" : 8,
            #    "Drafting Strategy Vol. 5" : 8
            #} 
            return self.items_for_sale
        
        elif self.name == "The Armory" : # Pour l'instant presque vide car nous n'avons pas implémenté les objets de l'arsenal
            self.items_for_sale = {
                "pelle" : 30,
                "kit de crochetage" : 20
            }
            #items = {
            #    "Morning Star" : 8,
            #    "hache" : 32,
            #    "Self Igniting Torch" : 8,
            #    "Knight's Shield" : 8    
            #}
            #self.items_for_sale = dict(random.sample(list(items.items(), 3))) 
            return self.items_for_sale
        
        elif self.name == "Mount Holly Gift Shop" :
            self.items_for_sale = {} 
            return self.items_for_sale
        else:
            return {}  # Laundry room n'a pas d'items en vente donc dictionnaire vide pour ne pas causer de problèmes 
            
    def enter_room(self, inventory : Inventory) :
        """Interface pour rentrer dans les magasins ou pièces jaunes."""
        
        print(f"\nVous êtes dans {self.name}.")

        if self.name == "Laundry Room" :
            return self.display_services(inventory)
        
        print("\nSouhaitez-vous entrer au magasin ?")

        response = ''
        while response != 'o' and response != 'n' :
                response = input("\nTapez 'o' pour oui et 'n' pour non : ")
        response = (response == 'o')
        if response :
            return self.shop_interface(inventory)
        else :
            print("\nPas d'achats pour le moment.")
            return False
        
    def shop_interface(self, inventory : Inventory) :
        """Interface générale des magasins"""
        if self.name == "Commissary" :
            print("\nMagasin du commissariat : ") 
        elif self.name == "Kitchen" :
            print("\nNourriture dans le frigo : ")
        elif self.name == "Locksmith" :
            print("\nMagasin de la serrurerie : ")
        elif self.name == "Showroom" :
            print("\nObjets en vente de la salle d'exposition : ")
        elif self.name == "Laundry Room" :
            print("\nServices de la laverie :")
            self.display_services(inventory)
            return self.interaction_with_services(inventory)
        elif self.name == "Bookshop" :
            print("\nLivres en vente :")
        elif self.name == "The Armory" :
            print("\nArmes en vente :")
        else :
            print("\nSouvenirs en vente :")

        self.display_items(inventory)
        return self.interaction_with_items(inventory)

    def display_items(self, inventory : Inventory) :
        """Affiche les objets disponible dans le magasin"""
        if not self.items_for_sale :
            print("\nLe magasin est en rupture de stock, nous sommes désolés :(")
            return
        
        items_list = list(self.items_for_sale.items())
        for item, price in items_list:
            print(f"{item:.<18} {price} pièces")
        print("\nAnnuler :(")
        print(f"\nVotre argent : {inventory.coins} pièces")

    def interaction_with_items(self, inventory : Inventory) :
        """Gère les intéractions dans un magasin"""
        while True :
            print("\nQue souhaitez-vous acheter ?")
            items_list = list(self.items_for_sale.items())
            if not items_list:
                print("\nPlus rien à acheter ici revenez demain !")
                return False
            for i, (item, price) in enumerate(items_list, 1):
                print(f"  {i}. {item:.<18} {price} pièces")
            print(f"  {len(items_list) + 1}. Annuler")
            try:
                response = int(input(f"Votre choix (1-{len(items_list) + 1}): "))
                
                if response == len(items_list) + 1:
                    print("Achat annulé")
                    return False
                
                # CORRECTION: 1 <= response au lieu de 1 < response
                if 1 <= response <= len(items_list):
                    item_name, price = items_list[response - 1]
                    if inventory.coins < price: 
                        print("\nVous n'avez pas assez d'argent !")
                        continue  # Continuer plutôt que retourner False
                    
                    print(f"\nVous êtes sûr(e) de vouloir acheter un/e {item_name} pour {price} pièces ?")
                    confirm = ''
                    while confirm != "o" and confirm != 'n':
                        confirm = input("Tapez 'o' pour oui et 'n' pour non: ")
                    
                    if confirm == 'o':
                        inventory.coins -= price
                        inventory.pick_up(Objet(item_name))
                        print(f"\nAchat réussi! Argent restant: {inventory.coins}")
                        return True
                    else:
                        print("Achat annulé.")
                        return False
                else:
                    print("Choix invalide!")
            
            except ValueError:
                print("Veuillez entrer un nombre valide!")

    def laundry_interface(self, inventory: Inventory):
        """Interface spécifique pour la laverie qui ne propse que des services (pas d'items)"""
        self.display_services(inventory)
        return self.interaction_with_services(inventory) 
     
    def display_services(self, inventory):
        """Affiche les services de la laverie"""

        print("\nServices disponibles:")
        services_list = list(self.services.items())

        for i, (service, price) in enumerate(services_list, 1):
            print(f"  {i}. {service:.<18} {price['cost']} pièces")

        print(f"\nVotre argent : {inventory.coins} pièces")
        print(f"\nVos clés : {inventory.keys}")
        print(f"\nVos gemmes : {inventory.gems}")

    def interaction_with_services(self, inventory : Inventory) :
        """Gère les services dans la laverie"""

        while True:
            print("\nSouhaitez-vous utiliser un service ?")

            response = ''
            while response != 'o' and response != 'n':
                    response = input("\nTapez 'o' pour oui et 'n' pour non : ")
            response = (response == 'o')

            if response :
                print("\nChoisissez le service :")
                print("\n1) Essorage")
                print("\n2) Lavage et séchage")
                print("\n3) Fluff and fold")

                response = ''
                while response != '1' and response != '2' and response != '3' :
                    response = input("\nTapez '1' pour service 1, '2' pour le service 2 et '3' pour le service 3 : ")
                services_list = list(self.services.items())

                if response == '1':
                    print(f"\nAvant : {inventory.coins} pièces et {inventory.gems} gemmes")
                    service_name, action = services_list[0]
                    if inventory.coins < action["cost"] :
                        print(f"Pas assez d'argent :(")
                        return
                    inventory.coins -= action["cost"]
                    
                    new_gems = inventory.coins
                    new_coins = inventory.gems
                    inventory.coins = new_coins
                    inventory.gems = new_gems

                    print("\nService complété ! Toutes vos gemmes ont été échangées par toutes vos pièces !")
                    print(f"\nAprès : {inventory.coins} pièces et {inventory.gems} gemmes")
                elif response == '2' :
                    print(f"\nAvant : {inventory.keys} clés et {inventory.gems} gemmes")
                    service_name, action = services_list[1]
                    if inventory.coins < action["cost"] :
                        print(f"Pas assez d'argent :(")
                        return
                    inventory.coins -= action["cost"]
                    
                    new_gems = inventory.keys
                    new_keys = inventory.gems
                    inventory.keys = new_keys
                    inventory.gems = new_gems

                    print("\nService complété ! Toutes vos clés ont été échangées par toutes vos gemmes !")
                    print(f"\nAprès : {inventory.keys} clés et {inventory.gems} gemmes")
                else:
                    print(f"\nAvant : {inventory.keys} clés et {inventory.coins} pièces")
                    service_name, action = services_list[2]
                    if inventory.coins < action["cost"] :
                        print(f"Pas assez d'argent :(")
                        return
                    inventory.coins -= action["cost"]
                    
                    new_coins = inventory.keys
                    new_keys = inventory.coins
                    inventory.keys = new_keys
                    inventory.coins = new_coins

                    print("\nService complété ! Toutes vos clés ont été échangées par toutes vos pièces !")
                    print(f"\nAprès : {inventory.keys} clés et {inventory.coins} pièces")
                
            else:
                print("\nAu revoir !")
                return True

class Purple(Room):
    rooms = ["Bedroom", "Boudoir", "Guest Bedroom", "Nursery", "Servant's Quarters", "Bunk Room", "Her Ladyship's Chamber", "Master Bedroom"] 
    
    def __init__(self, name:str):
        super().__init__(name, "red")
        self.dig_spots_available = self.dig_spots() # Nombre d'endroits à creuser
        self.dig_spots_position = self.dig_position() # Position des endroits à creuser s'il y en a
        self.permanent_objects = None # objets permanents (ex: pelle)
        self.available_items = self.items() # items que le joueur découvre en ouvrant des coffres, armoires etc. Ici, le joueur les obtient immédiatemment
        self.cost = self.gem_cost() # Coût de la pièce
        
    def items(self):
        """Génère les items des pièces"""
        if self.name == "Bedroom":
            room_items = {"pomme": 1, "dé": 1, "clé": 1, "gemme": 1, "pièce": 3, "coin purse":1, "masque pour dormir": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Boudoir":
            room_items = {"pièce": random.choice([2, 3, 5]), "clé": random.randint(1,2), "gemme": 1, "coin purse": 1, "masque pour dormir": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Guest Bedroom":
            room_items = {"clé": 1, "gemme": 1, "compas": 1}
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Nursery":
            room_items = {"dé": 2, "clé": 1, "gemme": 1, "pièce": 3, "patte de lapin": 1}
            return dict(random.sample(list(room_items.items()), 2)) 
        elif self.name == "Servant's Quarters":
            room_items = {"dé": 2, "gemme": 1, "levier cassé": 1, "détecteur de métal": 1, "pelle": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Bunk Room":
            room_items = {"banane": 2, "clé": 2, "gemme" : 2, "pièce": 4}
            return dict(random.sample(list(room_items.items()), random.randint(1, 2))) 
        elif self.name == "Her Ladyship's Chamber":
            room_items = {"banane": 1, "patte de lapin": 1, "clé": 1, "gemme": 1, "pièce":5, "coin purse" : 1, "masque pour dormir": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Master Bedroom":
            room_items = {"dé": 2, "pièce": random.choice([4, 5, 9]), "clé": 1, "gemme":random.randint(1,3), "kit de crochetage": 1, "masque pour dormir" :1, "compas": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 

    def gem_cost(self):
        """Génère le coût pour entrer dans chaque pièce"""
        cost = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 1,
            "Servant's Quarters": 1,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Her": 2
            }
        return cost.get(self.name)

    def dig_spots(self):
        """Génère un nombre d'endroits à creuser selon les pièces"""

        spots = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 0,
            "Servant's Quarters": 0,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Her": 0
            }
        return spots.get(self.name)

    def chest_spots(self):
        """Génère un nombre de coffres selon les pièces"""

        spots = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 0,
            "Servant's Quarters": 0,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Her": 0
            }
        return spots.get(self.name)
    
    def locker_spots(self):
            """Génère un nombre de lockers selon les pièces"""

            spots = {
                "Bedroom": 0,
                "Boudoir": 0,
                "Guest Bedroom": 0,
                "Nursery": 0,
                "Servant's Quarters": 0,
                "Bunk Room": 0,
                "Her Ladyship's Chamber": 0,
                "Her": 0
                }
            return spots.get(self.name)
    
    def enter_room(self, inventory : Inventory) :
        """Interface pour rentrer dans les pièces vertes"""

        print(f"Vous êtes dans {self.name} !")

        if self.cost>0 :
            print(f"Coût d'entrée : {self.cost} gemme/s.")
            print(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
            response = ''
            while response not in ['o', 'n']:
                response = input("Tapez 'o' pour oui et 'n' pour non : ").lower()
            
            if response == 'n':
                print("Vous ne souhaitez pas explorer la pièce.")
                return False

            if inventory.gems < self.cost :
                print(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                return False
            
            inventory.gems -= self.cost
            print(f"Gemmes restantes : {inventory.gems}")
            if inventory.gems < 5 :
                print("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
        
        if self.name == "Bedroom":
            extra_steps = 2

            print(f"Vois avez très bien dormi ! \n     + {extra_steps} pas")
            inventory.steps += 2
            print(f"Pas : {inventory.steps}")

        if self.name == "Boudoir" :
            extra_steps = random.randint(0, 4)
            print(f"Vois avez très bien dormi ! \n     + {extra_steps} pas")
            inventory.steps += extra_steps
            print(f"Pas : {inventory.steps}")

        if self.name == "Guest Bedroom" and not self.visited:
            extra_steps = 10
            print(f"Vois avez très bien dormi ! \n     + {extra_steps} pas")
            inventory.steps += extra_steps
            print(f"Pas : {inventory.steps}")
        if self.name == "Servant's Quarters" and not self.visited:
            print(f"Vous voyez 3 clés sur le lit.\n    + 3 clés")
            inventory.keys +=3
            print(f"Clés disponible dans l'inventaire : {inventory.keys}")
        # De façon aléatoire, certaines pièces contiennent des items dans les armoires, coffres etc. Pour l'instant, le joeur les obtient immédiatement
        if self.available_items and not self.visited :
            if self.name == "Bedroom" :
                print(random.choice(["Vous trouvez dans l'armoire :", "Vous trouvez sur la statue :"]))
            if self.name == "Boudoir" or self.name == "Guest Bedroom" or self.name == "Nursery" or self.name == "Master Bedroom":
                print("Vous trouvez sur la table :")
            if self.name == "Servant's Quarters" :
                print(random.choice(["Vous trouvez sur le lit :", "Vous trouvez sur la planche à repasser :"]))
            if self.name == "Her Ladyship's Chamber" :
                print(random.choice(["Vous trouvez sur la table :", "Vous trouvez sur la chaisse :"]))
            
            for item_name, _ in self.available_items.items():
                print(f"==> {item_name}")
                inventory.pick_up(Objet(item_name))
        
        self.visited = True
        return True

class Red(Room):

    rooms = ["Lavatory", "Chapel", "Maid's Chamber", "Archives", "Gymnasium", "Darkroom", "Weight Room", "Furnace"] 
    
    def __init__(self, name:str):
        super().__init__(name, "red")
        self.dig_spots_available = self.dig_spots() # Nombre d'endroits à creuser
        self.dig_spots_position = self.dig_position() # Position des endroits à creuser s'il y en a
        self.permanent_objects = None # objets permanents (ex: pelle)
        self.available_items = self.items() # items que le joueur découvre en ouvrant des coffres, armoires etc. Ici, le joueur les obtient immédiatemment
      
    def enter_room(self, inventory : Inventory) :
        """Interface pour entrer dans les pièces vertes"""

        print(f"Vous êtes dans {self.name} !")

        if self.name == "Weight Room":
            print(f"Après un long entraînement, vous êtes épuisé ! Vous perdez {inventory.steps//2} pas. Reposez-vous, avant de continuer.")
            inventory.steps = inventory.steps//2
            print(f"Pas restants : {inventory.steps}")

        if self.name == "Gymnasium" :
            print(f"Après un long entraînement, vous êtes épuisé ! Vous perdez {inventory.steps - 2} pas. Reposez-vous, avant de continuer.")
            inventory.steps = inventory.steps - 2
            print(f"Pas restants : {inventory.steps}")

        if self.name == "Chapel" :
            print(f"Vous faites une donation de 1 pièce. L'église vous remercie !")
            if inventory.coins >= 1:
                inventory.coins -= 1
                print(f"Pièces restantes : {inventory.coins}")
            else :
                print("Vous n'avez pas assez de pièces pour faire une donation.")

        # De façon aléatoire, certaines pièces contiennent des items dans les armoires, coffres etc. Pour l'instant, le joeur les obtient immédiatement
        if self.available_items and not self.visited :
            if self.name == "Chapel" :
                print("Vous trouvez sur les chandeliers :")
            if self.name == "Archives" :
                print("Vous fouillez les archives et trouvez :")
            if self.name == "Gymnasium" :
                print("Vous trouvez sur le banc :")
            if self.name == "Darkroom" :
                print("Vous ne voyez rien, vous ne pouvez pas explorer la pièce dans l'obscurité.")
                print("Voulez vous allumer la lumière ?")
                response = ''
                while response not in ['o', 'n']:
                    response = input("Tapez 'o' pour oui et 'n' pour non : ").lower()
                
                if response == 'o':
                    print("La lumière est allumée ! Vous trouvez :")
                else:
                    return False
            if self.name == "Weight Room" :
                print("Vous trouvez à côté des poids :")
            if self.name == "Furnace" :
                print("La chaleur est intense, vous voulez partir. Mais, au moins vous avez trouvé quelques items :")
            for item_name, _ in self.available_items.items():
                print(f"==> {item_name}")
                inventory.pick_up(Objet(item_name))
        
        print("\nGrille de la pièce :") # Grille à modifier
        self._display_text_grid()
        
        self.visited = True
        return True
    
    def items(self):
        """Génère les items des pièces"""
        if self.name == "Lavatory":
            room_items = {}
            return room_items
        elif self.name == "Chapel":
            gold = [2, 3, 4, 5, 12, 14]
            room_items = {"pièce": random.choice(gold), "gemme": random.randint(1,2)}
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Maid's Chamber":
            room_items = {}
            return room_items
        elif self.name == "Archives":
            room_items = {"gemme":random.randint(1,2), "pomme" : 1, "clé" : random.randint(1, 2), "levier cassé" : 1, "détecteur de métal" : 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Gymnasium":
            room_items = {"clé": 1, "pièce":3}
            return room_items
        elif self.name == "Darkroom":
            room_items = {"gemme": random.randint(1, 2), "clé": 1, "levier cassé": 1}
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Weight Room":
            room_items = {"pièce": 3, "levier cassé": 1}
            return room_items
        elif self.name == "Furnace":
            room_items = {}
            return room_items 
    
    def dig_spots(self):
        """Génère un nombre d'endroits à creuser selon les pièces"""

        spots = {
            "Lavatory" : 0, 
            "Chapel" : 0, 
            "Maid's Chamber" : 0, 
            "Archives" : 0, 
            "Gymnasium" : 0, 
            "Darkroom" : 0, 
            "Weight Room" : 0, 
            "Furnace" : random.randint(0, 2)
            }
        return spots.get(self.name)    

class Green(Room):
    """Ce sont des jardins d'intérieur, qui contiennent souvent des gemmes, des endroits où creuser, et des objets permanents"""
    
    rooms = ["Terrace", "Patio", "Courtyard", "Cloister", "Veranda", "Greenhouse", "Morning Room", "Secret Garden"]

    def __init__(self, name:str):
        super().__init__(name, "vert")
        self.cost = self.gem_cost() # Coût de la pièce
        self.dig_spots_available = self.dig_spots() # Nombre d'endroits à creuser
        self.dig_spots_position = self.dig_position() # Position des endroits à creuser s'il y en a
        self.gem_bonus = self.gem_bonus() # Bonus des pièces lorsque le joueur rentre dedans
        self.permanent_objects = None # objets permanents (ex: pelle)
        self.available_items = self.items() # items que le joueur découvre en ouvrant des coffres, armoires etc. Ici, le joueur les obtient immédiatemment
   
    def items(self):
        """Génère les items des pièces"""
        if self.name == "Terrace":
            room_items = {"banane": 1, "orange": 1, "gemme":random.randint(1,2), "pièce": 2, "compas":1, "pelle": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Patio":
            room_items = {"pomme": 1, "clé": 1, "gemme":random.randint(1,3), "détecteur de métal": 1, "pelle": 1}
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Courtyard":
            room_items = {"détecteur de métal": 1, "marteau": 1, "pelle": 1}
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Cloister":
            room_items = {"gemme":random.randint(1,3)}
            return room_items
        elif self.name == "Veranda":
            room_items = {"détecteur de métal": 1, "marteau": 1, "pelle": 1, "gemme":1}
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Greenhouse":
            room_items = {"détecteur de métal": 1, "marteau": 1, "pelle": 1}
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Morning Room":
            room_items = {"dé": 2, "patte de lapin": 1, "pelle": 1, "salière": 1, "coin purse":1}
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Secret Garden":
            room_items = {"détecteur de métal": 1, "pelle": 1, "marteau": 1, "levier cassé":1}
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
    
    def dig_spots(self):
        """Génère un nombre d'endroits à creuser selon les pièces"""

        spots = {
            "Terrace": random.randint(1, 3),
            "Patio": random.randint(2, 5),
            "Courtyard": random.randint(2, 3),
            "Cloister": random.randint(2, 4),
            "Veranda": random.randint(2, 4),
            "Greenhouse": random.randint(2, 4),
            "Morning Room": random.randint(0, 3),
            "Secret Garden":random.randint(3, 7)
            }
        return spots.get(self.name)

    def gem_cost(self):
        """Génère le coût pour entrer dans chaque pièce"""
        cost = {
            "Terrace": 0,
            "Patio": 1,
            "Courtyard": 1,
            "Cloister": 3,
            "Veranda": 2,
            "Greenhouse": 1,
            "Morning Room": 0,
            "Secret Garden": 0
            }
        return cost.get(self.name)

    def gem_bonus(self):
        """Indique si les pièces apportent un bonus (gemmes) ou pas"""
        rooms = {
            "Terrace": (True, random.randint(1, 2)),
            "Patio": (True, random.randint(1, 3)),
            "Courtyard": (True, 2),
            "Cloister": (False, 0),
            "Veranda": (True, 1),
            "Greenhouse": (False, 0),
            "Morning Room": (True, 2),
            "Secret Garden": (False, 0)
            }
        return rooms.get(self.name)

    def enter_room(self, inventory : Inventory) :
        """Interface pour rentrer dans les pièces vertes"""

        print(f"Vous êtes dans {self.name} !")

        if self.cost>0 :
            print(f"Coût d'entrée : {self.cost} gemme/s.")
            print(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
            response = ''
            while response not in ['o', 'n']:
                response = input("Tapez 'o' pour oui et 'n' pour non : ").lower()
            
            if response == 'n':
                print("Vous ne souhaitez pas explorer la pièce.")
                return False

            if inventory.gems < self.cost :
                print(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                return False
            
            inventory.gems -= self.cost
            print(f"Gemmes restantes : {inventory.gems}")
            if inventory.gems < 5 :
                print("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
        
        # Certaines pièces apportent des gemmes juste en les débloquants, puis après quelques jours
        has_bonus, bonus_amount = self.gem_bonus
        if has_bonus and bonus_amount > 0:
            print(f"Bonus ! \n+ {bonus_amount} gemme(s)")
            inventory.gems += bonus_amount
        
        # De façon aléatoire, certaines pièces contiennent des items dans les armoires, coffres etc. Pour l'instant, le joeur les obtient immédiatement
        if self.available_items and not self.visited:
            print("Objets découverts dans le jardin :")
            for item_name, _ in self.available_items.items():
                print(f"==> {item_name}")
                inventory.pick_up(Objet(item_name))
        
        self.visited = True
        return True
