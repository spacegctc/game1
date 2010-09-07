import pygame, os, explosionSmall01

class sprite(pygame.sprite.Sprite):
    def __init__(self, spriteGroups):
        pygame.sprite.Sprite.__init__(self)
        self.spriteGroups = spriteGroups
        self.image = pygame.image.load(os.path.join("images", "jet1", "jet1Bullet.bmp")).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect[0] = self.spriteGroups["me"].sprite.rect[0] + (self.spriteGroups["me"].sprite.rect[2] / 2)
        self.rect[1] = self.spriteGroups["me"].sprite.rect[1]
        self.life = 1

    def update(self):
        collide = 0
        self.rect[1] -= 16
        if self.rect[1] + self.rect[3] < 0:
            self.kill()
        sprites = pygame.sprite.spritecollide(self, self.spriteGroups["airEnemies"], False)
        if len(sprites) > 0:
            collide = 1
        for sprite in sprites:
            sprite.damage(self.life)
            
        sprites = pygame.sprite.spritecollide(self, self.spriteGroups["groundEnemies"], False)
        if len(sprites) > 0:
            collide = 1
        for sprite in sprites:
            sprite.damage(self.life)
            
        if collide == 1:
            self.spriteGroups["nonCollidables"].add(explosionSmall01.sprite(self.spriteGroups, self.rect[0], self.rect[1]))
            self.kill()
            
    def load_image(self):
        return pygame.image.load(os.path.join("images", "jet1", "enemy1Bullet.bmp")).convert()