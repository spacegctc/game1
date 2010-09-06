import pygame, os, sys, menu

from states.jet1 import jet1State

def newGame(gameStates):
    #person1.load(menuState.lists)
    jet1State.load(gameStates)

def quitGame():
    sys.exit()

def load(gameStates):
    #If we're at the main menu make sure we're the only active/visible/keyfocus state
    gameStates["ACTIVE"] = []
    gameStates["VISIBLE"] = []
    gameStates["KEYFOCUS"] = []
    
    #Load the resources for this state
    startSurface = pygame.image.load(os.path.join("images", "mainMenu", "start.bmp")).convert()
    startSurface.set_colorkey((255,255,255))
    startRolloverSurface = pygame.image.load(os.path.join("images", "mainMenu", "start_rollover.bmp")).convert()
    startRolloverSurface.set_colorkey((255,255,255))
    quitSurface = pygame.image.load(os.path.join("images", "mainMenu", "quit.bmp")).convert()
    quitSurface.set_colorkey((255,255,255))
    quitRolloverSurface = pygame.image.load(os.path.join("images", "mainMenu", "quit_rollover.bmp")).convert()
    quitRolloverSurface.set_colorkey((255,255,255))
    menuBackgroundSurface = pygame.image.load(os.path.join("images", "mainMenu", "menu_bg.bmp")).convert()

    #Init the menu
    menuState = menu.Menu(gameStates, background=menuBackgroundSurface)
    menuState.addEntry(text="Start", callback=newGame, callbackArg=gameStates, image=startSurface, rolloverImage=startRolloverSurface)
    menuState.addEntry(text="Quit", callback=quitGame, image=quitSurface, rolloverImage=quitRolloverSurface)
