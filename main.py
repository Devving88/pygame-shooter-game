import pygame
import sys

# กำหนดค่าคงที่ต่างๆ ของเกม
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# กำหนดสี (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)

# เริ่มต้นใช้งาน Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Step 1: Core Movement & Shooting")
clock = pygame.time.Clock()

# กำหนดคุณลักษณะของผู้เล่น (Player)
player_width = 60
player_height = 20
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 6

# กำหนดลิสต์เก็บกระสุน (Bullets)
bullets = []
bullet_width = 6
bullet_height = 15
bullet_speed = 10

# ตัวแปรสำหรับควบคุมการยิงต่อเนื่อง (Cooldown หรือเช็คปุ่มกด)
can_shoot = True

# Main Game Loop
running = True
while running:
    # 1. จัดการ Event (การกดปุ่ม คีย์บอร์ด/เมาส์)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ตรวจสอบการกดปุ่มคีย์บอร์ดต่อเนื่อง
    keys = pygame.key.get_pressed()
    
    # เคลื่อนที่ซ้าย - ขวา และจำกัดไม่ให้หลุดขอบจอ
    if keys[pygame.K_LEFT] or keys[pygame.K_ord('a') if hasattr(pygame, 'K_ord') else keys[pygame.K_a] if hasattr(pygame, 'K_a') else False]: # รองรับปุ่มลูกศรซ้าย หรือ A
        pass
    
    # จัดการการเคลื่อนที่ผู้เล่นแบบชัดเจน
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed

    # จำกัดขอบเขตผู้เล่นไม่ให้ออกนอกหน้าจอ
    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - player_width:
        player_x = SCREEN_WIDTH - player_width

    # ระบบยิงกระสุนเมื่อกด SPACEBAR
    if keys[pygame.K_SPACE]:
        if can_shoot:
            # สร้างกระสุนใหม่ตำแหน่งกึ่งกลางผู้เล่นพุ่งขึ้นบน
            bullet_x = player_x + (player_width // 2) - (bullet_width // 2)
            bullet_y = player_y
            bullets.append([bullet_x, bullet_y])
            can_shoot = False # ป้องกันยิงรัวพรวดพราดเกินไปใน 1 เฟรม (หรือทำ Cooldown ง่ายๆ)
    else:
        can_shoot = True

    # 2. อัปเดตสถานะเกม (Update Game State)
    # อัปเดตตำแหน่งกระสุนทั้งหมด และลบกระสุนที่หลุดขอบจอบนสุด
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # 3. วาดภาพกราฟิก (Render / Draw)
    # เคลียร์หน้าจอเป็นสีดำ
    screen.fill(BLACK)

    # วาดตัวละครผู้เล่น (สี่เหลี่ยมสีฟ้า)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # วาดกระสุนทั้งหมด (สี่เหลี่ยมสีเหลือง)
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))

    # สลับหน้าจอแสดงผล (Double Buffering)
    pygame.display.flip()

    # ควบคุมความเร็วให้อยู่ที่ 60 FPS
    clock.tick(FPS)

# ปิดการทำงาน Pygame เมื่อออกจากลูป
pygame.quit()
sys.exit()
