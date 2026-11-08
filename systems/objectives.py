
import pygame
from assets.colours import *


class objective_tracker:
    def __init__(self, font_path):
        self.font = pygame.font.Font(font_path, 24)

        self.objectives = [
            "Talk to Mara/Elliot",
            "Investigate the strange water",
            "Find the mysterious orb",
            "Investigate the blue house",
            "Complete the blue house quest",
            "Investigate the black house",
            "Complete the black house quest",
            "Investigate the green house",
            "Complete the green house quest",
            "Investigate the abandoned red house",
            "Uncover the mystery of Hollow Creek"
        ]

        self.current_objective = 0
        self.completed = False

    def complete_objective(self):
        if self.completed:
            return

        print("Objective completed!")

        if self.current_objective < len(self.objectives) - 1:
            self.current_objective += 1
            print("New objective:", self.objectives[self.current_objective])
        else:
            self.completed = True
            print("All objectives completed!")

    def draw(self, screen):
        if self.completed:
            text = "All objectives completed"
        else:
            text = "Objective: " + self.objectives[self.current_objective]

        surface = self.font.render(text, True, white)

        background = pygame.Rect(
            15,
            15,
            surface.get_width() + 30,
            surface.get_height() + 20
        )

        pygame.draw.rect(screen, (20, 20, 30), background)
        screen.blit(surface, (30, 25))
