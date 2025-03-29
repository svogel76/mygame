import pygame # type: ignore

class Player:
    def __init__(self, screen_width, screen_height):
        # Player settings
        self.width = 50
        self.height = 60
        self._screen_width = screen_width
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 10
        self.speed = 5

    def render(self, screen):
        # Draw the player
        p1 = (self.x, self.y + self.height)
        p2 = (self.x + self.width, self.y + self.height)
        p3 = (self.x + self.width // 2, self.y )
        pygame.draw.polygon(screen, (0, 128, 255), [p1, p2, p3])        

    def handleInput(self, pressed_keys):
        # Handle player movement
        # keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if pressed_keys[pygame.K_RIGHT] and self.x < self._screen_width - self.width:
            self.x += self.speed