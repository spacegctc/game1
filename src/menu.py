'''
Created by David Kelley
Copyright 2010

The interfaces to this class accept more parameters than are used.
Plans for the future are to expand this class to be more flexible, but for now, no.
Not all parameters are checked and are assumed to be correct when passed in.
No return values are checked.
This is bad, but oh well for now.
'''

import pygame
import gameState

ENTRY_ACTION = 1
ENTRY_SELECT = 2

CENTERED = 0
TOP      = 1
BOTTOM   = 2
LEFT     = 3
RIGHT    = 4

class Menu(gameState.GameState):
    def __init__(self, gameStates, parent=None, title=None, width=800, height=600, hAlign=CENTERED, background=None):
        gameState.GameState.__init__(self)
        if background:
            self.background = background
        else:
            self.background = pygame.Surface((1024,768))
            self.background.fill((255,255,255))
        self.dirty = 1
        self.gameStates = gameStates
        self.parent = parent
        self.title = title
        self.width = width
        self.height = height
        self.hAlign = hAlign
        self.selected = 0
        self.entries = []
        self.entry_height = 0
        self.dirtyRects = []
        self.gameStates["ACTIVE"].append(self)
        self.gameStates["KEYFOCUS"].append(self)
        self.gameStates["VISIBLE"].append(self)
        if parent in self.gameStates["ACTIVE"]: self.gameStates["ACTIVE"].remove(parent)
        if parent in self.gameStates["KEYFOCUS"]: self.gameStates["KEYFOCUS"].remove(parent)
        if parent in self.gameStates["VISIBLE"]: self.gameStates["VISIBLE"].remove(parent)

    def addEntry(self, entryType=ENTRY_ACTION, text=None, image=None, rolloverImage=None, rolloverSound=None, callback=None, callbackArg=None, options=None):
        self.entries.append((entryType, text, image, rolloverImage, rolloverSound, callback, callbackArg, options))
        self.entry_height += image.get_rect()[3]
        self.dirty = 1

    def draw(self, screen):
        #print screen
        if self.dirty == 1:
            screen.blit(self.background, (0, 0))

            x, y, width, height = screen.get_rect()
            y_off = (height - self.entry_height) / 2
            for entry in self.entries:
                #print entry
                if self.entries.index(entry) == self.selected:
                    surf = entry[3]
                else:
                    surf = entry[2]

                x_off = (width - surf.get_rect()[2]) / 2
                screen.blit(surf, (x_off,y_off))
                y_off += surf.get_rect()[3]
            
            self.dirty = None

    def select_next(self):
        self.selected += 1
        if self.selected >= len(self.entries):
            self.selected = 0
        self.dirty = 1


    def select_prev(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.entries) - 1
        self.dirty = 1

    def option_next(self):
        #option entries not implemented yet
        pass
        
    def option_prev(self):
        #option entries not implemented yet
        pass
        
    def action_current(self):
        callbackArg = self.entries[self.selected][6]
        if callbackArg:
            self.entries[self.selected][5](callbackArg)
        else:
            self.entries[self.selected][5]()

    def handleKey(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.dict["key"]
            if key == pygame.K_DOWN:
                self.select_next()
            if key == pygame.K_UP:
                self.select_prev()
            if key == pygame.K_LEFT:
                self.option_prev()
            if key == pygame.K_RIGHT:
                self.option_next()
            if key == pygame.K_RETURN:
                self.action_current()
            if key == pygame.K_ESCAPE:
                if self.parent:
                    self.gameStates["KEYFOCUS"].remove(self)
                    self.gameStates["VISIBLE"].remove(self)
                    self.gameStates["ACTIVE"].remove(self)
                    self.gameStates["KEYFOCUS"].append(self.parent)
                    self.gameStates["VISIBLE"].append(self.parent)
                    self.gameStates["ACTIVE"].append(self.parent)
