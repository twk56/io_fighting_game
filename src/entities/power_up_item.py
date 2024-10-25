# src/power_up_item.py

import pygame
import config
import math
import os

class PowerUpItem:
    def __init__(self, power_type, position):
        self.type = power_type
        self.position = list(position)
        self.size = config.POWER_UP_SIZE
        self.color = config.POWER_UP_COLORS.get(self.type, (255, 255, 255))
        self.is_active = True

        # โหลดรูปภาพไอเทมพลังเสริม (optional)
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', f'{self.type}_power_up.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded power-up image for {self.type} from {image_path}")
        except pygame.error as e:
            print(f"ไม่สามารถโหลดภาพไอเทมพลังเสริม {self.type} ได้: {e}")
            self.image = None

    def draw(self, screen, camera_x, camera_y):
        if self.is_active:
            if self.image:
                screen.blit(self.image, 
                            (int(self.position[0] - camera_x - self.size // 2), 
                             int(self.position[1] - camera_y - self.size // 2)))
            else:
                pygame.draw.rect(screen, self.color, 
                                 (self.position[0] - camera_x - self.size, 
                                  self.position[1] - camera_y - self.size, 
                                  self.size * 2, self.size * 2))

    def collect(self, player):
        # เช็คการชนกับผู้เล่น
        player_rect = pygame.Rect(player.position[0], player.position[1], player.size, player.size)
        item_rect = pygame.Rect(self.position[0] - self.size, self.position[1] - self.size, self.size * 2, self.size * 2)
        if player_rect.colliderect(item_rect):
            # ผู้เล่นเก็บไอเทมพลังเสริม
            self.is_active = False
            return True
        return False
