import pygame
import text
from objet import Objet
from inventory import Inventory
from chambres import Yellow
from colorpalet import couleurs

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
background.set_alpha(30)
noir = pygame.Surface((1280,720))
noir.fill([0,0,0])
noir.set_alpha(10)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            if game_state == "title":
                if event.key == pygame.K_SPACE:
                    game_state = "choix_clavier"
                    dt = 0

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
                    dt = 0
                
                if event.key == pygame.K_p:
                    game_state = "perdu"
                    dt = 0
                
                if event.key == pygame.K_m:
                    inventory.pick_up(Objet('casier'),screen)

                if event.key == pygame.K_b:
                    text.afficher_salle(Yellow("Bookshop"),screen)

            if game_state == "perdu":
                if event.key == pygame.K_SPACE:
                    game_state = "title"
                elif event.key == pygame.K_ESCAPE:
                    running = False
        

    if game_state == "title":
        
        player_pos = pygame.Vector2(centerx, centery)

        inventory = Inventory()
        inventory.shovel = True
        inventory_show = False

        pygame.Surface.blit(screen,titlecard,(0,0))
        pygame.display.flip()

    if game_state == "choix_clavier":
        dt += clock.tick(60) 
        if dt <= 2500:
            background.set_alpha(65)
            screen.blit(background,(0,0))
        elif dt <= 5000:
            background.set_alpha(160)
            screen.blit(background,(0,0))
        else:
            background.set_alpha(255)
            screen.blit(background,(0,0))
        
        text.texte_centre(["Voulez-vous jouer sur WASD ou QZSD ?","1. WASD","2. QZSD"],screen,-300,-100,font=text.font2)
        pygame.display.flip()
        
    if game_state == "jeu":
        
        if inventory_show == True:
            dt += clock.tick(60) 
            if dt <= 250:
                screen.blit(noir,(0,0))
                
            screen.blit(inventory.show_inventory(),(0,0))
            pygame.display.flip()
            
        else:
            screen.blit(background,(0,0))

            pygame.draw.circle(screen, couleurs['brightblue'], player_pos, 40)

            keys = pygame.key.get_pressed()
            if keys[key_avant]:
                if player_pos.y >= 40:
                    player_pos.y -= 300 * dt
            if keys[key_arriere]:
                if player_pos.y < screen.get_height()-40:
                    player_pos.y += 300 * dt
            if keys[key_gauche]:
                if player_pos.x > 40:
                    player_pos.x -= 300 * dt
            if keys[key_droite]:
                if player_pos.x < screen.get_width()-40:
                    player_pos.x += 300 * dt

            dt = clock.tick(60) / 800
        
        pygame.display.flip()

        if inventory.steps <= 0:
            game_state = "perdu"
            perdu = True
            dt = 0
    
    if game_state == "perdu":
        
        dt += clock.tick(60) 
        if dt <= 250:
            screen.blit(noir,(0,0))

        pygame.draw.rect(screen,couleurs['darkblue'],pygame.Rect(centerx - 300,centery - 100,600,200))
        pygame.draw.rect(screen,couleurs['lightblue'],pygame.Rect(centerx - 300,centery - 100,600,200),width=10)
        text.texte_centre(["Vous ne pouvez plus avancer", "Vous avez perdu"],screen,color=couleurs['lightblue'],offsety=-20)
        
        pygame.draw.rect(screen,couleurs['blue1'],pygame.Rect(centerx - 240, centery + 10,220,50))
        pygame.draw.rect(screen,couleurs['lightblue'],pygame.Rect(centerx - 240, centery + 10,220,50),width=6)
        text.ligne_texte_centre("Recommencer (SPACE)",screen,color="white",offsetx=-130,offsety=35,font=text.inventory_font)

        pygame.draw.rect(screen,couleurs['blue1'],pygame.Rect(centerx + 20, centery + 10,220,50))
        pygame.draw.rect(screen,couleurs['lightblue'],pygame.Rect(centerx + 20, centery + 10,220,50),width=6)
        text.ligne_texte_centre("Quitter (ESC)",screen,color="white",offsetx=130,offsety=35,font=text.inventory_font)

        pygame.display.flip()    

pygame.quit()

