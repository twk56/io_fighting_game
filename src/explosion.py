import pygame
import config
from PIL import Image
import os

class Explosion:
    def __init__(self, position):
        self.position = list(position)
        self.images = self.load_gif('assets/explosion/explosion1.gif')  # เส้นทางไปยัง GIF ที่อัปโหลด
        self.current_frame = 0
        self.frame_count = len(self.images)
        self.time_per_frame = 2  # จำนวนเฟรมที่จะแสดงแต่ละภาพ

    def load_gif(self, gif_path):
        """โหลด GIF และแยกเฟรม"""
        with Image.open(gif_path) as img:
            images = []
            for frame in range(img.n_frames):
                img.seek(frame)
                frame_image = img.convert("RGBA")  # แปลงเป็น RGBA
                mode = frame_image.mode
                size = frame_image.size
                data = frame_image.tobytes()
                # สร้าง Pygame Surface จากข้อมูลภาพ
                surface = pygame.image.fromstring(data, size, mode).convert_alpha()
                images.append(surface)
        return images

    def update(self):
        if self.current_frame < self.frame_count:
            self.current_frame += 1 / self.time_per_frame
        if self.current_frame >= self.frame_count:
            self.current_frame = self.frame_count  # ตั้งให้เป็นค่าเต็มเพื่อหยุด

    def draw(self, screen, camera_x, camera_y):
        if self.current_frame < self.frame_count:
            frame_index = int(self.current_frame)
            screen.blit(self.images[frame_index], 
                        (self.position[0] - camera_x, self.position[1] - camera_y))

    def is_finished(self):
        return self.current_frame >= self.frame_count
