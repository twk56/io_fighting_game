# src/options.py

import pygame
import config

# กำหนดสีจาก config
WHITE = config.COLOR_WHITE
BLACK = config.COLOR_BLACK
RED = config.COLOR_RED

def show_options_menu(screen, font):
    options_running = True
    selected_option = 0
    options = ["Volume", "Graphics", "Back"]

    while options_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        adjust_volume(screen, font)
                    elif selected_option == 1:
                        adjust_graphics(screen, font)
                    elif selected_option == 2:
                        options_running = False  # กลับไปที่เมนูเริ่มต้น

        # วาดพื้นหลัง
        screen.fill(BLACK)

        # วาดข้อความเมนู Options
        menu_text = font.render("Options Menu", True, WHITE)
        screen.blit(menu_text, (config.SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 150))

        for idx, option in enumerate(options):
            if idx == selected_option:
                color = RED  # สีแดงสำหรับตัวเลือกที่เลือก
            else:
                color = WHITE  # สีขาวสำหรับตัวเลือกอื่นๆ
            option_text = font.render(option, True, color)
            screen.blit(option_text, (config.SCREEN_WIDTH // 2 - option_text.get_width() // 2, 300 + idx * 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def adjust_volume(screen, font):
    adjusting = True
    volume = pygame.mixer.music.get_volume()
    while adjusting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    volume = max(0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_RIGHT:
                    volume = min(1, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_ESCAPE:
                    adjusting = False

        # วาดพื้นหลัง
        screen.fill(BLACK)

        # วาดข้อความการปรับระดับเสียง
        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, WHITE)
        screen.blit(volume_text, (config.SCREEN_WIDTH // 2 - volume_text.get_width() // 2, 200))

        instruction_text = font.render("Use LEFT and RIGHT to adjust. ESC to go back.", True, WHITE)
        screen.blit(instruction_text, (config.SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 300))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def adjust_graphics(screen, font):
    adjusting = True
    # ตัวอย่างการปรับกราฟิก สามารถเพิ่มฟังก์ชันที่ซับซ้อนได้
    quality = "High"
    while adjusting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    quality = "High" if quality == "Low" else "Low"
                if event.key == pygame.K_ESCAPE:
                    adjusting = False

        # วาดพื้นหลัง
        screen.fill(BLACK)

        # วาดข้อความการปรับกราฟิก
        graphics_text = font.render(f"Graphics Quality: {quality}", True, WHITE)
        screen.blit(graphics_text, (config.SCREEN_WIDTH // 2 - graphics_text.get_width() // 2, 200))

        instruction_text = font.render("Press UP/DOWN to toggle. ESC to go back.", True, WHITE)
        screen.blit(instruction_text, (config.SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 300))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
