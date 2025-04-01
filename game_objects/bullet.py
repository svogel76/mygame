"""Module containing the Bullet class for the game."""

import pygame

class Bullet:
    """A bullet object that can be fired by the player."""

    def __init__(self, pos_x : int, pos_y : int):
        """Initialize a bullet at the given position."""
        # Bullet settings
        self.width : int = 5
        self.height : int = 10
        self._speed : int = 7

        self.x : int = pos_x - self.width // 2
        self.y : int = pos_y

    def render(self, screen : pygame.Surface):
        """Render the bullet on the given screen."""
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def update_state(self):
        """Update the bullet's position."""
        self.y -= self._speed
