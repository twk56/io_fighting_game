# src/map.py

import pygame
import config

# กำหนดสีจาก config
WHITE = config.COLOR_WHITE
BLACK = config.COLOR_BLACK
RED = config.COLOR_WHITE

class Map:
    def __init__(self):
        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT
        self.boundary_radius = config.BOUNDARY_RADIUS
        self.center = (self.width // 2, self.height // 2)
        
        # สร้าง Surface สำหรับแผนที่
        self.surface = pygame.Surface((self.width, self.height)).convert()
        
        # โหลดและสเกลภาพพื้นหลัง
        try:
            self.background = pygame.image.load(config.BACKGROUND_IMAGE_PATH).convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except pygame.error as e:
            print(f"ไม่สามารถโหลดภาพพื้นหลังได้: {e}")
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill(BLACK)  # หากไม่สามารถโหลดภาพได้ ให้เติมพื้นหลังเป็นสีดำ
        
        # วาดภาพพื้นหลังลงบน Surface ของแผนที่
        self.surface.blit(self.background, (0, 0))
        
        # วาดกรอบสี่เหลี่ยม
        pygame.draw.rect(self.surface, WHITE, pygame.Rect(0, 0, self.width, self.height), 5)
        
        # วาดวงกลมขอบเขต
        #pygame.draw.circle(self.surface, RED, self.center, self.boundary_radius, 5)
    
    def draw(self, screen, camera_pos, screen_width, screen_height):
        """
        วาดส่วนของแผนที่ที่กล้องกำลังมองเห็นลงบนหน้าจอ
        """
        camera_x, camera_y = camera_pos
        # คำนวณตำแหน่งที่จะแสดงบนหน้าจอ
        blit_x = -camera_x + screen_width // 2 - config.SCREEN_WIDTH // 2
        blit_y = -camera_y + screen_height // 2 - config.SCREEN_HEIGHT // 2
        screen.blit(self.surface, (blit_x, blit_y))
