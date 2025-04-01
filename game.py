"""Main game module that initializes and runs the game loop."""
# pylint: disable=no-member
import pygame

from scenes import MenuScene

from engine import Engine

# Initialize PyGame
pygame.init()# pylint: disable=no-member

# Set up the game window
FPS : int = 60
SCREEN_WIDTH : int =  800
SCREEN_HEIGHT : int = 600
screen : pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Set the frame rate
clock = pygame.time.Clock()

engine = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, screen)

active_scene = MenuScene()

while active_scene is not None:
    dt = clock.tick(FPS)
    pressed_keys = pygame.key.get_pressed()

    # Event filtering
    filtered_events: list[pygame.event.Event] = []
    for event in pygame.event.get():
        quit_attempt : bool = False  # pylint: disable=C0103
        if event.type == pygame.QUIT:
            quit_attempt = True  # pylint: disable=C0103
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                            pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_ESCAPE:
                quit_attempt = True  # pylint: disable=C0103
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True  # pylint: disable=C0103

        if quit_attempt:
            active_scene.terminate()
        else:
            filtered_events.append(event)

    active_scene.process_input(filtered_events, pressed_keys)
    active_scene.update(dt)
    active_scene.render(screen)

    active_scene = active_scene.next

    pygame.display.flip()
