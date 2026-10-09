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

# เริ่มต้นใช้งาน Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Step 2: Enemies & Collision Detection")
clock = pygame.time.Clock()

# ฟอนต์สำหรับแสดงผลคะแนนและเลือด
font = pygame.font.SysFont("Arial", 28, bold=True)
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
enemy_spawn_interval = 40  # ทุกๆ 40 เฟรม ศัตรูจะเกิด 1 ตัว

# สถานะเกม
game_over = False

def reset_game():
    global player_x, player_y, player_hp, player_score, bullets, enemies, game_over
    player_x = (SCREEN_WIDTH - player_width) // 2
    player_hp = 3
    player_score = 0
    bullets.clear()
    enemies.clear()
    game_over = False

# Main Game Loop
running = True
while running:
    # 1. จัดการ Event (รวมถึงการกดปุ่มยิงและกดรีสตาร์ท)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if event.key == pygame.K_SPACE:
                    # ยิงกระสุน 1 นัดต่อการกด 1 ครั้ง
                    bullet_x = player_x + (player_width // 2) - (bullet_width // 2)
                    bullet_y = player_y
                    bullets.append([bullet_x, bullet_y])

    # ตรวจสอบการกดปุ่มคีย์บอร์ดค้างไว้สำหรับการเคลื่อนที่
    keys = pygame.key.get_pressed()

    if not game_over:
        # เคลื่อนที่ผู้เล่นซ้าย-ขวา
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
            espeed = random.randint(3, 6)
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
                    game_over = True
                continue

            # ตรวจสอบศัตรูชนผู้เล่น
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if player_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                player_hp -= 1
                if player_hp <= 0:
                    game_over = True
                continue

        # ตรวจสอบการชนระหว่างกระสุนกับศัตรู (Bullet vs Enemy Collision)
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

    # 3. วาดภาพกราฟิก (Render / Draw)
    screen.fill(BLACK)

    if not game_over:
        # วาดผู้เล่น
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # วาดกระสุน
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))

        # วาดศัตรู
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

        # แสดง Score และ HP
        score_surface = font.render(f"Score: {player_score}", True, WHITE)
        hp_surface = font.render(f"HP: {player_hp}", True, GREEN)
        screen.blit(score_surface, (20, 20))
        screen.blit(hp_surface, (SCREEN_WIDTH - 120, 20))
    else:
        # หน้าจอ Game Over
        game_over_surface = game_over_font.render("GAME OVER", True, RED)
        final_score_surface = font.render(f"Final Score: {player_score}", True, WHITE)
        restart_surface = font.render("Press 'R' to Restart or Close Window", True, YELLOW)

        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score_surface, (SCREEN_WIDTH // 2 - final_score_surface.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
