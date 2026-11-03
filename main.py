import pygame
from settings import *

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crescent")
menu_screen = True


def main():
    menu_option = 0
    run = True

    while run:
        for event in pygame.event.get(): # always stays on top
            if event.type == pygame.QUIT:
                run = False

            if menu_screen:
                if event.type == pygame.KEYDOWN: # menu selection
                    if event.key == pygame.K_UP:
                        menu_option -= 1
                        if menu_option < 0:
                            menu_option = 3
                        print(f"option: {menu_option}")

                    elif event.key == pygame.K_DOWN:
                        menu_option += 1
                        if menu_option > 3:
                            menu_option = 0
                        print(f"option: {menu_option}")

        screen.fill(background_colour)
        pygame.display.flip() # keep at bottom
        clock.tick(60)


        
if __name__ == "__main__":
    main()
