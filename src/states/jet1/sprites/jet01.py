import pygame, os
import bullet01

class sprite(pygame.sprite.Sprite):
    def __init__(self, spriteGroups):
        pygame.sprite.Sprite.__init__(self)
        self.spriteGroups = spriteGroups
        self.image = pygame.image.load(os.path.join("images", "jet1", "jet1.bmp")).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect[0] = 500
        self.rect[1] = 300
        self.health = 1000
        self.xmotion = 0
        self.ymotion = 0

        #key states
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        
        #these settings should come from the jet state but hack to get it working to show keith
        self.settings = dict()
        self.settings["flyspeed"] = 8  

    def _fire_primary_gun(self):
        b = bullet01.sprite(self.spriteGroups)
        self.spriteGroups["mine"].add(b)
         
    def update(self):
        if self.left and self.right:
            pass
        elif self.left:
            self.rect[0] -= self.settings["flyspeed"]
            if self.rect[0] < 0:
                self.rect[0] = 0
        elif self.right:
            self.rect[0] += self.settings["flyspeed"]
            if self.rect[0] + self.rect[2] > 1024:
                self.rect[0] = 1024 - self.rect[2]

        if self.up and self.down:
            pass
        elif self.up:
            self.rect[1] -= self.settings["flyspeed"]
            if self.rect[1] < 0:
                self.rect[1] = 0
        elif self.down:
            self.rect[1] += self.settings["flyspeed"]
            if self.rect[1] + self.rect[3] > 768:
                self.rect[1] = 768 - self.rect[3]

    def keyDown(self, key):
        if key == pygame.K_DOWN:
            self.down = 1
        if key == pygame.K_UP:
            self.up = 1
        if key == pygame.K_LEFT:
            self.left = 1
        if key == pygame.K_RIGHT:
            self.right = 1
        if key == pygame.K_SPACE:
            self._fire_primary_gun()

    def keyUp(self, key):
        if key == pygame.K_DOWN:
            self.down = 0
        if key == pygame.K_UP:
            self.up = 0
        if key == pygame.K_LEFT:
            self.left = 0
        if key == pygame.K_RIGHT:
            self.right = 0
    