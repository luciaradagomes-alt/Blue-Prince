#%%
from inventory import Inventory
from objet import Objet
from abc import ABC, abstractmethod
import random

class Room :
    """Classe qui définit les pièces du jeu."""
    

    def __init__(self, name : str, color : str):
        self.name = name
        self.color = color
        self.visited = False # False si la pièce n'a pas encore été visité, True sinon
        self.doors = [] # Liste des pièces qui peuvent être accédées à travers la pièce actuelle
    
    @abstractmethod
    def enter_room(self, inventory : Inventory):
        """Ajoute des effets lorsque le joueur rentre dans la pièce"""
        pass
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
        for (item, price) in enumerate(items_list):
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

# %%
