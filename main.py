import pygame
import os
from datetime import datetime

from settings import *  # do not change to import settings
from assets.colours import *
from scenes.menu import menu
from scenes.character_creation import *
from game.player import *
from game.map import game_map
from game.camera import camera
from scenes.settings_menu import settings_menu
from systems.interactions import *
from systems.objectives import objective_tracker
from game.npc import npc


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crescent")

menu = menu()
character_screen = character_creation()
settings_screen = settings_menu()
objective_system = objective_tracker(settings_screen.font_path)

current_screen = "menu"
scene_history = []

hollow_creek = game_map("assets/maps/hollow_creek.tmx")
interaction_system = interactions(hollow_creek.interactables)

camera_controller = camera(
    hollow_creek.pixel_width,
    hollow_creek.pixel_height
)

player_character = None
important_character = None


def change_scene(new_scene):
    global current_screen, scene_history

    scene_history.append(current_screen)
    current_screen = new_scene


def go_back():
    global current_screen, scene_history

    if current_screen == "game":
        current_screen = "menu"
        scene_history.clear()

    elif scene_history:
        current_screen = scene_history.pop()

    else:
        current_screen = "menu"


def toggle_fullscreen():
    global screen

    settings_screen.fullscreen = not settings_screen.fullscreen

    if settings_screen.fullscreen:
        screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode(
            (screen_width, screen_height)
        )

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)


def take_screenshot():
    os.makedirs("screenshots", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshots/crescent_{timestamp}.png"

    pygame.image.save(screen, filename)
    print(f"Screenshot saved: {filename}")


def main():
    global current_screen, active_field, option
    global player_character, important_character, screen

    active_field = 0
    run = True

    while run:
        dt = clock.tick(60)
        option = None
        screenshot_requested = False

        screen.fill(blue)
        interaction_system.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.WINDOWFOCUSGAINED:
                pygame.event.set_grab(False)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    screenshot_requested = True
                    continue

                elif event.key == pygame.K_ESCAPE:
                    go_back()
                    continue

                elif event.key == pygame.K_F1:
                    toggle_fullscreen()
                    continue

                elif (
                    current_screen == "game"
                    and player_character is not None
                    and event.key == player_character.keybinds["Interact"]
                ):
                    interaction_system.start_interaction()

            if current_screen == "menu":
                option = menu.menu_selection(event)

            elif current_screen == "character_creation":
                temp_active_fld = character_screen.field_selection(event)

                if temp_active_fld == 3:
                    go_back()

                elif temp_active_fld == 2:

                    # Remove the previous NPC when starting a new game
                    if important_character is not None:
                        hollow_creek.collision_rects.remove(
                            important_character.rect
                        )

                        hollow_creek.interactables = [
                            item for item in hollow_creek.interactables
                            if item["name"] != "npc"
                        ]

                        # Keep the interaction system connected to the list
                        interaction_system.interactables = hollow_creek.interactables

                    # Create the player
                    player_character = player(
                        character_screen.name,
                        character_screen.gender,
                        hollow_creek.pixel_width,
                        hollow_creek.pixel_height,
                        settings_screen.keybinds,
                        hollow_creek.collision_rects,
                        settings_screen.font_path
                    )

                    # Create the important character once
                    important_character = npc(
                        player_character.gender,
                        hollow_creek.interactables,
                        hollow_creek.collision_rects,
                        settings_screen.font_path
                    )

                    change_scene("game")

                elif temp_active_fld is not None:
                    active_field = temp_active_fld

                character_screen.name_selection(event)
                character_screen.gender_selection(event)

            elif current_screen == "settings":
                screen, current_screen = settings_screen.handle_event(
                    event,
                    screen
                )

        # Main menu
        if current_screen == "menu":
            menu.draw_menu(screen, settings_screen)

            if option is not None:

                if option == 0:
                    character_screen.active_field = 0
                    character_screen.name = ""
                    character_screen.gender = 0
                    change_scene("character_creation")

                elif option == 1:
                    if player_character is not None:
                        current_screen = "game"
                        scene_history.clear()

                elif option == 2:
                    settings_screen.option = 0
                    change_scene("settings")

                elif option == 3:
                    run = False

        # Character creation
        elif current_screen == "character_creation":
            character_screen.draw_character_creation(
                screen,
                settings_screen
            )

        # Settings
        elif current_screen == "settings":
            settings_screen.draw(screen)

        # Game
        elif current_screen == "game":

            player_character.movement()
            player_character.animate(dt)

            camera_controller.update(player_character, screen)
            interaction_system.check_nearby(player_character)

            # Draw the map
            hollow_creek.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            # Draw the NPC
            if important_character is not None:
                important_character.draw(
                    screen,
                    camera_controller.x,
                    camera_controller.y
                )

            # Draw the player
            player_character.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            # Draw interactions and objectives
            interaction_system.draw_prompt(screen, settings_screen)
            interaction_system.draw_dialog(screen, settings_screen)

            objective_system.draw(screen)

        if screenshot_requested:
            take_screenshot()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
