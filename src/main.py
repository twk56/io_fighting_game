# src/main.py

import pygame
import random
from entities.player import Player
from entities.enemy_types import FastEnemy, StrongEnemy, BalancedEnemy, MeleeEnemy, RangedEnemy
from entities.health_item import HealthItem
from entities.power_up_item import PowerUpItem
from entities.explosion import Explosion
import config
import os
from entities.enemy_bullet import EnemyBullet
import math

pygame.init()

# โหลดเสียง
try:
    shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'shoot.mp3'))
    hit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'hit.wav'))
    explosion_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'explosion.mp3'))
except pygame.error as e:
    print(f"Error loading sound: {e}")
    shoot_sound = None
    hit_sound = None
    explosion_sound = None

# กำหนดขนาดหน้าจอ
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Fighting .io Game")

# สร้างฟอนต์
font = pygame.font.Font(None, config.FONT_SIZE)

# ฟังก์ชันสำหรับโหลดภาพพื้นหลัง
def load_background():
    script_dir = os.path.dirname(__file__)  # ตำแหน่งของไฟล์ main.py
    image_path = os.path.join(script_dir, '..', config.BACKGROUND_IMAGE_PATH)
    image_path = os.path.normpath(image_path)  # ปรับเส้นทางให้ถูกต้องตามระบบปฏิบัติการ

    try:
        background_image = pygame.image.load(image_path)
        # ปรับขนาดภาพพื้นหลังให้ตรงกับขนาดแผนที่
        background_image = pygame.transform.scale(background_image, (config.MAP_WIDTH, config.MAP_HEIGHT))
        return background_image
    except Exception as e:
        print(f"ไม่สามารถโหลดภาพพื้นหลังได้: {e}")
        return None  # คืนค่า None หากไม่สามารถโหลดภาพพื้นหลังได้

background = load_background()

# อ่านคะแนนสูงสุดจากไฟล์
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read().strip())
except FileNotFoundError:
    high_score = 0

# ตัวแปรเก็บ Notifications
notifications = []

# ตัวแปรเก็บเอฟเฟกต์การระเบิด
explosions = []

# ฟังก์ชันสำหรับเพิ่ม Notification
def add_notification(message, duration=2000):
    notifications.append({"message": message, "duration": duration, "time_added": pygame.time.get_ticks()})

# ฟังก์ชันแสดง Notifications ที่ด้านขวามือของหน้าจอ
def display_notifications():
    padding_right = 20  # ระยะห่างจากขอบขวา
    padding_top = 20    # ระยะห่างจากขอบบน
    spacing = 30        # ระยะห่างระหว่างข้อความแต่ละรายการ
    current_time = pygame.time.get_ticks()
    
    # เริ่มต้นตำแหน่ง y
    y_offset = padding_top
    
    for notification in notifications[:]:
        if current_time - notification["time_added"] > notification["duration"]:
            notifications.remove(notification)
        else:
            text_surface = font.render(notification["message"], True, (255, 255, 0))
            text_rect = text_surface.get_rect()
            x = config.SCREEN_WIDTH - padding_right - text_rect.width
            y = y_offset
            screen.blit(text_surface, (x, y))
            y_offset += spacing  # เลื่อนตำแหน่ง y สำหรับข้อความถัดไป

# ฟังก์ชันแสดงหน้าจอเริ่มต้น
def show_start_screen():
    if background:
        # วาดพื้นหลังทั้งหมด
        screen.blit(background, (-camera_x, -camera_y))
    else:
        screen.fill(config.BACKGROUND_COLOR)
    title_text = font.render("Fighting .io Game", True, (0, 0, 0))
    start_text = font.render("Press SPACE to Start", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
    screen.blit(start_text, (config.SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
    screen.blit(high_score_text, (config.SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 400))
    pygame.display.flip()
    wait_for_key(pygame.K_SPACE)

# ฟังก์ชันแสดงหน้าจอเกมโอเวอร์
def show_game_over_screen(score):
    if background:
        screen.blit(background, (-camera_x, -camera_y))
    else:
        screen.fill(config.BACKGROUND_COLOR)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    restart_text = font.render("Press R to Restart", True, (0, 0, 0))
    screen.blit(game_over_text, (config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(high_score_text, (config.SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 400))
    screen.blit(restart_text, (config.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 500))
    pygame.display.flip()
    wait_for_key(pygame.K_r)

# ฟังก์ชันแสดงเมนู Pause
def show_pause_screen():
    paused = True
    pause_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
    pause_overlay.fill((0, 0, 0, 128))  # สีดำใส
    screen.blit(pause_overlay, (0, 0))
    pause_text = font.render("Paused", True, (255, 255, 255))
    resume_text = font.render("Press P to Resume", True, (255, 255, 255))
    screen.blit(pause_text, (config.SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 300))
    screen.blit(resume_text, (config.SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 350))
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# ฟังก์ชันรอการกดปุ่ม
def wait_for_key(key):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    waiting = False

# ฟังก์ชันอัพเกรด
def upgrade_player(upgrade_type):
    global score
    if score >= config.UPGRADE_COSTS[upgrade_type]:
        score -= config.UPGRADE_COSTS[upgrade_type]
        upgrades[upgrade_type] += 1
        if upgrade_type == 'speed':
            player.speed += config.UPGRADE_SPEED_INCREMENT
        elif upgrade_type == 'damage':
            player.damage += config.UPGRADE_DAMAGE_INCREMENT
        elif upgrade_type == 'shield':
            player.shield += config.UPGRADE_SHIELD_INCREMENT
            player.shield = min(player.shield, config.PLAYER_MAX_SHIELD)
        add_notification(f"Upgraded {upgrade_type.capitalize()}!", 2000)

# ฟังก์ชันแสดงเมนูอัพเกรด
def show_upgrade_menu():
    upgrade_options = config.power_up_types
    selected = 0
    while True:
        pause_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        pause_overlay.fill((50, 50, 50, 200))  # สีเทาเข้มใส
        screen.blit(pause_overlay, (0, 0))
        menu_text = font.render("Upgrade Menu", True, (255, 255, 255))
        screen.blit(menu_text, (config.SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 100))

        for i, upgrade in enumerate(upgrade_options):
            color = (255, 255, 255)
            if i == selected:
                color = (255, 0, 0)
            text = font.render(f"{upgrade.capitalize()} (Cost: {config.UPGRADE_COSTS[upgrade]})", True, color)
            screen.blit(text, (config.SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(upgrade_options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(upgrade_options)
                if event.key == pygame.K_RETURN:
                    upgrade_player(upgrade_options[selected])
                if event.key == pygame.K_ESCAPE:
                    return

# ตัวแปรสำหรับการเลเวลอัพ
score_thresholds = config.score_thresholds  # นำเข้า score_thresholds จาก config.py
current_level = 1
next_level_index = 0

# ฟังก์ชันสำหรับรีเซ็ตเกม
def reset_game():
    global score, current_level, next_level_index, high_score, player, enemies, bullets, enemy_bullets, health_items, power_ups, upgrades, current_item_spawn_interval
    score = 0
    current_level = 1
    next_level_index = 0
    player = Player()
    # สร้างศัตรูแบบผสมผสานระหว่าง Melee และ Ranged
    enemies = []
    for _ in range(2):
        enemies.append(FastEnemy())
        enemies.append(StrongEnemy())
        enemies.append(BalancedEnemy())
        enemies.append(MeleeEnemy())
        enemies.append(RangedEnemy())
    bullets = []
    enemy_bullets = []  # ลิสต์สำหรับกระสุนของศัตรู
    health_items = [HealthItem(random.randint(100, 400), random.randint(100, 400)) for _ in range(3)]
    power_up_spawn_positions = [(random.randint(100, 400), random.randint(100, 400)) for _ in range(3)]
    power_ups = [PowerUpItem(random.choice(config.power_up_types), pos) for pos in power_up_spawn_positions]
    upgrades = {'speed': 0, 'damage': 0, 'shield': 0}
    
    # ตั้งค่า Timer สำหรับการสุ่มไอเทมครั้งแรกเป็น 30 วินาที
    current_item_spawn_interval = config.ITEM_SPAWN_INTERVALS[0]  # เริ่มต้นด้วย 30,000 มิลลิวินาที (30 วินาที)
    pygame.time.set_timer(SPAWN_ITEM_EVENT, current_item_spawn_interval)

# ฟังก์ชันเพิ่มความยาก
def increase_difficulty():
    global current_level, next_level_index
    current_level += 1
    next_level_index += 1
    add_notification("Level Up!", 2000)

    for _ in range(5):  # เพิ่มศัตรู 5 ตัวเพิ่มเติมในแต่ละระดับ
        if len(enemies) < config.MAX_ENEMIES:
            enemies.append(random.choice([FastEnemy(), StrongEnemy(), BalancedEnemy(), MeleeEnemy(), RangedEnemy()]))
    
    for enemy in enemies:
        enemy.speed += 0.5

# ฟังก์ชันแสดง HUD
def draw_hud():
    """แสดง HUD ของเกมให้ดูสวยงามและชัดเจน"""

    # วาดกรอบพื้นหลังสีดำใสสำหรับ HUD
    hud_surface = pygame.Surface((220, 350), pygame.SRCALPHA)
    hud_surface.fill(config.HUD_BACKGROUND_COLOR)  # สีดำใส
    screen.blit(hud_surface, (10, 10))

    # แถบพลังชีวิตแบบสวยงาม
    health_bar_width = config.PLAYER_HEALTH_BAR_WIDTH
    health_ratio = player.health / config.PLAYER_MAX_HEALTH
    # กรอบแถบสุขภาพ
    pygame.draw.rect(screen, (100, 0, 0), (20, 20, config.PLAYER_HEALTH_BAR_WIDTH, 5))
    # แถบพลังชีวิต
    pygame.draw.rect(screen, (0, 200, 0), (20, 20, config.PLAYER_HEALTH_BAR_WIDTH * health_ratio, 5))
    health_text = font.render(f"Health: {int(player.health)} / {config.PLAYER_MAX_HEALTH}", True, (255, 255, 255))
    screen.blit(health_text, (20, 45))

    # แถบโล่
    shield_bar_width = config.PLAYER_SHIELD_BAR_WIDTH
    shield_ratio = player.shield / config.PLAYER_MAX_SHIELD
    # กรอบแถบโล่
    pygame.draw.rect(screen, (0, 0, 100), (20, 70, config.PLAYER_SHIELD_BAR_WIDTH, 20))
    # แถบโล่
    pygame.draw.rect(screen, (0, 0, 255), (20, 70, config.PLAYER_SHIELD_BAR_WIDTH * shield_ratio, 20))
    shield_text = font.render(f"Shield: {int(player.shield)} / {config.PLAYER_MAX_SHIELD}", True, (255, 255, 255))
    screen.blit(shield_text, (20, 95))

    # สถานะความเร็วและดาเมจพร้อมการออกแบบที่ชัดเจน
    speed_text = font.render(f"Speed: {player.speed}", True, (0, 0, 255))
    damage_text = font.render(f"Damage: {player.damage}", True, (255, 128, 0))
    screen.blit(speed_text, (20, 130))
    screen.blit(damage_text, (20, 160))

    # คะแนนและคะแนนสูงสุด
    score_text = font.render(f"Score: {score}", True, (0, 255, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 190))
    screen.blit(high_score_text, (20, 220))

    # เลเวลปัจจุบัน
    level_text = font.render(f"Level: {current_level}", True, (255, 255, 0))
    screen.blit(level_text, (20, 250))

    # การอัพเกรด
    upgrade_text = font.render("Upgrades:", True, (255, 255, 255))
    screen.blit(upgrade_text, (20, 280))
    for i, (upgrade, level) in enumerate(upgrades.items()):
        text = font.render(f"{upgrade.capitalize()}: {level}", True, config.POWER_UP_COLORS[upgrade])
        screen.blit(text, (20, 310 + i * 30))

# ฟังก์ชันแสดงเอฟเฟกต์การระเบิด
def handle_explosions():
    for explosion in explosions[:]:
        explosion.update()
        explosion.draw(screen, camera_x, camera_y)
        if explosion.is_finished():
            explosions.remove(explosion)

# กำหนดประเภทของ Event สำหรับการสร้างศัตรู
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
# ตั้งเวลาให้เกิด Event ทุกๆ 30,000 มิลลิวินาที (30 วินาที)
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 30000)

# กำหนด Custom Event สำหรับการสุ่มไอเทม
SPAWN_ITEM_EVENT = pygame.USEREVENT + 2

# ตัวแปรสำหรับการตั้งค่า Timer การสุ่มไอเทม
current_item_spawn_interval = config.ITEM_SPAWN_INTERVALS[0]  # เริ่มต้นด้วย 30,000 มิลลิวินาที (30 วินาที)

# เพิ่มลิสต์สำหรับกระสุนของศัตรู
enemy_bullets = []

# เพิ่มตัวแปรสำหรับติดตามการโจมตีของผู้เล่น
player_attacking = False
player_attack_time = 0
attack_duration = 1000  # ระยะเวลา (มิลลิวินาที) ที่ถือว่าผู้เล่นกำลังโจมตี (1 วินาที)

reset_game()

# ตัวแปรกล้อง
camera_x = 0
camera_y = 0

# แสดงหน้าจอเริ่มต้น
show_start_screen()

# ลูปหลัก
clock = pygame.time.Clock()
while True:
    clock.tick(60)  # จำกัดเฟรมเรตที่ 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                show_pause_screen()
            if event.key == pygame.K_u:
                show_upgrade_menu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                adjusted_mouse_pos = (mouse_pos[0] + camera_x, mouse_pos[1] + camera_y)
                bullets.append(player.shoot(adjusted_mouse_pos))
                if shoot_sound:
                    shoot_sound.play()
                # ตั้งค่าสถานะการโจมตีของผู้เล่น
                player_attacking = True
                player_attack_time = pygame.time.get_ticks()
        # ตรวจสอบการเกิดของ SPAWN_ENEMY_EVENT
        if event.type == SPAWN_ENEMY_EVENT:
            # สุ่มประเภทของศัตรูที่จะสร้าง 5 ตัว
            for _ in range(5):
                if len(enemies) < config.MAX_ENEMIES:
                    enemies.append(random.choice([FastEnemy(), StrongEnemy(), BalancedEnemy(), MeleeEnemy(), RangedEnemy()]))
            # เพิ่ม Notification ว่ามีศัตรูใหม่เกิดขึ้น
            add_notification(f"5 Enemies spawned!", 2000)
        # ตรวจสอบการเกิดของ SPAWN_ITEM_EVENT
        if event.type == SPAWN_ITEM_EVENT:
            # สุ่มจำนวนไอเทมที่จะสร้าง (ตัวอย่าง: สุ่มระหว่าง 1-3 ไอเทม)
            num_items_to_spawn = random.randint(config.ITEMS_PER_SPAWN_MIN, config.ITEMS_PER_SPAWN_MAX)
            for _ in range(num_items_to_spawn):
                # สุ่มประเภทไอเทม (Health หรือ Power-Up)
                item_type = random.choice(['health', 'power_up'])
                x = random.randint(100, config.MAP_WIDTH - 100)
                y = random.randint(100, config.MAP_HEIGHT - 100)
                if item_type == 'health':
                    health_items.append(HealthItem(x, y))
                    add_notification("Health Item Spawned!", 2000)
                else:
                    power_up_type = random.choice(config.power_up_types)
                    power_ups.append(PowerUpItem(power_up_type, (x, y)))
                    add_notification(f"{power_up_type.capitalize()} Power-Up Spawned!", 2000)
            
            # สลับระยะเวลาในการสุ่มไอเทมครั้งต่อไป
            if current_item_spawn_interval == config.ITEM_SPAWN_INTERVALS[0]:
                current_item_spawn_interval = config.ITEM_SPAWN_INTERVALS[1]  # เปลี่ยนเป็น 60,000 มิลลิวินาที (1 นาที)
            else:
                current_item_spawn_interval = config.ITEM_SPAWN_INTERVALS[0]  # เปลี่ยนเป็น 30,000 มิลลิวินาที (30 วินาที)
            
            # ตั้งค่า Timer สำหรับการสุ่มไอเทมครั้งต่อไป
            pygame.time.set_timer(SPAWN_ITEM_EVENT, current_item_spawn_interval)

    # อัพเดตสถานะการโจมตีของผู้เล่น
    current_time = pygame.time.get_ticks()
    if player_attacking and current_time - player_attack_time > attack_duration:
        player_attacking = False

    # วาดพื้นหลัง
    if background:
        # คำนวณตำแหน่งของพื้นหลังตามกล้อง
        screen.blit(background, (-camera_x, -camera_y))
    else:
        # ใช้สีพื้นหลังถ้าไม่พบภาพพื้นหลัง
        screen.fill(config.BACKGROUND_COLOR)

    # เรียกแสดง HUD และ Notifications
    draw_hud()
    display_notifications()

    # การแสดงเอฟเฟกต์การระเบิด
    handle_explosions()

    # อัพเดตตำแหน่งกล้อง
    camera_x = player.position[0] - config.SCREEN_WIDTH // 2
    camera_y = player.position[1] - config.SCREEN_HEIGHT // 2
    camera_x = max(0, min(camera_x, config.MAP_WIDTH - config.SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, config.MAP_HEIGHT - config.SCREEN_HEIGHT))

    # อัพเดตผู้เล่น
    player.update()
    player.draw(screen, camera_x, camera_y)

    # ตรวจสอบคะแนนเพื่อเพิ่มความยาก
    if next_level_index < len(score_thresholds) and score >= score_thresholds[next_level_index]:
        increase_difficulty()

    # อัพเดตศัตรู
    for enemy in enemies[:]:
        attack = enemy.update(player.position, player_attacking)
        if isinstance(attack, EnemyBullet):
            enemy_bullets.append(attack)
        elif attack:  # if attack is True (melee attack)
            player.take_damage(enemy.damage)
            if player.health <= 0:
                show_game_over_screen(score)
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))
                reset_game()
        enemy.draw(screen, camera_x, camera_y)

    # อัพเดตกระสุนของผู้เล่น
    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen, camera_x, camera_y)
        # ตรวจสอบการชนของกระสุนกับศัตรู
        for enemy in enemies[:]:
            if enemy.is_alive:
                # ใช้ระยะห่างแทนการตรวจสอบ bounding box สำหรับความแม่นยำที่ดีกว่า
                dx = enemy.position[0] - bullet.position[0]
                dy = enemy.position[1] - bullet.position[1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= enemy.size:
                    bullets.remove(bullet)
                    if hit_sound:
                        hit_sound.play()
                    enemy.take_damage(player.damage)
                    if not enemy.is_alive:
                        score += enemy.score_value
                        enemies.remove(enemy)  # ลบศัตรูที่ตายแล้วออกจากรายการ
                        if explosion_sound:
                            explosion_sound.play()
                        explosions.append(Explosion(enemy.position))
                    break  # กระสุนชนกับศัตรูแล้วไม่ต้องตรวจสอบศัตรูอื่น

    # อัพเดตกระสุนของศัตรู (ถ้ามี)
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.update()
        enemy_bullet.draw(screen, camera_x, camera_y)
        # ตรวจสอบการชนของกระสุนกับผู้เล่น
        dx = player.position[0] - enemy_bullet.position[0]
        dy = player.position[1] - enemy_bullet.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance <= player.size:
            enemy_bullets.remove(enemy_bullet)
            if hit_sound:
                hit_sound.play()
            player.take_damage(enemy_bullet.damage)
            if player.health <= 0:
                show_game_over_screen(score)
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))
                reset_game()

    # อัพเดตและวาดไอเท็มสุขภาพ
    for item in health_items[:]:
        if item.is_active:
            item.draw(screen, camera_x, camera_y)
            collected = item.collect(player)
            if collected:
                health_items.remove(item)
                add_notification("Collected Health Item!", 2000)
        else:
            health_items.remove(item)  # ลบไอเท็มที่ไม่ใช้งานออก

    # อัพเดตและวาดไอเท็มพลังเสริม
    for power_up in power_ups[:]:
        if power_up.is_active:
            power_up.draw(screen, camera_x, camera_y)
            collected = power_up.collect(player)
            if collected:
                if power_up.type == 'shield':
                    player.shield = min(player.shield + 20, config.PLAYER_MAX_SHIELD)
                elif power_up.type == 'speed':
                    player.speed += 1
                elif power_up.type == 'damage':
                    player.damage += 1
                power_ups.remove(power_up)
                add_notification(f"Collected {power_up.type.capitalize()} Power-Up!", 2000)
        else:
            power_ups.remove(power_up)  # ลบไอเท็มที่ไม่ใช้งานออก

    # อัพเดตพลังชีวิตของผู้เล่น
    player.regenerate_shield()

    pygame.display.flip()
