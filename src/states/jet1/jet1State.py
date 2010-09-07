import pygame, gameState, os, random
from menus.pauseMenu import pauseMenu
from sprites import jet01, enemy01
import sprites

        
class jet1State(gameState.GameState):
    def __init__(self, level="jet1-1.lev"):
        gameState.GameState.__init__(self)
        self.bgDict = dict()
        self.settingsDict = dict()
        self.spawnDict = dict()
        self.parse_lev(level)

        self.currentBg = 0
        self.nextBg = 1
        self.bgOffset = 0
        self.time = 0

        self.spriteGroups =  {"groundEnemies":[],
                              "airEnemies":[],
                              "enemyProjectiles":[],
                              "myUniversalProjectiles":[],
                              "myAirProjectiles":[],
                              "myGroundProjectiles":[],
                              "nonCollidables":[],
                              "me":[]}
        self.spriteGroups["groundEnemies"] = pygame.sprite.Group()
        self.spriteGroups["airEnemies"] = pygame.sprite.Group()
        self.spriteGroups["enemyProjectiles"] = pygame.sprite.Group()
        self.spriteGroups["myUniversalProjectiles"] = pygame.sprite.Group()
        self.spriteGroups["myAirProjectiles"] = pygame.sprite.Group()
        self.spriteGroups["myGroundProjectiles"] = pygame.sprite.Group()
        self.spriteGroups["nonCollidables"] = pygame.sprite.Group()
        self.spriteGroups["me"] = pygame.sprite.GroupSingle()

        me = jet01.sprite(self.spriteGroups, self.settingsDict)
        self.spriteGroups["me"].add(me)

        #later find a cleaver way to precache all images, or at least load only once
        #self.images = dict()
        #enemy1BulletImage = pygame.image.load(os.path.join("images", "jet1", "enemy1Bullet.bmp")).convert()

    def parse_lev(self, level):
        with open(os.path.join("levels/", level)) as f:
            for line in f:
                strippedLine = line.strip("\n\r")
                if "bgimage" in line:
                    index = strippedLine.split(" ")[1]
                    image = strippedLine.split(" ")[2]
                    self.bgDict[index] = pygame.image.load(os.path.join("images", "jet1", image)).convert()
                elif "scrollorder" in line:
                    self.bgOrderArray = strippedLine.split(" ")[1:]
                elif "setting" in line:
                    print strippedLine.split(" ")
                    (trash, key, value) = strippedLine.split(" ")
                    self.settingsDict[key] = int(value)
                elif "spawn" in line:
                    (trash, time, sprite, x, y, pre, post) = strippedLine.split(" ")
                    if self.spawnDict.has_key(time):
                        self.spawnDict[time] += ((sprite, x, y, pre, post),)
                    else:
                        self.spawnDict[time] = ((sprite, x, y, pre, post),)
            print "spawnDict:"
            print self.spawnDict
             
    def update(self):
        #update time and generate stuff from script
        oldtime = self.time
        self.time += self.settingsDict["scrollspeed"]
        for t in range(oldtime, self.time):
            if self.spawnDict.has_key(str(t)):
                print self.spawnDict[str(t)]
                for (sprite, x, y, pre, post) in self.spawnDict[str(t)]:
                    print sprite, x, y, pre, post
                    #e = getattr(sprites, sprite)
                    #print e
                    print (self.spriteGroups, x, y)
        
        
        #scroll the background offsets
        self.bgOffset += self.settingsDict["scrollspeed"]
        if self.bgOffset >= 768:
            self.currentBg = self.nextBg
            self.nextBg += 1
            self.bgOffset = 0
            if self.nextBg >= len(self.bgOrderArray):
                self.nextBg = 0

        #now update other stuff
        for group in self.spriteGroups.itervalues():
            group.update()

        #spawn some new ships
        if random.randrange(100) > 95:
            e = enemy01.sprite(self.spriteGroups, random.randrange(1024), 0)
            self.spriteGroups["airEnemies"].add(e) 

    def draw(self, screen):
        #background first
        if self.bgOffset > 0:
            bg2 = self.bgDict[self.bgOrderArray[self.nextBg]]
            subRect = (0, bg2.get_rect()[3] - self.bgOffset, bg2.get_rect()[2], self.bgOffset)
            screen.blit(bg2, (0,0), subRect)

        bg1 = self.bgDict[self.bgOrderArray[self.currentBg]]
        subRect = (0, 0, bg1.get_rect()[2], bg1.get_rect()[3] - self.bgOffset)
        screen.blit(bg1, (0,self.bgOffset), subRect)

        #now the rest of the sprites
        for group in self.spriteGroups.itervalues():
            group.draw(screen)


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


    