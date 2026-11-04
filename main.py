import pygame
from settings import * # do not change to import settings idk why it breaks
from assets.colours import *
from scenes.menu import menu
from scenes.character_creation import *

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crescent")
menu = menu()
character_screen = character_creation()
current_screen = "menu"

def main():
    global current_screen, active_field
    active_field = 0
    pygame.time.get_ticks()
    scene_change_cd = 500
    last_scene_change = 0
    run = True
    
    while run:
        screen.fill(blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # do not delete this
                run = False

            if current_screen == "menu":
                option = menu.menu_selection(event)
            elif current_screen == "character_creation":
                active_field = character_screen.field_selection(event)
                character_screen.name_selection(screen, event)
                character_screen.gender_selection(event)

        if current_screen == "menu":
            menu.draw_menu(screen)

            if option == 0:
                current_screen = "character_creation"
            elif option == 1:
                pass
            elif option == 2: # continue
                pass
            elif option == 3: # settings
                pass
            elif option == 4:
                run = False

        elif current_screen == "character_creation":
            character_screen.draw_character_creation(screen)

            if active_field == "back":
                current_screen = "menu"
                menu.draw_menu(screen)

        pygame.display.flip() # keep at bottom
        clock.tick(60)
        
if __name__ == "__main__":
    main()
