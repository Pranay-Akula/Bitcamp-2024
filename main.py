from audio_processing import *
from soundDetector import get_mean_freq
import numpy as np
# Pygame imports
import pygame
import numpy as np
from sys import exit

"""
filename = input("Enter the file path to a song of your choice (.wav): ")
framerate = get_framerate(filename)
extract_vocals(filename)
song_freqs = np.array(get_freqs("output.wav"))
"""

# soundDetector
low_calced = True
high_calced = True

while low_calced:
    user_input = input("Are you ready to record your lowest pitch? (yes/no): ").strip().lower()
    # Check user's response
    if user_input == "yes":
        low_frequency = get_mean_freq()
        low_calced = False
        
    elif user_input == "no":
        continue
    else:
        print("Please respond with 'yes' or 'no'.")
        continue

while high_calced:
    user_input = input("Are you ready to record your highest pitch? (yes/no): ").strip().lower()

    # Check user's response
    if user_input == "yes":
        high_frequency = get_mean_freq()
        high_calced = False    
    elif user_input == "no":
        continue
    else:
        print("Please respond with 'yes' or 'no'.")
        continue

"""
song_freqs[song_freqs > high_frequency] = 0
song_freqs[song_freqs < low_frequency] = 0
"""

# Pygame code

pygame.init()

pong_font = pygame.font.Font('media/bit5x3.ttf', 20)

screen = pygame.display.set_mode((800,500))
pygame.display.set_caption("Perfect Pitch")

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0
FPS = 30

class Player:
    def __init__ (self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.player_image = pygame.image.load('media/rocket-ship.png')
        self.player_image = pygame.transform.rotozoom(self.player_image, -45,0.2).convert_alpha()
        self.player_rect = self.player_image.get_rect(center=(xpos,ypos))
    
    def display (self):
        self.player_rect = self.player_image.get_rect(center=(self.xpos,self.ypos))
        screen.blit(self.player_image, self.player_rect)

    def update (self, new_ypos):
        self.ypos = new_ypos
    
    def displayScore(self, score):
        text = pong_font.render(str(score), True, 'white')
        textRect = text.get_rect()
        textRect.center = (700, 100)
 
        screen.blit(text, textRect)


class Coin:
    def __init__ (self, xpos, ypos, width=10,height=10):
        self.xpos = xpos
        self.ypos = ypos
        self.coin_image = pygame.image.load('media/coin.png')
        self.coin_image = pygame.transform.rotozoom(self.coin_image, 0, 0.2).convert_alpha()
        self.coin_rect = self.coin_image.get_rect(center=(xpos,ypos))
    
    def display (self):
        self.coin_rect = self.coin_image.get_rect(center=(self.xpos,self.ypos))
        screen.blit(self.coin_image, self.coin_rect)

    def update (self, new_ypos):
        self.ypos = new_ypos
        self.xpos = self.xpos - (200 * dt)





def main():

    running = True
    game_active = False
    score = 0

    player = Player(100,250)
    coins_group = []
    coin = Coin(800, 100)
    coins_group.append(coin)

    space_image = pygame.image.load('media/space-background.jpeg')
    space_image = pygame.transform.scale(space_image, (900,600))

    spawn_interval = 3000
    last_spawn_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(space_image,(0,0))

        # coin.update(coin.ypos)
        # if (coin.xpos < 0):
        #     coin.xpos = 800

        # if pygame.Rect.colliderect(player.player_rect, coin.coin_rect):
        #     score += 1

        player.display()
        player.displayScore(score)
        # coin.display()

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= spawn_interval:
            coin = Coin(800,250)
            coins_group.append(coin)
            last_spawn_time = current_time


        for coin in coins_group:
            coin.update(coin.ypos)
            coin.display()
            if (coin.xpos < 0):
                coins_group.remove(coin)
            if pygame.Rect.colliderect(player.player_rect, coin.coin_rect):
                coins_group.remove(coin)
                score += 1
        
        pygame.display.update()

    
main()
pygame.quit()





