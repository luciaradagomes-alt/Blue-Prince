import pygame
from inventory import Inventory
import text

pygame.init()
screen = pygame.display.set_mode((1280, 720))
centerx = screen.get_width() / 2
centery = screen.get_height() / 2

clock = pygame.time.Clock()
running = True
dt = 0

game_state = 'title'
titlecard = pygame.image.load("images\\titlecard.webp").convert()
titlecard = pygame.transform.scale(titlecard, (1280, 720))
text.ligne_texte_centre("Appuyez sur ESPACE pour commencer",titlecard,offsety=200)

background = pygame.image.load("images\\background.jpg").convert()

player_pos = pygame.Vector2(centerx, centery)
inventory = Inventory()
inventory.shovel = True
inventory_show = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            if game_state == "title":
                if event.key == pygame.K_SPACE:
                    game_state = "choix_clavier"

            if game_state == "choix_clavier":
                key_arriere = pygame.K_s
                key_droite = pygame.K_d
                if event.key == pygame.K_1:
                    key_avant = pygame.K_w
                    key_gauche = pygame.K_a
                    game_state = "jeu"
                if event.key == pygame.K_2:
                    key_avant = pygame.K_z
                    key_gauche = pygame.K_q
                    game_state = "jeu"
            
            if game_state == "jeu":

                if event.key == pygame.K_i:
                    inventory_show = not inventory_show

    if game_state == "title":
        pygame.Surface.blit(screen,titlecard,(0,0))
        pygame.display.flip()

    if game_state == "choix_clavier":
        screen.blit(background,(0,0))
        text.texte_centre(["Voulez-vous jouer sur WASD ou QZSD ?","1. WASD","2. QZSD"],screen,-300,-100,font=text.font2)
        pygame.display.flip()

    if game_state == "jeu":
        
        if inventory_show == True:
            screen.blit(inventory.show_inventory(),(0,0))
            
        else:
            screen.blit(background,(0,0))

            pygame.draw.circle(screen, "blue", player_pos, 40)

            keys = pygame.key.get_pressed()
            if keys[key_avant]:
                player_pos.y -= 300 * dt
            if keys[key_arriere]:
                player_pos.y += 300 * dt
            if keys[key_gauche]:
                player_pos.x -= 300 * dt
            if keys[key_droite]:
                player_pos.x += 300 * dt
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000


pygame.quit()

