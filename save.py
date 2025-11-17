import pygame 
from colorpalette import couleurs

vide = pygame.Surface((128,128))
pygame.draw.rect(vide,couleurs["blue2"],pygame.Rect((0,0,128,128)))
pygame.draw.rect(vide,couleurs["lightblue"],pygame.Rect((0,0,128,128)),width=1)
        
pygame.image.save(vide,"assets\\vide\\tuile_remplie.jpg")