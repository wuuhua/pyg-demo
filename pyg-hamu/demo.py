# 導入必要的模組
import pygame  # Pygame庫，用於處理圖形、聲音和事件。
import math    # 提供數學函數，例如sqrt和hypot。
import random  # 用於生成隨機遊戲元素，例如敵人的位置、等級、道具產生。
import os      # 處理文件路徑操作，用於載入資源。
from typing import List, Tuple  # 提供列表和元組的類型註解。
from enum import Enum  # 用於定義列舉類型的物品類別。
import sys     # 引入系統檔

# 初始化 Pygame
pygame.init()  # 初始化所有導入的Pygame模組。
pygame.mixer.init()  # 初始化用於聲音播放的混音器模組。


# 設定遊戲視窗圖標
icon = pygame.image.load(os.path.join('pyg-hamu/img', 'icon.png'))  # 載入圖標圖像。 
pygame.display.set_icon(icon)  # 設定視窗的圖標。

# 設定遊戲視窗
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600   # 定義遊戲視窗的尺寸，800*600。
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # 創建遊戲視窗。
pygame.display.set_caption("勇者哈姆")  # 設定視窗標題（遊戲名稱）。

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)     # 用於繪製的常用顏色。
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)

# 載入背景圖像，background1.png
background_img = pygame.image.load(os.path.join("pyg-hamu/img", "background1.png")).convert()


# 定義遊戲音效的類別
class Sounds:
    def __init__(self):
        # 載入射擊和爆炸的音效
        self.shoot = pygame.mixer.Sound("pyg-hamu/sound/shoot.wav")
        self.explosion = pygame.mixer.Sound("pyg-hamu/sound/expl0.wav")

    @staticmethod
    def create_default_sounds():
        # 如果音效文件不存在，創建預設音效
        if not os.path.exists("pyg-hamu/sound/shoot.wav"):
            pygame.mixer.Sound.play(pygame.mixer.Sound(pygame.mixer.Sound(bytes([0]*32))))
            pygame.mixer.Sound.play(pygame.mixer.Sound(pygame.mixer.Sound(bytes([0]*32))))
# class Sounds End

# 定義道具類型
class ItemType(Enum):
    HEART = 1   # 道具愛心
    SHIELD = 2  # 道具護盾

# 定義可收集道具的類別
class Item:
    def __init__(self, x, y, item_type: ItemType):
        # 初始化物品屬性，真正的座標是使用怪物死掉後的座標，會在line 168處理
        self.x = x
        self.y = y
        self.type = item_type
        self.radius = 30  # 道具半徑範圍，用於碰撞檢測
        # 載入並縮放愛心和護盾的圖像，pyg-hamu/img/heart.png, pyg-hamu/img/shield.png
        self.heart_image = pygame.image.load('pyg-hamu/img/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (self.radius*0.8, self.radius*0.8))
        self.shield_image = pygame.image.load('pyg-hamu/img/shield.png')
        self.shield_image = pygame.transform.scale(self.shield_image, (self.radius*0.8, self.radius))
    def draw(self):
        # 根據物品類型繪製相應的圖像
        if self.type == ItemType.HEART:
            # 繪製愛心形狀
            screen.blit(self.heart_image, (self.x, self.y))
        else:
            # 繪製盾牌形狀
            screen.blit(self.shield_image, (self.x, self.y))
# class Item End

# 定義玩家角色的類別
class Player:
    def __init__(self):
        # 設定初始位置在視窗中心 (400, 300)
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.radius = 20  # 碰撞檢測半徑
        self.speed = 5    # 移動速度
        self.last_shot_time = 0  # 上次射擊的時間
        self.shoot_delay = 500   # 射擊間隔（毫秒）
        self.hearts = 5          # 初始生命值心形圖標數量
        self.health = 100        # 初始生命值（5顆心 x 20點生命值）
        self.shield_active = False     # 是否獲得護盾效果（初始為否）
        self.shield_start_time = 0     # 護盾生效的時間
        self.shield_duration = 5000    # 護盾持續時間（毫秒）

        # 載入並縮放 player 圖像
        self.image = pygame.image.load('pyg-hamu/img/player0.png')
        self.image = pygame.transform.scale(self.image, (self.radius*2*8, self.radius*2*10))
        self.image_rect = self.image.get_rect(center=(self.x, self.y ))

        # 載入並縮放心形圖標用於顯示生命值
        self.heart_image = pygame.image.load('pyg-hamu/img/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (self.radius, self.radius))

    def move(self, keys):
        # 根據鍵盤輸入移動玩家，確保不超出視窗範圍
        if keys[pygame.K_a] and self.x > self.radius:
            self.x -= self.speed  # 向左移動
        if keys[pygame.K_d] and self.x < WINDOW_WIDTH - self.radius:
            self.x += self.speed  # 向右移動
        if keys[pygame.K_w] and self.y > self.radius:
            self.y -= self.speed  # 向上移動
        if keys[pygame.K_s] and self.y < WINDOW_HEIGHT - self.radius:
            self.y += self.speed  # 向下移動

    def update_shield(self, current_time):
        # 如果護盾已生效且持續時間已過，取消護盾
        if self.shield_active:
            if current_time - self.shield_start_time >= self.shield_duration:
                self.shield_active = False

    def draw(self):
        # 繪製玩家
        self.image_rect.center = (self.x, self.y + self.radius)
        screen.blit(self.image,self.image_rect)
        
        # 如果護盾生效，繪製護盾效果
        if self.shield_active:
            pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius + 15, 2)

        # 繪製生命值的心形圖標
        for i in range(self.hearts):
            heart_x = 30 + i * 30  # 計算心形圖標的位置
            heart_y = 50
            screen.blit(self.heart_image, (heart_x, heart_y))
# class Player End

# 定義敵人角色的類別
class Enemy:
    def __init__(self):
        # 視窗邊緣隨機生成敵人位置
        side = random.randint(0, 3)
        if side == 0:
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = 0  # 頂部邊緣
        elif side == 1:
            self.x = WINDOW_WIDTH
            self.y = random.randint(0, WINDOW_HEIGHT)  # 右側邊緣
        elif side == 2:
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = WINDOW_HEIGHT  # 底部邊緣
        else:
            self.x = 0
            self.y = random.randint(0, WINDOW_HEIGHT)  # 左側邊緣

        self.radius = 15  # 碰撞檢測半徑
        self.speed = 2    # 向玩家移動的速度
        self.level = random.randint(1, 3)  # 敵人等級影響生命值和外觀
        self.health = self.level  # 根據等級設定生命值

        # 根據敵人等級載入並縮放圖像
        if (self.level == 3):
            self.image = pygame.image.load('pyg-hamu/img/hedgehog0.png')
            self.image = pygame.transform.scale(self.image, (self.radius * 20, self.radius * 14))
        elif(self.level == 2):
            self.image = pygame.image.load('pyg-hamu/img/lizard0.png')
            self.image = pygame.transform.scale(self.image, (self.radius * 16, self.radius * 20))
        else:
            self.image = pygame.image.load('pyg-hamu/img/crow0.png')
            self.image = pygame.transform.scale(self.image, (self.radius * 20, self.radius * 16))

        self.color = {1: RED, 2: GREEN, 3: BLACK}[self.level]

    def move(self, player_x, player_y):
        # 向玩家當前位置移動
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)  # 計算到玩家的距離
        if distance != 0:
            self.x += (dx / distance) * self.speed  # 更新位置
            self.y += (dy / distance) * self.speed

    def draw(self):
        # 繪製敵人
        self.image_rect = self.image.get_rect(center=(self.x, self.y ))
        screen.blit(self.image, self.image_rect)
# class Enemy End

# 定義玩家發射的子彈類別
class Bullet:
    def __init__(self, start_x, start_y, target_x, target_y):
        # 初始化子彈位置並計算朝向目標的軌跡
        self.x = start_x
        self.y = start_y
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)  # 計算到目標的距離
        self.dx = (dx/distance) if distance != 0 else 0  # 調整方向
        self.dy = (dy/distance) if distance != 0 else 0
        self.angle = math.atan2(dy, dx)  # 計算旋轉角度
        self.speed = 7   # 子彈速度
        self.radius = 50  # 碰撞檢測半徑

        # 載入子彈圖像，並縮放至合適比例
        self.sprite = pygame.image.load('pyg-hamu/img/bullet.png')
        self.image_rect = self.sprite.get_rect(center=(self.x, self.y ))
        self.sprite = pygame.transform.scale(self.sprite, (self.radius, self.radius * 1.5))

    def move(self):
        # 移動子彈
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, enemy_x, enemy_y):
        # 繪製子彈，並根據目標位置旋轉圖像
        rotated_image = pygame.transform.rotate(self.sprite, math.degrees(self.angle))
        rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, rect)
# class Bullet End

# 查找距離玩家最近的敵人
def find_nearest_enemy(player: Player, enemies: List[Enemy]) -> Tuple[float, float]:
    if not enemies:
        return player.x, player.y  # 如果沒有敵人，返回玩家位置(不發射子彈)
    
    nearest_enemy = min(enemies, key=lambda e: math.sqrt((e.x - player.x)**2 + (e.y - player.y)**2))
    return nearest_enemy.x, nearest_enemy.y

# 顯示開始畫面並等待玩家按任意鍵
def show_start_screen():
    # 載入並縮放開始畫面的背景圖像
    start_bg = pygame.image.load(os.path.join("pyg-hamu/img", "start_screen4.png")).convert()
    start_bg = pygame.transform.scale(start_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(start_bg, (0, 0))
       
    pygame.display.flip()

    # 等待玩家輸入任意鍵開始
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
# function show_start_screen End

# 顯示結束畫面並顯示玩家的最終得分
def show_end_screen(score):
    # 載入並縮放結束畫面的背景圖片
    end_bg = pygame.image.load(os.path.join("pyg-hamu/img", "end_screen.png")).convert()
    end_bg = pygame.transform.scale(end_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # 顯示結束畫面
    screen.blit(end_bg, (0, 0))
    font = pygame.font.Font(None, 72)

    # 顯示玩家的最終得分    
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 300))
    
    # 顯示退出遊戲的提示
    instruction_text = font.render("Press any key to exit", True, WHITE)
    screen.blit(instruction_text, (WINDOW_WIDTH // 2 - instruction_text.get_width() // 2, 500))
    
    pygame.display.flip()
    
    # 等待玩家按任意鍵退出
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
# function show_end_screen End

# 運行遊戲的主函式
def main():
    # 顯示開始畫面
    show_start_screen()

    # 初始化音效
    Sounds.create_default_sounds()
    sounds = Sounds()
    
    clock = pygame.time.Clock()  # 創建時鐘對象，用於控制幀率
    player = Player()            # 創建玩家對象
    enemies: List[Enemy] = []    # 保存敵人對象的列表
    bullets: List[Bullet] = []   # 保存子彈對象的列表
    items: List[Item] = []       # 保存物品對象的列表
    enemy_spawn_timer = 0        # 控制敵人生成的計時器
    enemy_spawn_delay = 1000     # 初始敵人生成間隔（毫秒）
    score = 0                    # 初始得分
    font = pygame.font.Font(None, 36)  # 用於顯示文本的字體

    running = True

    # 計時器設置
    game_duration = 3 * 60 * 1000  # 遊戲持續時間 3 分鐘（毫秒）
    start_time = pygame.time.get_ticks()  # 獲取遊戲開始的時間戳

    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time  # 遊戲已經進行的時間
        remaining_time = max(0, (game_duration - elapsed_time) // 1000)  # 剩餘時間（秒）

        # 檢查遊戲時間是否結束
        if elapsed_time >= game_duration:
            running = False

        # 處理事件，例如退出遊戲
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 獲取當前鍵盤按鍵狀態
        keys = pygame.key.get_pressed()
        player.move(keys)    # 更新玩家位置

        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新玩家位置和盾牌狀態
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update_shield(current_time)   # 更新護盾狀態
 
        # 根據分數調整敵人生成速度
        if score >= 1000:
            enemy_spawn_delay = 500  # 增加生成速度

        # 自動向最近的敵人射擊
        if current_time - player.last_shot_time >= player.shoot_delay:
            target_x, target_y = find_nearest_enemy(player, enemies)
            if((target_x != player.x)and (target_y != player.y)):
                bullets.append(Bullet(player.x, player.y, target_x, target_y))  # 創建新子彈
                sounds.shoot.play()  # 播放射擊音效
            player.last_shot_time = current_time # 主要循環更新玩家、敵人和子彈的狀態。
            

        # 生成敵人
        if current_time - enemy_spawn_timer >= enemy_spawn_delay:
            enemies.append(Enemy())    # 添加新敵人
            enemy_spawn_timer = current_time  # 重置敵人生成計時器

        # 更新子彈位置
        for bullet in bullets[:]:
            bullet.move()
            if (bullet.x < 0 or bullet.x > WINDOW_WIDTH or 
                bullet.y < 0 or bullet.y > WINDOW_HEIGHT):
                bullets.remove(bullet)

        # 更新敵人位置和碰撞檢測
        for enemy in enemies[:]:
            enemy.move(player.x, player.y)
            
            # 檢查與玩家的碰撞
            if math.sqrt((enemy.x - player.x)**2 + (enemy.y - player.y)**2) < player.radius + enemy.radius:
                if not player.shield_active:
                    player.health -= 20   # 減少玩家生命值（扣除一顆愛心）
                    player.hearts = player.health // 20
                    if player.health <= 0:
                        running = False  # 如果生命值耗盡，結束遊戲
                enemies.remove(enemy)
                continue

            # 檢查子彈碰撞
            for bullet in bullets[:]:
                if math.sqrt((enemy.x - bullet.x)**2 + (enemy.y - bullet.y)**2) < (enemy.radius + bullet.radius-30):
                    enemy.health -= 1
                    bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += 10  # 擊敗敵人增加得分
                        sounds.explosion.play()  # 播放擊殺音效
                        
                        # 隨機掉落道具（20%機率）
                        if random.random() < 0.2:
                            item_type = random.choice([ItemType.HEART, ItemType.SHIELD])
                            items.append(Item(enemy.x, enemy.y, item_type))
                    break

        # 更新道具碰撞檢測
        for item in items[:]:
            if math.sqrt((item.x - player.x)**2 + (item.y - player.y)**2) < player.radius + item.radius:#判斷玩家與道具之間的距離是否小於它們的半徑總和，偵測是否發生碰撞。
                if item.type == ItemType.HEART:   # 獲得愛心
                    if player.hearts < 5:
                        player.hearts += 1  # 增加玩家生命值
                        player.health = min(60, player.health + 20)  # 增加生命值但不超過100
                else:  # 獲得盾牌
                    player.shield_active = True      # 啟用玩家護盾
                    player.shield_start_time = current_time  # 記錄生效時間
                items.remove(item)

        # 繪製所有遊戲元素
        screen.blit(background_img, (0, 0))  # 繪製背景圖
        player.draw()                         # 繪製玩家
        for enemy in enemies:
            enemy.draw()                      # for 迴圈繪製三種敵人
        for bullet in bullets:
            target_x, target_y = find_nearest_enemy(player, enemies)
            bullet.draw(target_x, target_y)   # for 迴圈繪製子彈射擊
        for item in items:
            item.draw()                       # 繪製道具

        # 顯示分數
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 如果護盾生效，顯示護盾剩餘時間
        if player.shield_active:
            shield_time = (player.shield_duration - (current_time - player.shield_start_time)) // 1000
            shield_text = font.render(f"SHIELD: {shield_time}S", True, BLUE)
            screen.blit(shield_text, (10, 90))

        pygame.display.flip()
        clock.tick(60)
        
        # 顯示遊戲剩餘時間
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"TIME: {remaining_time}s", True, WHITE)
        screen.blit(timer_text, (WINDOW_WIDTH - 150, 10))

        pygame.display.flip()  # 更新整個螢幕的顯示
        clock.tick(60)         # 將遊戲的幀率限制在每秒60幀

    # 顯示結束畫面
    show_end_screen(score)
    pygame.quit()
    
    pygame.quit()

# 執行進入遊戲主程式
if __name__ == "__main__":
    main()  
