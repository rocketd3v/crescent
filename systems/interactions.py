
import pygame
from assets.colours import *


class interactions():
    def __init__(self, interactables):
        self.interactables = interactables
        self.active_interactable = None
        self.dialog = ""
        self.dialog_active = False
        self.dialog_cooldown = 0

        self.dialogues = {
            "pond": "The water is completely still...",
            "red_house": "A red house. Someone lives here.",
            "blue_house": "A blue house. The curtains are closed.",
            "black_house": "A dark, quiet-looking house.",
            "green_house": "A green house surrounded by greenery."
        }

    def check_nearby(self, player):
        self.active_interactable = None

        for interactable in self.interactables:
            player_cx = player.x + player.width / 2
            player_cy = player.y + player.height / 2

            player_center = (player_cx, player_cy)

            expanded_interactable = interactable["rect"].inflate(96, 96)
            nearby = expanded_interactable.collidepoint(player_center)

            if nearby:
                self.active_interactable = interactable
                return True

        return False

    def start_interaction(self):
        if self.dialog_active:
            if self.dialog_cooldown <= 0:
                self.dialog_active = False

        elif self.active_interactable is not None:
            self.dialog_active = True

            interactable_name = self.active_interactable["name"]

            self.dialog = self.dialogues.get(
                interactable_name,
                "There doesn't seem to be anything here."
            )

            self.dialog_cooldown = 17

    def draw_dialog(self, screen, settings_screen):
        if self.dialog_active:

            dialog_font = pygame.font.Font(settings_screen.font_path, 28)

            dialog_lines = []
            words = self.dialog.split()
            current_line = ""

            for word in words:
                test_line = current_line + word + " "

                if dialog_font.size(test_line)[0] > screen.get_width() - 120:
                    if current_line:
                        dialog_lines.append(current_line)

                    current_line = word + " "
                else:
                    current_line = test_line

            if current_line:
                dialog_lines.append(current_line)

            line_height = dialog_font.get_linesize()
            dialog_height = len(dialog_lines) * line_height + 40

            dialog_rect = pygame.Rect(
                40,
                screen.get_height() - dialog_height - 20,
                screen.get_width() - 80,
                dialog_height
            )

            pygame.draw.rect(screen, (20, 20, 30), dialog_rect)

            for index, line in enumerate(dialog_lines):
                dialog_surface = dialog_font.render(line, True, white)

                text_rect = dialog_surface.get_rect()
                text_rect.x = dialog_rect.x + 20
                text_rect.y = dialog_rect.y + 20 + index * line_height

                screen.blit(dialog_surface, text_rect)

    def draw_prompt(self, screen, settings_screen):
        if self.active_interactable is not None and not self.dialog_active:
            prompt_font = pygame.font.Font(settings_screen.font_path, 46)
            prompt_surface = prompt_font.render("[E] Interact", True, black)

            prompt_rect = prompt_surface.get_rect()
            prompt_rect.centerx = screen.get_width() / 2
            prompt_rect.centery = screen.get_height() - 60

            screen.blit(prompt_surface, prompt_rect)

    def update(self):
        if self.dialog_cooldown > 0:
            self.dialog_cooldown -= 1
