from objet import Objet

class Inventory:
    """ Classe qui contient les objets dans l'inventaire du joueur.

    Attributes:
    ---------------
    - steps : int
        Le nombre de pas restants au joueur
    - coins : int
        Le nombre de pièces d'or que possède le joueur, utilisées pour acheter des produits 
    - gems : int
        Le nombre de gemmes que possède le joueur, utilisées pour choisir des salles lors du tirage au sort
    - keys : int
        Le nombre de clés que possède le joueur, utilisées pour ouvrir des pièces, des coffres ou des casiers
    - dice : int
        Le nombre de dés que possède le joueur, utilisés pour tirer à nouveau les pièces proposées
    - shovel : bool
        Indique si le joueur possède une pelle, utilisé pour creuser à certains endroits
    - hammer : bool
        Indique si le joueur possède un marteau, utilisé pour briser le cadenas des coffres
    - lockpit_kit : bool
        Indique si le joueur possède un kit de crochetage, utilisé pour ouvrir certaines portes sans dépenser de clé
    - rabbit_foot : bool
        Indique si le joueur possède un pied de lapin, qui augmente la chance de trouver des objets dans le manoir
    - metal_detector : bool
        Indique si le joueur possède un détecteur de métal, qui augmente la chance de trouver des clés ou des pièces d'or dans le manoir
    """
    
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
        """ Permet d'afficher l'inventaire du joueur
        """
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
        print()
        if self.shovel:
            print("- Pelle")
        if self.hammer:
            print("- Marteau")
        if self.lockpick_kit:
            print("- Kit de crochetage")
        if self.rabbit_foot:
            print("- Patte de lapin")
        if self.metal_detector:
            print("- Détecteur de métaux")
        print(f"----------------------------------------------------------------------")

    def move(self):
        self.steps -= 1
    
    def pick_up(self,object,nb=1):
        """ Définit les actions réalisées lorsqu'on ramasse un objet dans le manoir

        Parameters:
        ---------------
        - object : Objet
            L'objet qui est recueilli
        - nb : int (optional)
            Le nombre d'objets (1 par défaut)

        Raises:
        ---------------
            TypeError: Si l'argument n'est pas un objet
        """
        if type(object) != Objet:
            raise TypeError("Ce n'est pas un objet")
        
        print(f"-> Trouvé: {nb} {object}", end='')
        if nb != 1:
            print("s")
        else: print()

        if object.food:
            self.steps += nb*object.steps

        if object.stackable:
            if object.name == 'pièce':
                self.coins += nb

            if object.name == 'gemme':
                self.gems += nb

            if object.name == 'clé':
                self.keys += nb
            
            if object.name == 'dé':
                self.dice += nb

        if object.locker or object.chest:
            print(f"Ceci est un {object.name}.", end =' ')
            if self.keys > 0:
                reponse = ''
                while reponse != 'o' and reponse != 'n':
                    print("Voulez-vous l'ouvrir ?", end=" ")
                    if object.locker or not self.hammer:
                        print("Cela coûtera 1 clé.")
                    else:
                        print()
                    reponse = input("Tapez 'o' pour oui et 'n' pour non : ")
                reponse = (reponse == 'o') 
                if reponse:
                    if object.locker or not self.hammer:
                        self.keys -= 1
                    print("Ouvert")
                    vide = True
                    for obj in object.objects.items():
                        if obj[1] > 0:
                            vide = False
                            self.pick_up(Objet(obj[0]),obj[1])
                    if vide:
                        print("... mais c'était vide :(")
            else:
                print("Vous n'avez pas de clés pour l'ouvrir.")
                
        if object.dig_spot:
            print("Ceci est un endroit creusable.", end=" ")
            if self.shovel:
                print("Voulez-vous le creuser ?")
                reponse = ''
                while reponse != 'o' and reponse != 'n':
                    reponse = input("Tapez 'o' pour oui et 'n' pour non : ")
                reponse = (reponse == 'o')
                if reponse:
                    print("Creusé")
                    vide = True
                    for obj in object.objects.items():
                        if obj[1] > 0:
                            vide = False
                            self.pick_up(Objet(obj[0]),obj[1])
                    if vide:
                        print("... mais c'était vide :(")
            else:
                print("Vous n'avez pas de pelle pour le creuser.")

        # Objets spéciaux:

        if object.name == "pelle":
            self.shovel = True

        if object.name == "patte de lapin":
            self.rabbit_foot = True

        if object.name == "marteau":
            self.hammer = True

        if object.name == "kit de crochetage":
            self.lockpick_kit = True
        
        if object.name == "détecteur de métal":
            self.metal_detector = True

    def buy(self,object):
        if type(object) != Objet:
            raise TypeError("Ce n'est pas un objet")
        
        if self.coins < object.price:
            return ("Vous n'avez pas assez de pièces !")
        
        self.coins -= object.price
        # ajouter les objets qu'on aura trouvés
        if object.name == 'pelle':
            self.shovel = True

        if object.food:
            self.steps += object.steps
    
    def open_door(self,niveau):
        """ Permet au joueur d'ouvrir une porte

        Parameters:
        ---------------
        - niveau : int
            Indique combien de clés le joueur devra dépenser pour ouvrir cette porte
        """
        print(f"La porte est vérouillée à clé. Voulez-vous l'ouvrir? Cela coûtera {niveau} clé", end='')
        if niveau != 1:
            print("s.")
        print(".")
        while reponse != 'o' and reponse != 'n':
            reponse = input("Tapez 'o' pour oui et 'n' pour non : ")
        reponse = (reponse == 'o')
        if reponse:
            self.keys -= niveau
        
#tests
#pomme = Objet('pomme')

inventory = Inventory()

#inventory.show_inventory()

#inventory.pick_up(pomme)

#inventory.show_inventory()

cle = Objet("clé")

inventory.pick_up(cle,4)

casier = Objet("casier")

inventory.pick_up(casier)

inventory.show_inventory()

coffre = Objet("coffre")
inventory.pick_up(Objet("marteau"))
inventory.pick_up(coffre)

inventory.show_inventory()

creuse = Objet("endroit creusable")

inventory.pick_up(creuse)

inventory.show_inventory()

pelle = Objet("pelle")
inventory.pick_up(pelle)
inventory.pick_up(creuse)

inventory.show_inventory()