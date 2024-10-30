# src/bullet.py

import pygame
import math
import config
import os

class Bullet:
    def __init__(self, position, target_pos, damage):
        self.position = list(position)
        self.size = config.BULLET_SIZE
        self.damage = damage
        self.speed = config.BULLET_SPEED

        # โหลดรูปภาพกระสุน
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', config.BULLET_IMAGE_PATH)
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            # ปรับขนาดภาพกระสุนให้ตรงกับขนาดที่กำหนด
            self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
            print(f"Loaded bullet image from {image_path}")
        except pygame.error as e:
            print(f"ไม่สามารถโหลดภาพกระสุนได้: {e}")
            # ใช้วงกลมแทนกระสุนหากไม่สามารถโหลดภาพได้
            self.image = None
            self.color = config.BULLET_COLOR

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

    def is_off_screen(self):
        """ตรวจสอบว่ากระสุนออกนอกขอบเขตแผนที่หรือไม่"""
        return (self.position[0] < 0 or self.position[0] > config.MAP_WIDTH or
                self.position[1] < 0 or self.position[1] > config.MAP_HEIGHT)
