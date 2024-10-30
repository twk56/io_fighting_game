# src/player.py

import pygame
import config
import math
import os
from bullet import Bullet
from utils import check_boundary

class Player:
    def __init__(self, add_notification_func, background_size):
        self.add_notification = add_notification_func
        self.position = [config.MAP_WIDTH // 2, config.MAP_HEIGHT // 2]
        self.size = config.PLAYER_SIZE
        self.color = config.PLAYER_COLOR
        self.speed = config.PLAYER_SPEED
        self.damage = 10
        self.health = config.PLAYER_MAX_HEALTH
        self.shield = config.PLAYER_MAX_SHIELD
        self.direction = [0, 0]
        self.hit_flash_duration = 0

        # ตัวแปรสำหรับโหมดปืน
        self.gun_mode = False
        self.gun_mode_end_time = 0
        self.gun_shoot_cooldown = 300
        self.last_shot_time = pygame.time.get_ticks()

        # โหลดรูปภาพผู้เล่น
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'player.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded player image from {image_path}")
        except pygame.error as e:
            print(f"ไม่สามารถโหลดภาพผู้เล่นได้: {e}")
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
        new_position_x = self.position[0] + self.direction[0] * self.speed
        new_position_y = self.position[1] + self.direction[1] * self.speed

        # ตรวจสอบขอบเขตของแผนที่
        if (0 <= new_position_x <= config.MAP_WIDTH and
            0 <= new_position_y <= config.MAP_HEIGHT):

            # อัปเดตตำแหน่งถ้าไม่มีการชน
            self.position[0] = new_position_x
            self.position[1] = new_position_y

        if check_boundary((new_position_x, new_position_y), config.BOUNDARY_RADIUS):
            self.position[0] = new_position_x
            self.position[1] = new_position_y
        else:
            # ถ้าผู้เล่นพยายามเคลื่อนที่ออกนอกขอบเขต วางไว้ที่ขอบสุด
            center_x = config.MAP_WIDTH // 2
            center_y = config.MAP_HEIGHT // 2
            angle = math.atan2(new_position_y - center_y, new_position_x - center_x)
            self.position[0] = center_x + config.BOUNDARY_RADIUS * math.cos(angle)
            self.position[1] = center_y + config.BOUNDARY_RADIUS * math.sin(angle)

        # Update hit flash
        if self.hit_flash_duration > 0:
            self.hit_flash_duration -= 1

        # Update gun mode duration
        current_time = pygame.time.get_ticks()
        if self.gun_mode and current_time > self.gun_mode_end_time:
            self.gun_mode = False
            self.add_notification("Gun Mode Deactivated!", 2000)  # แจ้งเตือนเมื่อโหมดปืนถูกปิดใช้งาน

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
        current_time = pygame.time.get_ticks()
        bullets = []

        if self.gun_mode:
            if current_time - self.last_shot_time >= self.gun_shoot_cooldown:
                self.last_shot_time = current_time
                bullets.extend(self.shoot_gun(target_pos))
        else:
            # โหมดยิงปกติ (กระสุนเดียว)
            bullet = Bullet(self.position, target_pos, self.damage)
            bullets.append(bullet)

        return bullets

    def shoot_gun(self, target_pos):
        # การยิงกระจาย 3 ลูก
        bullets = []
        angle = math.atan2(target_pos[1] - self.position[1], target_pos[0] - self.position[0])
        spread_angle = math.radians(15)  # กระจาย ±15 องศา

        for i in range(-1, 2):  # -1, 0, 1 สำหรับการกระจายทั้งซ้ายและขวา
            new_angle = angle + i * spread_angle
            dx = math.cos(new_angle)
            dy = math.sin(new_angle)
            # คำนวณตำแหน่งเป้าหมายใหม่สำหรับกระสุนแต่ละลูก
            new_target = (
                self.position[0] + dx * 1000,  # 1000 เป็นระยะทางที่กระสุนจะไปถึง
                self.position[1] + dy * 1000
            )
            bullet = Bullet(self.position, new_target, self.damage)
            bullets.append(bullet)

        return bullets

    def enable_gun_mode(self):
        self.gun_mode = True
        self.gun_mode_end_time = pygame.time.get_ticks() + config.GUN_DURATION
        self.add_notification("Gun Mode Activated!", 2000)  # แจ้งเตือนเมื่อโหมดปืนถูกเปิดใช้งาน

    def take_damage(self, damage):
        if self.shield > 0:
            self.shield -= damage
            if self.shield < 0:
                self.health += self.shield  # self.shield เป็นค่าลบ
                self.shield = 0
        else:
            self.health -= damage
        self.hit_flash_duration = 10  # ตั้งค่าระยะเวลาการเปลี่ยนสี

    def regenerate_shield(self):
        # สามารถเพิ่มการรีเจนเนอเรทโล่ได้ถ้าต้องการ
        regen_rate = 1  # จำนวนที่ฟื้นฟูต่อเฟรม
        if self.shield < config.PLAYER_MAX_SHIELD:
            self.shield += regen_rate
            if self.shield > config.PLAYER_MAX_SHIELD:
                self.shield = config.PLAYER_MAX_SHIELD
