import pygame, os
from states.jet1.sprites.projectiles import bullet01

class sprite(pygame.sprite.Sprite):
    def __init__(self, spriteGroups, settingsDict={"flyspeed":8}):
        pygame.sprite.Sprite.__init__(self)
        self.spriteGroups = spriteGroups
        self.image = pygame.image.load(os.path.join("images", "jet1", "jet1.bmp")).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect[0] = 500
        self.rect[1] = 500
        self.life = 3
        self.dead = 0
        self.lives = 3

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
        self.ticks = 0
        
        self.settingsDict = settingsDict

    def _fire_primary_gun(self):
        b = bullet01.sprite(self.spriteGroups)
        self.spriteGroups["myUniversalProjectiles"].add(b)
    
    def _fire_special_gun(self):
        pass
    
    def _fire_bomb(self):
        pass
         
    def update(self):
        if self.dead:
            if self.respawnTicks > 0:
                self.respawnTicks -= 1
            else:
                self.respawn()
            return

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
        
        if self.firing_primary and self.ticks % 1 == 0:
            self._fire_primary_gun()

        sprites  = pygame.sprite.spritecollide(self, self.spriteGroups["airEnemies"], False)
        sprites += pygame.sprite.spritecollide(self, self.spriteGroups["enemyProjectiles"], False)
        for sprite in sprites:
            self.damage(sprite.life)
            sprite.damage(self.life)

        sprites = pygame.sprite.spritecollide(self, self.spriteGroups["bonuses"], False)
        for sprite in sprites:
            self.bonus(sprite.bonusType)
            sprite.damage(1)
            
        self.ticks += 1

    def keyDown(self, key):
        if key == pygame.K_DOWN:
            self.up = 0
            self.down_tmp = self.down = 1
        elif key == pygame.K_UP:
            self.down = 0
            self.up_tmp = self.up = 1
        elif key == pygame.K_LEFT:
            self.right = 0
            self.left_tmp = self.left = 1
        elif key == pygame.K_RIGHT:
            self.left_tmp = self.left
            self.left = 0
            self.right_tmp = self.right = 1
        elif key == pygame.K_SPACE:
            self.firing_primary = 1

    def keyUp(self, key):
        if key == pygame.K_DOWN:
            self.up = self.up_tmp
            self.down_tmp = self.down = 0
        elif key == pygame.K_UP:
            self.down = self.down_tmp
            self.up_tmp = self.up = 0
        elif key == pygame.K_LEFT:
            self.right = self.right_tmp
            self.left_tmp = self.left = 0
        elif key == pygame.K_RIGHT:
            self.left = self.left_tmp
            self.right_tmp = self.right = 0
        elif key == pygame.K_SPACE:
            self.firing_primary = 0

    def gameOver(self):
        self.respawn()

    def respawn(self):
        self.dead = 0
        self.rect[0] = 500
        self.rect[1] = 500
        self.life = 3

    def die(self):
        if self.lives > 1:
            self.lives -= 1
            self.dead = 1
            self.respawnTicks = 60
        else:
            self.gameOver()

    def damage(self, damage=1):
        if damage > self.life:
            self.die()
        else:
            self.life -= damage

    def bonus(self, bonusType):
        pass