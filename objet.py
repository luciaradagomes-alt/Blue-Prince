import random

class Objet:
    """ Classe qui définit la nature des objets contenus dans le jeu

    Attributes:
    ---------------
    - possible : list[str] <<class attribute>>
        Liste de tous les objets dans notre jeu
    - name : str
        Nom de l'objet, parmi les possibilités dans la Liste possible
    - food : bool
        Détermine si l'objet est de la nourriture
    - locker : bool
        Détermine si l'objet est un casier
    - chest : bool
        Détermine si l'objet est un coffre
    - dig_spot : bool
        Détermine si l'endroit est un endroit creusable
    - stackable : bool
        Détermine si l'objet est stackable (pièces d'or, gemmes, clés et dés)
    """

    possible = ["pomme","banane","gâteau","repas","sandwich", "bacon et oeufs", "salade", "soupe", 
                "pièce", "gemme", "clé", "dé",
                "coffre", "casier", "endroit creusable",
                "pelle", "marteau", "patte de lapin", "kit de crochetage", "détecteur de métal", "levier cassé",
                "loupe", "salière", "compas", "masque pour dormir", "coin purse"]

    def __init__(self, name):
        self.name = name
        self.food = False
        self.locker = False
        self.chest = False
        self.dig_spot = False
        self.stackable = False

        self.steps = 0
        self.objects = None

        self.is_food()
        self.is_stackable()
        self.is_locker()
        self.is_chest()
        self.is_dig_spot()

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,name):
        if name not in Objet.possible:
            raise ValueError("Ce n'est pas un objet")
        self.__name = name

    def is_stackable(self):
        stackable_objects = ["pièce", "gemme", "clé", "dé"]
        if self.name in stackable_objects:
            self.stackable = True

    def is_food(self):
        food = {"pomme" : 2, "banane" : 3, "salade" : 5, "soupe" : 5, "gâteau" : 10, "sandwich" : 15, "bacon et oeufs" : 15, "repas" : 25}
        if self.name in food:
            self.food = True
            self.steps = food[self.name]

    def is_locker(self):
        proba = random.randint(1, 100)

        if self.name == "casier":
            self.locker = True
            self.required_tool = "clé"   # L'outil nécessaire pour ouvrir le locker
            if proba <= 50:             
                self.objects = {}

            elif proba <= 80 :
                self.objects = {"gemme" : 0, "pièce" :  0}  
                for i in range(1, 4):
                    valeur = random.randint(1,len(self.objects))
                    if valeur == 1:
                        self.objects["gemme"] += 1
                    else:
                        self.objects["pièce"] += random.randint(1, 5)  
                
            else :
                self.objects = {"pomme" : 0, "clé" : 0, "gemme": 0, "pièce" : 0}

                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))

                    if valeur == 1:
                        self.objects["pomme"] += 1
                    elif valeur == 2:
                        self.objects["clé"] += 1
                    elif valeur == 3:
                        self.objects["gemme"] += 1
                    else:
                        self.objects["pièce"] += random.randint(1, 5)   
            
    def is_chest(self):
        proba = random.randint(1, 100)

        if self.name == "coffre":
            self.chest = True
            self.required_tool = "clé"   # L'outil nécessaire pour ouvrir le coffre
            if proba <= 50:             
                self.objects = {}

            elif proba <= 80 :
                self.objects = {"gemme" : 0, "pièce" :  0}  
                for i in range(1, 4):
                    valeur = random.randint(1,len(self.objects))
                    if valeur == 1:
                        self.objects["gemme"] += 1
                    else:
                        self.objects["pièce"] += random.randint(1, 5)  
                
            else :
                self.objects = {"pomme" : 0, "clé" : 0, "gemme": 0, "pièce" : 0}

                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))

                    if valeur == 1:
                        self.objects["pomme"] += 1
                    elif valeur == 2:
                        self.objects["clé"] += 1
                    elif valeur == 3:
                        self.objects["gemme"] += 1
                    else:
                        self.objects["pièce"] += random.randint(1, 5)   
                
            
    def is_dig_spot(self):
        proba = random.randint(1, 100)

        if self.name == "dig_spot":
            self.dig_spot = True
            if proba <=30:
                self.objects = {}
                
            elif proba <=80:
                self.objects = {"clé" : 0, "pièce" : 0, "levier cassé" : 0}
                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))

                    if valeur == 1:
                        self.objects["clé"] += 1
                    elif valeur == 2:
                        self.objects["pièce"] += random.randint(1, 4)
                    else:
                        self.objects["levier cassé"] += 1  
                
            else:
                self.objects = {"dés" : 0, "gemme" : 0}
                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))
                    if valeur == 1:
                        self.objects["dés"] += random.randint(1, 3) 
                    else:
                        self.objects["gemme"] += random.randint(1, 3)  
    
    def __str__(self):
        return self.name
        