# src/config.py

import os

# ขนาดหน้าจอ
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# ขนาดแผนที่
MAP_WIDTH = 3000
MAP_HEIGHT = 2000

# สีพื้นหลัง (ใช้เป็นสีสำรองหากไม่พบภาพพื้นหลัง)
BACKGROUND_COLOR = (255, 255, 255)  # สีขาว

# พาธของภาพพื้นหลัง
BACKGROUND_IMAGE_PATH = os.path.join('assets', 'images', 'background.jpg')

# สีของผู้เล่น
PLAYER_COLOR = (0, 128, 255)
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 100
PLAYER_MAX_SHIELD = 50

# สีของศัตรู
ENEMY_COLOR = (255, 0, 0)
ENEMY_SIZE = 50
ENEMY_SPEED = 2
ENEMY_MAX_HEALTH = 100

# ระยะโจมตีของศัตรู
ENEMY_ATTACK_RANGE = 150  # พิกเซล

# ระยะโจมตีสำหรับ MeleeEnemy
MELEE_ATTACK_RANGE = 50  # พิกเซล

# ระยะโจมตีสำหรับ RangedEnemy
RANGED_ATTACK_RANGE = 300  # พิกเซล

# หน่วงเวลาโจมตีของศัตรู (เฟรม)
ENEMY_ATTACK_COOLDOWN = 60  # 1 วินาทีที่ 60 FPS

# ขนาดแถบชีวิตของศัตรู
ENEMY_HEALTH_BAR_WIDTH = 50

# สีของกระสุน
BULLET_COLOR = (255, 0, 0)  # สีแดง
BULLET_SIZE = 10
BULLET_SPEED = 10
BULLET_IMAGE_PATH = os.path.join('assets', 'images', 'bullet.png')  # เพิ่มพาธของ bullet.png

# ฟอนต์และข้อความ
FONT_SIZE = 36
SCORE_COLOR = (0, 0, 0)

# สีและขนาดของไอเทมฟื้นฟูชีวิต
HEALTH_ITEM_COLOR = (0, 255, 0)
HEALTH_ITEM_SIZE = 20

# สีและขนาดของไอเทมพลังเสริม
POWER_UP_COLORS = {
    'speed': (0, 0, 255),
    'damage': (255, 165, 0),
    'shield': (128, 128, 128)
}
POWER_UP_SIZE = 20

# ระดับคะแนนสำหรับเพิ่มความยาก
score_thresholds = [1000, 2000, 3000, 5000]  # ตัวอย่างคะแนนที่จะเพิ่มระดับความยาก

# ประเภทของ Power-Ups
power_up_types = ['speed', 'damage', 'shield']

# ความเร็วที่เพิ่มขึ้นเมื่อมีการอัพเกรด
UPGRADE_SPEED_INCREMENT = 1
UPGRADE_DAMAGE_INCREMENT = 1
UPGRADE_SHIELD_INCREMENT = 10

# สีของ HUD
HUD_BACKGROUND_COLOR = (0, 0, 0, 128)  # สีดำใส

# จำนวนศัตรูสูงสุด
MAX_ENEMIES = 100

# ระบบการอัพเกรด
UPGRADE_COSTS = {
    'speed': 500,
    'damage': 500,
    'shield': 500
}

# ขนาดกระสุนของศัตรู
ENEMY_BULLET_SIZE = 8
ENEMY_BULLET_SPEED = 12
ENEMY_BULLET_COLOR = (255, 165, 0)  # สีส้ม
ENEMY_BULLET_IMAGE_PATH = os.path.join('assets', 'images', 'enemy_bullet.png')  # หากมี

# ขนาดแถบสุขภาพและโล่ของผู้เล่น
PLAYER_HEALTH_BAR_WIDTH = 180
PLAYER_SHIELD_BAR_WIDTH = 180

# ค่าคงที่สำหรับการสุ่มไอเทม
ITEM_SPAWN_INTERVALS = [30000, 60000]  # 30,000 ms (30 วินาที) และ 60,000 ms (1 นาที)
ITEMS_PER_SPAWN_MIN = 5
ITEMS_PER_SPAWN_MAX = 10