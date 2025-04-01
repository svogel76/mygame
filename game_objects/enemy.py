"""Module containing the Enemy class for the game."""

import random
import pygame # type: ignore


class Enemy:
    """Enemy class has health and an optional shield"""
    def __init__(self, screen_width : int, has_shield : bool = False):
        # Enemy settings
        self.width = 50
        self.height = 50
        self._speed = 2

        self.x : int = random.randint(0, screen_width - self.width)
        self.y : int = -self.height
        self.health : int = 2 if has_shield else 1

        self.hitbox = (self.x, self.y, self.width, self.height)

        # Define Color
        r = random.randint(10, 255)
        g = random.randint(10, 255)
        b = random.randint(10, 255)
        self._color = (r, g, b)

    def render(self, screen : pygame.Surface) -> None:
        """renders the enemy"""
        self.hitbox = (self.x, self.y, self.width, self.height)
        if self.health > 1:
            center : tuple[float, float] = (self.x + self.width / 2, self.y + self.height / 2)
            radius : float = self.width / 2 + 20
            pygame.draw.circle(screen, (0, 0, 200), center, radius)
            self.hitbox = (self.x - 20, self.y, self.width + 40, self.height)
        pygame.draw.rect(screen, (self._color), (self.x, self.y, self.width, self.height))

    def update_state(self) -> None:
        """updates enemy position depending on speed"""
        self.y += self._speed
