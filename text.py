import pygame

pygame.font.init()

font1 = pygame.font.Font('fonts\\damned architect.ttf',32)
font2 = pygame.font.SysFont('couriernew',24)
font3 = pygame.font.SysFont('franklingothicdemicond',64)

room_font = pygame.font.SysFont('franklingothicdemicond',96)
inventory_font = pygame.font.SysFont('couriernew',16)

#font = pygame.font.get_fonts()
#for f in font:
#    print(f)


def ligne_texte(texte,screen,x,y,color="white",font=font1,modifier=None):
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
    - modifier : str (optional)
        Définit si le texte doit être affiché en gras, italique ou souligné
    """
    if modifier == 'bold':
        font.bold = True
    elif modifier == 'italic':
        font.italic =  True
    elif modifier == 'underline':
        font.underline = True
    else:
        font.bold = False
        font.italic = False
        font.underline = False

    texte = font.render(texte,False,color)
    return screen.blit(texte,(x,y))


def texte(texte,screen,x,y,color="white",font=font1,modifiers={}):
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
    - modifiers : dict[int:str]
        Pour chaque ligne de texte à modifier, définit si le texte doit être affiché en gras, italique ou souligné
        Les clés du dictionnaire représentent l'index de la ligne à modifier
    """
    if len(modifiers) != len(texte):
        for i in range(len(texte)):
            if i not in modifiers.keys():
                modifiers[i] = None

    _,height = font.size(texte[0])
    for i in range(len(texte)):
        ligne_texte(texte[i],screen,x,y,color,font,modifiers[i])
        y += height


def ligne_texte_centre(texte,screen,offsetx=0,offsety=0,color="white",font=font1,modifier=None):
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
    - modifier : str (optional)
        Définit si le texte doit être affiché en gras, italique ou souligné
    """
    x = screen.get_width() / 2 - font.size(texte)[0] / 2 + offsetx
    y = screen.get_height() / 2 - font.size(texte)[1] / 2 + offsety
    return ligne_texte(texte,screen,x,y,color,font,modifier)


def texte_centre(texte,screen,offsetx=0,offsety=0,color="white",font=font1,modifiers={}):
    """ Ajoute à une Surface pygame plusieurs lignes de texte, par défaut centralisées.

    Paramètres
    ---------------
    - texte : list[str] | str
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
    - modifiers : dict[int:str]
        Pour chaque ligne de texte à modifier, définit si le texte doit être affiché en gras, italique ou souligné
        Les clés du dictionnaire représentent l'index de la ligne à modifier
    """

    if len(modifiers) != len(texte):
        for i in range(len(texte)):
            if i not in modifiers.keys():
                modifiers[i] = None

    if type(texte) == str:
        ligne_texte_centre(texte,screen,offsetx,offsety,color,font,modifiers[0])
    else:
        _,height = font.size(texte[0])
        offsety -= len(texte) / 2 * height
        for i in range(len(texte)):
            ligne_texte_centre(texte[i],screen,offsetx,offsety,color,font,modifiers[i])
            offsety += height


def afficher_message_temps(texte,screen,time=1000,font=font3):
    """ Permet d'afficher un message au centre l'interface graphique pendant un temps donné.

    Paramètres
    ---------------
    - texte : list[str] | str
        Liste des lignes de texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée, à mettre "screen", l'interface graphique
    - time : int (optional)
        Le temps (en ms) pendant lequel le message s'affiche, 1000 par défaut
    - font : Font (optional)
        La police désirée pour afficher le texte, Franklin Gothic DemiCond taille 96 par défaut
    """
    noir = pygame.Surface((1280,720))
    noir.fill([0,0,0])
    noir.set_alpha(70)
    screen.blit(noir,(0,0))
    texte_centre(texte,screen,font=font)
    pygame.display.flip()
    pygame.time.delay(time)

def afficher_message(texte,screen,font=font3): # à FINIR
    """ Permet d'afficher un message au centre l'interface graphique.

    Paramètres
    ---------------
    - texte : list[str] | str
        Liste des lignes de texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée, à mettre "screen", l'interface graphique
    - time : int (optional)
        Le temps (en ms) pendant lequel le message s'affiche, 1000 par défaut
    - font : Font (optional)
        La police désirée pour afficher le texte, Franklin Gothic DemiCond taille 96 par défaut
    """
    noir = pygame.Surface((1280,720))
    noir.fill([0,0,0])
    noir.set_alpha(70)
    screen.blit(noir,(0,0))
    texte_centre(texte,screen,font=font)
    pygame.display.flip()
    # ne pas changer avant que le joueur clique sur un bouton !

def afficher_salle(room,screen):
    """ Permet d'afficher le nom d'une salle sur l'interface graphique.

    Paramètres
    ---------------
    - texte : list[str] | str
        Liste des lignes de texte à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée, à mettre "screen", l'interface graphique
    """
    afficher_message_temps(room.name.upper(),screen,3000,room_font)