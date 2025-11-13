import pygame
import text
from objet import Objet
from player import Player
from map import Map
from room_draw import RoomDraw
from colorpalette import couleurs
from Chambres import Yellow, Green

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Manoir Mystère")
centerx = screen.get_width() / 2
centery = screen.get_height() / 2

clock = pygame.time.Clock()
running = True
dt = 0

game_state = 'title'
titlecard = pygame.image.load("images\\titlecard.webp").convert()
titlecard = pygame.transform.scale(titlecard, (1280, 720))
text.ligne_texte_centre("Appuyez sur ESPACE pour commencer", titlecard, offsety=200)

background = pygame.image.load("images\\background.jpg").convert()
background.set_alpha(30)
noir = pygame.Surface((1280, 720))
noir.fill([0, 0, 0])
noir.set_alpha(10)

mansion = pygame.image.load("images\\mansion.webp").convert()
mansion = pygame.transform.scale(mansion, (1280, 720))

# var de jeu
game_map = None
player = None
inventory_show = False
room_draw_system = None
current_room_node = None
show_room_interface = False
key_avant = pygame.K_w
key_arriere = pygame.K_s
key_gauche = pygame.K_a
key_droite = pygame.K_d

# temp
message_timer = 0
current_message = ""

def init_game():
    """Initialise une nouvelle partie"""
    global game_map, player, room_draw_system, current_room_node, message_timer, current_message
    
    message_timer = 0
    current_message = ""
    
    # initialisation de la map a partir du json
    game_map = Map()
    game_map.load_from_json("map_layout.json")
    game_map.generate_map()
    
    # positionner le joueur a la case depart
    start_x, start_y = game_map.get_start_position()
    player = Player(start_x, start_y, game_map.tile_size)
    
    # Système de tirage des pièces
    room_draw_system = RoomDraw()
    
    # position actuelle
    current_room_node = game_map.get_room_at(start_x, start_y)
    
    # marquage de la salle a visiter
    current_room_node.room.visited = True
    
    print(f"Jeu initialisé. Position de départ: {start_x}, {start_y}")
    print(f"Salle actuelle: {current_room_node.room.name}")

def show_message(message, duration=2000):
    """Affiche un message temporaire"""
    global current_message, message_timer
    current_message = message
    message_timer = duration

def get_camera_offset():
    """Calcule l'offset de la caméra pour centrer sur le joueur"""
    if player is None:
        return (0, 0)
    
    # utilisation position de la tuile (pas la position animée) pour un centrage stable
    px = player.tile_x * player.tile_size
    py = player.tile_y * player.tile_size
    ui_height = 60
    
    # centre la caméra sur le joueur (ajusté pour l'UI)
    offset_x = px - centerx + player.tile_size // 2
    offset_y = py - (centery + ui_height // 2) + player.tile_size // 2
    
    # limiter la caméra aux bords de la carte
    max_offset_x = max(0, len(game_map.map_grid[0]) * game_map.tile_size - screen.get_width())
    max_offset_y = max(0, len(game_map.map_grid) * game_map.tile_size - screen.get_height())
    
    offset_x = max(0, min(offset_x, max_offset_x))
    offset_y = max(0, min(offset_y, max_offset_y))
    
    return (offset_x, offset_y)

def draw_fog_of_war(surface, camera_offset):
    """Dessine le brouillard de guerre sur les salles non visitées"""
    fog_color = couleurs["darkblue"]  #
    
    for (x, y), room_node in game_map.room_nodes.items():
        if not room_node.room.visited:
            
            draw_x = x * game_map.tile_size - camera_offset[0]
            draw_y = y * game_map.tile_size - camera_offset[1]
            
            #même couleur que le fond
            fog_surface = pygame.Surface((game_map.tile_size, game_map.tile_size))
            fog_surface.fill(fog_color)
            
            
            surface.blit(fog_surface, (draw_x, draw_y))
            
            #bordure pour distinguer les salles du vide
            pygame.draw.rect(surface, couleurs["grey"], 
                           pygame.Rect(draw_x, draw_y, game_map.tile_size, game_map.tile_size), 1)

def draw_ui():
    """Dessine l'interface utilisateur (barre de stats)"""
    # Barre en haut
    ui_height = 60
    pygame.draw.rect(screen, couleurs["darkblue"], pygame.Rect(0, 0, screen.get_width(), ui_height))
    pygame.draw.rect(screen, couleurs["lightblue"], pygame.Rect(0, 0, screen.get_width(), ui_height), 3)
    
    #statistiques
    font = text.inventory_font
    x_offset = 20
    
    #pas
    steps_text = font.render(f"Pas: {player.inventory.steps}", True, "white")
    screen.blit(steps_text, (x_offset, 20))
    x_offset += 150
    
    # clefs
    keys_text = font.render(f"Clés: {player.inventory.keys}", True, "white")
    screen.blit(keys_text, (x_offset, 20))
    x_offset += 120
    
    # pieces
    coins_text = font.render(f"Pièces: {player.inventory.coins}", True, "white")
    screen.blit(coins_text, (x_offset, 20))
    x_offset += 150
    
    # gems
    gems_text = font.render(f"Gemmes: {player.inventory.gems}", True, "white")
    screen.blit(gems_text, (x_offset, 20))
    x_offset += 150
    
    # des
    dice_text = font.render(f"Dés: {player.inventory.dice}", True, "white")
    screen.blit(dice_text, (x_offset, 20))
    
    # Salle actuelle
    room_name_text = font.render(f"Salle: {current_room_node.room.name}", True, "white")
    screen.blit(room_name_text, (screen.get_width() - 400, 20))
    
    # messages temporaires a render
    if message_timer > 0:
        message_surface = pygame.Surface((600, 80))
        message_surface.fill(couleurs["darkblue"])
        pygame.draw.rect(message_surface, couleurs["brightblue"], 
                        pygame.Rect(0, 0, 600, 80), 3)
        
        # decoupe des msg trop longs
        words = current_message.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] < 560:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # affichage
        y_offset = 15
        for line in lines[:2]:  # Maximum 2 lignes
            msg_text = font.render(line, True, "white")
            msg_rect = msg_text.get_rect(center=(300, y_offset + 15))
            message_surface.blit(msg_text, msg_rect)
            y_offset += 25
        
        screen.blit(message_surface, (centerx - 300, 80))

def enter_current_room():
    """Gère l'entrée dans la salle actuelle"""
    global show_room_interface, current_room_node
    
    room = current_room_node.room
    
    
    if not room.visited:
        room.visited = True
    
    # if première fois qu'on entre, faire les actions spéciales
    if isinstance(room, Yellow):
        # 
        result = room.enter_room(player.inventory)
        if result:
            show_message(f"Transaction effectuée dans {room.name}")
    elif isinstance(room, Green):
        # Jardin - interface console
        result = room.enter_room(player.inventory)
        if result:
            show_message(f"Vous avez exploré {room.name}")
    else:
        # Salle générique
        show_message(f"Vous explorez {room.name}")
        
        # ajout de quelques objets aléatoirement dans les salles génériques
        import random
        if random.random() < 0.3:  # 30% de chance
            items = ["pièce", "gemme", "clé"]
            item = random.choice(items)
            quantity = random.randint(1, 3) if item == "pièce" else 1
            
            for _ in range(quantity):
                player.inventory.pick_up(Objet(item), screen)
            
            show_message(f"Trouvé: {quantity} {item}(s) !")

def check_win_condition():
    """Vérifie si le joueur a gagné (atteint l'antichambre)"""
    room = current_room_node.room
    if "antichambre" in room.name.lower() or "antechamber" in room.name.lower():
        return True
    return False

def handle_movement(dx, dy):
    """Gère les tentatives de déplacement du joueur"""
    global current_room_node
    
    if player.is_moving:
        return
    
    #gestion de la limite des cartes
    new_x=player.tile_x + dx
    new_y=player.tile_y + dy
    
    if new_x < 0 or new_y < 0:
        show_message("Impossible: Hors limites")
        return
    if new_y >= len(game_map.map_grid ) or new_x >= len(game_map.map_grid[0]):
        show_message("Impossible: Hors limites")
        return
    
    # Vérifier qu'il y a une salle à la destination
    target_room_node = game_map.get_room_at(new_x, new_y)
    if target_room_node is None:
        show_message("Impossible: Pas de salle ici")
        print(f"Debug: Tentative d'aller vers ({new_x}, {new_y}) - Aucune salle trouvée")
        return
    
    # Vérifier la porte entre les deux salles
    current_node = game_map.get_room_at(player.tile_x, player.tile_y)
    door = current_node.get_door_to(target_room_node)
    
    if door is None:
        # Pas de porte = pas de connexion entre ces salles
        show_message("Impossible: Pas de passage ici")
        print(f"Debug: Pas de porte entre {current_node.room.name} et {target_room_node.room.name}")
        return
    
    # Si la porte est verrouillée, gérer l'ouverture
    if door.locked:
        # Utiliser kit de crochetage si disponible et niveau 1
        if door.lock_level == 1 and player.inventory.lockpick_kit:
            door.unlock()
            show_message("Porte ouverte avec le kit de crochetage !")
        elif player.inventory.keys >= door.lock_level:
            player.inventory.keys -= door.lock_level
            door.unlock()
            show_message(f"Porte ouverte ! (Clés restantes: {player.inventory.keys})")
        else:
            show_message(f"Porte verrouillée - Besoin de {door.lock_level} clé(s)")
            return
    
    # Effectuer le déplacement - IMPORTANT: mettre à jour la position ET démarrer l'animation
    player.tile_x += dx
    player.tile_y += dy
    player.target_x = player.tile_x * player.tile_size
    player.target_y = player.tile_y * player.tile_size
    player.is_moving = True
    
    # Décrémenter les pas
    player.inventory.move()
    
    # Mettre à jour la salle actuelle et la marquer comme visitée
    current_room_node = game_map.get_room_at(player.tile_x, player.tile_y)
    current_room_node.room.visited = True  # Marquer comme visitée dès qu'on y entre
    
    show_message(f"→ {current_room_node.room.name}")
    print(f"Déplacement vers {current_room_node.room.name} à ({player.tile_x}, {player.tile_y})")

# Boucle principale
while running:
    frame_dt = clock.tick(60)
    
    # Mettre à jour le timer des messages
    if message_timer > 0:
        message_timer -= frame_dt
        if message_timer < 0:
            message_timer = 0
            current_message = ""
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            if game_state == "title":
                if event.key == pygame.K_SPACE:
                    game_state = "choix_clavier"
                    dt = 0

            elif game_state == "choix_clavier":
                if event.key == pygame.K_1:
                    key_avant = pygame.K_w
                    key_gauche = pygame.K_a
                    key_arriere = pygame.K_s
                    key_droite = pygame.K_d
                    game_state = "jeu"
                    init_game()
                elif event.key == pygame.K_2:
                    key_avant = pygame.K_z
                    key_gauche = pygame.K_q
                    key_arriere = pygame.K_s
                    key_droite = pygame.K_d
                    game_state = "jeu"
                    init_game()
            
            elif game_state == "jeu":
                if event.key == pygame.K_i:
                    inventory_show = not inventory_show
                    dt = 0
                
                # Déplacements (seulement si pas en mouvement et pas dans l'inventaire)
                if not player.is_moving and not inventory_show:
                    if event.key == key_avant:
                        handle_movement(0, -1)
                    elif event.key == key_arriere:
                        handle_movement(0, 1)
                    elif event.key == key_gauche:
                        handle_movement(-1, 0)
                    elif event.key == key_droite:
                        handle_movement(1, 0)
                
                # Entrer dans la salle
                if event.key == pygame.K_e and not inventory_show:
                    enter_current_room()
                
                # Tirer des pièces
                if event.key == pygame.K_t and not inventory_show:
                    show_message("Système de tirage - À implémenter avec interface graphique")
                
                # Ramasser des objets (pour tester)
                if event.key == pygame.K_o and not inventory_show:
                    # Test: ajouter des objets aléatoires
                    import random
                    items = ["pièce", "gemme", "clé", "banane", "pelle"]
                    item = random.choice(items)
                    player.inventory.pick_up(Objet(item), screen)
                    show_message(f"Ramassé: {item}")
                
                # Debug
                if event.key == pygame.K_p:
                    game_state = "perdu"
                    dt = 0
                if event.key == pygame.K_g:
                    game_state = "gagne"
                    dt = 0

            elif game_state == "perdu" or game_state == "gagne":
                if event.key == pygame.K_SPACE:
                    game_state = "title"
                    inventory_show = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # Rendu
    if game_state == "title":
        screen.blit(titlecard, (0, 0))
        pygame.display.flip()

    elif game_state == "choix_clavier":
        dt += frame_dt
        if dt <= 2500:
            background.set_alpha(65)
            screen.blit(background, (0, 0))
        elif dt <= 5000:
            background.set_alpha(160)
            screen.blit(background, (0, 0))
        else:
            background.set_alpha(255)
            screen.blit(background, (0, 0))
        
        text.texte_centre(["Voulez-vous jouer sur WASD ou QZSD ?", "1. WASD", "2. QZSD"],
                         screen, -300, -100, font=text.font2)
        pygame.display.flip()
        
    elif game_state == "jeu":
        if inventory_show:
            dt += frame_dt
            if dt <= 250:
                screen.blit(noir, (0, 0))
            screen.blit(player.inventory.show_inventory(), (400, 250))
            
            # Instructions pour fermer
            help_text = text.inventory_font.render("Appuyez sur I pour fermer l'inventaire", 
                                                   True, "white")
            screen.blit(help_text, (centerx - 150, 700))
            
            pygame.display.flip()
        else:
            # mettre à jour le joueur
            player.update(frame_dt / 1000.0)
            ## dessin de chaque partie de la map 
            # dessiner la carte
            camera_offset = get_camera_offset()
            screen.fill(couleurs["darkblue"])
            game_map.draw(screen, camera_offset)
            
            # dessiner le brouillard de guerre
            draw_fog_of_war(screen, camera_offset)
            
            # Dessiner le joueur
            player.draw(screen, camera_offset)
            
            # Dessiner l'UI
            draw_ui()
            
            # Instructions
            help_text = text.inventory_font.render(
                "I: Inventaire | E: Entrer | O: Ramasser (test) | T: Tirer des pièces", 
                True, "white")
            screen.blit(help_text, (20, screen.get_height() - 30))
            
            pygame.display.flip()

        # Vérifier fin de partie
        if player.inventory.steps <= 0:
            game_state = "perdu"
            dt = 0
        elif check_win_condition():
            game_state = "gagne"
            dt = 0
    
    elif game_state == "perdu":
        dt += frame_dt
        if dt <= 250:
            screen.blit(noir, (0, 0))
        pygame.draw.rect(screen, couleurs['darkblue'], 
                        pygame.Rect(centerx - 300, centery - 100, 600, 200))
        pygame.draw.rect(screen, couleurs['lightblue'], 
                        pygame.Rect(centerx - 300, centery - 100, 600, 200), width=10)
        text.texte_centre(["Vous ne pouvez plus avancer", "Vous avez perdu"], 
                         screen, color=couleurs['lightblue'], offsety=-20)
        pygame.draw.rect(screen, couleurs['blue1'], 
                        pygame.Rect(centerx - 240, centery + 10, 220, 50))
        pygame.draw.rect(screen, couleurs['lightblue'], 
                        pygame.Rect(centerx - 240, centery + 10, 220, 50), width=6)
        text.ligne_texte_centre("Recommencer (SPACE)", screen, color="white", 
                               offsetx=-130, offsety=35, font=text.inventory_font)

        pygame.draw.rect(screen, couleurs['blue1'], 
                        pygame.Rect(centerx + 20, centery + 10, 220, 50))
        pygame.draw.rect(screen, couleurs['lightblue'], 
                        pygame.Rect(centerx + 20, centery + 10, 220, 50), width=6)
        text.ligne_texte_centre("Quitter (ESC)", screen, color="white", 
                               offsetx=130, offsety=35, font=text.inventory_font)

        pygame.display.flip()  

    elif game_state == "gagne":
        screen.blit(mansion, (0, 0))
        text.ligne_texte_centre("Vous avez gagné !", screen, color="white", 
                               font=text.room_font)
        text.ligne_texte_centre("Appuyez sur ESC pour quitter ou SPACE pour rejouer", 
                               screen, color="white", font=text.font2, offsety=100)
        pygame.display.flip()

pygame.quit()