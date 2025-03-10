import pygame # type: ignore
import sys

from engine import Engine

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width =  800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

# Set the frame rate
clock = pygame.time.Clock()

engine = Engine(screen_width, screen_height, screen)

# Main game loop
while True:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            engine.handleInput(event) 

    engine.player.handleInput()

    engine.updateStates()

    engine.render()    

    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)