import pygame
import math
import random
import os
from typing import List, Tuple
from enum import Enum

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 設定視窗圖示
icon = pygame.image.load(os.path.join('pyg-hamu/img', 'icon.png'))
pygame.display.set_icon(icon)

# 遊戲視窗設置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("勇者哈姆")

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)

# 載入音效
class Sounds:
    def __init__(self):
        self.shoot = pygame.mixer.Sound("pyg-hamu/sound/shoot.wav")
        self.explosion = pygame.mixer.Sound("pyg-hamu/sound/expl0.wav")

    @staticmethod
    def create_default_sounds():
        # 如果音效文件不存在，創建預設音效
        if not os.path.exists("pyg-hamu/sound/shoot.wav"):
            pygame.mixer.Sound.play(pygame.mixer.Sound(pygame.mixer.Sound(bytes([0]*32))))
            pygame.mixer.Sound.play(pygame.mixer.Sound(pygame.mixer.Sound(bytes([0]*32))))

class ItemType(Enum):
    HEART = 1
    SHIELD = 2

class Item:
    def __init__(self, x, y, item_type: ItemType):
        self.x = x
        self.y = y
        self.type = item_type
        self.radius = 30
        # self.color = PINK if item_type == ItemType.HEART else GREEN
        self.heart_image = pygame.image.load('pyg-hamu/img/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (self.radius*0.8, self.radius*0.8))
        self.shield_image = pygame.image.load('pyg-hamu/img/shield.png')
        self.shield_image = pygame.transform.scale(self.shield_image, (self.radius*0.8, self.radius))
    def draw(self):
        # pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if self.type == ItemType.HEART:
            # 繪製愛心形狀
            screen.blit(self.heart_image, (self.x, self.y))
            # pygame.draw.polygon(screen, RED, [
            #     (self.x, self.y - 5),
            #     (self.x - 5, self.y - 8),
            #     (self.x - 5, self.y - 2)
            # ])
            # pygame.draw.polygon(screen, RED, [
            #     (self.x, self.y - 5),
            #     (self.x + 5, self.y - 8),
            #     (self.x + 5, self.y - 2)
            # ])
        else:
            # 繪製盾牌形狀
            screen.blit(self.shield_image, (self.x, self.y))
            # pygame.draw.rect(screen, BLUE, (self.x - 5, self.y - 5, 10, 10))

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.radius = 20
        self.speed = 5
        self.last_shot_time = 0
        self.shoot_delay = 500
        self.hearts = 5
        self.health = 100  # 5顆心 × 20點生命值
        self.shield_active = False
        self.shield_start_time = 0
        self.shield_duration = 5000  # 5秒盾牌持續時間
        #載入player 圖像
        self.image = pygame.image.load('pyg-hamu/img/player0.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2*8, self.radius*2*10)) #手動調整顯示尺寸
        self.image_rect = self.image.get_rect(center=(self.x, self.y ))
        # 載入生命值圖像
        self.heart_image = pygame.image.load('pyg-hamu/img/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (self.radius, self.radius))
        
    def move(self, keys):
        if keys[pygame.K_a] and self.x > self.radius:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < WINDOW_WIDTH - self.radius:
            self.x += self.speed
        if keys[pygame.K_w] and self.y > self.radius:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < WINDOW_HEIGHT - self.radius:
            self.y += self.speed

    def update_shield(self, current_time):
        if self.shield_active:
            if current_time - self.shield_start_time >= self.shield_duration:
                self.shield_active = False

    def draw(self):
        # 繪製玩家
        # pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius)
        self.image_rect.center = (self.x, self.y + self.radius) #取得角色中心位置，將角色放置在該物件中央
        screen.blit(self.image,self.image_rect)
        
        # 如果盾牌激活，繪製盾牌效果
        if self.shield_active:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius + 15, 2)

        # 繪製生命值
        for i in range(self.hearts):
            heart_x = 30 + i * 30
            heart_y = 50
            screen.blit(self.heart_image, (heart_x, heart_y))
            # pygame.draw.circle(screen, RED, (heart_x, heart_y), 10)

class Enemy:
    def __init__(self):
        side = random.randint(0, 3)
        if side == 0:
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = 0
        elif side == 1:
            self.x = WINDOW_WIDTH
            self.y = random.randint(0, WINDOW_HEIGHT)
        elif side == 2:
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = WINDOW_HEIGHT
        else:
            self.x = 0
            self.y = random.randint(0, WINDOW_HEIGHT)

        self.radius = 15
        self.speed = 2
        self.level = random.randint(1, 3)
        self.health = self.level
        if (self.level == 3):
            self.image = pygame.image.load('pyg-hamu/img/hedgehog0.png')
            self.image = pygame.transform.scale(self.image, (self.radius*2*10, self.radius*2*7)) #手動調整顯示尺寸
        elif(self.level == 2):
            self.image = pygame.image.load('pyg-hamu/img/lizard0.png')
            self.image = pygame.transform.scale(self.image, (self.radius*2*8, self.radius*2*10)) #手動調整顯示尺寸
        else:
            self.image = pygame.image.load('pyg-hamu/img/crow0.png')
            self.image = pygame.transform.scale(self.image, (self.radius*2*10, self.radius*2*8)) #手動調整顯示尺寸
        self.color = {1: RED, 2: GREEN, 3: BLACK}[self.level]

    def move(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            self.x += (dx/distance) * self.speed
            self.y += (dy/distance) * self.speed

    def draw(self):
        # pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        self.image_rect = self.image.get_rect(center=(self.x, self.y ))
       
        screen.blit(self.image, self.image_rect)
            
        

class Bullet:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        self.dx = (dx/distance) if distance != 0 else 0
        self.dy = (dy/distance) if distance != 0 else 0
        self.angle = math.atan2(dy, dx)
        # self.angle = math.atan2(target_y - start_y, target_x - start_x)
        self.speed = 7
        self.radius = 50
        self.sprite = pygame.image.load('pyg-hamu/img/bullet.png')
        self.image_rect = self.sprite.get_rect(center=(self.x, self.y ))
        self.sprite = pygame.transform.scale(self.sprite, (self.radius, self.radius*1.5))
        # self.sprite = pygame.transform.rotate(self.sprite, 90)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, enemy_x, enemy_y):
        angle = math.atan2(enemy_y - self.y, enemy_x - self.x)
        rotated_image = pygame.transform.rotate(self.sprite, math.degrees(self.angle))
        rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, rect)
         # pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)


def find_nearest_enemy(player: Player, enemies: List[Enemy]) -> Tuple[float, float]:
    if not enemies:
        return player.x, player.y
    
    nearest_enemy = min(enemies, key=lambda e: math.sqrt((e.x - player.x)**2 + (e.y - player.y)**2))
    return nearest_enemy.x, nearest_enemy.y

def main():
    # 初始化音效
    Sounds.create_default_sounds()
    sounds = Sounds()
    
    clock = pygame.time.Clock()
    player = Player()
    enemies: List[Enemy] = []
    bullets: List[Bullet] = []
    items: List[Item] = []
    enemy_spawn_timer = 0
    enemy_spawn_delay = 1000  # 初始生成延遲
    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新玩家位置和盾牌狀態
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update_shield(current_time)

        # 根據分數調整敵人生成速度
        if score >= 1000:
            enemy_spawn_delay = 500

        # 自動射擊
        if current_time - player.last_shot_time >= player.shoot_delay:
            target_x, target_y = find_nearest_enemy(player, enemies)
            if((target_x != player.x)and (target_y != player.y)):
                bullets.append(Bullet(player.x, player.y, target_x, target_y))
            player.last_shot_time = current_time
            sounds.shoot.play()

        # 生成敵人
        if current_time - enemy_spawn_timer >= enemy_spawn_delay:
            enemies.append(Enemy())
            enemy_spawn_timer = current_time

        # 更新子彈位置
        for bullet in bullets[:]:
            bullet.move()
            if (bullet.x < 0 or bullet.x > WINDOW_WIDTH or 
                bullet.y < 0 or bullet.y > WINDOW_HEIGHT):
                bullets.remove(bullet)


        # 更新敵人位置和碰撞檢測
        for enemy in enemies[:]:
            enemy.move(player.x, player.y)
            
            # 檢查玩家碰撞
            if math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2) < player.radius + enemy.radius:
                if not player.shield_active:
                    player.health -= 20
                    player.hearts = player.health // 20
                    if player.health <= 0:
                        running = False
                enemies.remove(enemy)
                continue

            # 檢查子彈碰撞
            for bullet in bullets[:]:
                if math.sqrt((enemy.x - bullet.x)**2 + (enemy.y - bullet.y)**2) < (enemy.radius + bullet.radius-30):
                    enemy.health -= 1
                    bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += 10
                        sounds.explosion.play()
                        
                        # 隨機掉落道具（20%機率）
                        if random.random() < 0.2:
                            item_type = random.choice([ItemType.HEART, ItemType.SHIELD])
                            items.append(Item(enemy.x, enemy.y, item_type))
                    # else:
                    #     enemy.color = {1: RED, 2: GREEN, 3: BLACK}[enemy.health]
                    break

        # 更新道具碰撞檢測
        for item in items[:]:
            if math.sqrt((item.x - player.x)**2 + (item.y - player.y)**2) < player.radius + item.radius:
                if item.type == ItemType.HEART:
                    if player.hearts < 5:
                        player.hearts += 1
                        player.health = min(60, player.health + 20)
                else:  # SHIELD
                    player.shield_active = True
                    player.shield_start_time = current_time
                items.remove(item)

        # 繪製
        screen.fill((50, 50, 50))
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            target_x, target_y = find_nearest_enemy(player, enemies)
            bullet.draw(target_x, target_y)
        for item in items:
            item.draw()

        # 顯示分數
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 顯示盾牌剩餘時間
        if player.shield_active:
            shield_time = (player.shield_duration - (current_time - player.shield_start_time)) // 1000
            shield_text = font.render(f"SHIELD: {shield_time}秒", True, GREEN)
            screen.blit(shield_text, (10, 90))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
