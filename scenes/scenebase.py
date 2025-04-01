"""Base module for scene management in the game, providing the foundation for all game scenes."""

import pygame
from pygame.key import ScancodeWrapper

class SceneBase:
    """Base class for all game scenes, providing common scene management functionality."""

    def __init__(self):
        """Initialize the scene with itself as the next scene."""
        self.next: 'SceneBase | None' = self

    def process_input(self, _events: list[pygame.event.Event], _pressed_keys: ScancodeWrapper):
        """Process input events and pressed keys. Should be overridden by child classes."""
        print("uh-oh, you didn't override this in the child class")

    def update(self, _dt : int):
        """Update the scene state. Should be overridden by child classes."""
        print("uh-oh, you didn't override this in the child class")

    def render(self, _screen : pygame.Surface):
        """Render the scene. Should be overridden by child classes."""
        print("uh-oh, you didn't override this in the child class")

    def switch_to_scene(self, next_scene : 'SceneBase') -> None:
        """Switch to the specified next scene."""
        self.next: 'SceneBase | None' = next_scene

    def terminate(self) -> None:
        """Terminate the current scene and stop the game loop."""
        self.next = None
