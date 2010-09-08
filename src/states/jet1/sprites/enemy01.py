import pygame, os

class sprite(pygame.sprite.Sprite):
    def __init__(self, parrent, spriteGroups, y, x, pre, post):
        pygame.sprite.Sprite.__init__(self)
        self.spriteGroups = spriteGroups
        self.image = pygame.image.load(os.path.join("images", "jet1", "enemy1.bmp")).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y - self.rect[3]
        self.life = 1

    def update(self):
        self.rect[1] += 2 + 2 #SCROLL_SPEED (what?)
        if self.rect[1] > 768:
            self.kill()

    def damage(self, life=1):
        self.life -= 1
        if self.life < 1:
            self.kill()

    def getGroups(self):
        yield "airEnemies"
        