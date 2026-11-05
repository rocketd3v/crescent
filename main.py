import pygame
from settings import * # do not change to import settings idk why it breaks
from assets.colours import *
from scenes.menu import menu
from scenes.character_creation import *
from game.player import *
from game.map import game_map

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crescent")

menu = menu()
character_screen = character_creation()
current_screen = "menu"
hollow_creek = game_map("assets/maps/hollow_creek.tmx")


def main():
    global current_screen, active_field, option, player_character

    active_field = 0
    run = True

    while run:
        option = None
        screen.fill(blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # do not delete this
                run = False

            if current_screen == "menu":
                option = menu.menu_selection(event)

            elif current_screen == "character_creation":
                temp_active_fld = character_screen.field_selection(event)

                if temp_active_fld == 3: # back
                    current_screen = "menu"

                elif temp_active_fld == 2: # start game
                    player_character = player(
                        character_screen.name,
                        character_screen.gender
                    )
                    current_screen = "game"

                elif temp_active_fld is not None:
                    active_field = temp_active_fld

                character_screen.name_selection(event)
                character_screen.gender_selection(event)

        if current_screen == "menu":
            menu.draw_menu(screen)

            if option is not None:
                if option == 0:
                    character_screen.active_field = 0
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

        elif current_screen == "game":
            hollow_creek.draw(screen)
            player_character.draw(screen)
            player_character.movement()

        pygame.display.flip() # keep at bottom
        clock.tick(60)


if __name__ == "__main__":
    main()
