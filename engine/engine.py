import pygame # type: ignore
import random
from game_objects import Player, Bullet, Enemy

class Engine:
    def __init__(self, screen_width : int, screen_height : int, screen):
        # PLAYER
        self.player : Player = Player(screen_width, screen_height)

        # GAME OBJECTS
        self._bullets : list[Bullet] = []
        self._enemies : list[Enemy] = []

        # GAME SETTINGS
        self._enemy_timer = 0
        self._enemy_spawn_time = 2000 # Spawn an enemy every 2 seconds
        
        # GRAPHICS SETTINGS
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = screen

        # GAME STATE
        self._hits = 0

    # Collision detection function
    def __check_collision(self, rect1, rect2):
        return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

    def handleInput(self, event):    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a bullet at the current player position
                self._bullets.append(Bullet(self.player.x + self.player.width // 2, self.player.y))

    def updateStates(self):
        for bullet in self._bullets:
            bullet.updateState()
        self._bullets = [bullet for bullet in self._bullets if bullet.y > 0]

        # Spawn new ones
        current_time = pygame.time.get_ticks()
        if current_time - self._enemy_timer > self._enemy_spawn_time:
            hasShield = True if random.randint(0, 10) > 5 else False
            self._enemies.append(Enemy(self._screen_width, hasShield))
            self._enemy_timer = current_time

        # Update enemy positions
        for enemy in self._enemies:
            enemy.updateState()

        # Check for collisions
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                if self.__check_collision((bullet.x, bullet.y, bullet._width, bullet._height),
                                (enemy.hitbox)):
                    # Ziel wurde getroffen
                    enemy.health -= 1
                    self._bullets.remove(bullet)
                    if enemy.health <= 0:
                        self._enemies.remove(enemy) 
                        self._hits += 1 
                    break

        # Remove enemies that are off the screen
        self._enemies = [enemy for enemy in self._enemies if enemy.y < self._screen_height]

    def render(self):
        self._screen.fill((0, 0, 0))

        self.player.render(self._screen)

        # Draw the bullets
        for bullet in self._bullets:
            bullet.render(self._screen)

        # Draw the enemies
        for enemy in self._enemies:
            enemy.render(self._screen)

        font = pygame.font.SysFont("Arial", 16)
        txtsurf = font.render(f"Treffer: {self._hits}", True, (255,255,255))
        self._screen.blit(txtsurf,(50 - txtsurf.get_width() // 2, 20 - txtsurf.get_height() // 2))