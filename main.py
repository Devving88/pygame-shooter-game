import pygame
import sys
import random

# กำหนดค่าคงที่ต่างๆ ของเกม
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# กำหนดสี (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
RED = (230, 50, 50)
GREEN = (50, 200, 50)
PURPLE = (150, 50, 200)
CYAN = (0, 200, 200)

# เริ่มต้นใช้งาน Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Step 3: Stage Progression & Game States")
clock = pygame.time.Clock()

# ฟอนต์สำหรับแสดงผล
font = pygame.font.SysFont("Arial", 28, bold=True)
title_font = pygame.font.SysFont("Arial", 50, bold=True)
game_over_font = pygame.font.SysFont("Arial", 60, bold=True)

# ตัวแปรผู้เล่น (Player)
player_width = 60
player_height = 20
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 6
player_hp = 3
player_score = 0

# ระบบกระสุน (Bullets)
bullets = []
bullet_width = 6
bullet_height = 15
bullet_speed = 10

# ระบบศัตรู (Enemies)
enemies = []
enemy_width = 40
enemy_height = 40
enemy_spawn_timer = 0
enemy_spawn_interval = 40  # จะถูกปรับตามด่าน

# ระบบด่านและสถานะเกม (Stage Progression & Game States)
# Game States: "PLAYING", "STAGE_CLEARED", "GAME_OVER", "VICTORY"
game_state = "PLAYING"
current_stage = 1
max_stage = 3
enemies_killed_in_stage = 0
enemies_target_per_stage = 10

def reset_game():
    global player_x, player_hp, player_score, bullets, enemies, game_state, current_stage, enemies_killed_in_stage, enemy_spawn_interval
    player_x = (SCREEN_WIDTH - player_width) // 2
    player_hp = 3
    player_score = 0
    current_stage = 1
    enemies_killed_in_stage = 0
    bullets.clear()
    enemies.clear()
    enemy_spawn_interval = 40
    game_state = "PLAYING"

def start_next_stage():
    global current_stage, enemies_killed_in_stage, bullets, enemies, game_state, enemy_spawn_interval
    current_stage += 1
    enemies_killed_in_stage = 0
    bullets.clear()
    enemies.clear()
    
    # ปรับความยากตามด่าน (เช่น ศัตรูเกิดเร็วขึ้น)
    if current_stage == 2:
        enemy_spawn_interval = 32
    elif current_stage == 3:
        enemy_spawn_interval = 25
        
    game_state = "PLAYING"

# Main Game Loop
running = True
while running:
    # 1. จัดการ Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "GAME_OVER" or game_state == "VICTORY":
                if event.key == pygame.K_r:
                    reset_game()
            elif game_state == "STAGE_CLEARED":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if current_stage < max_stage:
                        start_next_stage()
                    else:
                        game_state = "VICTORY"
            elif game_state == "PLAYING":
                if event.key == pygame.K_SPACE:
                    # ยิงกระสุน
                    bullet_x = player_x + (player_width // 2) - (bullet_width // 2)
                    bullet_y = player_y
                    bullets.append([bullet_x, bullet_y])

    # ตรวจสอบการกดปุ่มคีย์บอร์ดค้างไว้สำหรับการเคลื่อนที่ (เฉพาะตอน PLAYING)
    if game_state == "PLAYING":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        # จำกัดขอบเขตผู้เล่นไม่ให้ออกนอกจอ
        if player_x < 0:
            player_x = 0
        elif player_x > SCREEN_WIDTH - player_width:
            player_x = SCREEN_WIDTH - player_width

        # 2. อัปเดตสถานะเกม (Update Game State)
        
        # สุ่มเกิดศัตรู
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemy_spawn_timer = 0
            ex = random.randint(0, SCREEN_WIDTH - enemy_width)
            ey = -enemy_height
            # ความเร็วศัตรูเพิ่มขึ้นตามด่าน
            min_speed = 3 + (current_stage - 1)
            max_speed = 6 + (current_stage - 1)
            espeed = random.randint(min_speed, max_speed)
            enemies.append([ex, ey, espeed])

        # อัปเดตตำแหน่งกระสุน
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # อัปเดตตำแหน่งศัตรูและการชนกับผู้เล่น / หลุดขอบจอ
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for enemy in enemies[:]:
            enemy[1] += enemy[2]
            
            # ถ้าศัตรูตกหลุดขอบล่างจอ
            if enemy[1] > SCREEN_HEIGHT:
                enemies.remove(enemy)
                player_hp -= 1
                if player_hp <= 0:
                    game_state = "GAME_OVER"
                continue

            # ตรวจสอบศัตรูชนผู้เล่น
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if player_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                player_hp -= 1
                if player_hp <= 0:
                    game_state = "GAME_OVER"
                continue

        # ตรวจสอบการชนระหว่างกระสุนกับศัตรู
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            hit_enemy = None
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                if bullet_rect.colliderect(enemy_rect):
                    hit_enemy = enemy
                    break
            
            if hit_enemy:
                if hit_enemy in enemies:
                    enemies.remove(hit_enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                player_score += 10
                enemies_killed_in_stage += 1

                # ตรวจสอบว่ากำจัดศัตรูครบตามเป้าหมายของด่านนี้หรือยัง
                if enemies_killed_in_stage >= enemies_target_per_stage:
                    if current_stage < max_stage:
                        game_state = "STAGE_CLEARED"
                    else:
                        game_state = "VICTORY"
                    break

    # 3. วาดภาพกราฟิก (Render / Draw)
    screen.fill(BLACK)

    if game_state == "PLAYING":
        # วาดผู้เล่น
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # วาดกระสุน
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))

        # วาดศัตรู (เปลี่ยนสีตามด่านเพื่อให้เห็นความแตกต่าง)
        enemy_color = RED if current_stage == 1 else (PURPLE if current_stage == 2 else CYAN)
        for enemy in enemies:
            pygame.draw.rect(screen, enemy_color, (enemy[0], enemy[1], enemy_width, enemy_height))

        # แสดง UI ข้อมูลเกม (Stage, Progress, Score, HP)
        stage_surface = font.render(f"Stage: {current_stage}/{max_stage}", True, WHITE)
        progress_surface = font.render(f"Killed: {enemies_killed_in_stage}/{enemies_target_per_stage}", True, YELLOW)
        score_surface = font.render(f"Score: {player_score}", True, WHITE)
        hp_surface = font.render(f"HP: {player_hp}", True, GREEN)

        screen.blit(stage_surface, (20, 20))
        screen.blit(progress_surface, (20, 55))
        screen.blit(score_surface, (20, 90))
        screen.blit(hp_surface, (SCREEN_WIDTH - 120, 20))

    elif game_state == "STAGE_CLEARED":
        # หน้าจอ Stage Cleared
        cleared_title = title_font.render(f"STAGE {current_stage} CLEARED!", True, GREEN)
        next_prompt = font.render("Press 'SPACE' or 'ENTER' to Next Stage", True, YELLOW)
        score_info = font.render(f"Current Score: {player_score}", True, WHITE)

        screen.blit(cleared_title, (SCREEN_WIDTH // 2 - cleared_title.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(score_info, (SCREEN_WIDTH // 2 - score_info.get_width() // 2, SCREEN_HEIGHT // 2 - 10))
        screen.blit(next_prompt, (SCREEN_WIDTH // 2 - next_prompt.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    elif game_state == "GAME_OVER":
        # หน้าจอ Game Over
        game_over_surface = game_over_font.render("GAME OVER", True, RED)
        final_score_surface = font.render(f"Final Score: {player_score}", True, WHITE)
        restart_surface = font.render("Press 'R' to Restart", True, YELLOW)

        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score_surface, (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    elif game_state == "VICTORY":
        # หน้าจอชนะเกมทั้งหมด
        victory_surface = title_font.render("VICTORY! YOU WIN!", True, GREEN)
        final_score_surface = font.render(f"Final Score: {player_score}", True, WHITE)
        restart_surface = font.render("Press 'R' to Play Again", True, YELLOW)

        screen.blit(victory_surface, (SCREEN_WIDTH // 2 - victory_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score_surface, (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
