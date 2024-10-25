# src/explosion.py

import pygame
import config
import math
import os

class Explosion:
    def __init__(self, position):
        self.position = list(position)
        self.size = 50  # สามารถปรับขนาดได้
        self.max_size = 100
        self.growth_rate = 5
        self.color = (255, 165, 0)  # สีส้ม
        self.duration = 20  # จำนวนเฟรมที่แสดง

    def update(self):
        if self.size < self.max_size:
            self.size += self.growth_rate
        if self.duration > 0:
            self.duration -= 1

    def draw(self, screen, camera_x, camera_y):
        if self.duration > 0:
            pygame.draw.circle(screen, self.color, 
                               (int(self.position[0] - camera_x), int(self.position[1] - camera_y)), self.size, 2)

    def is_finished(self):
        return self.duration <= 0
