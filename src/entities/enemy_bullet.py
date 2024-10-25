# src/enemy_bullet.py

import pygame
import math
import config
import os

class EnemyBullet:
    def __init__(self, position, target_pos, damage):
        self.position = list(position)
        self.size = config.ENEMY_BULLET_SIZE
        self.damage = damage
        self.speed = config.ENEMY_BULLET_SPEED

        # โหลดรูปภาพกระสุนของศัตรู
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', config.ENEMY_BULLET_IMAGE_PATH)
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            # ปรับขนาดภาพกระสุนให้ตรงกับขนาดที่กำหนด
            self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
            print(f"Loaded enemy bullet image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพกระสุนของศัตรูได้: {e}")
            # ใช้วงกลมแทนกระสุนหากไม่สามารถโหลดภาพได้
            self.image = None
            self.color = config.ENEMY_BULLET_COLOR

        # คำนวณทิศทางของกระสุน
        direction = [target_pos[0] - self.position[0], target_pos[1] - self.position[1]]
        magnitude = math.sqrt(direction[0]**2 + direction[1]**2)
        if magnitude != 0:
            self.direction = [direction[0] / magnitude, direction[1] / magnitude]
        else:
            self.direction = [0, 0]

    def update(self):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed

    def draw(self, screen, camera_x, camera_y):
        if self.image:
            screen.blit(self.image, 
                        (int(self.position[0] - camera_x - self.size), 
                         int(self.position[1] - camera_y - self.size)))
        else:
            pygame.draw.circle(screen, self.color, 
                               (int(self.position[0] - camera_x), int(self.position[1] - camera_y)), self.size)
