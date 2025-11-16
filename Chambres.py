from inventory import Inventory
from objet import Objet
from colorpalette import couleurs
import text
import random
import pygame
from abc import ABC, abstractmethod


class Room(ABC) :
    """Classe abstraite qui définit les pièces du jeu.

    Attributes
    - possible : list[str] <<class attribute>>
        Liste de toutes les salles dans notre jeu
    - name : str
        Le nom de la pièce
    - color : str
        La couleur de la pièce (chaque couleur représente une catégorie de pièce)
    - visited : bool
        Indique si la pièce a déjà été visitée
    - doors : list[Door]
        Liste des pièces qui peuvent être accédées à travers la pièce actuelle
    - message : str
        Message qui s'affiche sur l'interface 
    """
    
    possible = ["Commissary", "Kitchen", "Locksmith", "Laundry Room", "Bookshop", "The Armory", "Showroom", "Mount Holly Gift Shop",
                "Terrace", "Patio", "Courtyard", "Cloister", "Veranda", "Greenhouse", "Morning Room", "Secret Garden",
                "Bedroom", "Boudoir", "Guest Bedroom", "Nursery", "Servant's Quarters", "Bunk Room", "Her Ladyship's Chamber", "Master Bedroom",
                "Hallway", "West Wing Hall", "East Wing Hall", "Corridor", "Passageway", "Secret Passage", "Foyer", "Great Hall",
                "Lavatory", "Chapel", "Maid's Chamber", "Archives", "Gymnasium", "Darkroom", "Weight Room", "Furnace",
                "The Foundation", "Entrance Hall", "Spare Room", "Rotunda", "Parlor", "Billiard Room", "Gallery", "Room 8", "Closet", "Walk-in Closet", "Attic", "Storeroom", "Nook", "Garage", "Music Room", "Locker Room", "Den", "Wine Cellar", "Trophy Room", "Ballroom", "Pantry", "Rumpus Room", "Vault", "Office", "Drawing Room", "Study", "Library", "Chamber of Mirrors", "The Pool", "Drafting Studio", "Utility Closet", "Boiler Room", "Pump Room", "Security", "Workshop", "Laboratory", "Sauna", "Coat Check", "Mail Room", "Freezer", "Dining Room", "Observatory", "Conference Room", "Aquarium", "Antechamber", "Room 46"]
    

    def __init__(self, name : str, color : str):
        self.name = name
        self.color = color
        self.visited = False 
        self.doors = [] 
        self.message = ""

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if name not in Room.possible:
            name_cleaned = name.replace("_", " ").title()
            if name_cleaned in Room.possible:
                self.__name = name_cleaned
                return
            print(f"Attention: '{name}' n'est pas dans la liste des salles possibles")
            self.__name = name
        else:
            self.__name = name
    
    @abstractmethod
    def enter_room(self):
        """Ajoute des effets lorsque le joueur rentre dans la pièce
        
        """
        pass

    def add_door(self, room):
        """Ajoute une porte vers une nouvelle pièce.
        
        Parameters:
        - room : Room
            La pièce vers laquelle on ajoute une porte
        """
        self.doors.append(room)
    
    def __str__(self):
        return f"{self.name} (pièce {self.color})"
    
    def show_room(self,screen):
        """ Permet d'afficher la chambre dans laquelle se trouve le joueur sur l'interface graphique.

        Parameters:
        - screen : Surface
            La surface sur laquelle on affiche la chambre (écran du jeu)
        """
        width = screen.get_width()
        height = screen.get_height()//2 
        chambre = pygame.Surface((width,height))
        chambre.fill(couleurs["darkblue"])
        pygame.draw.rect(chambre,couleurs['brightblue'],pygame.Rect(0,0,width,height),width=15)
        
        afficher = [f"Salle : {self.name}","------------------------------------------------------------------------------------------------",self.message]       
        text.texte(afficher,chambre,x=30,y=30,color="white",font=text.room_font,modifiers={0:'bold'})
        
        return chambre

class Yellow(Room) :
    """Ce sont des magasins dans lesquels il est possible d'échanger de l'or contre d'autres objets.

    Attributes:
    - rooms : list[str] <<class attribute>>
        Liste de toutes les pièces vertes
    - cost : int
        Coût de la pièce lors du tirage
    - items_for_sale : dict[str, int]
        Items en vente dans le magasin
    - services : dict[str, dict]
        Services de la laverie
    """
    
    rooms = ["Commissary", "Kitchen", "Locksmith", "Laundry Room", "Bookshop", "The Armory", "Showroom", "Mount Holly Gift Shop"]
    
    def __init__(self, name:str):
        super().__init__(name, "yellow")
        self.cost = self.gem_cost()
        self.items_for_sale = self.items()
        self.services = {
            "Essorage" : {"cost" : 5, "action" : "exchange_all_gems_with_all_gold"},
            "Lavage et séchage" : {"cost" : 5, "action" : "exchange_all_keys_with_all_gems"},
            "Fluff and fold" : {"cost" : 5, "action" : "exchange_all_keys_with_all_gold"}
        }
            
    def items(self):
        """Renvoie la liste d'objets pour chacun des magasins.
        
        Returns:
        - items_for_sale : dict[str, int]
            Renvoie un dictionnaire d'items et leur prix en pièces
        """

        if self.name == "Commissary" :
            items = {
                "gemme" : 3,
                "banane" : 3,
                "pelle" : 6, 
                "marteau" : 8,
                "détecteur de métal" : 10,
                "clé" : 10
            }
            self.items_for_sale = dict(random.sample(list(items.items()), 4)) 
            return self.items_for_sale
        
        elif self.name == "Kitchen" :
        
            special_items = {
                "repas" : 20,
                "bacon et oeufs" : 8,
                "salade" : 5,
                "soupe" : 5
            }

            special_item = random.choice(list(special_items.keys()))

            self.items_for_sale = {
                "banane" : 2,
                "sandwich" : 8,
                special_item : special_items[special_item]
            } 
            return self.items_for_sale
        
        elif self.name == "Locksmith" :
            self.items_for_sale = {
                "clé" : 5,
                "kit de crochetage" : 10
            }
            return self.items_for_sale
        
        elif self.name == "Showroom" :
            self.items_for_sale = {}
            return self.items_for_sale
        
        elif self.name == "Bookshop" : 
            self.items_for_sale = {}
            return self.items_for_sale
        
        elif self.name == "The Armory" : 
            self.items_for_sale = {
                "pelle" : 30,
                "kit de crochetage" : 20
            }
            
            return self.items_for_sale
        
        elif self.name == "Mount Holly Gift Shop" :
            self.items_for_sale = {} 
            return self.items_for_sale
        else:
            return {} 

    def gem_cost(self):
        """Indique le coût pour entrer dans la pièce.
        
        Returns:
        -int
            Prix en gemmes de la pièce lors du premier tirage
        """
        
        cost = {"Commissary": 1, 
                "Kitchen": 1, 
                "Locksmith": 1, 
                "Laundry Room": 1, 
                "Bookshop": 1, 
                "The Armory": 0, 
                "Showroom": 2, 
                "Mount Holly Gift Shop": 0
            }
        
        return cost.get(self.name)
            
    def enter_room(self, inventory : Inventory) :
        """Interface pour rentrer dans les magasins ou pièces jaunes.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -display_services
            Si le magasin est une laverie alors renvoie les service de celle-ci
        -shop_interface
            Interface du magasin qui n'est pas une laverie
        -bool
            Renvoie False si le joueur n'a pas assez de gemmes pour payer l'entrée au magasin lors du tirage ou si le joueur décide de ne pas explorer le magasin
        """
        if self.name == "Laundry Room" :
            return self.display_services(inventory)
        
        message= [f"Vous êtes dans {self.name}."]
        if self.cost > 0 :
            
            reponse = ''
            while reponse != 'o' and reponse != 'n':
                message.append(f"Coût d'entrée : {self.cost} gemme/s.")
                message.append(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
                reponse = input("Tapez 'o' pour oui et 'n' pour non : ").lower()

            reponse = pygame.event.get()
            if reponse.key == pygame.K_o:
                if inventory.gems < self.cost :
                    message.append(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                    return False
                message.append("Vous avez fait le bon choix !")
                inventory.gems -= self.cost
                if inventory.gems < 5 :
                    message.append("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
                return self.shop_interface(inventory)
            else:    
                message.append("Pas de shopping pour le moment.")
                return False
             
    def shop_interface(self, inventory : Inventory) :
        """Interface générale des magasins.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -interaction_with_items
            Gère les intéractions avec les items du magasin
        
        """
        message= [f"Vous êtes dans {self.name}."]
        if self.name == "Commissary" :
            message.append("\nMagasin du commissariat : ") 
        elif self.name == "Kitchen" :
            message.append("\nNourriture dans le frigo : ")
        elif self.name == "Locksmith" :
            message.append("\nMagasin de la serrurerie : ")
        elif self.name == "Showroom" :
            message.append("\nObjets en vente de la salle d'exposition : ")
        elif self.name == "Laundry Room" :
            message.append("\nServices de la laverie :")
            self.display_services(inventory)
            return self.interaction_with_services(inventory)
        elif self.name == "Bookshop" :
            message.append("\nLivres en vente :")
        elif self.name == "The Armory" :
            message.append("\nArmes en vente :")
        else :
            message.append("\nSouvenirs en vente :")

        self.display_items(inventory)
        return self.interaction_with_items(inventory)

    def display_items(self, inventory : Inventory) :
        """Affiche les objets disponible dans le magasin.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        """
        message= [f"Vous êtes dans {self.name}."]
        if not self.items_for_sale :
            message.append("\nLe magasin est en rupture de stock, nous sommes désolés :(")
            return
        
        items_list = list(self.items_for_sale.items())
        for item, price in items_list:
            message.append(f"{item:.<18} {price} pièces")
        message.append("\nAnnuler :(")
        message.append(f"\nVotre argent : {inventory.coins} pièces")

    def interaction_with_items(self, inventory : Inventory) :
        """Gère les intéractions dans un magasin.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -bool
            True si l'achat est réussi, False sinon
        """
        message= [f"Vous êtes dans {self.name}."]
        while True :
            message.append("\nQue souhaitez-vous acheter ?")
            items_list = list(self.items_for_sale.items())
            if not items_list:
                message.append("\nPlus rien à acheter ici revenez demain !")
                return False
            for i, (item, price) in enumerate(items_list, 1):
                message.append(f"  {i}. {item:.<18} {price} pièces")
            message.append(f"  {len(items_list) + 1}. Annuler")
            try:
                response = int(input(f"Votre choix (1-{len(items_list) + 1}): "))
                
                if response == len(items_list) + 1:
                    message.append("Achat annulé")
                    return False
                
                if 1 <= response <= len(items_list):
                    item_name, price = items_list[response - 1]
                    if inventory.coins < price: 
                        message.append("\nVous n'avez pas assez d'argent !")
                        continue 
                    
                    message.append(f"\nVous êtes sûr(e) de vouloir acheter un/e {item_name} pour {price} pièces ?")
                    confirm = ''
                    while confirm != "o" and confirm != 'n':
                        confirm = input("Tapez 'o' pour oui et 'n' pour non: ")
                    
                    if confirm == 'o':
                        inventory.coins -= price
                        inventory.pick_up(Objet(item_name))
                        message.append(f"\nAchat réussi!")
                        return True
                    else:
                        message.append("Achat annulé.")
                        return False
                else:
                    message.append("Choix invalide!")
            
            except ValueError:
                message.append("Veuillez entrer un nombre valide!")

    def laundry_interface(self, inventory: Inventory):
        """Interface spécifique pour la laverie qui ne propose que des services (pas d'items).
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        - interaction_with_services
            Gère les interactions avec les services de la laverie
        """
        self.display_services(inventory)
        return self.interaction_with_services(inventory) 
     
    def display_services(self):
        """Affiche les services de la laverie."""

        message= [f"Vous êtes dans {self.name}."]
        message.append("\nServices disponibles:")
        services_list = list(self.services.items())

        for i, (service, price) in enumerate(services_list, 1):
            message.append(f"  {i}. {service:.<18} {price['cost']} pièces")

    def interaction_with_services(self, inventory : Inventory) :
        """Gère les services dans la laverie.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur

        Returns:
        -bool
            True si l'achat est réussi, False sinon
        """
        message= [f"Vous êtes dans {self.name}."]
        while True:
            message.append("\nSouhaitez-vous utiliser un service ?")

            response = ''
            while response != 'o' and response != 'n':
                    response = input("\nTapez 'o' pour oui et 'n' pour non : ")
            response = (response == 'o')

            if response :
                message.append("\nChoisissez le service :")
                message.append("\n1) Essorage")
                message.append("\n2) Lavage et séchage")
                message.append("\n3) Fluff and fold")

                response = ''
                while response != '1' and response != '2' and response != '3' :
                    response = input("\nTapez '1' pour service 1, '2' pour le service 2 et '3' pour le service 3 : ")
                services_list = list(self.services.items())

                if response == '1':
                    message.append(f"\nAvant : {inventory.coins} pièces et {inventory.gems} gemmes")
                    service_name, action = services_list[0]
                    if inventory.coins < action["cost"] :
                        message.append(f"Pas assez d'argent :(")
                        return False
                    inventory.coins -= action["cost"]
                    
                    new_gems = inventory.coins
                    new_coins = inventory.gems
                    inventory.coins = new_coins
                    inventory.gems = new_gems

                    message.append("\nService complété ! Toutes vos gemmes ont été échangées par toutes vos pièces !")
                    message.append(f"\nAprès : {inventory.coins} pièces et {inventory.gems} gemmes")
                elif response == '2' :
                    message.append(f"\nAvant : {inventory.keys} clés et {inventory.gems} gemmes")
                    service_name, action = services_list[1]
                    if inventory.coins < action["cost"] :
                        message.append(f"Pas assez d'argent :(")
                        return False
                    inventory.coins -= action["cost"]
                    
                    new_gems = inventory.keys
                    new_keys = inventory.gems
                    inventory.keys = new_keys
                    inventory.gems = new_gems

                    message.append("\nService complété ! Toutes vos clés ont été échangées par toutes vos gemmes !")
                    message.append(f"\nAprès : {inventory.keys} clés et {inventory.gems} gemmes")
                else:
                    message.append(f"\nAvant : {inventory.keys} clés et {inventory.coins} pièces")
                    service_name, action = services_list[2]
                    if inventory.coins < action["cost"] :
                        message.append(f"Pas assez d'argent :(")
                        return False
                    inventory.coins -= action["cost"]
                    
                    new_coins = inventory.keys
                    new_keys = inventory.coins
                    inventory.keys = new_keys
                    inventory.coins = new_coins

                    message.append("\nService complété ! Toutes vos clés ont été échangées par toutes vos pièces !")
                    message.append(f"\nAprès : {inventory.keys} clés et {inventory.coins} pièces")
                
            else:
                message.append("\nAu revoir !")
                return True

class Orange(Room):
    """Ce sont des couloirs, qui ont souvent beaucoup de portes.

    Attributes:
    - rooms : list[str] <<class attribute>>
        Liste de toutes les pièces oranges
    - cost : int
        Coût de la pièce lors du tirage
    - dig_spots_available : int
        Nombre d'endroits où creuser pour la pièce choisie
    - chest_spots_available : int
        Nombre de coffres pour la pièce choisie
    - locker_spots_available : int
        Nombre de casiers pour la pièce choisie
    - available_items : dict[str, int]
        Dictionnaire de tous les items se retrouvant dans la pièce
    """
    rooms = ["Hallway", "West Wing Hall", "East Wing Hall", "Corridor", "Passageway", "Secret Passage", "Foyer", "Great Hall"]

    def __init__(self, name:str):
        super().__init__(name, "orange")
        self.cost = self.gem_cost()
        self.dig_spots_available = self.dig_spots() 
        self.chest_spots_available = self.chest_spots()
        self.locker_spots_available = self.locker_spots()
        self.available_items = self.items() 
               
    def items(self, inventory : Inventory):
        """Indique les items de la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -dict[str, int]
            Renvoie un dictionnaire d'items disponibles dans la pièce
        """
        room_items = {
            "banane": 1, 
            "orange": 1, 
            "pomme" : 1, 
            "gemme" : random.randint(1,3), 
            "pièce": random.randint(1,3), 
            "clé": random.randint(1,3), 
            "dé": random.randint(1,3), 
            "levier cassé":random.randint(1,3),
            "pelle": 1,
            "détecteur de métal": 1,
            "marteau": 1, 
            "patte de lapin": 1
            }
        
        if inventory.shovel:
            room_items["pelle"] = 0
        if inventory.hammer:
            room_items["marteau"] = 0
        if inventory.lockpick_kit:
            room_items["kit de crochetage"] = 0 
        if inventory.rabbit_foot:
            room_items["patte de lapin"] = 0
        if inventory.metal_detector:
            room_items["détecteur de métal"] = 0 
            
        if self.name == "Hallway":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "West Wing Hall":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "East Wing Hall":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Corridor":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Passageway":
            return {}
        elif self.name == "Secret Passage":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Foyer":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Great Hall":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 

    def gem_cost(self):
        """Indique le coût pour entrer dans la pièce pièce.
        
        Returns:
        - int
            Renvoie le coût en gemmes de la pièce lors du tirage
        """

        cost = {
            "Hallway": 0,
            "West Wing Hall": 0,
            "East Wing Hall": 0,
            "Corridor": 0,
            "Passageway": 2,
            "Secret Passage": 1,
            "Foyer": 2,
            "Great Hall": 0
            }
        
        return cost.get(self.name)

    def dig_spots(self):
        """Indique le nombre d'endroits où creuser dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre d'endroits où creuser dans la pièce
        """

        spots = {
            "Hallway": 0,
            "West Wing Hall": 0,
            "East Wing Hall": 0,
            "Corridor": 0,
            "Passageway": 0,
            "Secret Passage": 0,
            "Foyer": 0,
            "Great Hall": 0
            }
        
        return spots.get(self.name)

    def chest_spots(self):
        """Indique le nombre de coffres dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de coffres disponibles dans la pièce
        """

        spots = {
            "Hallway": 0,
            "West Wing Hall": 0,
            "East Wing Hall": 0,
            "Corridor": 0,
            "Passageway": 0,
            "Secret Passage": 0,
            "Foyer": 0,
            "Great Hall": 0
            }
        
        return spots.get(self.name)
    
    def locker_spots(self):
        """Indique le nombre de casiers dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de casiers disponibles dans la pièce
        """
        spots = {
            "Hallway": 0,
            "West Wing Hall": 0,
            "East Wing Hall": 0,
            "Corridor": 0,
            "Passageway": 0,
            "Secret Passage": 0,
            "Foyer": 0,
            "Great Hall": 0
            }
        
        return spots.get(self.name)

    def enter_room(self, inventory : Inventory) :
        """Gère les intéractions dans la pièce.
        
        Parameters:
        ---------------
        - inventory : Inventory
            L'inventaire du joueur
        Returns:
        - bool
            True si l'entrée est réussi, False sinon
        """

        message = [f"Vous êtes dans {self.name} !"]
        
        if self.cost>0 :
            reponse = ''
            while reponse != 'o' and reponse != 'n':
                message.append(f"Coût d'entrée : {self.cost} gemme/s.")
                message.append(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
                reponse = input("Tapez 'o' pour oui et 'n' pour non : ").lower()

            reponse = pygame.event.get()
            if reponse.key == pygame.K_o:
                if inventory.gems < self.cost :
                    message.append(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                    return False
                message.append("Vous avez fait le bon choix !")
            else:    
                message.append("Vous ne souhaitez pas explorer la pièce.")
                return False
            
            inventory.gems -= self.cost
            if inventory.gems < 5 :
                message.append("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
        
        if self.available_items and not self.visited :
            for item_name, _ in self.available_items.items():
                inventory.pick_up(Objet(item_name))
        
        if self.chest_spots_available>0:
            for i in range(self.chest_spots_available):
                inventory.pick_up("chest")
        if self.locker_spots_available>0:
            for i in range(self.locker_spots_available):
                inventory.pick_up("locker") 

        self.visited = True
        return True

class Blue(Room):
    """Ce sont les pièces les plus communes, avec des effets variés.

    Attributes:
    - rooms : list[str] <<class attribute>>
        Liste de toutes les pièces bleues
    - cost : int
        Coût de la pièce lors du tirage
    - dig_spots_available : int
        Nombre d'endroits où creuser pour la pièce choisie
    - chest_spots_available : bool
        Nombre de coffres pour la pièce choisie
    - locker_spots_available : bool
        Nombre de casiers pour la pièce choisie
    - available_items : dict[str, int]
        Dictionnaire de tous les items se retrouvant dans la pièce
    """
    rooms = ["The Foundation", "Entrance Hall", "Spare Room", "Rotunda", "Parlor", "Billiard Room", "Gallery", "Room 8", "Closet", "Walk-in Closet", "Attic", "Storeroom", "Nook", "Garage", "Music Room", "Locker Room", "Den", "Wine Cellar", "Trophy Room", "Ballroom", "Pantry", "Rumpus Room", "Vault", "Office", "Drawing Room", "Study", "Library", "Chamber of Mirrors", "The Pool", "Drafting Studio", "Utility Closet", "Boiler Room", "Pump Room", "Security", "Workshop", "Laboratory", "Sauna", "Coat Check", "Mail Room", "Freezer", "Dining Room", "Observatory", "Conference Room", "Aquarium", "Antechamber", "Room 46"]

    def __init__(self, name:str):
        super().__init__(name, "blue")
        self.cost = self.gem_cost()
        self.dig_spots_available = self.dig_spots() 
        self.chest_spots_available = self.chest_spots()
        self.locker_spots_available = self.locker_spots()
        self.available_items = self.items() 
        
    def items(self, inventory: Inventory):
        """Indique les items de la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -dict[str, int]
            Renvoie un dictionnaire d'items disponibles dans la pièce
        """
        room_items = {
            "banane": 1, 
            "orange": 1, 
            "pomme" : 1, 
            "gemme" : random.randint(1,3), 
            "pièce": random.randint(1,3), 
            "clé": random.randint(1,3), 
            "dé": random.randint(1,3), 
            "levier cassé":random.randint(1,3),
            "pelle": 1,
            "détecteur de métal": 1,
            "marteau": 1, 
            "patte de lapin": 1
            }
        
        if inventory.shovel:
            room_items["pelle"] = 0
        if inventory.hammer:
            room_items["marteau"] = 0
        if inventory.lockpick_kit:
            room_items["kit de crochetage"] = 0 
        if inventory.rabbit_foot:
            room_items["patte de lapin"] = 0
        if inventory.metal_detector:
            room_items["détecteur de métal"] = 0 

        if self.name == "The Foundation":
            return {}
        elif self.name == "Entrance Hall":
            return {}
        elif self.name == "Spare Room":
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Rotunda":
            return {} 
        elif self.name == "Parlor":
            room_items = {"pomme": 2}
            return room_items
        elif self.name == "Billiard Room":
            room_items["pièce"] =random.choice([1, 5, 6, 10, 11])
            return dict(random.sample(list(room_items.items()), random.randint(1, 2))) 
        elif self.name == "Gallery":
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Room 8":
            return {}
        elif self.name == "Closet":
            return dict(random.sample(list(room_items.items()), 2)) 
        elif self.name == "Walk-in Closet":
            return dict(random.sample(list(room_items.items()), 4))
        elif self.name == "Attic":
            return dict(random.sample(list(room_items.items()), 8))
        elif self.name == "Storeroom":
            room_items = {"clé" : 1, "gemme" : 1, "pièce" : 1}
            return room_items
        elif self.name == "Nook":
            room_items = {"clé" : 1}
            return room_items
        elif self.name == "Garage":
            room_items = {"clé" : 3}
            return room_items
        elif self.name == "Music Room":
            room_items = {"clé" : 1}
            return room_items
        elif self.name == "Locker Room":
            room_items = {"clé" : 1}
            return room_items
        elif self.name == "Den":
            room_items = {"gemme" : 1}
            return room_items
        elif self.name == "Wine Cellar":
            room_items = {"gemme" : 3}
            return room_items
        elif self.name == "Trophy Room":
            room_items = {"gemme" : 8}
            return room_items
        elif self.name == "Ballroom":
            return {}
        elif self.name == "Pantry":
            room_items = {"pièce" : 4, "pomme" : 1, "banane" : 1}
            return room_items
        elif self.name == "Rumpus Room":
            room_items = {"pièce" : 8}
            return room_items
        elif self.name == "Vault":
            room_items = {"pièce" : 40}
            return room_items
        elif self.name == "Office":
            room_items = {"pièce" : 2}
            return room_items
        elif self.name == "Drawing Room":
            room_items = {}
            return {}
        elif self.name == "Study":
            return {}
        elif self.name == "Library":
            return {}
        elif self.name == "Chamber of Mirrors":
            return {}
        elif self.name == "The Pool":
            return {}
        elif self.name == "Drafting Studio":
            return {}
        elif self.name == "Utility Closet":
            return {}
        elif self.name == "Boiler Room":
            return {}
        elif self.name == "Pump Room":
            return {}
        elif self.name == "Security":
            return {}
        elif self.name == "Workshop":
            return dict(random.sample(list(room_items.items()), 1))
        elif self.name == "Security":
            return {}
        elif self.name == "Laboratory":
            return {}
        elif self.name == "Sauna":
            return {}
        elif self.name == "Coat Check":
            return {}
        elif self.name == "Mail Room":
            return {}
        elif self.name == "Freezer":
            return {}
        elif self.name == "Dining Room":
            room_items = {"repas" : 1}
            return room_items
        elif self.name == "Observatory":
            return {}
        elif self.name == "Conference Room":
            return {}
        elif self.name == "Aquarium":
            return {}
        elif self.name == "Antechamber":
            return {}
        elif self.name == "Room 46":
            return {}
    
    def gem_cost(self):
        """Indique le coût pour entrer dans la pièce pièce.
        
        Returns:
        - int
            Renvoie le coût en gemmes de la pièce lors du tirage
        """
        cost = {
            "The Foundation" : 0,
            "Entrance Hall" : 0,
            "Spare Room" : 0, 
            "Rotunda" : 3, 
            "Parlor" : 0, 
            "Billiard Room" : 0, 
            "Gallery" : 0, 
            "Room 8" : 0, 
            "Closet" : 0, 
            "Walk-in Closet" : 1, 
            "Attic" : 3, 
            "Storeroom" : 0, 
            "Nook" : 0, 
            "Garage" : 1, 
            "Music Room" : 2, 
            "Locker Room" : 1, 
            "Den" : 0, 
            "Wine Cellar" : 0, 
            "Trophy Room" : 5, 
            "Ballroom" : 2, 
            "Pantry" : 0, 
            "Rumpus Room" : 1, 
            "Vault" : 3, 
            "Office" : 2, 
            "Drawing Room" : 1, 
            "Study" : 0, 
            "Library" : 0, 
            "Chamber of Mirrors" : 0, 
            "The Pool" : 1, 
            "Drafting Studio" : 2, 
            "Utility Closet" : 0, 
            "Boiler Room" : 1, 
            "Pump Room" : 0, 
            "Security" : 0, 
            "Workshop" : 0, 
            "Laboratory" : 0, 
            "Sauna" : 0, 
            "Coat Check" : 0, 
            "Mail Room" : 0, 
            "Freezer" : 0, 
            "Dining Room" : 0, 
            "Observatory" : 1, 
            "Conference Room" : 0, 
            "Aquarium" : 1, 
            "Antechamber" : 0, 
            "Room 46" : 0
        }

        return cost.get(self.name)

    def dig_spots(self):
        """Indique le nombre d'endroits où creuser dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre d'endroits où creuser dans la pièce
        """
        spots = {
            "The Foundation" : random.randint(2, 5),
            "Entrance Hall" : 0,
            "Spare Room" : 0, 
            "Rotunda" : 0, 
            "Parlor" : 0, 
            "Billiard Room" : 0, 
            "Gallery" : 0, 
            "Room 8" : 0, 
            "Closet" : 0, 
            "Walk-in Closet" : 0, 
            "Attic" : 0, 
            "Storeroom" : 0, 
            "Nook" : 0, 
            "Garage" : 0, 
            "Music Room" : 0, 
            "Locker Room" : 0, 
            "Den" : 0, 
            "Wine Cellar" : 1, 
            "Trophy Room" : 0, 
            "Ballroom" : 0, 
            "Pantry" : 0, 
            "Rumpus Room" : 0, 
            "Vault" : 0, 
            "Office" : 0, 
            "Drawing Room" : 0, 
            "Study" : 0, 
            "Library" : 0, 
            "Chamber of Mirrors" : 0, 
            "The Pool" : 0, 
            "Drafting Studio" : 0, 
            "Utility Closet" : 0, 
            "Boiler Room" : 0, 
            "Pump Room" : 0, 
            "Security" : 0, 
            "Workshop" : 0, 
            "Laboratory" : 0, 
            "Sauna" : 0, 
            "Coat Check" : 0, 
            "Mail Room" : 0, 
            "Freezer" : 0, 
            "Dining Room" : 0, 
            "Observatory" : 0, 
            "Conference Room" : 0, 
            "Aquarium" : 0, 
            "Antechamber" : 0, 
            "Room 46" : 0
        }
        return spots.get(self.name)

    def chest_spots(self):
        """Indique le nombre de coffres dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de coffres disponibles dans la pièce
        """
        spots = {
            "The Foundation" : 0,
            "Entrance Hall" : 0,
            "Spare Room" : 0, 
            "Rotunda" : 0, 
            "Parlor" : 0, 
            "Billiard Room" : 0, 
            "Gallery" : 0, 
            "Room 8" : 0, 
            "Closet" : 0, 
            "Walk-in Closet" : 0, 
            "Attic" : 0, 
            "Storeroom" : 0, 
            "Nook" : 0, 
            "Garage" : 0, 
            "Music Room" : 0, 
            "Locker Room" : 0, 
            "Den" : 0, 
            "Wine Cellar" : 0, 
            "Trophy Room" : 0, 
            "Ballroom" : 0, 
            "Pantry" : 0, 
            "Rumpus Room" : 0, 
            "Vault" : 2, 
            "Office" : 0, 
            "Drawing Room" : 0, 
            "Study" : 0, 
            "Library" : 0, 
            "Chamber of Mirrors" : 0, 
            "The Pool" : 0, 
            "Drafting Studio" : 0, 
            "Utility Closet" : 0, 
            "Boiler Room" : 0, 
            "Pump Room" : 0, 
            "Security" : 0, 
            "Workshop" : 0, 
            "Laboratory" : 0, 
            "Sauna" : 0, 
            "Coat Check" : 0, 
            "Mail Room" : 0, 
            "Freezer" : 0, 
            "Dining Room" : 0, 
            "Observatory" : 0, 
            "Conference Room" : 0, 
            "Aquarium" : 0, 
            "Antechamber" : 0, 
            "Room 46" : 0
        }
        return spots.get(self.name)
    
    def locker_spots(self):
        """Indique le nombre de casiers dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de casiers disponibles dans la pièce
        """
        spots = {
            "The Foundation" : 0,
            "Entrance Hall" : 0,
            "Spare Room" : 0, 
            "Rotunda" : 0, 
            "Parlor" : 0, 
            "Billiard Room" : 0, 
            "Gallery" : 0, 
            "Room 8" : 0, 
            "Closet" : 0, 
            "Walk-in Closet" : 0, 
            "Attic" : 0, 
            "Storeroom" : 0, 
            "Nook" : 0, 
            "Garage" : 0, 
            "Music Room" : 0, 
            "Locker Room" : random.randint(3, 5), 
            "Den" : 0, 
            "Wine Cellar" : 0, 
            "Trophy Room" : 0, 
            "Ballroom" : 0, 
            "Pantry" : 0, 
            "Rumpus Room" : 0, 
            "Vault" : 0, 
            "Office" : 0, 
            "Drawing Room" : 0, 
            "Study" : 0, 
            "Library" : 0, 
            "Chamber of Mirrors" : 0, 
            "The Pool" : 0, 
            "Drafting Studio" : 0, 
            "Utility Closet" : 0, 
            "Boiler Room" : 0, 
            "Pump Room" : 0, 
            "Security" : 0, 
            "Workshop" : 0, 
            "Laboratory" : 0, 
            "Sauna" : 0, 
            "Coat Check" : 0, 
            "Mail Room" : 0, 
            "Freezer" : 0, 
            "Dining Room" : 0, 
            "Observatory" : 0, 
            "Conference Room" : 0, 
            "Aquarium" : 0, 
            "Antechamber" : 0, 
            "Room 46" : 0
        }
        return spots.get(self.name)
    
    def enter_room(self, inventory : Inventory) :
        """Gère les intéractions dans la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur

        Returns:
        - bool
            True si l'entrée est réussi, False sinon
        """

        message = [f"Vous êtes dans {self.name} !"]

        if self.cost > 0 :

            reponse = ''
            while reponse != 'o' and reponse != 'n':
                message.append(f"Coût d'entrée : {self.cost} gemme/s.")
                message.append(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
                reponse = input("Tapez 'o' pour oui et 'n' pour non : ").lower()

            reponse = pygame.event.get()
            if reponse.key == pygame.K_o:
                if inventory.gems < self.cost :
                    message.append(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                    return False
                message.append("Vous avez fait le bon choix !")
            else:    
                message.append("Vous ne souhaitez pas explorer la pièce.")
                return False
            
            inventory.gems -= self.cost
            if inventory.gems < 5 :
                message.append("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
                
        message = [f"Vous êtes dans {self.name} !"]
        if self.name == "Ballroom":
            if inventory.gems > 2 :
                message.append(f"Vos gemmes ont disparu ! \n    - {inventory.gems + 2} gemmes")
                inventory.gems = 2
            else:
                message.append(f"Vous avez maintenant 2 gemmes !")
                inventory.gems = 2

        if self.name == "Pump Room" :
            response = ''
            while reponse != 'o' and reponse != 'n':
                message.append(f"Voulez-vous vider la piscine ?")
                response = input("Tapez 'o' pour oui et 'n' pour non : ").lower()
            if reponse.key == pygame.K_o:
                message.append("Vous avez trouvé 12 pièces.")
            else:
                message.append("Vous préférez laisser la psicine telle qu'elle est.")

        if self.name == "Sauna" :
            extra_steps = 15
            message.append(f"Petit moment de détente ! \n    + {extra_steps} pas")
            inventory.steps += extra_steps

        if self.available_items and not self.visited :
            for item_name, _ in self.available_items.items():
                inventory.pick_up(Objet(item_name))
        
        if self.chest_spots_available>0:
            for i in range(self.chest_spots_available):
                inventory.pick_up("chest")
        if self.locker_spots_available>0:
            for i in range(self.locker_spots_available):
                inventory.pick_up("locker") 

        self.visited = True
        return True

class Purple(Room):
    """Ce sont des chambres, qui ont souvent des effets permettant de regagner des pas.
    
    Attributes:
    - rooms : list[str] <<class attribute>>
        Liste de toutes les pièces violettes
    - cost : int
        Coût de la pièce lors du tirage
    - dig_spots_available : int
        Nombre d'endroits où creuser pour la pièce choisie
    - chest_spots_available : int
        Nombre de coffres pour la pièce choisie
    - locker_spots_available : int
        Nombre de casiers pour la pièce choisie
    - available_items : dict[str, int]
        Dictionnaire de tous les items se retrouvant dans la pièce
    """

    rooms = ["Bedroom", "Boudoir", "Guest Bedroom", "Nursery", "Servant's Quarters", "Bunk Room", "Her Ladyship's Chamber", "Master Bedroom"] 
    
    def __init__(self, name:str):
        super().__init__(name, "purple")
        self.cost = self.gem_cost()
        self.dig_spots_available = self.dig_spots()
        self.chest_spots_available = self.dig_spots()
        self.locker_spots_available = self.dig_spots()
        self.available_items = self.items()
        
    def items(self, inventory: Inventory):
        """Indique les items de la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -dict[str, int]
            Renvoie un dictionnaire d'items disponibles dans la pièce
        """
        room_items = {
            "banane": 1, 
            "orange": 1, 
            "pomme" : 1, 
            "gemme" : random.randint(1,3), 
            "pièce": random.randint(1,3), 
            "clé": random.randint(1,3), 
            "dé": random.randint(1,3), 
            "levier cassé":random.randint(1,3),
            "pelle": 1,
            "détecteur de métal": 1,
            "marteau": 1, 
            "patte de lapin": 1
            }
        
        if inventory.shovel:
            room_items["pelle"] = 0
        if inventory.hammer:
            room_items["marteau"] = 0
        if inventory.lockpick_kit:
            room_items["kit de crochetage"] = 0 
        if inventory.rabbit_foot:
            room_items["patte de lapin"] = 0
        if inventory.metal_detector:
            room_items["détecteur de métal"] = 0 

        if self.name == "Bedroom":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Boudoir":
            room_items["pièce"] = random.choice([2, 3, 5])
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Guest Bedroom":
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Nursery":
            return dict(random.sample(list(room_items.items()), 2)) 
        elif self.name == "Servant's Quarters":
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Bunk Room":
            return dict(random.sample(list(room_items.items()), random.randint(1, 2))) 
        elif self.name == "Her Ladyship's Chamber":
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Master Bedroom":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 

    def gem_cost(self):
        """Indique le coût pour entrer dans la pièce pièce.
        
        Returns:
        - int
            Renvoie le coût en gemmes de la pièce lors du tirage
        """
        cost = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 1,
            "Servant's Quarters": 1,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Master Bedroom": 2
            }
        
        return cost.get(self.name)

    def dig_spots(self):
        """Indique le nombre d'endroits où creuser dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre d'endroits où creuser dans la pièce
        """
        spots = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 0,
            "Servant's Quarters": 0,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Master Bedroom": 0
            }
        
        return spots.get(self.name)

    def chest_spots(self):
        """Indique le nombre de coffres dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de coffres disponibles dans la pièce
        """
        spots = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 0,
            "Servant's Quarters": 0,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Master Bedroom": 0
            }
        
        return spots.get(self.name)
    
    def locker_spots(self):
        """Indique le nombre de casiers dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de casiers disponibles dans la pièce
        """
        spots = {
            "Bedroom": 0,
            "Boudoir": 0,
            "Guest Bedroom": 0,
            "Nursery": 0,
            "Servant's Quarters": 0,
            "Bunk Room": 0,
            "Her Ladyship's Chamber": 0,
            "Master Bedroom": 0
            }
            
        return spots.get(self.name)
    
    def enter_room(self, inventory : Inventory) :
        """Gère les intéractions dans la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
            
        Returns:
        - bool
            True si l'entrée est réussi, False sinon
        """

        message = [f"Vous êtes dans {self.name} !"]

        if self.cost>0 :
            reponse = ''
            while reponse != 'o' and reponse != 'n':
                message.append(f"Coût d'entrée : {self.cost} gemme/s.")
                message.append(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
                reponse = input("Tapez 'o' pour oui et 'n' pour non : ").lower()

            reponse = pygame.event.get()
            if reponse.key == pygame.K_o:
                if inventory.gems < self.cost :
                    message.append(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                    return False
                message.append("Vous avez fait le bon choix !")
            else:    
                message.append("Vous ne souhaitez pas explorer la pièce.")
                return False

            if inventory.gems < self.cost :
                message.append(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                return False
            
            inventory.gems -= self.cost
            if inventory.gems < 5 :
                message.append("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
        
        message = [f"Vous êtes dans {self.name} !"]

        if self.name == "Bedroom":
            extra_steps = 2
            message.append(f"Vois avez très bien dormi ! \n     + {extra_steps} pas")
            inventory.steps += 2

        if self.name == "Boudoir" :
            extra_steps = random.randint(0, 4)
            message.append(f"Vois avez très bien dormi ! \n     + {extra_steps} pas")
            inventory.steps += extra_steps

        if self.name == "Guest Bedroom" and not self.visited:
            extra_steps = 10
            message.append(f"Vois avez très bien dormi ! \n     + {extra_steps} pas")
            inventory.steps += extra_steps

        if self.name == "Servant's Quarters" and not self.visited:
            message.append(f"Vous voyez 3 clés sur le lit.\n    + 3 clés")
            inventory.keys +=3

        message = [f"Vous êtes dans {self.name} !"]

        if self.available_items and not self.visited :
            if self.name == "Bedroom" :
                message.append(random.choice(["Vous trouvez dans l'armoire :", "Vous trouvez sur la statue :"]))
            if self.name == "Boudoir" or self.name == "Guest Bedroom" or self.name == "Nursery" or self.name == "Master Bedroom":
                message.append("Vous trouvez sur la table :")
            if self.name == "Servant's Quarters" :
                message.append(random.choice(["Vous trouvez sur le lit :", "Vous trouvez sur la planche à repasser :"]))
            if self.name == "Her Ladyship's Chamber" :
                message.append(random.choice(["Vous trouvez sur la table :", "Vous trouvez sur la chaisse :"]))
            
            for item_name, _ in self.available_items.items():
                inventory.pick_up(Objet(item_name))

        if self.chest_spots_available>0:
            for i in range(self.chest_spots_available):
                inventory.pick_up("chest")
        if self.locker_spots_available>0:
            for i in range(self.locker_spots_available):
                inventory.pick_up("locker") 
                
        self.visited = True
        return True

class Red(Room):
    """Ce sont des pièces qui ont souvent des caractéristiques ou des effets les rendant indésirables (peu de portes, retirent des pas, etc.).
    
    Attributes:
    - rooms : list[str] <<class attribute>>
        Liste de toutes les pièces rouges
    - cost : int
        Coût de la pièce lors du tirage
    - dig_spots_available : int
        Nombre d'endroits où creuser pour la pièce choisie
    - chest_spots_available : int
        Nombre de coffres pour la pièce choisie
    - locker_spots_available : int
        Nombre de casiers pour la pièce choisie
    - available_items : dict[str, int]
        Dictionnaire de tous les items se retrouvant dans la pièce
    """

    rooms = ["Lavatory", "Chapel", "Maid's Chamber", "Archives", "Gymnasium", "Darkroom", "Weight Room", "Furnace"] 
    
    def __init__(self, name:str):
        super().__init__(name, "red")
        self.cost = self.gem_cost()
        self.dig_spots_available = self.dig_spots()
        self.chest_spots_available = self.chest_spots()
        self.locker_spots_available = self.locker_spots()
        self.available_items = self.items() 

    def items(self, inventory : Inventory):
        """Indique les items de la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -dict[str, int]
            Renvoie un dictionnaire d'items disponibles dans la pièce
        """

        room_items = {
            "banane": 1, 
            "orange": 1, 
            "pomme" : 1, 
            "gemme" : random.randint(1,3), 
            "pièce": random.randint(1,3), 
            "clé": random.randint(1,3), 
            "dé": random.randint(1,3), 
            "levier cassé":random.randint(1,3),
            "pelle": 1,
            "détecteur de métal": 1,
            "marteau": 1, 
            "patte de lapin": 1
            }
        
        if inventory.shovel:
            room_items["pelle"] = 0
        if inventory.hammer:
            room_items["marteau"] = 0
        if inventory.lockpick_kit:
            room_items["kit de crochetage"] = 0 
        if inventory.rabbit_foot:
            room_items["patte de lapin"] = 0
        if inventory.metal_detector:
            room_items["détecteur de métal"] = 0 

        if self.name == "Lavatory":
            return {}
        elif self.name == "Chapel":
            room_items["pièce"] = random.choice([2, 3, 4, 5, 12, 14])
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Maid's Chamber":
            return {}
        elif self.name == "Archives":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Gymnasium":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Darkroom":
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Weight Room":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Furnace":
            return {} 

    def gem_cost(self):
        """Indique le coût pour entrer dans la pièce pièce.
        
        Returns:
        - int
            Renvoie le coût en gemmes de la pièce lors du tirage
        """
        spots = {
            "Lavatory" : 0, 
            "Chapel" : 0, 
            "Maid's Chamber" : 0, 
            "Archives" : 0, 
            "Gymnasium" : 0, 
            "Darkroom" : 0, 
            "Weight Room" : 0, 
            "Furnace" : 0
            }
        
        return spots.get(self.name)
        
    def dig_spots(self):
        """Indique le nombre d'endroits où creuser dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre d'endroits où creuser dans la pièce
        """
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

    def chest_spots(self):
        """Indique le nombre de coffres dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de coffres disponibles dans la pièce
        """
        spots = {
            "Lavatory" : 0, 
            "Chapel" : 0, 
            "Maid's Chamber" : 0, 
            "Archives" : 0, 
            "Gymnasium" : 0, 
            "Darkroom" : 0, 
            "Weight Room" : 0, 
            "Furnace" : 0
            }
        
        return spots.get(self.name) 
    
    def locker_spots(self):
        """Indique le nombre de casiers dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de casiers disponibles dans la pièce
        """
        spots = {
            "Lavatory" : 0, 
            "Chapel" : 0, 
            "Maid's Chamber" : 0, 
            "Archives" : 0, 
            "Gymnasium" : 0, 
            "Darkroom" : 0, 
            "Weight Room" : 0, 
            "Furnace" : 0
            }
        
        return spots.get(self.name) 
       
    def enter_room(self, inventory : Inventory) :
        """Gère les intéractions dans la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
            
        Returns:
        - bool
            True si l'entrée est réussi, False sinon
        """

        message = [f"Vous êtes dans {self.name} !"]

        if self.name == "Weight Room":
            message.append(f"Soulever des poids vous fatigue beaucoup ! Vous perdez {inventory.steps//2} pas. Reposez-vous, avant de continuer.")
            inventory.steps = inventory.steps//2
            message.append(f"Pas restants : {inventory.steps}")
        
        if self.name == "Maid's Chamber":
            message.append(f"En faisant le ménage vous avez perdu : \n    - 2 pas\n    - 1 clé\n    - 1 gemme\n    - 1 pièce")
            inventory.steps -= 2
            inventory.coins -= 1
            inventory.gems -= 1

        if self.name == "Gymnasium" :
            message.append(f"Après un long entraînement, vous êtes épuisés ! Vous perdez {inventory.steps - 2} pas. Reposez-vous, avant de continuer.")
            inventory.steps -= 2

        if self.name == "Chapel" :
            message.append(f"Vous faites une donation de 1 pièce. L'église vous remercie !")
            if inventory.coins >= 1:
                inventory.coins -= 1
            else :
                message.append("Vous n'avez pas assez de pièces pour faire une donation :(")

        if self.available_items and not self.visited :
            if self.name == "Chapel" :
                message.append("Vous trouvez sur les chandeliers :")
            if self.name == "Archives" :
                message.append("Vous fouillez les archives et trouvez :")
            if self.name == "Gymnasium" :
                message.append("Vous trouvez sur le banc :")
            if self.name == "Darkroom" :
                message.append("Vous ne voyez rien, vous ne pouvez pas explorer la pièce dans l'obscurité.")
                message.append("Voulez vous allumer la lumière ?")
                reponse = ''
                while reponse != 'o' and reponse != 'n':
                    reponse = input("Tapez 'o' pour oui et 'n' pour non : ").lower()
                
                reponse = pygame.event.get()
                if reponse.key == pygame.K_o:
                    message.append("La lumière est allumée ! Vous trouvez :")
                else:
                    message.append("Vous ne voyez rien, donc vous ne pouvez pas explorer la pièce.")
                    return False
            if self.name == "Weight Room" :
                message.append("Vous trouvez à côté des poids :")
            if self.name == "Furnace" :
                message.append("La chaleur est intense, vous voulez partir. Mais, au moins vous avez trouvé quelques items :")
            for item_name, _ in self.available_items.items():
                inventory.pick_up(Objet(item_name))
        
        if self.chest_spots_available>0:
            for i in range(self.chest_spots_available):
                inventory.pick_up("chest")
        if self.locker_spots_available>0:
            for i in range(self.locker_spots_available):
                inventory.pick_up("locker")   
                     
        self.visited = True
        return True
    
class Green(Room):
    """Ce sont des jardins d'intérieur, qui contiennent souvent des gemmes, des endroits où creuser, et des objets permanents.

    Attributes:
    - rooms : list[str] <<class attribute>>
        Liste de toutes les pièces vertes
    - cost : int
        Coût de la pièce lors du tirage
    - dig_spots_available : int
        Nombre d'endroits où creuser pour la pièce choisie
    - chest_spots_available : int
        Nombre de coffres pour la pièce choisie
    - locker_spots_available : int
        Nombre de casiers pour la pièce choisie
    - available_items : dict[str, int]
        Dictionnaire de tous les items se retrouvant dans la pièce
    - bonus : int
        Nombre de gemmes bonus de la pièce 
    
    """
    
    rooms = ["Terrace", "Patio", "Courtyard", "Cloister", "Veranda", "Greenhouse", "Morning Room", "Secret Garden"]

    def __init__(self, name:str):
        super().__init__(name, "green")
        self.cost = self.gem_cost() 
        self.dig_spots_available = self.dig_spots() 
        self.chest_spots_available = self.chest_spots()
        self.locker_spots_available = self.locker_spots()
        self.available_items = self.items() 
        self.bonus = self.gem_bonus() 
        
    def items(self, inventory : Inventory):
        """Indique les items de la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
        
        Returns:
        -dict[str, int]
            Renvoie un dictionnaire d'items disponibles dans la pièce
        """

        room_items = {
            "banane": 1, 
            "orange": 1, 
            "pomme" : 1, 
            "gemme" : random.randint(1,3), 
            "pièce": random.randint(1,3), 
            "clé": random.randint(1,3), 
            "dé": random.randint(1,3), 
            "levier cassé":random.randint(1,3),
            "pelle": 1,
            "détecteur de métal": 1,
            "marteau": 1, 
            "patte de lapin": 1
            }
        
        if inventory.shovel:
            room_items["pelle"] = 0
        if inventory.hammer:
            room_items["marteau"] = 0
        if inventory.lockpick_kit:
            room_items["kit de crochetage"] = 0 
        if inventory.rabbit_foot:
            room_items["patte de lapin"] = 0
        if inventory.metal_detector:
            room_items["détecteur de métal"] = 0   
            
        if self.name == "Terrace":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Patio":
            return dict(random.sample(list(room_items.items()), random.randint(1,3))) 
        elif self.name == "Courtyard":
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Cloister":
            return room_items
        elif self.name == "Veranda":
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Greenhouse":
            return dict(random.sample(list(room_items.items()), 1)) 
        elif self.name == "Morning Room":
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 
        elif self.name == "Secret Garden":
            return dict(random.sample(list(room_items.items()), random.randint(1,2))) 

    def gem_cost(self):
        """Indique le coût pour entrer dans la pièce pièce.
        
        Returns:
        - int
            Renvoie le coût en gemmes de la pièce lors du tirage
        """

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
    
    def dig_spots(self):
        """Indique le nombre d'endroits où creuser dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre d'endroits où creuser dans la pièce
        """

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
    
    def chest_spots(self):
        """Indique le nombre de coffres dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de coffres disponibles dans la pièce
        """

        spots = {
            "Terrace": 0,
            "Patio": 0,
            "Courtyard": 0,
            "Cloister": 0,
            "Veranda": 0,
            "Greenhouse": 0,
            "Morning Room": 0,
            "Secret Garden": 0
            }
        
        return spots.get(self.name)
    
    def locker_spots(self):
        """Indique le nombre de casiers dans la pièce.
        
        Returns:
        -int
            Renvoie le nombre de casiers disponibles dans la pièce
        """

        spots = {
            "Terrace": 0,
            "Patio": 0,
            "Courtyard": 0,
            "Cloister": 0,
            "Veranda": 0,
            "Greenhouse": 0,
            "Morning Room": 0,
            "Secret Garden": 0
            }
        
        return spots.get(self.name)

    def gem_bonus(self):
        """Indique si la pièce apporte des gemmes bonus ou pas, et la quantité.
        
        Returns:
        -int
            Renvoie le bonus en gemmes de la pièce
        """

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
        """Gère les intéractions dans la pièce.
        
        Parameters:
        - inventory : Inventory
            L'inventaire du joueur
            
        Returns:
        - bool
            True si l'entrée est réussi, False sinon
        """

        message = [f"Vous êtes dans la pièce {self.name}."]

        if self.cost > 0 :
            
            reponse = ''
            while reponse != 'o' and reponse != 'n':
                message.append(f"Coût d'entrée : {self.cost} gemme/s.")
                message.append(f"Souhaitez-vous dépenser {self.cost} gemme/s ?")
                reponse = input("Tapez 'o' pour oui et 'n' pour non : ").lower()

            reponse = pygame.event.get()
            if reponse.key == pygame.K_o:
                if inventory.gems < self.cost :
                    message.append(f"Vous n'avez pas assez de gemmes. Vous êtes en manque de {self.cost - inventory.gems} gemme/s.")
                    return False
                message.append("Vous avez fait le bon choix !")
            else:    
                message.append("Vous ne souhaitez pas explorer la pièce.")
                return False
            
            
            inventory.gems -= self.cost
            if inventory.gems < 5 :
                message.append("Économisez bien vos gemmes ! Vous n'en avez à peine :(")
        
        message = [f"Vous êtes dans la pièce {self.name}."]

        has_bonus, bonus_amount = self.bonus
        if has_bonus and bonus_amount > 0:
            message.append(f"Bonus ! \n    + {bonus_amount} gemme(s)")
            inventory.gems += bonus_amount

        if self.available_items and not self.visited:
            message.append("Objets découverts :")
            for item_name, _ in self.available_items.items():
                inventory.pick_up(Objet(item_name))
                
        if self.chest_spots_available>0:
            for i in range(self.chest_spots_available):
                inventory.pick_up("chest")
        if self.locker_spots_available>0:
            for i in range(self.locker_spots_available):
                inventory.pick_up("locker") 
                
        self.visited = True
        return True
