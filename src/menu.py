# src/menu.py

import pygame
import config
from options import show_options_menu

# กำหนดสีจาก config
WHITE = config.COLOR_WHITE
BLACK = config.COLOR_BLACK
RED = config.COLOR_RED

def show_start_menu(screen, font):
    menu_running = True
    selected_option = 0
    options = ["Start Game", "Options", "Quit"]

    while menu_running:
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
                        menu_running = False  # เริ่มเกม
                        return "PLAYING"
                    elif selected_option == 1:
                        show_options_menu(screen, font)
                    elif selected_option == 2:
                        pygame.quit()
                        exit()

        # วาดพื้นหลัง
        screen.fill(BLACK)

        # วาดข้อความเมนู
        title_text = font.render("Fighting .io Game", True, WHITE)
        screen.blit(title_text, (config.SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        for idx, option in enumerate(options):
            if idx == selected_option:
                color = RED  # สีแดงสำหรับตัวเลือกที่เลือก
            else:
                color = WHITE  # สีขาวสำหรับตัวเลือกอื่นๆ
            option_text = font.render(option, True, color)
            screen.blit(option_text, (config.SCREEN_WIDTH // 2 - option_text.get_width() // 2, 300 + idx * 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def show_game_over_menu(screen, font, score, high_score):
    menu_running = True
    selected_option = 0
    options = ["Restart Game", "Quit"]

    while menu_running:
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
                        menu_running = False  # รีสตาร์ทเกม
                        return "PLAYING"
                    elif selected_option == 1:
                        pygame.quit()
                        exit()

        # วาดพื้นหลัง
        screen.fill(BLACK)

        # วาดข้อความ Game Over
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))

        # วาดคะแนน
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))

        # วาดคะแนนสูงสุด
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (config.SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 300))

        for idx, option in enumerate(options):
            if idx == selected_option:
                color = RED
            else:
                color = WHITE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (config.SCREEN_WIDTH // 2 - option_text.get_width() // 2, 400 + idx * 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)
