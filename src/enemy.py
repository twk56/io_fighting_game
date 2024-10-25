# src/enemy.py

import pygame
import random
import config
import os
import math

class Enemy:
    def __init__(self):
        # กำหนดตำแหน่งสุ่มของศัตรูภายในขอบเขตของแมพ
        self.position = [
            random.randint(0, config.MAP_WIDTH - config.ENEMY_SIZE),
            random.randint(0, config.MAP_HEIGHT - config.ENEMY_SIZE)
        ]
        self.size = config.ENEMY_SIZE  # ขนาดของศัตรู
        self.health = config.ENEMY_MAX_HEALTH  # ค่าชีวิตของศัตรู
        self.damage = 5  # ดาเมจการโจมตีระยะใกล้
        self.is_alive = True  # ตรวจสอบว่ายังมีชีวิตอยู่หรือไม่
        self.attack_cooldown = config.ENEMY_ATTACK_COOLDOWN  # หน่วงเวลาโจมตี (เฟรม)
        self.attack_timer = 0  # ตัวจับเวลาหน่วงการโจมตี
        self.speed = config.ENEMY_SPEED

        # โหลดรูปภาพศัตรูและปรับขนาด
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'enemy.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded enemy image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพศัตรูได้: {e}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(config.ENEMY_COLOR)  # ใช้สีพื้นหลังแทนภาพถ้าไม่พบไฟล์

    def update(self, player_position, player_attacking):
        # เมธอดนี้จะถูก override โดย subclasses
        pass

    def draw(self, screen, camera_x, camera_y):
        if self.is_alive:
            # วาดศัตรูโดยใช้รูปภาพ
            screen.blit(self.image, (self.position[0] - camera_x, self.position[1] - camera_y))
            
            # วาดแถบชีวิตของศัตรู
            health_bar_width = self.size * (self.health / config.ENEMY_MAX_HEALTH)  # ความยาวของแถบชีวิตสัมพันธ์กับค่าชีวิต
            pygame.draw.rect(screen, (100, 0, 0), (self.position[0] - camera_x, self.position[1] - 10 - camera_y, 
                                                  config.ENEMY_HEALTH_BAR_WIDTH, 5))  # กรอบแถบสุขภาพ
            pygame.draw.rect(screen, (0, 200, 0), (self.position[0] - camera_x, self.position[1] - 10 - camera_y, 
                                                  health_bar_width, 5))  # แถบพลังชีวิต

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False  # ถ้าค่าชีวิตเป็น 0 หรือต่ำกว่าให้ตาย
