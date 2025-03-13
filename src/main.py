# src/main.py

import pygame
import config
from game import Game

def main():
    pygame.init()
    
    # กำหนดขนาดหน้าจอ
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Fighting .io Game")
    
    # สร้างอินสแตนซ์ของเกม
    game = Game(screen)
    
    # รันเกม
    game.run()

if __name__ == "__main__":
    main()
