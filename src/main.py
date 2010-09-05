'''
Created on Feb 15, 2010

@author: dkelley
'''

#classes, etc
import sys, pygame

#helper functions!
from menus.titleMenu import titleMenu

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024,768))
pygame.display.set_caption("game1 by Ian Owens and David Kelley, Copyright 2010")

#All game states require access to this tuple containing the list of active, visible, and keyfocus states
gameStates = {"ACTIVE":[], "VISIBLE":[], "KEYFOCUS":[]}

#Load the main menu as the first active/visible/keyfocus state
titleMenu.load(gameStates)

#Enter the main loop
while True:
    #limit to 30fps
    clock.tick(60)

    #handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        for state in gameStates["KEYFOCUS"]:
            state.handleKey(event)

    #update active states
    for state in gameStates["ACTIVE"]:
        state.update()

    #render visible states
    for state in gameStates["VISIBLE"]:    
        state.draw(screen)

    #update the screen
    pygame.display.flip()

