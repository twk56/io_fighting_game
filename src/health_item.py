# src/health_item.py

import pygame
import config
import math
import os

class HealthItem:
    def __init__(self, position):
        self.position = list(position)
        self.size = config.HEALTH_ITEM_SIZE
        self.color = config.HEALTH_ITEM_COLOR
        self.is_active = True

        # โหลดรูปภาพไอเทมสุขภาพ (optional)
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'health_item.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded health item image from {image_path}")
        except pygame.error as e:
            print(f"ไม่สามารถโหลดภาพไอเทมสุขภาพได้: {e}")
            self.image = None

    def draw(self, screen, camera_x, camera_y):
        if self.is_active:
            if self.image:
                screen.blit(self.image, 
                            (int(self.position[0] - camera_x - self.size // 2), 
                             int(self.position[1] - camera_y - self.size // 2)))
            else:
                pygame.draw.circle(screen, self.color, 
                                   (int(self.position[0] - camera_x), int(self.position[1] - camera_y)), self.size)

    def collect(self, player):
        # เช็คการชนกับผู้เล่น
        player_rect = pygame.Rect(player.position[0], player.position[1], player.size, player.size)
        item_rect = pygame.Rect(self.position[0] - self.size, self.position[1] - self.size, self.size * 2, self.size * 2)
        if player_rect.colliderect(item_rect):
            # เพิ่มพลังชีวิตให้ผู้เล่น
            player.health = min(player.health + 20, config.PLAYER_MAX_HEALTH)
            self.is_active = False
            return True
        return False
