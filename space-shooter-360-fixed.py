import pygame
import math
import random
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('360度射擊飛機大戰')

# 顏色定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 創建一個三角形的飛機
        self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, BLUE, [(15, 0), (0, 30), (30, 30)])
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.centery = WINDOW_HEIGHT // 2
        self.speed = 5
        self.shoot_delay = 200  # 射擊延遲（毫秒）
        self.last_shot = pygame.time.get_ticks()
        self.bullet_count = 8  # 每次發射的子彈數量

    def update(self):
        # 獲取按鍵輸入
        keys = pygame.key.get_pressed()
        
        # 移動控制
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

        # 射擊控制（改為持續按住空格鍵射擊）
        now = pygame.time.get_ticks()
        if keys[K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        angle_step = 360 / self.bullet_count
        for i in range(self.bullet_count):
            angle = math.radians(i * angle_step)
            bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # 如果子彈離開屏幕則刪除
        if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        # 隨機選擇生成位置（屏幕外圍）
        side = random.randint(1, 4)
        if side == 1:  # 上方
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = -20
        elif side == 2:  # 右方
            self.rect.x = WINDOW_WIDTH + 20
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        elif side == 3:  # 下方
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = WINDOW_HEIGHT + 20
        else:  # 左方
            self.rect.x = -20
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        
        self.speed = random.randint(2, 4)

    def update(self):
        # 向玩家移動
        if player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        if player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed
        if player.rect.centery > self.rect.centery:
            self.rect.y += self.speed
        if player.rect.centery < self.rect.centery:
            self.rect.y -= self.speed

        # 如果敵人離開屏幕太遠則刪除
        if (self.rect.right < -100 or self.rect.left > WINDOW_WIDTH + 100 or 
            self.rect.bottom < -100 or self.rect.top > WINDOW_HEIGHT + 100):
            self.kill()

# 創建精靈組
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()  # 確保子彈組被正確創建

# 創建玩家
player = Player()
all_sprites.add(player)

# 遊戲循環
running = True
clock = pygame.time.Clock()
enemy_spawn_delay = 1000
last_enemy_spawn = pygame.time.get_ticks()
score = 0
font = pygame.font.Font(None, 36)

while running:
    clock.tick(60)
    
    # 事件處理
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # 生成敵人
    now = pygame.time.get_ticks()
    if now - last_enemy_spawn > enemy_spawn_delay:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        last_enemy_spawn = now

    # 更新所有精靈
    all_sprites.update()

    # 碰撞檢測
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        score += 10

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # 清空屏幕並繪製
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # 顯示分數
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 更新顯示
    pygame.display.flip()

pygame.quit()
