class Objet:
    def __init__(self,name,food,steps,locker,chest,price):
        self.name = name
        self.food = food
        self.steps = steps
        self.locker = locker
        self.chest = chest
        self.price = price

class Inventory:
    
    def __init__(self):
        self.steps = 70
        self.coins = 0
        self.gems = 2 
        self.keys = 0
        self.dice = 0
        self.shovel = False
        self.hammer = False
        self.lockpick_kit = False
        self.rabbit_foot = False
        self.metal_detector = False

    def show_inventory(self):
    # une fonction pour afficher l'inventaire sur l'interface graphique, à faire avec pygame
    # nécessitera d'images pour les coins, steps, dice, keys
    # pour l'instant je vais juste print les valeurs sur la console
        print(f"----------------------------------------------------------------------")
        print(f"Inventaire")
        print(f"------------------")
        print(f"Pas : {self.steps}")
        print(f"Pièces : {self.coins}")
        print(f"Gemmes : {self.gems}")
        print(f"Clés : {self.keys}")
        print(f"Dés : {self.dice}")
        if self.shovel:
            print("- Pelle")
        if self.hammer:
            print("- Marteau")
        if self.lockpick_kit:
            print("- Kit de crochetage")
        if self.rabbit_foot:
            print("- Patte de lapin")
        if self.metal_detector:
            print("- Décteteur de métaux")

    def move(self):
        self.steps -= 1
    
    def pick_up(self,object,nb=1):
        if type(object) != Objet:
            raise TypeError("Ce n'est pas un objet")
        
        if object.food:
            self.steps += nb*object.steps

        if object.name == 'coin':
            self.coins += nb

        if object.name == 'gem':
            self.gems += nb

        if object.name == 'key':
            self.keys += nb

        if object.locker:
            if self.keys > 0:
                # demander à l'utilisateur s'il veut ouvrir le locker
                reponse = True # définir en fonction de la réponse de l'utilsateur
                if reponse:
                    self.keys -= 1
                    # ajouter les objets qu'on aura trouvés
                
        if object.chest:
            if self.keys > 0 or self.hammer:
                # demander à l'utilisateur s'il veut ouvrir le coffre
                # ajouter les objets qu'on aura trouvés
                if not self.hammer:
                    self.keys -= 1

    def buy(self,object):
        if type(object) != Objet:
            raise TypeError("Ce n'est pas un objet")
        
        if self.coins < object.price:
            return ("Vous n'avez pas assez de pièces !")
        
        self.coins -= object.price
        # ajouter les objets qu'on aura trouvés
        if object.name == 'shovel':
            self.shovel = True

        if object.food:
            self.steps += object.steps
        

# les objets: chaînes de caractère avec un compteur, à tester pour chaque action? ou autre fonctionnement dans la classe? 


#tests
pomme = Objet('pomme',True,2,False,False,5)

inventory = Inventory()

inventory.pick_up(pomme)

inventory.show_inventory()

for i in range(10):
    inventory.move()

inventory.show_inventory()

inventory.pick_up(Objet('coin',False,0,False,False,0),5)

inventory.show_inventory()

inventory.buy(pomme)

inventory.show_inventory()

