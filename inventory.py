import pygame
from objet import Objet
import text
from colorpalette import couleurs

class Inventory:
    """ Classe qui contient les objets dans l'inventaire du joueur.

    Attributes:
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
    symboles = {"step":pygame.image.load("images\\Steps_icon.webp"),
                "key":pygame.image.load("images\\key.png"),
                "coin":pygame.image.load("images\\gold.png"),
                "gem":pygame.image.load("images\\gem.webp"),
                "die":pygame.image.load("images\\ivory_dice.png")}
    for obj in symboles.keys():
        symboles[obj] = pygame.transform.scale(symboles[obj], (18,18))

    def __init__(self):
        self.steps = 70
        self.coins = 0
        self.gems = 10 
        self.keys = 10
        self.dice = 0
        self.shovel = False
        self.hammer = False
        self.lockpick_kit = False
        self.rabbit_foot = False
        self.metal_detector = False

    def show_inventory(self,screen):
        """ Permet d'afficher l'inventaire du joueur sur l'interface graphique.

        Parameters:
        - screen : Surface
            La surface sur laquelle on affiche l'inventaire (écran du jeu)
        """
        
        width = screen.get_width() - 640
        height = screen.get_height()//2 - 60
        inventaire = pygame.Surface((width,height))
        inventaire.fill(couleurs["darkblue"])
        pygame.draw.rect(inventaire,couleurs['green'],pygame.Rect(0,0,width,height),width=15)
        
        afficher = ["Inventaire","----------------------------------------------------------",
                    f"   Pas : {self.steps}", f"   Clés : {self.keys}", f"   Pièces : {self.coins}", f"   Gemmes : {self.gems}", f"   Dés : {self.dice}",""]
        if self.shovel:
            afficher.append(" - Pelle")
        if self.hammer:
            afficher.append(" - Marteau")
        if self.lockpick_kit:
            afficher.append(" - Kit de crochetage")
        if self.rabbit_foot:
            afficher.append(" - Patte de lapin")
        if self.metal_detector:
            afficher.append(" - Détecteur de métaux")
        
        text.texte(afficher,inventaire,x=30,y=30,color="white",font=self.my_font,modifiers={0:'bold'})
        
        i = 0
        for s in self.symboles.values():
            inventaire.blit(s,(34,68+i*19))
            i += 1

        return inventaire

    def move(self):
        self.steps -= 1
    
    def pick_up(self,object,screen,nb=1):
        """ Définit les actions réalisées lorsqu'on ramasse un objet dans le manoir.

        Parameters:
        - object : Objet
            L'objet qui est recueilli
        - nb : int (optional)
            Le nombre d'objets (1 par défaut)

        Raises:
        - TypeError: Si l'argument n'est pas un objet
        """

        if type(object) != Objet:
            raise TypeError("Ce n'est pas un objet")
        
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
            message = [f"Ceci est un {object.name}."]
            if self.keys > 0:
                reponse = ''
                while reponse != 'o' and reponse != 'n':
                    message.append("Voulez-vous l'ouvrir ?")
                    if object.locker or not self.hammer:
                        message.append("Cela coûtera 1 clé.")
                        text.afficher_message(message,screen)
                    reponse = input("Tapez 'o' pour oui et 'n' pour non : ")
                
                reponse = pygame.event.get()
                if reponse.key == pygame.K_o:
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

    def buy(self,room):
        """ Permet au joueur d'acheter un objet, sous condition qu'il ait assez de pièces.

        Parameters:
        - room : Room
            Salle dans laquelle on cherche à acheter l'objet

        Raises:
        - TypeError : si on ne se trouve pas dans un marché (salle jaune) 
        """
        
        if self.coins < object.price:
            return ("Vous n'avez pas assez de pièces !")
        
        self.coins -= object.price
        # ajouter les objets qu'on aura trouvés
        if object.name == 'pelle':
            self.shovel = True

        if object.food:
            self.steps += object.steps
    
    def open_door(self,niveau):
        """ Permet au joueur d'ouvrir une porte.

        Parameters:
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
        