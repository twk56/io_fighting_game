# src/player.py

import pygame
import config
import math
from entities.bullet import Bullet  # เพิ่มการนำเข้าคลาส Bullet
import os

class Player:
    def __init__(self):
        self.position = [config.MAP_WIDTH // 2, config.MAP_HEIGHT // 2]
        self.size = config.PLAYER_SIZE
        self.color = config.PLAYER_COLOR
        self.speed = config.PLAYER_SPEED
        self.damage = 10
        self.health = config.PLAYER_MAX_HEALTH
        self.shield = config.PLAYER_MAX_SHIELD
        self.direction = [0, 0]
        self.hit_flash_duration = 0  # ระยะเวลาการเปลี่ยนสีเมื่อถูกโจมตี

        # โหลดรูปภาพผู้เล่น
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'player.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            # ปรับขนาดภาพผู้เล่นให้ตรงกับขนาดที่กำหนด
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded player image from {image_path}")
        except pygame.error as e:
            print(f"ไม่สามารถโหลดภาพผู้เล่นได้: {e}")
            # ใช้สีแทนผู้เล่นหากไม่สามารถโหลดภาพได้
            self.image = None

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction = [0, 0]
        if keys[pygame.K_w]:
            self.direction[1] -= 1
        if keys[pygame.K_s]:
            self.direction[1] += 1
        if keys[pygame.K_a]:
            self.direction[0] -= 1
        if keys[pygame.K_d]:
            self.direction[0] += 1

        # Normalize direction
        magnitude = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
        if magnitude != 0:
            self.direction = [self.direction[0] / magnitude, self.direction[1] / magnitude]

        # Update position
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed

        # Keep player within map bounds
        self.position[0] = max(0, min(self.position[0], config.MAP_WIDTH - self.size))
        self.position[1] = max(0, min(self.position[1], config.MAP_HEIGHT - self.size))

        # Update hit flash
        if self.hit_flash_duration > 0:
            self.hit_flash_duration -= 1

    def draw(self, screen, camera_x, camera_y):
        if self.hit_flash_duration > 0:
            color = (255, 255, 0)  # สีเปลี่ยนเมื่อถูกโจมตี
        else:
            color = self.color

        if self.image:
            screen.blit(self.image, 
                        (int(self.position[0] - camera_x), 
                         int(self.position[1] - camera_y)))
        else:
            pygame.draw.rect(screen, color, 
                             (self.position[0] - camera_x, self.position[1] - camera_y, self.size, self.size))

    def shoot(self, target_pos):
        return Bullet(self.position, target_pos, self.damage)

    def take_damage(self, damage):
        if self.shield > 0:
            self.shield -= damage
            if self.shield < 0:
                self.health += self.shield  # self.shield is negative
                self.shield = 0
        else:
            self.health -= damage
        self.hit_flash_duration = 10  # ตั้งค่าระยะเวลาการเปลี่ยนสี

    def regenerate_shield(self):
        # สามารถเพิ่มการรีเจนเนอเรทโล่ได้ถ้าต้องการ
        pass
