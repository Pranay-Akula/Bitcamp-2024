import pygame
import numpy as np

pygame.init()

pong_font = pygame.font.Font('freesansbold.ttf', 20)

screen = pygame.display.set_mode((900,600))
pygame.display.set_caption("Perfect Pitch")

clock = pygame.time.Clock()
FPS = 30

class Coin:

    def __init__ (self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    
    

