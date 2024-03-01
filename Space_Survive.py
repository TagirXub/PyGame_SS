import pygame
import random
import sys

pygame.init()

width = 400
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Survive")

player_img1 = pygame.image.load('player1.png')
player_img1 = pygame.transform.scale(player_img1, (50, 50))

player_img2 = pygame.image.load('player2.png')
player_img2 = pygame.transform.scale(player_img2, (50, 50))

player_images = [player_img1, player_img2]
current_player_img = 0

player_animation_timer = pygame.time.get_ticks()

enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (width, height))

player_size = 30
player_x = width // 2
player_y = height - 2 * player_size
player_speed = 5

enemy_size = 40
enemy_speed = 5
enemies = []

bullet_speed = 10
bullets = []
last_shot_time = pygame.time.get_ticks()

score = 0
high_score = 0
game_over = False
victory = False
level_target = 0

clock = pygame.time.Clock()

def redraw_game_window():
    win.blit(background_img, (0, 0))
    win.blit(player_images[current_player_img], (player_x, player_y))
    redraw_bullets()

    for enemy in enemies:
        win.blit(enemy_img, (enemy[0], enemy[1]))

    font = pygame.font.SysFont(None, 30)
    text = font.render("Очки: " + str(score), True, (255, 255, 255))
    win.blit(text, (10, 10))

    text = font.render("Цель: " + str(level_target), True, (255, 255, 255))
    win.blit(text, (width - 150, 10))

    pygame.display.update()

def check_collision(player_x, player_y, enemy_x, enemy_y, player_size, enemy_size):
    player_rect = pygame.Rect(player_x, player_y, player_size + 1, player_size + 1)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size + 1, enemy_size + 1)

    return player_rect.colliderect(enemy_rect)

def redraw_bullets():
    for bullet in bullets:
        win.blit(bullet_img, (bullet[0], bullet[1]))

def start_screen():
    win.blit(background_img, (0, 0))

    font = pygame.font.SysFont(None, 50)
    text = font.render("Space survive", True, (255, 255, 255))
    win.blit(text, (width // 2 - 120, height // 2 - 100))

    font = pygame.font.SysFont(None, 30)
    how_to_play_text = font.render("Как играть", True, (255, 255, 255))
    win.blit(how_to_play_text, (width // 2 - 70, height // 2 + 30))

    pygame.display.update()

    start_button = pygame.Rect(width // 2 - 80, height // 2 + 20, 160, 40)
    how_to_play_button = pygame.Rect(width // 2 - 80, height // 2 + 70, 160, 40)

    pygame.draw.rect(win, (0, 128, 255), start_button)
    pygame.draw.rect(win, (0, 128, 255), how_to_play_button)

    font = pygame.font.SysFont(None, 30)
    text = font.render("Старт", True, (255, 255, 255))
    win.blit(text, (width // 2 - 30, height // 2 + 30))

    text = font.render("Как играть", True, (255, 255, 255))
    win.blit(text, (width // 2 - 55, height // 2 + 80))

    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    level_selection_screen()
                    return
                elif how_to_play_button.collidepoint(event.pos):
                    how_to_play_screen()

def level_selection_screen():
    win.blit(background_img, (0, 0))

    font = pygame.font.SysFont(None, 50)
    text = font.render("Выберите уровень", True, (255, 255, 255))
    win.blit(text, (width // 2 - 160, height // 2 - 90))

    level1_button = pygame.Rect(width // 2 - 105, height // 2 + 20, 210, 40)
    level2_button = pygame.Rect(width // 2 - 105, height // 2 + 70, 210, 40)
    level3_button = pygame.Rect(width // 2 - 105, height // 2 + 120, 210, 40)
    endless_button = pygame.Rect(width // 2 - 105, height // 2 + 170, 210, 40)
    return_button = pygame.Rect(width // 2 - 105, height // 2 + 220, 210, 40)

    pygame.draw.rect(win, (0, 128, 255), level1_button)
    pygame.draw.rect(win, (0, 128, 255), level2_button)
    pygame.draw.rect(win, (0, 128, 255), level3_button)
    pygame.draw.rect(win, (0, 128, 255), endless_button)
    pygame.draw.rect(win, (0, 128, 255), return_button)

    font = pygame.font.SysFont(None, 25)
    text = font.render("Уровень 1 (20 очков)", True, (255, 255, 255))
    win.blit(text, (width // 2 - 90, height // 2 + 30))

    text = font.render("Уровень 2 (35 очков)", True, (255, 255, 255))
    win.blit(text, (width // 2 - 90, height // 2 + 80))

    text = font.render("Уровень 3 (50 очков)", True, (255, 255, 255))
    win.blit(text, (width // 2 - 90, height // 2 + 130))

    text = font.render("Бесконечный уровень", True, (255, 255, 255))
    win.blit(text, (width // 2 - 90, height // 2 + 180))

    text = font.render("Вернуться", True, (255, 255, 255))
    win.blit(text, (width // 2 - 55, height // 2 + 230))

    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if level1_button.collidepoint(event.pos):
                    reset_game(20)
                    return
                elif level2_button.collidepoint(event.pos):
                    reset_game(35)
                    return
                elif level3_button.collidepoint(event.pos):
                    reset_game(50)
                    return
                elif endless_button.collidepoint(event.pos):
                    reset_game(0)
                    return
                elif return_button.collidepoint(event.pos):
                    start_screen()
                    return

def how_to_play_screen():
    win.blit(background_img, (0, 0))

    font = pygame.font.SysFont(None, 50)
    text = font.render("Как играть", True, (255, 255, 255))
    win.blit(text, (width // 2 - 100, height // 2 - 90))

    font = pygame.font.SysFont(None, 25)
    instructions_text = [
        "Используйте стрелки для передвижения.",
        "Используйте пробел для стрельбы.",
        "Уничтожайте врагов, чтобы заработать очки.",
        "Достигните цели, чтобы победить."
    ]

    for i, line in enumerate(instructions_text):
        text = font.render(line, True, (255, 255, 255))
        win.blit(text, (20, height // 2 - 30 + i * 40))

    return_button = pygame.Rect(width // 2 - 90, height // 2 + 120, 160, 40)
    pygame.draw.rect(win, (0, 128, 255), return_button)

    text = font.render("Вернуться", True, (255, 255, 255))
    win.blit(text, (width // 2 - 55, height // 2 + 130))

    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_button.collidepoint(event.pos):
                    start_screen()
                    return

# Экран поражения
def defeat_screen():
    global high_score
    font = pygame.font.SysFont(None, 50)
    text = font.render("Поражение!", True, (255, 255, 255))
    win.blit(text, (width // 2 - 100, height // 2 - 90))

    font = pygame.font.SysFont(None, 50)
    text = font.render("Счет: " + str(score), True, (255, 255, 255))
    win.blit(text, (width // 2 - 60, height // 2 - 50))

    if score > high_score:
        high_score = score

    restart_button = pygame.Rect(width // 2 - 80, height // 2 + 20, 160, 40)
    return_button = pygame.Rect(width // 2 - 80, height // 2 + 70, 160, 40)

    pygame.draw.rect(win, (0, 128, 255), restart_button)
    pygame.draw.rect(win, (0, 128, 255), return_button)

    font = pygame.font.SysFont(None, 30)
    text = font.render("Заново", True, (255, 255, 255))
    win.blit(text, (width // 2 - 35, height // 2 + 30))

    text = font.render("Вернуться", True, (255, 255, 255))
    win.blit(text, (width // 2 - 50, height // 2 + 80))

    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    reset_game(level_target)
                    return
                elif return_button.collidepoint(event.pos):
                    start_screen()
                    return

def victory_screen():
    global high_score
    font = pygame.font.SysFont(None, 50)
    text = font.render("Победа!", True, (255, 255, 255))
    win.blit(text, (width // 2 - 80, height // 2 - 90))

    font = pygame.font.SysFont(None, 50)
    text = font.render("Счет: " + str(score), True, (255, 255, 255))
    win.blit(text, (width // 2 - 60, height // 2 - 50))

    if score > high_score:
        high_score = score

    restart_button = pygame.Rect(width // 2 - 80, height // 2 + 20, 160, 40)
    return_button = pygame.Rect(width // 2 - 80, height // 2 + 70, 160, 40)

    pygame.draw.rect(win, (0, 128, 255), restart_button)
    pygame.draw.rect(win, (0, 128, 255), return_button)

    font = pygame.font.SysFont(None, 30)
    text = font.render("Заново", True, (255, 255, 255))
    win.blit(text, (width // 2 - 35, height // 2 + 30))

    text = font.render("Вернуться", True, (255, 255, 255))
    win.blit(text, (width // 2 - 50, height // 2 + 80))

    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    reset_game(level_target)
                    return
                elif return_button.collidepoint(event.pos):
                    start_screen()
                    return

def reset_game(target):
    global player_x, player_y, enemies, bullets, score, game_over, enemy_size, level_target, victory
    player_x = width // 2
    player_y = height - 2 * player_size
    enemies = []
    bullets = []
    score = 0
    game_over = False
    enemy_size = 40
    level_target = target
    victory = False

start_screen()
running = True
victory = False
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x - player_speed > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_speed < width - player_size:
        player_x += player_speed

    if not game_over and not victory:
        if pygame.time.get_ticks() - player_animation_timer > 30:
            current_player_img = 1 - current_player_img
            player_animation_timer = pygame.time.get_ticks()

        if len(enemies) == 0 or random.random() < 0.01:
            enemies.append([random.randint(0, width - enemy_size), 0])

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > height:
                enemies.remove(enemy)
            if check_collision(player_x, player_y, enemy[0], enemy[1], player_size, enemy_size):
                game_over = True

        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time > 1000:
            bullets.append([player_x + player_size // 2 - 5, player_y])
            last_shot_time = pygame.time.get_ticks()

        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        for bullet in bullets:
            for enemy in enemies:
                if (enemy[0] < bullet[0] < enemy[0] + enemy_size) and (enemy[1] < bullet[1] < enemy[1] + enemy_size):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

        redraw_game_window()

        if game_over:
            defeat_screen()

        if score >= level_target and level_target != 0:
            victory = True
            game_over = True

    if game_over and victory:
        victory_screen()

pygame.quit()

