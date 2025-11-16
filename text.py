import pygame

pygame.font.init()

font1 = pygame.font.Font('fonts\\damned architect.ttf',32)
font2 = pygame.font.SysFont('couriernew',24)
font3 = pygame.font.SysFont('franklingothicdemicond',54)
font4 = pygame.font.SysFont('franklingothicdemicond',128)
font5 = pygame.font.SysFont('couriernew',20)

room_font = pygame.font.SysFont('franklingothic',28)
inventory_font = pygame.font.SysFont('couriernew',16)

def ligne_texte(txt,screen,x,y,color="white",font=font1,modifier=None,marge=10,sep=" "):
    """ Ajoute à une Surface pygame une ligne de texte. Si la ligne est supérieure à la largeur de la Surface, elle est séparée en 2 lignes.

    Parameters
    - txt : str
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
    - sep : str (optional)
        Définit le séparateur si la ligne est trop longue pour Être affiché sur 1 seule ligne, ' ' par défaut 
    - marge : int | str (optional)
        Espace qui reste à gauche du texte, 10 par défaut
        Peut aussi être 'same', qui affecte la valeur de x à la marge

    Returns:
    - screen.blit
        Renvoie une ligne de texte
    """
    if marge == 'same':
        marge = x
    elif type(marge) == str:
        marge=10 #marge défaut

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

    if font.size(txt)[0] <= screen.get_width() - x - marge:
        txt = font.render(txt,False,color)
        return screen.blit(txt,(x,y))

    txt_fin = ""
    while font.size(txt)[0] > screen.get_width() - x - marge:
        mots = txt.rsplit(sep,maxsplit=1)
        txt = mots[0]
        if len(mots) > 1:
            txt_fin = mots[1] + sep + txt_fin
    texte([txt,txt_fin],screen,x,y,color,font,modifiers={0:modifier,1:modifier},marge=marge)
    
                
def texte(txt,screen,x,y,color="white",font=font1,modifiers={},marge=10,leading=0):
    """ Ajoute à une Surface pygame plusieurs ligne de texte.

    Parameters
    - txt : list[str]
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
    - marge : dict{int : int | float | str} | int | float | str (optional)
        Espace qui reste à gauche du texte, 10 par défaut
        Peut aussi être 'same', qui affecte la valeur de x à la marge
    - leading : int (optional)
        Espace entre les différentes lignes ou paragraphes de texte, 0 par défaut
    """
    if len(modifiers) != len(txt):
        for i in range(len(txt)):
            if i not in modifiers.keys():
                modifiers[i] = None
    if type(marge) in (int,str,float):
        marge_ind = marge
        marge = {}
        for i in range(len(txt)):
            if i not in marge.keys():
                marge[i] = marge_ind
    elif len(marge) != len(txt):
        for i in range(len(txt)):
            if i not in marge.keys():
                marge[i] = 'same'

    _,height = font.size(txt[0]) 
    for i in range(len(txt)):
        ligne_texte(txt[i],screen,x,y,color,font,modifiers[i],marge[i])
        if marge[i] == 'same':
            marge[i] = x
        nb_lignes = font.size(txt[i])[0]//(screen.get_width() - x - marge[i]) + 1
        y += nb_lignes * height + leading


def ligne_texte_centre(txt,screen,offsetx=0,offsety=0,color="white",font=font1,modifier=None):
    """ Ajoute à une Surface pygame une ligne de texte, par défaut centralisée.

    Parameters
    - txt : str
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

    Returns:
    - ligne_texte
        Renvoie une ligne de texte, centralisée
    """
    x = screen.get_width() / 2 - font.size(txt)[0] / 2 + offsetx
    y = screen.get_height() / 2 - font.size(txt)[1] / 2 + offsety
    return ligne_texte(txt,screen,x,y,color,font,modifier)


def texte_centre(txt,screen,offsetx=0,offsety=0,color="white",font=font1,modifiers={}):
    """ Ajoute à une Surface pygame plusieurs lignes de texte, par défaut centralisées.

    Parameters
    - txt : list[str] | str
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

    if len(modifiers) != len(txt):
        for i in range(len(txt)):
            if i not in modifiers.keys():
                modifiers[i] = None

    if type(txt) == str:
        ligne_texte_centre(txt,screen,offsetx,offsety,color,font,modifiers[0])
    else:
        _,height = font.size(txt[0])
        offsety -= len(txt) / 2 * height
        for i in range(len(txt)):
            ligne_texte_centre(txt[i],screen,offsetx,offsety,color,font,modifiers[i])
            offsety += height


def afficher_message_temps(txt,screen,time=1000,font=font3):
    """ Permet d'afficher un message au centre l'interface graphique pendant un temps donné.

    Parameters
    - txt : list[str] | str
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
    texte_centre(txt,screen,font=font)
    pygame.display.flip()
    pygame.time.delay(time)

def afficher_message(txt,screen,font=font3): # à FINIR
    """ Permet d'afficher un message au centre l'interface graphique.

    Parameters
    - txt : list[str] | str
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
    texte_centre(txt,screen,font=font)
    pygame.display.flip()
    # ne pas changer avant que le joueur clique sur un bouton !

def afficher_salle(room,screen):
    """ Permet d'afficher le nom d'une salle sur l'interface graphique.

    Parameters
    - room : Room
        Nom de la chambre à afficher
    - screen (Surface): 
        La Surface sur laquelle le texte sera placée, à mettre "screen", l'interface graphique
    """
    afficher_message_temps(room.name.upper(),screen,3000,room_font)