import pygame # type: ignore
import random

class Enemy:
    def __init__(self, screen_width, hasShield = False):
        # Enemy settings
        self._width = 50
        self._height = 60
        self._speed = 2
        
        self.x = random.randint(0, screen_width - self._width)
        self.y = -self._height
        self.health = 2 if hasShield else 1

        self.hitbox = (self.x, self.y, self._width, self._height)

        # Define Color
        r = random.randint(10, 255)
        g = random.randint(10, 255)
        b = random.randint(10, 255)
        self._color = (r, g, b)

    def render(self, screen):
        self.hitbox = (self.x, self.y, self._width, self._height)
        if(self.health > 1):
            pygame.draw.circle(screen, (0, 0, 200), (self.x + self._width / 2, self.y + self._height / 2), self._width / 2 + 20)
            self.hitbox = (self.x - 20, self.y, self._width + 40, self._height)
        pygame.draw.rect(screen, (self._color), (self.x, self.y, self._width, self._height))

    def updateState(self):
        self.y += self._speed