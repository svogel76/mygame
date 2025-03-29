import pygame # type: ignore
import sys

from scenes import MenuScene

from engine import Engine

# Initialize PyGame
pygame.init()

# Set up the game window
fps = 60
screen_width =  800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

# Set the frame rate
clock = pygame.time.Clock()

engine = Engine(screen_width, screen_height, screen)

active_scene = MenuScene()

while active_scene != None:
    pressed_keys = pygame.key.get_pressed()
    
    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                            pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_ESCAPE:
                quit_attempt = True
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True
        
        if quit_attempt:
            active_scene.Terminate()
        else:
            filtered_events.append(event)
    
    active_scene.ProcessInput(filtered_events, pressed_keys)
    active_scene.Update()
    active_scene.Render(screen)
    
    active_scene = active_scene.next
    
    pygame.display.flip()
    clock.tick(fps)