"""Main game scene module that handles the core gameplay mechanics."""
# pylint: disable=no-member
import os
import random
import pygame
from pygame.key import ScancodeWrapper
from pygame.mixer import Sound
from scenes import SceneBase
from game_objects import Player, Bullet, Enemy, ExplosionParticle

class GameScene(SceneBase):
    """Main game scene that handles player input, game logic, and rendering."""

    def __init__(self):
        w, h = pygame.display.get_surface().get_size()

        SceneBase.__init__(self)
        # PLAYER
        self.player : Player = Player(w, h)
        base_path : str = os.path.dirname(os.path.dirname(__file__))  # gehe aus /scenes raus

        # load music
        self.game_music : None = pygame.mixer.music.load(
            os.path.join(base_path, "assets", "sound", "music.mp3")
        )
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # declare sounds
        self.shot_sound : Sound = pygame.mixer.Sound(
            os.path.join(base_path, "assets", "sound", "laser.mp3")
        )
        self.shot_sound.set_volume(0.2)
        self.shield_sound : Sound = pygame.mixer.Sound(
            os.path.join(base_path, "assets", "sound", "shield.mp3")
        )
        self.shield_sound.set_volume(0.4)
        self.explosion_sound : Sound = pygame.mixer.Sound(
            os.path.join(base_path, "assets", "sound", "explosion.mp3")
        )
        self.explosion_sound.set_volume(0.2)
        # GAME OBJECTS
        self._bullets : list[Bullet] = []
        self._enemies : list[Enemy] = []
        self._explosions : list[ExplosionParticle] = []

        # GAME SETTINGS
        self._enemy_timer : int = 0
        self._enemy_spawn_time : int = 4000 # Spawn an enemy every 2 seconds

        # GRAPHICS SETTINGS
        self._screen_width : int = w
        self._screen_height : int = h

        # GAME STATE
        self._hits : int = 0
        self._game_over : bool = False
        self._victory : bool = False

    # Collision detection function
    def __check_collision(
        self,
        rect1: tuple[int, int, int, int],
        rect2: tuple[int, int, int, int]
    ) -> bool:
        """Check if two rectangles are colliding."""
        return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

    def process_input(
        self,
        events: list[pygame.event.Event],
        pressed_keys: ScancodeWrapper
    ) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a bullet at the current player position
                    bullet_x = self.player.x + self.player.width // 2
                    self._bullets.append(Bullet(bullet_x, self.player.y))
                    self.shot_sound.play()

        self.player.handle_input(pressed_keys)

    def update(self, dt : int):
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

        # Update enemy positions
        for particle in self._explosions:
            particle.updateState(dt)

        # Check for collisions
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                if self.__check_collision((bullet.x, bullet.y, bullet.width, bullet.height),
                                (enemy.hitbox)):
                    # Ziel wurde getroffen
                    enemy.health -= 1
                    self._bullets.remove(bullet)
                    if enemy.health > 0:
                        self.shield_sound.play()
                    else:
                        self._enemies.remove(enemy)
                        self.explosion_sound.play()
                        self._hits += 1
                        for _ in range(15):
                            particle_x = enemy.x + enemy.width // 2
                            particle_y = enemy.y + enemy.height // 2
                            self._explosions.append(ExplosionParticle(particle_x, particle_y))
                    break

        # Remove enemies that are off the screen
        remaining_enemies : list[Enemy] = []
        for enemy in self._enemies:
            if enemy.y < self._screen_height:
                remaining_enemies.append(enemy)
            else:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self._game_over = True

        self._enemies = remaining_enemies

        # Remove explosions that are done animating
        self._explosions = [p for p in self._explosions if not p.is_dead()]

    def render(self, screen : pygame.Surface) -> None:
        """Render the game scene."""
        screen.fill((0, 0, 0))

        self.player.render(screen)

        # Draw the bullets
        for bullet in self._bullets:
            bullet.render(screen)

        # Draw the enemies
        for enemy in self._enemies:
            enemy.render(screen)

        for particle in self._explosions:
            particle.render(screen)

        font = pygame.font.SysFont("Arial", 16)
        txtsurf = font.render(f"Treffer: {self._hits}", True, (255,255,255))
        screen.blit(txtsurf,(50 - txtsurf.get_width() // 2, 20 - txtsurf.get_height() // 2))

        # txtlives = font.render(f"Leben: {self.player.lives}", True, (255,255,255))
        # x = screen.get_width() - 50 - txtlives.get_width() // 2
        # y = 20 - txtlives.get_height() // 2
        # screen.blit(txtlives, (x, y))
