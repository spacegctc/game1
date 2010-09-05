import pygame, gameState, os, random
from menus.pauseMenu import pauseMenu
from sprites import jet01, enemy01

        
class jet1State(gameState.GameState):
    def __init__(self, level="jet1.lev"):
        gameState.GameState.__init__(self)
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

        me = jet01(self.spriteGroups)
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
            e = enemy01(self.spriteGroups, random.randrange(1024))
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


    