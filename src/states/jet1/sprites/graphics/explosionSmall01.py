import pygame, os

class sprite(pygame.sprite.Sprite):
    def __init__(self, spriteGroups, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.spriteGroups = spriteGroups
        self.image = pygame.image.load(os.path.join("images", "jet1", "explode1Small.bmp")).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.state = 0

    def update(self):
        if self.state < 6:
            self.state += 1
        elif self.state < 12:
            self.state += 1
            pygame.transform.flip(self.image, 1, 0)
        elif self.state < 18:
            self.kill()