import pygame
from settings import *  # do not change to import settings
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
        dt = clock.tick(60)
        option = None
        screen.fill(blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if current_screen == "menu":
                option = menu.menu_selection(event)

            elif current_screen == "character_creation":
                temp_active_fld = character_screen.field_selection(event)

                if temp_active_fld == 3:
                    current_screen = "menu"

                elif temp_active_fld == 2:
                    player_character = player(
                        character_screen.name,
                        character_screen.gender,
                        hollow_creek.pixel_width,
                        hollow_creek.pixel_height
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
                elif option == 2:
                    pass
                elif option == 3:
                    pass
                elif option == 4:
                    run = False

        elif current_screen == "character_creation":
            character_screen.draw_character_creation(screen)

        elif current_screen == "game":
            player_character.movement()
            player_character.animate(dt)

            # Calculate camera position
            camera_x = (
                player_character.x
                + player_character.width / 2
                - screen_width / 2
            )

            camera_y = (
                player_character.y
                + player_character.height / 2
                - screen_height / 2
            )

            # Keep camera inside map boundaries
            camera_x = max(
                0,
                min(camera_x, hollow_creek.pixel_width - screen_width)
            )

            camera_y = max(
                0,
                min(camera_y, hollow_creek.pixel_height - screen_height)
            )

            # Draw map and player
            hollow_creek.draw(screen, camera_x, camera_y)
            player_character.draw(screen, camera_x, camera_y)

        pygame.display.flip()


if __name__ == "__main__":
    main()
