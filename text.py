import pygame

pygame.font.init()

font1 = pygame.font.Font('images\\damned architect.ttf',32)
font2 = pygame.font.SysFont('couriernew',24)

inventory_font = pygame.font.SysFont('couriernew',16)

def ligne_texte(texte,screen,x,y,color="white",font=font1):
    """ Ajoute à une Surface pygame une ligne de texte.

    Paramètres
    ---------------
    - texte : str
        Texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée
    - x : int 
        La coordonnée x (horizontale) du point en haut à gauche du texte
    - y : int 
        La coordonnée y (verticale) du point en haut à gauche du texte
    - color : str | Tuple[int][3] (optional)
        La couleur désirée pour afficher le texte, blanc par défaut
    - font : Font (optional)
        La police désirée pour afficher le texte, Damned Architect par défaut
    """
    texte = font.render(texte,False,color)
    return screen.blit(texte,(x,y))

def texte(texte,screen,x,y,color="white",font=font1):
    """ Ajoute à une Surface pygame plusieurs ligne de texte.

    Paramètres
    ---------------
    - texte : list[str]
        Liste des lignes de texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée
    - x : int 
        La coordonnée x (horizontale) du point en haut à gauche du texte
    - y : int 
        La coordonnée y (verticale) du point en haut à gauche du texte
    - color : str | Tuple[int][3] (optional)
        La couleur désirée pour afficher le texte, blanc par défaut
    - font : Font (optional)
        La police désirée pour afficher le texte, Damned Architect par défaut
    """
    _,height = font.size(texte[0])
    for ligne in texte:
        ligne_texte(ligne,screen,x,y,color,font)
        y += height

def ligne_texte_centre(texte,screen,offsetx=0,offsety=0,color="white",font=font1):
    """ Ajoute à une Surface pygame une ligne de texte, par défaut centralisée.

    Paramètres
    ---------------
    - texte : str
        Texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée
    - offsetx : int (optional)
        La décentralisation sur la coordonnée x (horizontalement)
    - offsety : int (optional)
        La décentralisation sur la coordonnée y (verticalement)
    - color : str | Tuple[int][3] (optional)
        La couleur désirée pour afficher le texte, blanc par défaut
    - font : Font (optional)
        La police désirée pour afficher le texte, Damned Architect par défaut
    """
    texte = font.render(texte,False,color)
    x = screen.get_width() / 2 - texte.get_width() / 2 + offsetx
    y = screen.get_height() / 2 - texte.get_height() / 2 + offsety
    return screen.blit(texte,(x,y))

def texte_centre(texte,screen,offsetx=0,offsety=0,color="white",font=font1):
    """ Ajoute à une Surface pygame plusieurs lignes de texte, par défaut centralisées.

    Paramètres
    ---------------
    - texte : list[str]
        Liste des lignes de texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée
    - offsetx : int (optional)
        La décentralisation sur la coordonnée x (horizontalement)
    - offsety : int (optional)
        La décentralisation sur la coordonnée y (verticalement)
    - color : str | Tuple[int][3] (optional)
        La couleur désirée pour afficher le texte, blanc par défaut
    - font : Font (optional)
        La police désirée pour afficher le texte, Damned Architect par défaut
    """
    _,height = font.size(texte[0])
    offsety -= len(texte) / 2 * height
    for ligne in texte:
        ligne_texte_centre(ligne,screen,offsetx,offsety,color,font)
        offsety += height
