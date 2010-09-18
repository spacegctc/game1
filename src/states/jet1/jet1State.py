'''
TO DO:
- Implement single image load sprites, preferable pre-cache all images and make available in a dict
- Fix keyboard whackyness in jet01.py key handling (if you press left/right really quick it gets stuck scrolling
- Implement pre/post sprite callbacks (pause, resume being the major callbacks)
- Allow .lev file to specify a time when random enemies may appear (for how long do random enemies appear, how many appear, which types may appear, etc?)
- Come up with way more enemies, weapons, etc, add music/sound effects, improve graphics, yah yah yah
'''

import pygame, gameState, os
from menus.pauseMenu import pauseMenu
from sprites import jet01
from sprites.enemies import enemy01

        
class jet1State(gameState.GameState):
    def __init__(self, level="jet1-1.lev"):
        gameState.GameState.__init__(self)

        self.currentBg = 0
        self.nextBg = 1
        self.bgOffset = 0
        self.time = 0

        self.bgDict = dict()
        self.settingsDict = dict()
        self.spawnDict = dict()
        self.spriteMap = {"enemy01":enemy01}

        self.spriteGroups =  {"groundEnemies":[],            # Tanks and bases and such
                              "airEnemies":[],               # Planes and helicopters and stuff, also enemy missiles which can be shot down
                              "enemyProjectiles":[],         # Enemy bullets/missiles which cannot be shot down
                              "myUniversalProjectiles":[],   # Bullets/missiles/bombs capable of hitting all targets
                              "myAirProjectiles":[],         # Bullets/missiles/bombs capable of hitting air targets only
                              "myGroundProjectiles":[],      # Bullets/missiles/bombs capable of hitting ground targets only
                              "bonuses":[],                  # Weapon upgrades, money, etc
                              "nonCollidables":[]}           # Explosion graphics and such
        for key in self.spriteGroups:
            self.spriteGroups[key] = pygame.sprite.Group()

        me = jet01.sprite(self.spriteGroups, self.settingsDict)
        self.spriteGroups["me"] = pygame.sprite.GroupSingle()
        self.spriteGroups["me"].add(me)

        self.parse_lev(level)

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
                    (trash, key, value) = strippedLine.split(" ")
                    self.settingsDict[key] = int(value)
                elif "spawn" in line:
                    (trash, time, sprite, y, x, pre, post) = strippedLine.split(" ")
                    if self.spawnDict.has_key(time):
                        self.spawnDict[time] += ((self.spriteMap[sprite], int(y), int(x), pre, post),)
                    else:
                        self.spawnDict[time] = ((self.spriteMap[sprite], int(y), int(x), pre, post),)
             
    def update(self):
        #update time and generate stuff from script
        oldtime = self.time
        self.time += self.settingsDict["scrollspeed"]
        for t in range(oldtime, self.time):
            if self.spawnDict.has_key(str(t)):
                for (sprite, y, x, pre, post) in self.spawnDict[str(t)]:
                    s = sprite.sprite(self, self.spriteGroups, y, x, pre, post)
                    for group in s.getGroups():
                        self.spriteGroups[group].add(s)        
        
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
        #if random.randrange(100) > 95:
            #e = enemy01.sprite(self, self.spriteGroups, 0, random.randrange(1024), None, None)
            #self.spriteGroups["airEnemies"].add(e)


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
            if group == self.spriteGroups["me"]:
                if group.sprite.dead == 0:
                    group.draw(screen) #Allow jet01 to draw itself
                else:
                    group.clear(screen, screen)
            else:
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


    