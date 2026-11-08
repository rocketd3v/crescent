
import pygame
import os
from settings import *
from assets.colours import *


class settings_menu():
    def __init__(self):
        self.options = [
            "Fullscreen",
            "Volume",
            "Font",
            "Interact",
            "Move up",
            "Move down",
            "Move right",
            "Move left",
            "Open menu",
            "Back"
        ]

        self.default_keybinds = {
            "Interact": pygame.K_e,
            "Move up": pygame.K_w,
            "Move down": pygame.K_s,
            "Move right": pygame.K_d,
            "Move left": pygame.K_a,
            "Open menu": pygame.K_ESCAPE
        }

        self.keybinds = self.default_keybinds.copy()

        self.option = 0
        self.fullscreen = False
        self.volume = 100

        self.fonts = sorted([
            font for font in os.listdir("assets/fonts")
            if font.endswith((".ttf", ".otf"))
        ])

        self.default_font = "gluten_font.ttf"
        self.font_index = self.fonts.index(self.default_font)

        self.font_path = os.path.join(
            "assets/fonts",
            self.fonts[self.font_index]
        )

    def reset_settings(self):
        self.fullscreen = False
        self.volume = 100
        self.keybinds = self.default_keybinds.copy()

        self.font_index = self.fonts.index(self.default_font)

        self.font_path = os.path.join(
            "assets/fonts",
            self.fonts[self.font_index]
        )

    def handle_event(self, event, screen):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                self.reset_settings()

            elif event.key == pygame.K_UP:
                self.option -= 1

                if self.option < 0:
                    self.option = len(self.options) - 1

            elif event.key == pygame.K_DOWN:
                self.option += 1

                if self.option >= len(self.options):
                    self.option = 0

            elif self.option == 1:
                if event.key == pygame.K_LEFT:
                    self.volume = max(0, self.volume - 5)

                elif event.key == pygame.K_RIGHT:
                    self.volume = min(100, self.volume + 5)

            elif self.option == 2:
                if event.key == pygame.K_LEFT:
                    self.font_index -= 1

                    if self.font_index < 0:
                        self.font_index = len(self.fonts) - 1

                elif event.key == pygame.K_RIGHT:
                    self.font_index += 1

                    if self.font_index >= len(self.fonts):
                        self.font_index = 0

                self.font_path = os.path.join(
                    "assets/fonts",
                    self.fonts[self.font_index]
                )

            elif 3 <= self.option <= 8:
                if event.key not in [
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT
                ]:
                    option_name = self.options[self.option]
                    self.keybinds[option_name] = event.key

            elif event.key == pygame.K_ESCAPE:
                return screen, "menu"

            elif event.key == pygame.K_RETURN:
                if self.option == len(self.options) - 1:
                    return screen, "menu"

        return screen, "settings"

    def draw(self, screen):
        title_font = pygame.font.Font(self.font_path, 76)
        menu_font = pygame.font.Font(self.font_path, 46)

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Title
        title_surface = title_font.render("SETTINGS", True, gray)

        title_rect = title_surface.get_rect()
        title_rect.centerx = screen_width // 2
        title_rect.centery = screen_height // 10

        screen.blit(title_surface, title_rect)

        # Options
        for option in range(len(self.options)):
            option_name = self.options[option]

            if option_name == "Fullscreen":
                value = "ON" if self.fullscreen else "OFF"
                value += " (F1)"

            elif option_name == "Volume":
                value = f"{self.volume}%"

            elif option_name == "Font":
                font_name = self.fonts[self.font_index]

                value = (
                    os.path.splitext(font_name)[0]
                    .replace("_", " ")
                    .replace("font", "")
                    .strip()
                    .title()
                )

            elif option_name == "Back":
                value = ""

            else:
                key = self.keybinds[option_name]
                value = pygame.key.name(key).upper()

            if option_name == "Back":
                text = "> Back" if option == self.option else "Back"

            elif option == self.option:
                text = f"> {option_name}: {value}"

            else:
                text = f"{option_name}: {value}"

            colour = yellow if option == self.option else black

            option_surface = menu_font.render(
                text,
                True,
                colour
            )

            option_rect = option_surface.get_rect()
            option_rect.centerx = screen_width // 2
            option_rect.centery = (screen_height // 4) + (option * 48)

            screen.blit(option_surface, option_rect)

        # Reset instructions
        reset_font = pygame.font.Font(self.font_path, 20)

        reset_surface = reset_font.render(
            "Press R to reset settings to default",
            True,
            gray
        )

        reset_rect = reset_surface.get_rect()
        reset_rect.centerx = screen_width // 2
        reset_rect.bottom = screen_height - 20

        screen.blit(reset_surface, reset_rect)
