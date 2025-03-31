import os
import pygame
import random
from scenes import SceneBase
from game_objects import Player, Bullet, Enemy, ExplosionParticle

class GameScene(SceneBase):
    def __init__(self):
        w, h = pygame.display.get_surface().get_size()

        SceneBase.__init__(self)
        # PLAYER
        self.player : Player = Player(w, h)
        base_path = os.path.dirname(os.path.dirname(__file__))  # gehe aus /scenes raus
        
        # load music
        self.game_music = pygame.mixer.music.load(os.path.join(base_path, "assets", "sound", "music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)


        # declare sounds
        self.shot_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "sound", "laser.mp3"))
        self.shot_sound.set_volume(0.2)
        self.shield_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "sound", "shield.mp3"))
        self.shield_sound.set_volume(0.4)
        self.explosion_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "sound", "explosion.mp3"))
        self.explosion_sound.set_volume(0.2)
        # GAME OBJECTS
        self._bullets : list[Bullet] = []
        self._enemies : list[Enemy] = []
        self._explosions : list[ExplosionParticle] = []

        # GAME SETTINGS
        self._enemy_timer = 0
        self._enemy_spawn_time = 2000 # Spawn an enemy every 2 seconds
        
        # GRAPHICS SETTINGS
        self._screen_width = w
        self._screen_height = h

        # GAME STATE
        self._hits = 0

    # Collision detection function
    def __check_collision(self, rect1, rect2):
        return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a bullet at the current player position
                    self._bullets.append(Bullet(self.player.x + self.player.width // 2, self.player.y))
                    self.shot_sound.play()
        
        self.player.handleInput(pressed_keys)
        
    def Update(self, dt):
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

        # Update enemy positions
        for particle in self._explosions:
            particle.updateState(dt)

        # Check for collisions
        for bullet in self._bullets[:]:
            for enemy in self._enemies[:]:
                if self.__check_collision((bullet.x, bullet.y, bullet._width, bullet._height),
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
                            self._explosions.append(ExplosionParticle(enemy.x + enemy._width // 2, enemy.y + enemy._height // 2))
                    break

        # Remove enemies that are off the screen
        self._enemies = [enemy for enemy in self._enemies if enemy.y < self._screen_height]

        # Remove explosions that are done animating
        self._explosions = [p for p in self._explosions if not p.is_dead()]

    
    def Render(self, screen):
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