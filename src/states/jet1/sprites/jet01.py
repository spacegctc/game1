import pygame, os
import bullet01

class sprite(pygame.sprite.Sprite):
    def __init__(self, spriteGroups, settingsDict={"flyspeed":8}):
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
        self.left_tmp = 0
        self.right = 0
        self.right_tmp = 0
        self.up = 0
        self.up_tmp = 0
        self.down = 0
        self.down_tmp = 0
        self.firing_primary = 0
        
        #these settings should come from the jet state but hack to get it working to show keith
        self.settingsDict = settingsDict 

    def _fire_primary_gun(self):
        b = bullet01.sprite(self.spriteGroups)
        self.spriteGroups["myUniversalProjectiles"].add(b)
    
    def _fire_special_gun(self):
        pass
    
    def _fire_bomb(self):
        pass
         
    def update(self):
        if self.left:
            self.rect[0] -= self.settingsDict["flyspeed"]
            if self.rect[0] < 0:
                self.rect[0] = 0
        elif self.right:
            self.rect[0] += self.settingsDict["flyspeed"]
            if self.rect[0] + self.rect[2] > 1024:
                self.rect[0] = 1024 - self.rect[2]

        if self.up:
            self.rect[1] -= self.settingsDict["flyspeed"]
            if self.rect[1] < 0:
                self.rect[1] = 0
        elif self.down:
            self.rect[1] += self.settingsDict["flyspeed"]
            if self.rect[1] + self.rect[3] > 768:
                self.rect[1] = 768 - self.rect[3]
        
        if self.firing_primary:
            self._fire_primary_gun()

    def keyDown(self, key):
        if key == pygame.K_DOWN:
            self.up_tmp = self.up
            self.up = 0
            self.down = 1
        elif key == pygame.K_UP:
            self.down_tmp = self.down
            self.down = 0
            self.up = 1
        elif key == pygame.K_LEFT:
            self.right_tmp = self.right
            self.right = 0
            self.left = 1
        elif key == pygame.K_RIGHT:
            self.left_tmp = self.left
            self.left = 0
            self.right = 1
        elif key == pygame.K_SPACE:
            self.firing_primary = 1

    def keyUp(self, key):
        if key == pygame.K_DOWN:
            self.up = self.up_tmp
            self.up_tmp = 0
            self.down = 0
        elif key == pygame.K_UP:
            self.down = self.down_tmp
            self.down_tmp = 0
            self.up = 0
        elif key == pygame.K_LEFT:
            self.right = self.right_tmp
            self.right_tmp = 0
            self.left = 0
        elif key == pygame.K_RIGHT:
            self.left = self.left_tmp
            self.left_tmp = 0
            self.right = 0
        elif key == pygame.K_SPACE:
            self.firing_primary = 0

    