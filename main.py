import pygame

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
from game.npc import npc, house_npc


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

# Ending screen
ending_alpha = 0

hollow_creek = game_map("assets/maps/hollow_creek.tmx")
interaction_system = interactions(hollow_creek.interactables)

camera_controller = camera(
    hollow_creek.pixel_width,
    hollow_creek.pixel_height
)

player_character = None
important_character = None


# Create the house residents once.

blue_npc = house_npc(
    "Thomas",
    "blue_house",
    hollow_creek.interactables,
    hollow_creek.collision_rects,
    settings_screen.font_path
)

black_npc = house_npc(
    "Evelyn",
    "black_house",
    hollow_creek.interactables,
    hollow_creek.collision_rects,
    settings_screen.font_path
)

green_npc = house_npc(
    "Arthur",
    "green_house",
    hollow_creek.interactables,
    hollow_creek.collision_rects,
    settings_screen.font_path
)


def change_scene(new_scene):
    global current_screen, scene_history

    scene_history.append(current_screen)
    current_screen = new_scene


def go_back():
    global current_screen, scene_history

    if current_screen == "ending":
        current_screen = "menu"
        scene_history.clear()

    elif current_screen == "game":
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


def draw_ending():
    global ending_alpha

    # Fade to black
    screen.fill((0, 0, 0))

    if ending_alpha < 255:
        ending_alpha = min(255, ending_alpha + 4)

    # Ending title
    title_font = pygame.font.Font(
        settings_screen.font_path,
        76
    )

    title_surface = title_font.render(
        "THE END",
        True,
        white
    )

    title_surface.set_alpha(ending_alpha)

    title_rect = title_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 - 50)
    )

    screen.blit(title_surface, title_rect)

    # Return to menu option
    button_font = pygame.font.Font(
        settings_screen.font_path,
        32
    )

    button_surface = button_font.render(
        "Return to Main Menu",
        True,
        white
    )

    button_surface.set_alpha(ending_alpha)

    button_rect = button_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 50)
    )

    screen.blit(button_surface, button_rect)


def main():
    global current_screen, active_field, option
    global player_character, important_character, screen
    global ending_alpha

    active_field = 0
    run = True

    while run:
        dt = clock.tick(60)
        option = None

        screen.fill(blue)
        interaction_system.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.WINDOWFOCUSGAINED:
                pygame.event.set_grab(False)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    if current_screen == "ending":
                        current_screen = "menu"
                        scene_history.clear()
                    else:
                        go_back()

                    continue

                elif event.key == pygame.K_F1:
                    toggle_fullscreen()
                    continue

                # Ending screen controls
                elif current_screen == "ending":

                    if event.key in (
                        pygame.K_RETURN,
                        pygame.K_SPACE
                    ):
                        current_screen = "menu"
                        scene_history.clear()

                # Interactions
                elif (
                    current_screen == "game"
                    and player_character is not None
                    and event.key == player_character.keybinds["Interact"]
                ):

                    if interaction_system.dialog_active:
                        interaction_system.start_interaction()

                    elif interaction_system.active_interactable is not None:

                        interactable_name = (
                            interaction_system.active_interactable["name"]
                        )

                        print("Interacted with:", interactable_name)

                        interaction_system.handle_interaction(
                            interactable_name,
                            objective_system
                        )

            # Mouse controls for ending screen
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and current_screen == "ending"
            ):
                current_screen = "menu"
                scene_history.clear()

            if current_screen == "menu":
                option = menu.menu_selection(event)

            elif current_screen == "character_creation":

                temp_active_fld = character_screen.field_selection(event)

                if temp_active_fld == 3:
                    go_back()

                elif temp_active_fld == 2:

                    # Remove the previous Mara / Elliot
                    if important_character is not None:

                        if important_character.rect in hollow_creek.collision_rects:
                            hollow_creek.collision_rects.remove(
                                important_character.rect
                            )

                        hollow_creek.interactables = [
                            item for item in hollow_creek.interactables
                            if item["name"] != "npc"
                        ]

                        interaction_system.interactables = (
                            hollow_creek.interactables
                        )

                    # Reset objectives
                    objective_system.current_objective = 0
                    objective_system.completed = False

                    # Reset quest progress and remove quest items
                    interaction_system.reset_story()

                    # Reset ending fade
                    ending_alpha = 0

                    # Create player
                    player_character = player(
                        character_screen.name,
                        character_screen.gender,
                        hollow_creek.pixel_width,
                        hollow_creek.pixel_height,
                        settings_screen.keybinds,
                        hollow_creek.collision_rects,
                        settings_screen.font_path
                    )

                    # Create Mara / Elliot
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

        # Detect when the final note dialogue has been closed.
        if (
            current_screen == "game"
            and interaction_system.quest_stage == 9
            and not interaction_system.dialog_active
        ):
            current_screen = "ending"
            ending_alpha = 0

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

                        # Continue to the ending if the story is finished.
                        if interaction_system.quest_stage == 9:
                            current_screen = "ending"
                            ending_alpha = 0
                        else:
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

            hollow_creek.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            # Draw quest items
            interaction_system.draw_pond_clue(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            interaction_system.draw_photo(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            interaction_system.draw_red_house_key(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            # Draw house residents
            blue_npc.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            black_npc.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            green_npc.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            # Draw Mara / Elliot
            if important_character is not None:
                important_character.draw(
                    screen,
                    camera_controller.x,
                    camera_controller.y
                )

            player_character.draw(
                screen,
                camera_controller.x,
                camera_controller.y
            )

            interaction_system.draw_prompt(screen, settings_screen)
            interaction_system.draw_dialog(screen, settings_screen)

            objective_system.draw(screen)

        # Ending
        elif current_screen == "ending":

            draw_ending()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
