# src/enemy_types.py

from enemy import Enemy
import config
import pygame
import os
import math
from enemy_bullet import EnemyBullet
import random



class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = config.ENEMY_SPEED * 1.5  # ความเร็วสูงขึ้น
        self.health = 70  # พลังชีวิตปกติ
        self.damage = 12  # ดาเมจปกติ
        self.score_value = 20  # คะแนนที่ได้รับเมื่อจัดการได้

        # โหลดรูปภาพเฉพาะสำหรับ FastEnemy
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'fast_enemy.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded FastEnemy image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพ FastEnemy ได้: {e}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((255, 0, 0))  # ใช้สีแดงแทน

    def update(self, player_position, player_attacking):
        if self.is_alive:
            # เคลื่อนที่ไปยังผู้เล่น
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                self.direction = [dx / distance, dy / distance]
                self.position[0] += self.direction[0] * self.speed
                self.position[1] += self.direction[1] * self.speed

            # ลดค่าหน่วงเวลาโจมตี
            if self.attack_timer > 0:
                self.attack_timer -= 1

            # คำนวณระยะห่างระหว่างศัตรูกับผู้เล่น
            distance_to_player = distance

            # กำหนดเงื่อนไขการโจมตี
            if distance_to_player <= config.MELEE_ATTACK_RANGE and self.attack_timer == 0:
                self.attack_timer = config.ENEMY_ATTACK_COOLDOWN
                return True  # ส่งสัญญาณให้ศัตรูโจมตีผู้เล่นแบบ Melee

        return False  # หากไม่โจมตี

class StrongEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = config.ENEMY_SPEED * 0.8  # ความเร็วต่ำลง
        self.health = 150  # พลังชีวิตสูงขึ้น
        self.damage = 20  # ดาเมจสูงขึ้น
        self.score_value = 30  # คะแนนที่ได้รับเมื่อจัดการได้

        # โหลดรูปภาพเฉพาะสำหรับ StrongEnemy
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'strong_enemy.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded StrongEnemy image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพ StrongEnemy ได้: {e}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((128, 0, 128))  # ใช้สีม่วงแทน

    def update(self, player_position, player_attacking):
        if self.is_alive:
            # เคลื่อนที่ไปยังผู้เล่น
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                self.direction = [dx / distance, dy / distance]
                self.position[0] += self.direction[0] * self.speed
                self.position[1] += self.direction[1] * self.speed

            # ลดค่าหน่วงเวลาโจมตี
            if self.attack_timer > 0:
                self.attack_timer -= 1

            # คำนวณระยะห่างระหว่างศัตรูกับผู้เล่น
            distance_to_player = distance

            # กำหนดเงื่อนไขการโจมตี
            if distance_to_player <= config.MELEE_ATTACK_RANGE and self.attack_timer == 0:
                self.attack_timer = config.ENEMY_ATTACK_COOLDOWN
                return True  # ส่งสัญญาณให้ศัตรูโจมตีผู้เล่นแบบ Melee

        return False  # หากไม่โจมตี

class BalancedEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = config.ENEMY_SPEED * 1.0  # ความเร็วปกติ
        self.health = 100  # พลังชีวิตปกติ
        self.damage = 15  # ดาเมจปกติ
        self.score_value = 25  # คะแนนที่ได้รับเมื่อจัดการได้

        # โหลดรูปภาพเฉพาะสำหรับ BalancedEnemy
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'balanced_enemy.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded BalancedEnemy image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพ BalancedEnemy ได้: {e}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((0, 255, 0))  # ใช้สีเขียวแทน

    def update(self, player_position, player_attacking):
        if self.is_alive:
            # เคลื่อนที่ไปยังผู้เล่น
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                self.direction = [dx / distance, dy / distance]
                self.position[0] += self.direction[0] * self.speed
                self.position[1] += self.direction[1] * self.speed

            # ลดค่าหน่วงเวลาโจมตี
            if self.attack_timer > 0:
                self.attack_timer -= 1

            # คำนวณระยะห่างระหว่างศัตรูกับผู้เล่น
            distance_to_player = distance

            # กำหนดเงื่อนไขการโจมตี
            if distance_to_player <= config.MELEE_ATTACK_RANGE and self.attack_timer == 0:
                self.attack_timer = config.ENEMY_ATTACK_COOLDOWN
                return True  # ส่งสัญญาณให้ศัตรูโจมตีผู้เล่นแบบ Melee

        return False  # หากไม่โจมตี

class MeleeEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = config.ENEMY_SPEED * 1.3  # ความเร็วสูงขึ้นเล็กน้อย
        self.health = 200  # พลังชีวิตสูงสุด
        self.damage = 25  # ดาเมจสูงสุด
        self.score_value = 50  # คะแนนที่ได้รับเมื่อจัดการได้

        # โหลดรูปภาพเฉพาะสำหรับ MeleeEnemy
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'melee_enemy.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded MeleeEnemy image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพ MeleeEnemy ได้: {e}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((0, 0, 255))  # ใช้สีน้ำเงินแทน

    def update(self, player_position, player_attacking):
        if self.is_alive:
            # เคลื่อนที่ไปยังผู้เล่น
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                self.direction = [dx / distance, dy / distance]
                self.position[0] += self.direction[0] * self.speed
                self.position[1] += self.direction[1] * self.speed

            # ลดค่าหน่วงเวลาโจมตี
            if self.attack_timer > 0:
                self.attack_timer -= 1

            # คำนวณระยะห่างระหว่างศัตรูกับผู้เล่น
            distance_to_player = distance

            # กำหนดเงื่อนไขการโจมตี
            if distance_to_player <= config.MELEE_ATTACK_RANGE and self.attack_timer == 0:
                self.attack_timer = config.ENEMY_ATTACK_COOLDOWN
                return True  # ส่งสัญญาณให้ศัตรูโจมตีผู้เล่นแบบ Melee

        return False  # หากไม่โจมตี

class RangedEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = config.ENEMY_SPEED * 0.8  # ความเร็วต่ำลง
        self.health = 80  # พลังชีวิตต่ำกว่า
        self.damage = 10  # ดาเมจปกติ
        self.score_value = 15  # คะแนนที่ได้รับเมื่อจัดการได้

        # โหลดรูปภาพเฉพาะสำหรับ RangedEnemy
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'ranged_enemy.png')
        image_path = os.path.normpath(image_path)

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            print(f"Loaded RangedEnemy image from {image_path}")
        except Exception as e:
            print(f"ไม่สามารถโหลดภาพ RangedEnemy ได้: {e}")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((255, 0, 255))  # ใช้สีม่วงแทน

    def update(self, player_position, player_attacking):
        if self.is_alive:
            # ลดค่าหน่วงเวลาโจมตี
            if self.attack_timer > 0:
                self.attack_timer -= 1

            # คำนวณระยะห่างระหว่างศัตรูกับผู้เล่น
            dx = player_position[0] - self.position[0]
            dy = player_position[1] - self.position[1]
            distance_to_player = math.sqrt(dx**2 + dy**2)

            # กำหนดเงื่อนไขการโจมตี
            should_attack = False

            if distance_to_player <= config.RANGED_ATTACK_RANGE and self.attack_timer == 0:
                should_attack = True
            elif player_attacking and self.attack_timer == 0:
                should_attack = True

            if should_attack:
                self.attack_timer = config.ENEMY_ATTACK_COOLDOWN
                # ยิงกระสุนไปยังผู้เล่น
                return self.shoot(player_position)
        return False  # หากไม่โจมตี

    def shoot(self, target_pos):
        return EnemyBullet(self.position, target_pos, self.damage)
    
class BossEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = config.ENEMY_SPEED * 0.5
        self.health = 300
        self.damage = 0
        self.score_value = 100

        # โหลดภาพ
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, '..', 'assets', 'images', 'boss_enemy.png')
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.rect = self.image.get_rect(center=(self.position[0], self.position[1]))
            print(f"Loaded BossEnemy image from {image_path}")
        except Exception as e:
            print(f"Failed to load BossEnemy image: {e}")
            self.image = pygame.Surface((150, 150))
            self.image.fill((255, 0, 0))  # ใช้สีแดงแทน
            self.rect = self.image.get_rect(center=(self.position[0], self.position[1]))

        self.direction = random.choice([-1, 1])  # กำหนดทิศทางเริ่มต้น

    def update(self, player_position=None, player_attacking=None):
        if self.is_alive:
            self.position[0] += self.direction * self.speed
            # ตรวจสอบขอบเขตหน้าจอ
            if self.position[0] <= 0 or self.position[0] >= config.SCREEN_WIDTH - self.image.get_width():
                self.direction *= -1  # เปลี่ยนทิศทางเมื่อถึงขอบ
            self.rect.topleft = self.position  # อัปเดต rect

            # ตัวอย่างการใช้พารามิเตอร์เพิ่มเติม
            if player_position:
                # ทำบางอย่างกับตำแหน่งของผู้เล่น เช่น การเคลื่อนที่เข้าหาผู้เล่น
                dx = player_position[0] - self.position[0]
                dy = player_position[1] - self.position[1]
                angle = math.atan2(dy, dx)
                self.position[0] += math.cos(angle) * self.speed * 0.1  # เคลื่อนที่เข้าหาผู้เล่นช้าๆ
                self.position[1] += math.sin(angle) * self.speed * 0.1
                self.rect.topleft = self.position  # อัปเดต rect

            # คุณสามารถเพิ่มลอจิกอื่นๆ ตามต้องการ เช่น การโจมตีเมื่อผู้เล่นอยู่ในระยะใกล้

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.topleft[0] - camera_x, self.rect.topleft[1] - camera_y))
        # วาดหลอดเลือด
        health_bar_width = 150  # ความกว้างของหลอดเลือด
        health_ratio = self.health / 300  # เปลี่ยน 300 เป็นพลังชีวิตสูงสุดของบอส
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.topleft[0] - camera_x, self.rect.topleft[1] - camera_y - 10, health_bar_width, 10))  # กรอบหลอดเลือด
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.topleft[0] - camera_x, self.rect.topleft[1] - camera_y - 10, health_bar_width * health_ratio, 10))  # แถบพลังชีวิต



        