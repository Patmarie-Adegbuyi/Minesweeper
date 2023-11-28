import pygame
import pygame.freetype

import MSGame

# The main class creates a game and then asks the GAME to determine the state of the system
# MSGame sets up how to run the game by looping through paint and user interface (UI)
# handling events.
pygame.init()
pygame.freetype.init()
game = MSGame.MSGame('medium')

# Game loop
while game.is_game_running():
    for event in pygame.event.get():
        # Throwing all events at the MVC_Canvas class
        if game.handleUIEvent(event):
            game.draw_game()

pygame.freetype.quit()
pygame.quit()
