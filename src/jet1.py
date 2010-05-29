import pygame, gs, os, random

import pauseMenu

class explosion1Small(pygame.sprite.Sprite):
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

class enemy1(pygame.sprite.Sprite):
    def __init__(self, spriteGroups, x):
        pygame.sprite.Sprite.__init__(self)
        self.spriteGroups = spriteGroups
        self.image = pygame.image.load(os.path.join("images", "jet1", "enemy1.bmp")).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = -self.rect[3]

    def update(self):
        self.rect[1] += 2 + 2 #SCROLL_SPEED (what?)
        if self.rect[1] > 768:
            self.kill()

class bullet(pygame.sprite.Sprite):
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
            self.spriteGroups["nonCollidables"].add(explosion1Small(self.spriteGroups, self.rect[0], self.rect[1]))
            self.kill()

class jet(pygame.sprite.Sprite):
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
        b = bullet(self.spriteGroups)
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
        
class jet1State(gs.GameState):
    def __init__(self, level="jet1.lev"):
        gs.GameState.__init__(self)
        self.bgArray = []
        self.bgArray.append(pygame.image.load(os.path.join("images", "jet1", "bg1.bmp")).convert())
        self.bgArray.append(pygame.image.load(os.path.join("images", "jet1", "bg2.bmp")).convert())
        self.bgArray.append(pygame.image.load(os.path.join("images", "jet1", "bg3.bmp")).convert())
        self.bgArray.append(pygame.image.load(os.path.join("images", "jet1", "bg4.bmp")).convert())
        self.bgArray.append(pygame.image.load(os.path.join("images", "jet1", "bg5.bmp")).convert())
        self.currentBg = 0
        self.nextBg = 1
        self.bgOffset = 0
        self.time = 0
        self.settings = { "scrollspeed":2, "flyspeed":8 }

        self.spriteGroups =  {"collidables":[], "nonCollidables":[], "mine":[], "me":[]}
        self.spriteGroups["collidables"] = pygame.sprite.Group()
        self.spriteGroups["nonCollidables"] = pygame.sprite.Group()
        self.spriteGroups["mine"] = pygame.sprite.Group()
        self.spriteGroups["me"] = pygame.sprite.GroupSingle()

        me = jet(self.spriteGroups)
        self.spriteGroups["me"].add(me)

        """
        with open(level) as lev:
            for line in lev:
                print line
        """
#        self.enemy1BulletImage = pygame.image.load(os.path.join("images", "jet1", "enemy1Bullet.bmp")).convert()
        
    def update(self):
        #update time and generate stuff from script
        self.time += self.settings["scrollspeed"]
        
        #scroll the background offsets
        self.bgOffset += self.settings["scrollspeed"]
        if self.bgOffset >= 768:
            self.currentBg = self.nextBg
            self.nextBg += 1
            self.bgOffset = 0
            if self.nextBg >= 5:
                self.nextBg = 0

        #now update other stuff
        self.spriteGroups["me"].update()
        self.spriteGroups["mine"].update()
        self.spriteGroups["nonCollidables"].update()
        self.spriteGroups["collidables"].update()

        #spawn some new ships
        if random.randrange(100) > 95:
            e = enemy1(self.spriteGroups, random.randrange(1024))
            self.spriteGroups["collidables"].add(e) 

    def draw(self, screen):
        #background first
        if self.bgOffset > 0:
            bg2 = self.bgArray[self.nextBg]
            subRect = (0, bg2.get_rect()[3] - self.bgOffset, bg2.get_rect()[2], self.bgOffset)
            screen.blit(bg2, (0,0), subRect)

        bg1 = self.bgArray[self.currentBg]
        subRect = (0, 0, bg1.get_rect()[2], bg1.get_rect()[3] - self.bgOffset)
        screen.blit(bg1, (0,self.bgOffset), subRect)

        #now the rest of the sprites
        self.spriteGroups["me"].draw(screen)
        self.spriteGroups["mine"].draw(screen)
        self.spriteGroups["collidables"].draw(screen)
        self.spriteGroups["nonCollidables"].draw(screen)

    def handleKey(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.dict["key"]
            if key == pygame.K_ESCAPE:
                pauseMenu.load()
            else:
                self.spriteGroups["me"].sprite.keyDown(key)

        if event.type == pygame.KEYUP:
            key = event.dict["key"]
            self.spriteGroups["me"].sprite.keyUp(key)

def load(gameStates):
    gameStates["ACTIVE"] = []
    gameStates["VISIBLE"] = []
    gameStates["KEYFOCUS"] = []
    
    jetState = jet1State();
    gameStates["ACTIVE"].append(jetState)
    gameStates["VISIBLE"].append(jetState)
    gameStates["KEYFOCUS"].append(jetState)


    