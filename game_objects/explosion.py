# explosion.py
import pygame
import random

class ExplosionParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 500  # in Millisekunden
        self.size = random.randint(2, 4)
        self.color = (
            random.randint(200, 255),
            random.randint(50, 100),
            random.randint(0, 50)
        )

    def updateState(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.life -= dt

    def render(self, screen):
        if self.life > 0:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def is_dead(self):
        return self.life <= 0
