"""Engine module that handles core game mechanics and state management."""

# pylint: disable=no-member
import random
import pygame
from game_objects import Player, Bullet, Enemy

class Engine:
    """Engine class that manages game state, objects, and rendering."""

    def __init__(self, screen_width : int, screen_height : int, screen : pygame.Surface):
        """Initialize the game engine with screen dimensions and surface."""
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

    def __check_collision(
        self,
        rect1: tuple[int, int, int, int],
        rect2: tuple[int, int, int, int]
    ) -> bool:
        """Check if two rectangles are colliding."""
        return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

    def handle_input(self, event : pygame.event.Event) -> None:
        """Handle keyboard input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a bullet at the current player position
                self._bullets.append(Bullet(self.player.x + self.player.width // 2, self.player.y))

    def update_states(self) -> None:
        """Update the state of all game objects."""
        for bullet in self._bullets:
            bullet.update_state()
        self._bullets = [bullet for bullet in self._bullets if bullet.y > 0]

        # Spawn new ones
        current_time = pygame.time.get_ticks()
        if current_time - self._enemy_timer > self._enemy_spawn_time:
            has_shield = True if random.randint(0, 10) > 5 else False
            self._enemies.append(Enemy(self._screen_width, has_shield))
            self._enemy_timer = current_time

        # Update enemy positions
        for enemy in self._enemies:
            enemy.update_state()

        # Check for collisions
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                if self.__check_collision((bullet.x, bullet.y, bullet.width, bullet.height),
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

    def render(self) -> None:
        """Render all game objects to the screen."""
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
