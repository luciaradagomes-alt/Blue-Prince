#%%
import pygame
import random

#%%
class Objet:

    def __init__(self, name):
        self.name = name
        self.food = False
        self.locker = False
        self.chest = False
        self.dig_spot = False
        self.stackable = False

        self.steps = 0
        self.objects = None
        self.required_tool = None

        self.is_food()
        self.is_stackable()
        self.is_locker()
        self.is_chest()
        self.is_dig_spot()


    def is_stackable(self):
        stackable_objects = {"pomme", "banane", "gâteau", "sandwich", "repas", "pièces", "gemmes", "clé", "levier cassé"}
        if self.name in stackable_objects:
            self.stackable = True

    def is_food(self):
        food = {"pomme" : 2, "banane" : 3, "gâteau" : 10, "sandwich" : 15, "repas" : 25}
        if self.name in food:
            self.food = True
            self.steps = food[self.name]

    def is_locker(self):
        proba = random.randint(1, 100)

        if self.name == "locker":
            self.locker = True
            self.required_tool = "clé"   # L'outil nécessaire pour ouvrir le locker
            if proba <= 50:             
                self.objects = {}
                return self.objects

            elif proba <= 80 :
                self.objects = {"gemmes" : 0, "pièces" :  0}  
                for i in range(1, 4):
                    valeur = random.randint(1,len(self.objects))
                    if valeur == 1:
                        self.objects["gemmes"] += 1
                    else:
                        self.objects["pièces"] += random.randint(1, 5)  
                return self.objects 
            else :
                self.objects = {"pomme" : 0, "clé" : 0, "gemmes": 0, "pièces" : 0}

                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))

                    if valeur == 1:
                        self.objects["pomme"] += 1
                    elif valeur == 2:
                        self.objects["clé"] += 1
                    elif valeur == 3:
                        self.objects["gemmes"] += 1
                    else:
                        self.objects["pièces"] += random.randint(1, 5)   
                return self.objects 
            
    def is_chest(self):
        proba = random.randint(1, 100)

        if self.name == "chest":
            self.chest = True
            self.required_tool = "clé"   # L'outil nécessaire pour ouvrir le coffre
            if proba <= 50:             
                self.objects = {}
                return self.objects

            elif proba <= 80 :
                self.objects = {"gemmes" : 0, "pièces" :  0}  
                for i in range(1, 4):
                    valeur = random.randint(1,len(self.objects))
                    if valeur == 1:
                        self.objects["gemmes"] += 1
                    else:
                        self.objects["pièces"] += random.randint(1, 5)  
                return self.objects 
            else :
                self.objects = {"pomme" : 0, "clé" : 0, "gemmes": 0, "pièces" : 0}

                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))

                    if valeur == 1:
                        self.objects["pomme"] += 1
                    elif valeur == 2:
                        self.objects["clé"] += 1
                    elif valeur == 3:
                        self.objects["gemmes"] += 1
                    else:
                        self.objects["pièces"] += random.randint(1, 5)   
                return self.objects 
            
    def is_dig_spot(self):
        proba = random.randint(1, 100)

        if self.name == "dig spot":
            self.dig_spot = True
            self.required_tool = "pelle"
            if proba <=30:
                self.objects = {}
                return self.objects
            elif proba <=80:
                self.objects = {"clé" : 0, "pièces" : 0, "levier cassé" : 0}
                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))

                    if valeur == 1:
                        self.objects["clé"] += 1
                    elif valeur == 2:
                        self.objects["pièces"] += random.randint(1, 4)
                    else:
                        self.objects["levier cassé"] += 1  
                return self.objects 
            else:
                self.objects = {"dés" : 0, "gemmes" : 0}
                for i in range(1, 3):
                    valeur = random.randint(1,len(self.objects))
                    if valeur == 1:
                        self.objects["dés"] += random.randint(1, 3) 
                    else:
                        self.objects["gemmes"] += random.randint(1, 3)  
                return self.objects
            
    def open(self, tool, inventory):
        if not self.locker and not self.chest:
            return False
        
        elif not inventory.is_in_inventory(self.required_tool):
            return False, f"{self.required_tool} manquant."
        
        elif tool != self.required_tool:
            return False, "Outil incorrect."

        elif self.objects == {}:
            return True, "Ouvert, mais vide."
        
        else:
            for item, quantity in self.objects.items():
                inventory.add_items(item, quantity)
            
            self.objects = {}
            return True, "Ouvert !"
        
    def dig(self, tool, inventory):
        if not self.dig_spot:
            return False
        
        elif not inventory.is_in_inventory(self.required_tool):
            return False, "Pelle manquante."
        
        elif tool != self.required_tool:
            return False, "Outil incorrect. Nécessite une pelle pour creuser."
        
        elif self.objects == {}:
            return True, "Rien trouvé en creusant."
        
        else:
            for item, quantity in self.objects.items():
                inventory.add_items(item, quantity)
            
            self.objects = {}
            return True, "Objet(s) trouvé(s) !"
    
    def __str__(self):
        return f"Objet: {self.name}"
        


#%%
# tests

pomme = Objet("pomme")
print(f"{pomme.name} : nourriture ? {pomme.food}, stackable ? {pomme.stackable}, nombre de pas : {pomme.steps}")

coffre = Objet("chest")
print(f"{coffre.name} : nourriture ? {coffre.food}, stackable ? {coffre.stackable}, outil nécessaire pour l'ouvrir : {coffre.required_tool}, objets dans le {coffre.name} : {coffre.objects}")

casier = Objet("locker")
print(f"{casier.name} : nourriture ? {casier.food}, stackable ? {casier.stackable}, outil nécessaire pour l'ouvrir : {casier.required_tool}, objets dans le {casier.name} : {casier.objects}")

# %%
