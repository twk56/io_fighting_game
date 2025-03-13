# src/game.py

import pygame
import random
import math
import config
import os
from player import Player
from enemy_types import FastEnemy, StrongEnemy, BalancedEnemy, MeleeEnemy, RangedEnemy, BossEnemy
from health_item import HealthItem
from power_up_item import PowerUpItem
from explosion import Explosion
from enemy_bullet import EnemyBullet
from map import Map
from menu import show_start_menu, show_game_over_menu
from utils import check_boundary

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('assets/fonts/Popcat.otf', config.FONT_SIZE)
        self.high_score = self.load_high_score()
        self.notifications = []
        self.explosions = []
        self.enemy_bullets = []
        self.score = 0
        self.current_level = 1
        self.next_level_index = 0
        self.game_map = Map()
        self.load_sounds()
        self.reset_game()
        self.game_state = "MENU"

        # กำหนดแอตทริบิวต์สำหรับการโจมตีของผู้เล่น
        self.player_attacking = False
        self.player_attack_time = 0
        self.attack_duration = config.attack_duration

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def load_sounds(self):
        try:
            pygame.mixer.music.load(os.path.join('assets', 'sounds', 'background_music.mp3'))
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error loading background music: {e}")
        
        try:
            self.shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'shoot.mp3'))
            self.hit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'hit.wav'))
            self.explosion_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'explosion.mp3'))
        except pygame.error as e:
            print(f"Error loading sound: {e}")
            self.shoot_sound = None
            self.hit_sound = None
            self.explosion_sound = None

    def add_notification(self, message, duration=2000):
        self.notifications.append({"message": message, "duration": duration, "time_added": pygame.time.get_ticks()})
    
    def display_notifications(self):
        padding_right = 20
        padding_top = 20
        spacing = 30
        current_time = pygame.time.get_ticks()
        y_offset = padding_top

        for notification in self.notifications[:]:
            if current_time - notification["time_added"] > notification["duration"]:
                self.notifications.remove(notification)
            else:
                text_surface = self.font.render(notification["message"], True, (255, 255, 0))
                x = config.SCREEN_WIDTH - padding_right - text_surface.get_width()
                self.screen.blit(text_surface, (x, y_offset))
                y_offset += spacing

    def upgrade_player(self, upgrade_type):
        if self.score >= config.UPGRADE_COSTS[upgrade_type]:
            self.score -= config.UPGRADE_COSTS[upgrade_type]
            self.upgrades[upgrade_type] += 1
            if upgrade_type == 'speed':
                self.player.speed += config.UPGRADE_SPEED_INCREMENT
            elif upgrade_type == 'damage':
                self.player.damage += config.UPGRADE_DAMAGE_INCREMENT
            elif upgrade_type == 'shield':
                self.player.shield += config.UPGRADE_SHIELD_INCREMENT
                self.player.shield = min(self.player.shield, config.PLAYER_MAX_SHIELD)
            elif upgrade_type == 'gun':
                self.player.enable_gun_mode()
                self.add_notification("Gun Mode Activated!", 2000)
            self.add_notification(f"Upgraded {upgrade_type.capitalize()}!", 2000)

    def show_upgrade_menu(self):
        upgrade_options = config.power_up_types
        selected = 0
        
        while True:
            pause_overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            pause_overlay.fill((50, 50, 50, 200))
            self.screen.blit(pause_overlay, (0, 0))
            menu_text = self.font.render("Upgrade Menu", True, (255, 255, 255))
            self.screen.blit(menu_text, (config.SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 100))

            for i, upgrade in enumerate(upgrade_options):
                color = (255, 0, 0) if i == selected else (255, 255, 255)
                text = self.font.render(f"{upgrade.capitalize()} (Cost: {config.UPGRADE_COSTS[upgrade]})", True, color)
                self.screen.blit(text, (config.SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
            
            pygame.display.flip()
            self.clock.tick(60)

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
                        self.upgrade_player(upgrade_options[selected])
                    if event.key == pygame.K_ESCAPE:
                        return

    def reset_game(self):
        self.score = 0
        self.current_level = 1
        self.next_level_index = 0
        self.player = Player(self.add_notification, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.player.position = [config.MAP_WIDTH // 2, config.MAP_HEIGHT // 2]
        
        # แก้ไขการสร้างศัตรูให้ถูกต้อง
        self.enemies = []
        for _ in range(2):
            self.enemies.extend([FastEnemy(), StrongEnemy(), BalancedEnemy(), MeleeEnemy(), RangedEnemy()])
        
        self.bullets = []
        self.enemy_bullets = []
        self.health_items = [HealthItem((random.randint(100, 400), random.randint(100, 400))) for _ in range(3)]
        power_up_spawn_positions = [(random.randint(100, 400), random.randint(100, 400)) for _ in range(3)]
        self.power_ups = [PowerUpItem(random.choice(config.power_up_types), pos) for pos in power_up_spawn_positions]
        self.upgrades = {upgrade: 0 for upgrade in config.power_up_types}
        pygame.time.set_timer(pygame.USEREVENT + 2, config.ITEM_SPAWN_INTERVALS[0])

    def increase_difficulty(self):
        self.current_level += 1
        self.next_level_index += 1
        self.add_notification("Level Up!", 2000)
        for _ in range(5):
            if len(self.enemies) < config.MAX_ENEMIES:
                self.enemies.append(random.choice([FastEnemy(), StrongEnemy(), BalancedEnemy(), MeleeEnemy(), RangedEnemy()]))
        for enemy in self.enemies:
            enemy.speed += 0.5

    def draw_hud(self):
        hud_surface = pygame.Surface((220, 400), pygame.SRCALPHA)
        hud_surface.fill(config.HUD_BACKGROUND_COLOR)
        self.screen.blit(hud_surface, (10, 10))

        # Health Bar
        health_ratio = self.player.health / config.PLAYER_MAX_HEALTH
        pygame.draw.rect(self.screen, (100, 0, 0), (20, 20, config.PLAYER_HEALTH_BAR_WIDTH, 5))
        pygame.draw.rect(self.screen, (0, 200, 0), (20, 20, config.PLAYER_HEALTH_BAR_WIDTH * health_ratio, 5))
        health_text = self.font.render(f"Health: {int(self.player.health)} / {config.PLAYER_MAX_HEALTH}", True, (255, 255, 255))
        self.screen.blit(health_text, (20, 45))

        # Shield Bar
        shield_ratio = self.player.shield / config.PLAYER_MAX_SHIELD
        pygame.draw.rect(self.screen, (0, 0, 100), (20, 70, config.PLAYER_SHIELD_BAR_WIDTH, 20))
        pygame.draw.rect(self.screen, (0, 0, 255), (20, 70, config.PLAYER_SHIELD_BAR_WIDTH * shield_ratio, 20))
        shield_text = self.font.render(f"Shield: {int(self.player.shield)} / {config.PLAYER_MAX_SHIELD}", True, (255, 255, 255))
        self.screen.blit(shield_text, (20, 95))

        # Speed and Damage
        speed_text = self.font.render(f"Speed: {self.player.speed}", True, (0, 0, 255))
        damage_text = self.font.render(f"Damage: {self.player.damage}", True, (255, 128, 0))
        self.screen.blit(speed_text, (20, 130))
        self.screen.blit(damage_text, (20, 160))

        # Score and High Score
        score_text = self.font.render(f"Score: {self.score}", True, (0, 255, 0))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 190))
        self.screen.blit(high_score_text, (20, 220))

        # Current Level
        level_text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 0))
        self.screen.blit(level_text, (20, 250))

        # Upgrades
        upgrade_text = self.font.render("Upgrades:", True, (255, 255, 255))
        self.screen.blit(upgrade_text, (20, 280))
        for i, (upgrade, level) in enumerate(self.upgrades.items()):
            color = config.POWER_UP_COLORS.get(upgrade, (255, 255, 255))
            text = self.font.render(f"{upgrade.capitalize()} : {level}", True, color)
            self.screen.blit(text, (20, 310 + i * 30))
        
        # Gun Mode Status
        if self.player.gun_mode:
            gun_text = self.font.render("Gun Mode!", True, (255, 255, 0))
            self.screen.blit(gun_text, (20, 400))

    def handle_explosions(self):
        for explosion in self.explosions[:]:
            explosion.update()
            explosion.draw(self.screen, self.camera_x, self.camera_y)
            if explosion.is_finished():
                self.explosions.remove(explosion)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        show_pause_screen(self.screen, self.font)
                    if event.key == pygame.K_u:
                        self.show_upgrade_menu()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    adjusted_mouse_pos = (mouse_pos[0] + self.camera_x, mouse_pos[1] + self.camera_y)
                    new_bullets = self.player.shoot(adjusted_mouse_pos)
                    self.bullets.extend(new_bullets)
                    if self.shoot_sound:
                        self.shoot_sound.play()
                    self.player_attacking = True
                    self.player_attack_time = pygame.time.get_ticks()
                
                if event.type == pygame.USEREVENT + 1:  # SPAWN_ENEMY_EVENT
                    for _ in range(5):
                        if len(self.enemies) < config.MAX_ENEMIES:
                            self.enemies.append(random.choice([FastEnemy(), StrongEnemy(), BalancedEnemy(), MeleeEnemy(), RangedEnemy()]))
                    self.add_notification("5 Enemies spawned!", 2000)
                
                if event.type == pygame.USEREVENT + 2:  # SPAWN_ITEM_EVENT
                    for _ in range(random.randint(config.ITEMS_PER_SPAWN_MIN, config.ITEMS_PER_SPAWN_MAX)):
                        x = random.randint(0, config.MAP_WIDTH)
                        y = random.randint(0, config.MAP_HEIGHT)
                        item_class = random.choice([HealthItem, PowerUpItem])
                        if item_class == PowerUpItem:
                            item_type = random.choice(config.power_up_types)
                            item = PowerUpItem(item_type, (x, y))
                        else:
                            item = HealthItem((x, y))
                        
                        if isinstance(item, HealthItem):
                            self.health_items.append(item)
                        else:
                            self.power_ups.append(item)
                    self.add_notification("Items spawned!", 2000)

    def update_game_state(self):
        if self.game_state == "MENU":
            self.game_state = show_start_menu(self.screen, self.font)
        elif self.game_state == "PLAYING":
            # Update camera position
            self.camera_x = self.player.position[0] - config.SCREEN_WIDTH // 2
            self.camera_y = self.player.position[1] - config.SCREEN_HEIGHT // 2
            self.camera_x = max(0, min(self.camera_x, config.MAP_WIDTH - config.SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y, config.MAP_HEIGHT - config.SCREEN_HEIGHT))

            # Draw map
            self.game_map.draw(self.screen, (self.camera_x, self.camera_y), config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

            # Update and draw enemies
            for enemy in self.enemies[:]:
                if isinstance(enemy, BossEnemy):
                    attack = enemy.update(self.player.position, self.player_attacking)
                else:
                    attack = enemy.update(self.player.position, self.player_attacking)
                
                if isinstance(attack, EnemyBullet):
                    self.enemy_bullets.append(attack)
                elif attack:
                    self.player.take_damage(enemy.damage)
                    if self.player.health <= 0:
                        self.game_state = "GAME_OVER"
                        if self.score > self.high_score:
                            self.high_score = self.score
                            with open("highscore.txt", "w") as file:
                                file.write(str(self.high_score))
                        # ไม่เรียกใช้ self.reset_game() ที่นี่
                    
                enemy.draw(self.screen, self.camera_x, self.camera_y)
                
                if isinstance(enemy, BossEnemy) and not enemy.is_alive:
                    self.enemies.remove(enemy)

            # Update and draw player
            self.player.update()
            self.player.draw(self.screen, self.camera_x, self.camera_y)

            # Update attack status
            current_time = pygame.time.get_ticks()
            if self.player_attacking and current_time - self.player_attack_time > self.attack_duration:
                self.player_attacking = False

            # Draw HUD and Notifications
            self.draw_hud()
            self.display_notifications()

            # Handle explosions
            self.handle_explosions()

            # Check score thresholds for difficulty
            if self.next_level_index < len(config.score_thresholds) and self.score >= config.score_thresholds[self.next_level_index]:
                self.increase_difficulty()

            # Update player bullets
            for bullet in self.bullets[:]:
                bullet.update()
                bullet.draw(self.screen, self.camera_x, self.camera_y)
                for enemy in self.enemies[:]:
                    if enemy.is_alive:
                        dx = enemy.position[0] - bullet.position[0]
                        dy = enemy.position[1] - bullet.position[1]
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance <= enemy.size:
                            self.bullets.remove(bullet)
                            if self.hit_sound:
                                self.hit_sound.play()
                            enemy.take_damage(self.player.damage)
                            if not enemy.is_alive:
                                self.score += enemy.score_value
                                self.enemies.remove(enemy)
                                if self.explosion_sound:
                                    self.explosion_sound.play()
                                self.explosions.append(Explosion(enemy.position))
                            break
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)

            # Update enemy bullets
            for enemy_bullet in self.enemy_bullets[:]:
                enemy_bullet.update()
                enemy_bullet.draw(self.screen, self.camera_x, self.camera_y)
                dx = self.player.position[0] - enemy_bullet.position[0]
                dy = self.player.position[1] - enemy_bullet.position[1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= self.player.size:
                    self.enemy_bullets.remove(enemy_bullet)
                    if self.hit_sound:
                        self.hit_sound.play()
                    self.player.take_damage(enemy_bullet.damage)
                    if self.player.health <= 0:
                        self.game_state = "GAME_OVER"
                        if self.score > self.high_score:
                            self.high_score = self.score
                            with open("highscore.txt", "w") as file:
                                file.write(str(self.high_score))
                        # ไม่เรียกใช้ self.reset_game() ที่นี่

            # Update and draw health items
            for item in self.health_items[:]:
                if item.is_active:
                    item.draw(self.screen, self.camera_x, self.camera_y)
                    if item.collect(self.player):
                        self.health_items.remove(item)
                        self.add_notification("Collected Health Item!", 2000)
                else:
                    self.health_items.remove(item)

            # Update and draw power-ups
            for power_up in self.power_ups[:]:
                if power_up.is_active:
                    power_up.draw(self.screen, self.camera_x, self.camera_y)
                    if power_up.collect(self.player):
                        if power_up.type == 'shield':
                            self.player.shield = min(self.player.shield + 20, config.PLAYER_MAX_SHIELD)
                        elif power_up.type == 'speed':
                            self.player.speed += 1
                        elif power_up.type == 'damage':
                            self.player.damage += 1
                        elif power_up.type == 'gun':
                            self.player.enable_gun_mode()
                        self.power_ups.remove(power_up)
                        self.add_notification(f"Collected {power_up.type.capitalize()} Power-Up!", 2000)
                else:
                    self.power_ups.remove(power_up)

        def run(self):
            while True:
                self.clock.tick(60)
                self.handle_events()
                self.update_game_state()
                pygame.display.flip()

def show_pause_screen(screen, font):
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
