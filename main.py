import pygame
from settings import * # do not change to import settings idk why it breaks
from scenes.menu import menu

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crescent")
menu = menu()

def main():
    run = True
    
    while run:
        for event in pygame.event.get(): # always stays on top
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: # pressing x key ends game (pressing the buttonw was too long)
                    run = False
            if event.type == pygame.QUIT:
                run = False

            menu.menu_selection(event) # do the menu selection method from menu class from menu.py which is in scenes

        screen.fill(background_colour)
        menu.draw_menu(screen)
        pygame.display.flip() # keep at bottom
        clock.tick(60)


        
if __name__ == "__main__":
    main()
