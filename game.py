import pygame
from map import Map

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blue Prince Prototype")
clock = pygame.time.Clock()

# Crée la map
game_map = Map()
game_map.load_from_json("map_layout.json")
game_map.generate_map()

# Définir une couleur de bordure selon le type de pièce
color_mapping = {
    "blue": (0, 100, 255),
    "red": (220, 50, 50),
    "orange": (255, 140, 0),
    "purple": (150, 0, 200),
    "yellow": (255, 215, 0),
    "start": (0, 255, 0),
    "end": (255, 0, 255)
}

# Ajout d'une fonction draw améliorée
def draw_tiles(surface, tiles):
    for tile in tiles:
        surface.blit(tile.image, (tile.x, tile.y))

        # Bordure couleur selon type
        name = tile.name.lower()
        for key, col in color_mapping.items():
            if key in ["start", "end"] and name in game_map.room_images[key]:
                border_color = col
                break
            elif name in game_map.room_images.get(key, {}):
                border_color = col
                break
        else:
            border_color = (255, 255, 255)

        rect = pygame.Rect(tile.x, tile.y, game_map.tile_size, game_map.tile_size)
        pygame.draw.rect(surface, border_color, rect, 3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    draw_tiles(screen, game_map.tiles)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
