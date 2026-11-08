
import pygame
from assets.colours import *


class interactions:
    def __init__(self, interactables):
        self.interactables = interactables
        self.active_interactable = None

        self.dialog = ""
        self.dialog_active = False
        self.dialog_cooldown = 0

        # Quest stages:
        # 0: Talk to Mara/Elliot
        # 1: Investigate pond
        # 2: Collect orb
        # 3: Talk to Thomas
        # 4: Collect photograph
        # 5: Talk to Evelyn
        # 6: Talk to Arthur
        # 7: Collect key
        # 8: Investigate red house
        # 9: Story complete

        self.quest_stage = 0

        self.clue_interactable = None
        self.clue_visible = False

        self.photo_interactable = None
        self.photo_visible = False

        self.key_interactable = None
        self.key_visible = False

        self.dialogues = {
            "pond": "The water is completely still...",
            "red_house": "The front door is locked. There is a strange scratching sound coming from inside...",
            "blue_house": "A blue house. The curtains are closed.",
            "black_house": "A dark, quiet-looking house.",
            "green_house": "A green house surrounded by greenery.",
            "npc": (
                "I've been waiting for you. Something strange is "
                "happening in Hollow Creek."
            ),
            "pond_clue": "There is something strange here.",
            "blue_house_npc": (
                "You found the orb? Thomas studies it carefully. "
                "I've seen something like this before. I lost an old "
                "photograph that might explain it. Could you find it?"
            ),
            "black_house_npc": (
                "Evelyn examines the photograph. I recognise this place. "
                "Arthur knows more about what happened here. "
                "You should speak to him."
            ),
            "green_house_npc": (
                "Arthur studies the photograph. So it's happening again... "
                "I hid a key near my house. Take it. The red house must be opened."
            ),
            "photograph": (
                "You found an old photograph. There is something written "
                "on the back: HOLLOW CREEK, 1987."
            ),
            "red_house_key": "You found an old brass key. It might open the red house.",
            "red_house_note": (
                "Inside the red house, you discover a note. It reads: "
                "'If you are reading this, then the water has chosen "
                "someone new. Do not trust what you remember. "
                "None of Hollow Creek is what it seems.'"
            )
        }

    def reset_story(self):
        self.dialog_active = False
        self.active_interactable = None
        self.dialog_cooldown = 0
        self.dialog = ""
        self.quest_stage = 0

        # Remove old quest items
        for item in (
            self.clue_interactable,
            self.photo_interactable,
            self.key_interactable
        ):
            if item is not None and item in self.interactables:
                self.interactables.remove(item)

        self.clue_interactable = None
        self.clue_visible = False

        self.photo_interactable = None
        self.photo_visible = False

        self.key_interactable = None
        self.key_visible = False

    def spawn_item(self, house_name, item_name):
        house = None

        for interactable in self.interactables:
            if interactable["name"] == house_name:
                house = interactable["rect"]
                break

        if house is None:
            print("Could not find house:", house_name)
            return None

        item_rect = pygame.Rect(
            house.left - 350,
            house.centery - 14,
            28,
            28
        )

        item = {
            "name": item_name,
            "class": "item",
            "rect": item_rect
        }

        self.interactables.append(item)
        return item

    def create_pond_clue(self):
        if self.clue_interactable is not None:
            return

        pond = None

        for item in self.interactables:
            if item["name"] == "pond":
                pond = item["rect"]
                break

        if pond is None:
            return

        self.clue_interactable = {
            "name": "pond_clue",
            "class": "clue",
            "rect": pygame.Rect(
                pond.right + 35,
                pond.centery - 14,
                28,
                28
            )
        }

        self.interactables.append(self.clue_interactable)
        self.clue_visible = True

    def draw_item(self, screen, item, camera_x, camera_y, colour):
        if item is None:
            return

        rect = item["rect"]

        x = int(rect.centerx - camera_x)
        y = int(rect.centery - camera_y)

        pygame.draw.circle(screen, colour, (x, y), 12)
        pygame.draw.circle(screen, white, (x, y), 5)

    def draw_pond_clue(self, screen, camera_x, camera_y):
        if self.clue_visible:
            self.draw_item(
                screen,
                self.clue_interactable,
                camera_x,
                camera_y,
                (255, 210, 90)
            )

    def draw_photo(self, screen, camera_x, camera_y):
        if self.photo_visible:
            self.draw_item(
                screen,
                self.photo_interactable,
                camera_x,
                camera_y,
                (180, 180, 220)
            )

    def draw_red_house_key(self, screen, camera_x, camera_y):
        if self.key_visible:
            self.draw_item(
                screen,
                self.key_interactable,
                camera_x,
                camera_y,
                (255, 210, 50)
            )

    def check_nearby(self, player):
        self.active_interactable = None

        player_cx = player.x + player.width / 2
        player_cy = player.y + player.height / 2

        nearest_distance = float("inf")

        for interactable in self.interactables:
            expanded_rect = interactable["rect"].inflate(96, 96)

            if expanded_rect.collidepoint((player_cx, player_cy)):
                distance_x = interactable["rect"].centerx - player_cx
                distance_y = interactable["rect"].centery - player_cy

                distance = distance_x ** 2 + distance_y ** 2

                if distance < nearest_distance:
                    nearest_distance = distance
                    self.active_interactable = interactable

        return self.active_interactable is not None

    def handle_interaction(self, name, objective_system):

        # Stage 0: Talk to Mara / Elliot
        if name == "npc" and self.quest_stage == 0:
            self.dialog = self.dialogues["npc"]

            self.quest_stage = 1
            objective_system.complete_objective()

        # Stage 1: Investigate the pond
        elif name == "pond" and self.quest_stage == 1:
            self.dialog = (
                "Wait... something is moving beneath the water. "
                "That shouldn't be possible. There is something "
                "beside the pond..."
            )

            self.create_pond_clue()

            self.quest_stage = 2
            objective_system.complete_objective()

        elif name == "pond" and self.quest_stage < 1:
            self.dialog = "Perhaps I should speak to someone first."

        # Stage 2: Collect the orb
        elif name == "pond_clue" and self.quest_stage == 2:
            self.dialog = (
                "You found a mysterious orb. It feels unusually cold. "
                "There is something engraved on it: DON'T TRUST THE WATER."
            )

            if self.clue_interactable in self.interactables:
                self.interactables.remove(self.clue_interactable)

            self.clue_interactable = None
            self.clue_visible = False

            self.quest_stage = 3
            objective_system.complete_objective()

        # Stage 3: Talk to Thomas
        elif name == "blue_house_npc" and self.quest_stage == 3:
            self.dialog = self.dialogues["blue_house_npc"]

            self.photo_interactable = self.spawn_item(
                "blue_house",
                "photograph"
            )

            self.photo_visible = self.photo_interactable is not None

            self.quest_stage = 4
            objective_system.complete_objective()

        elif name == "blue_house_npc" and self.quest_stage < 3:
            self.dialog = "Thomas seems busy. I should investigate the pond first."

        # Stage 4: Collect the photograph
        elif name == "photograph" and self.quest_stage == 4:
            self.dialog = self.dialogues["photograph"]

            if self.photo_interactable in self.interactables:
                self.interactables.remove(self.photo_interactable)

            self.photo_interactable = None
            self.photo_visible = False

            self.quest_stage = 5
            objective_system.complete_objective()

        # Stage 5: Talk to Evelyn
        elif name == "black_house_npc" and self.quest_stage == 5:
            self.dialog = self.dialogues["black_house_npc"]

            self.quest_stage = 6

            # Speaking to Evelyn completes the black house objective
            objective_system.complete_objective()
            objective_system.complete_objective()

        elif name == "black_house_npc" and self.quest_stage < 5:
            self.dialog = "There is no reason to visit Evelyn yet."

        # Stage 6: Talk to Arthur
        elif name == "green_house_npc" and self.quest_stage == 6:
            self.dialog = self.dialogues["green_house_npc"]

            self.key_interactable = self.spawn_item(
                "green_house",
                "red_house_key"
            )

            self.key_visible = self.key_interactable is not None

            self.quest_stage = 7
            objective_system.complete_objective()

        elif name == "green_house_npc" and self.quest_stage < 6:
            self.dialog = "I should speak to Evelyn first."

        # Stage 7: Collect the key
        elif name == "red_house_key" and self.quest_stage == 7:
            self.dialog = self.dialogues["red_house_key"]

            if self.key_interactable in self.interactables:
                self.interactables.remove(self.key_interactable)

            self.key_interactable = None
            self.key_visible = False

            self.quest_stage = 8
            objective_system.complete_objective()

        # Stage 8: Investigate the red house
        elif name == "red_house" and self.quest_stage == 8:
            self.dialog = self.dialogues["red_house_note"]

            self.quest_stage = 9

            # Complete the red house and final mystery objectives
            objective_system.complete_objective()
            objective_system.complete_objective()

        elif name == "red_house" and self.quest_stage < 8:
            self.dialog = "The door is locked. I need to find a key."

        elif name == "red_house" and self.quest_stage == 9:
            self.dialog = "The note... I should think about what it means."

        else:
            self.dialog = self.dialogues.get(
                name,
                "There doesn't seem to be anything here."
            )

        self.dialog_active = True
        self.dialog_cooldown = 17

    def start_interaction(self):
        # This method only closes an open dialogue.
        if self.dialog_active and self.dialog_cooldown <= 0:
            self.dialog_active = False

    def draw_dialog(self, screen, settings_screen):
        if not self.dialog_active:
            return

        dialog_font = pygame.font.Font(
            settings_screen.font_path,
            28
        )

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
            dialog_surface = dialog_font.render(
                line,
                True,
                white
            )

            text_rect = dialog_surface.get_rect()
            text_rect.x = dialog_rect.x + 20
            text_rect.y = dialog_rect.y + 20 + index * line_height

            screen.blit(dialog_surface, text_rect)

    def draw_prompt(self, screen, settings_screen):
        if self.active_interactable is not None and not self.dialog_active:
            prompt_font = pygame.font.Font(
                settings_screen.font_path,
                46
            )

            prompt_surface = prompt_font.render(
                "[E] Interact",
                True,
                black
            )

            prompt_rect = prompt_surface.get_rect()
            prompt_rect.centerx = screen.get_width() / 2
            prompt_rect.centery = screen.get_height() - 60

            screen.blit(prompt_surface, prompt_rect)

    def update(self):
        if self.dialog_cooldown > 0:
            self.dialog_cooldown -= 1
