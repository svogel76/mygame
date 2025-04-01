"""Menu scene module that handles the game's main menu and scene transitions."""

# pylint: disable=no-member
import pygame # type: ignore
from pygame.key import ScancodeWrapper
from scenes import SceneBase, GameScene

class MenuScene(SceneBase):
    """Menu scene that handles the game's main menu and scene transitions."""

    def __init__(self):
        SceneBase.__init__(self)

    def process_input(self, events : list[pygame.event.Event], _pressed_keys : ScancodeWrapper) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.switch_to_scene(GameScene())

    def update(self, dt : int) -> None:
        pass

    def render(self, screen : pygame.Surface) -> None:
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        w, h = pygame.display.get_surface().get_size()

        font = pygame.font.SysFont("Arial", 16)
        txtsurf = font.render("Zum STARTEN, Return Taste drücken", True, (255,255,255))
        screen.blit(txtsurf,((w - txtsurf.get_width()) // 2, (h - txtsurf.get_height()) // 2))
