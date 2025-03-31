import pygame # type: ignore
from scenes import SceneBase, GameScene

class MenuScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene())
    
    def Update(self, dt):
        pass
    
    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 0, 0))
        w, h = pygame.display.get_surface().get_size()

        font = pygame.font.SysFont("Arial", 16)
        txtsurf = font.render("Zum STARTEN, Return Taste drücken", True, (255,255,255))
        screen.blit(txtsurf,((w - txtsurf.get_width()) // 2, (h - txtsurf.get_height()) // 2))