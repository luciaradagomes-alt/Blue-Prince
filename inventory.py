import pygame
from objet import Objet
import text

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
    
    pygame.font.init()
    my_font = text.inventory_font

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
        """ Permet d'afficher l'inventaire du joueur sur l'interface graphique
        """
        inventaire = pygame.Surface((500,400))
        inventaire.fill((14, 27, 49))
        afficher = ["----------------------------------------------------------------------",
                    "Inventaire","------------------",
                    f"Pas : {self.steps}", f"Pièces : {self.coins}", f"Gemmes : {self.gems}",f"Clés : {self.keys}",f"Dés : {self.dice}",""]
        if self.shovel:
            afficher.append("- Pelle")
        if self.hammer:
            afficher.append("- Marteau")
        if self.lockpick_kit:
            afficher.append("- Kit de crochetage")
        if self.rabbit_foot:
            afficher.append("- Patte de lapin")
        if self.metal_detector:
            afficher.append("- Détecteur de métaux")
        afficher.append(f"----------------------------------------------------------------------")
        
        text.texte(afficher,inventaire,x=10,y=10,color="white",font=self.my_font)
        
        return inventaire

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
        