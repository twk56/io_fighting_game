# src/utils.py

import math
import config

def check_boundary(position, boundary_radius):
    """
    ตรวจสอบว่าตำแหน่งอยู่ภายในขอบเขตวงกลมหรือไม่

    :param position: ทูเพิล (x, y) ของตำแหน่งใหม่ของผู้เล่น
    :param boundary_radius: รัศมีของขอบเขตวงกลม
    :return: True ถ้าอยู่ภายในขอบเขต, False ถ้าอยู่นอกขอบเขต
    """
    center_x = config.MAP_WIDTH // 2
    center_y = config.MAP_HEIGHT // 2
    x, y = position
    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    return distance <= boundary_radius
