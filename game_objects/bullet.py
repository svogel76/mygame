import pygame # type: ignore

class Bullet:
    def __init__(self, posX, posY):
        # Bullet settings
        self._width : int = 5
        self._height : int = 10
        self._speed : int = 7

        self.x : int = posX - self._width // 2
        self.y : int = posY
        

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self._width, self._height))

    def updateState(self):
        self.y -= self._speed