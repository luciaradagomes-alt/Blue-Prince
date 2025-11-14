import pygame
import sys
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

# --- Écrans et images ---
titlecard = pygame.image.load("images/titlecard.webp").convert()
titlecard = pygame.transform.scale(titlecard, (1280, 720))
text.ligne_texte_centre("Appuyez sur ESPACE pour commencer", titlecard, offsety=200)

background = pygame.image.load("images/background.jpg").convert()
background.set_alpha(30)
noir = pygame.Surface((1280, 720))
noir.fill([0, 0, 0])
noir.set_alpha(10)

mansion = pygame.image.load("images/mansion.webp").convert()
mansion = pygame.transform.scale(mansion, (1280, 720))

# --- Variables globales de jeu ---
game_map = None
player = None
inventory_show = False
room_draw_system = None
current_room_node = None
show_room_interface = False


# ------------------------------------------------------------
# Initialisation de la partie
# ------------------------------------------------------------
def init_game():
    """Initialise une nouvelle partie"""
    global game_map, player, room_draw_system, current_room_node

    # Créer la carte
    game_map = Map()
    game_map.load_from_json("map_layout.json")
    game_map.generate_map()

    # Créer le joueur à la position de départ
    start_x, start_y = game_map.get_start_position()
    player = Player(start_x, start_y, game_map.tile_size)

    # Système de tirage des pièces
    room_draw_system = RoomDraw()

    # Position actuelle
    current_room_node = game_map.get_room_at(start_x, start_y)

    print(f"Jeu initialisé. Position de départ: {start_x}, {start_y}")
    print(f"Salle actuelle: {current_room_node.room.name}")


# ------------------------------------------------------------
# Caméra
# ------------------------------------------------------------
def get_camera_offset():
    """Calcule l'offset de la caméra pour centrer sur le joueur"""
    if player is None:
        return (0, 0)

    px, py = player.get_pixel_position()
    ui_height = 60  # même hauteur que la barre d'UI

    offset_x = px - centerx + player.tile_size // 2
    offset_y = py - (centery + ui_height // 2) + player.tile_size // 2  # centrage ajusté

    # Limites caméra
    max_offset_x = max(0, len(game_map.map_grid[0]) * game_map.tile_size - screen.get_width())
    max_offset_y = max(0, len(game_map.map_grid) * game_map.tile_size - screen.get_height())

    offset_x = max(0, min(offset_x, max_offset_x))
    offset_y = max(0, min(offset_y, max_offset_y))

    return (offset_x, offset_y)


# ------------------------------------------------------------
# Interface utilisateur
# ------------------------------------------------------------
def draw_ui():
    """Dessine la barre d'informations du joueur"""
    ui_height = 60
    pygame.draw.rect(screen, couleurs["darkblue"], pygame.Rect(0, 0, screen.get_width(), ui_height))
    pygame.draw.rect(screen, couleurs["lightblue"], pygame.Rect(0, 0, screen.get_width(), ui_height), 3)

    font = text.inventory_font
    x_offset = 20

    steps_text = font.render(f"Pas: {player.inventory.steps}", True, "white")
    screen.blit(steps_text, (x_offset, 20))
    x_offset += 150

    keys_text = font.render(f"Clés: {player.inventory.keys}", True, "white")
    screen.blit(keys_text, (x_offset, 20))
    x_offset += 120

    coins_text = font.render(f"Pièces: {player.inventory.coins}", True, "white")
    screen.blit(coins_text, (x_offset, 20))
    x_offset += 150

    gems_text = font.render(f"Gemmes: {player.inventory.gems}", True, "white")
    screen.blit(gems_text, (x_offset, 20))
    x_offset += 150

    dice_text = font.render(f"Dés: {player.inventory.dice}", True, "white")
    screen.blit(dice_text, (x_offset, 20))

    room_name_text = font.render(f"Salle: {current_room_node.room.name}", True, "white")
    screen.blit(room_name_text, (screen.get_width() - 300, 20))


# ------------------------------------------------------------
# Gestion des salles
# ------------------------------------------------------------
def enter_current_room():
    """Gère l'entrée dans la salle actuelle"""
    global show_room_interface, current_room_node

    room = current_room_node.room

    if room.visited:
        print(f"Vous êtes déjà entré dans {room.name}")
        return

    if isinstance(room, Yellow):
        room.enter_room(player.inventory)
    elif isinstance(room, Green):
        room.enter_room(player.inventory)
    else:
        print(f"Vous entrez dans {room.name}")
        room.visited = True


def check_win_condition():
    """Vérifie si le joueur est arrivé à l'antichambre"""
    room = current_room_node.room
    if "antichambre" in room.name.lower() or "antechamber" in room.name.lower():
        return True
    return False


# ------------------------------------------------------------
# Boucle principale
# ------------------------------------------------------------
while running:
    dt = clock.tick(60) / 1000.0  # secondes écoulées depuis la dernière frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "title":
                if event.key == pygame.K_SPACE:
                    game_state = "choix_clavier"

            elif game_state == "choix_clavier":
                key_arriere = pygame.K_s
                key_droite = pygame.K_d
                if event.key == pygame.K_1:
                    key_avant = pygame.K_w
                    key_gauche = pygame.K_a
                    game_state = "jeu"
                    init_game()
                if event.key == pygame.K_2:
                    key_avant = pygame.K_z
                    key_gauche = pygame.K_q
                    game_state = "jeu"
                    init_game()

            elif game_state == "jeu":
                if event.key == pygame.K_i:
                    inventory_show = not inventory_show

                if not player.is_moving:
                    moved = False
                    if event.key == key_avant:
                        moved = player.move(0, -1, game_map)
                    elif event.key == key_arriere:
                        moved = player.move(0, 1, game_map)
                    elif event.key == key_gauche:
                        moved = player.move(-1, 0, game_map)
                    elif event.key == key_droite:
                        moved = player.move(1, 0, game_map)

                    if moved:
                        px, py = player.get_tile_position()
                        current_room_node = game_map.get_room_at(px, py)
                        print(f"Nouvelle salle: {current_room_node.room.name}")

                if event.key == pygame.K_e:
                    enter_current_room()

                if event.key == pygame.K_t:
                    print("Tirage de pièces - à implémenter")

                if event.key == pygame.K_p:
                    game_state = "perdu"
                if event.key == pygame.K_g:
                    game_state = "gagne"

            elif game_state in ["perdu", "gagne"]:
                if event.key == pygame.K_SPACE:
                    game_state = "title"
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # --- États du jeu ---
    if game_state == "title":
        screen.blit(titlecard, (0, 0))
        pygame.display.flip()

    elif game_state == "choix_clavier":
        screen.blit(background, (0, 0))
        text.texte_centre(["Voulez-vous jouer sur WASD ou QZSD ?", "1. WASD", "2. QZSD"],
                          screen, -300, -100, font=text.font2)
        pygame.display.flip()

    elif game_state == "jeu":
        if inventory_show:
            screen.blit(noir, (0, 0))
            screen.blit(player.inventory.show_inventory(), (0, 0))
            pygame.display.flip()
        else:
            player.update(dt)

            camera_offset = get_camera_offset()
            screen.fill(couleurs["darkblue"])
            game_map.draw(screen, camera_offset)
            player.draw(screen, camera_offset)
            draw_ui()

            help_text = text.inventory_font.render(
                "I: Inventaire | E: Entrer | T: Tirer des pièces", True, "white")
            screen.blit(help_text, (20, screen.get_height() - 30))

            pygame.display.flip()

        if player.inventory.steps <= 0:
            game_state = "perdu"
        elif check_win_condition():
            game_state = "gagne"

    elif game_state == "perdu":
        screen.blit(noir, (0, 0))
        pygame.draw.rect(screen, couleurs['darkblue'],
                         pygame.Rect(centerx - 300, centery - 100, 600, 200))
        pygame.draw.rect(screen, couleurs['lightblue'],
                         pygame.Rect(centerx - 300, centery - 100, 600, 200), width=10)
        text.texte_centre(["Vous ne pouvez plus avancer", "Vous avez perdu"],
                          screen, color=couleurs['lightblue'], offsety=-20)
        pygame.display.flip()

    elif game_state == "gagne":
        screen.blit(mansion, (0, 0))
        text.ligne_texte_centre("Vous avez gagné !", screen, color="white", font=text.room_font)
        text.ligne_texte_centre("Appuyez sur ESC pour quitter ou SPACE pour rejouer",
                                screen, color="white", font=text.font2, offsety=100)
        pygame.display.flip()

pygame.quit()
sys.exit()
