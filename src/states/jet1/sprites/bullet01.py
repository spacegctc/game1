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

    def update(self):
        self.rect[1] -= 16
        if self.rect[1] + self.rect[3] < 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.spriteGroups["collidables"]):
            self.spriteGroups["nonCollidables"].add(explosionSmall01.sprite(self.spriteGroups, self.rect[0], self.rect[1]))
            self.kill()