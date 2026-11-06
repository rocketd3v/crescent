
import pygame
from settings import *
from assets.colours import *

class settings_menu():
    def __init__(self):
        self.options = ["Fullscreen", "Volume", "Interact", "Move up", "Move down", "Move right", "Move left", "Open menu", "Back"]

        self.keybinds = {"Interact": pygame.K_e, "Move up": pygame.K_w, "Move down": pygame.K_s, "Move right": pygame.K_d, "Move left": pygame.K_a, "Open menu": pygame.K_ESCAPE}

        self.option = 0
        self.fullscreen = False
        self.volume = 100

    def handle_event(self, event, screen):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.option -= 1

                if self.option < 0:
                    self.option = len(self.options) - 1

            elif event.key == pygame.K_DOWN:
                self.option += 1

                if self.option >= len(self.options):
                    self.option = 0

            elif self.option == 1:
                if event.key == pygame.K_LEFT:
                    self.volume = min(100, self.volume - 5)

                elif event.key == pygame.K_RIGHT:
                    self.volume = max(0, self.volume + 5)

            elif self.option >= 2 and self.option <= 7:
                if event.key not in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    option_name = self.options[self.option]
                    self.keybinds[option_name] = event.key

            elif event.key == pygame.K_ESCAPE:
                return screen, "menu"

            elif event.key == pygame.K_RETURN:
                if self.option == len(self.options) - 1:
                    return screen, "menu"

        return screen, "settings"

    def draw(self, screen):
        title_surface = gluten_title_font.render("SETTINGS", True, black)
        title_rect = title_surface.get_rect()
        title_rect.centerx = screen_width / 2
        title_rect.centery = screen_height / 10

        screen.blit(title_surface, title_rect)

        for option in range(len(self.options)):
            option_name = self.options[option]

            if option_name == "Fullscreen":
                value = "ON" if self.fullscreen else "OFF"
                value += " (F11)"

            elif option_name == "Volume":
                value = f"{self.volume}%"

            elif option_name == "Back":
                value = ""

            else:
                key = self.keybinds[option_name]
                value = pygame.key.name(key).upper()

            text = f"> {option_name}: {value}"

            if option_name == "Back":
                text = "> Back"

            if option == self.option:
                option_surface = gluten_menu_font.render(text, True, yellow)
            else:
                option_surface = gluten_menu_font.render(text, True, black)

            option_rect = option_surface.get_rect()
            option_rect.centerx = screen_width / 2
            option_rect.centery = (screen_height / 4) + (option * 48)

            screen.blit(option_surface, option_rect)
