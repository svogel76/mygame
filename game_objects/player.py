"""Module containing the Player class for the game."""

# pylint: disable=no-member
import pygame # type: ignore
from pygame.key import ScancodeWrapper

class Player:
    """Player class that handles player movement and rendering."""

    def __init__(self, screen_width : int, screen_height : int):
        """Initialize the player with screen dimensions and default settings."""
        # Player settings
        self.width = 50
        self.height = 60
        self._screen_width = screen_width
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 10
        self.speed = 5
        self.lives = 3

    def render(self, screen : pygame.Surface):
        """Render the player as a triangle on the given screen."""
        # Draw the player
        p1 = (self.x, self.y + self.height)
        p2 = (self.x + self.width, self.y + self.height)
        p3 = (self.x + self.width // 2, self.y )
        pygame.draw.polygon(screen, (0, 128, 255), [p1, p2, p3])        

    def handle_input(self, pressed_keys : ScancodeWrapper) -> None:
        """Handle player movement based on keyboard input."""
        # Handle player movement
        # keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if pressed_keys[pygame.K_RIGHT] and self.x < self._screen_width - self.width:
            self.x += self.speed