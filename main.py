import random

import pygame
import sys


# tạo hai sàn để khi lùi sàn sẽ k bị mất
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


# tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)  # chọn chiều cao ngẫu nhiên cho ống
    bot_pipe = pipe_surface.get_rect(midtop=(650, random_pipe_pos))  # ống dưới
    top_pipe = pipe_surface.get_rect(midtop=(650, random_pipe_pos - 700))  # ống trên
    if score > 2:
        bot_pipe = pipe_surface.get_rect(midtop=(650, random_pipe_pos))  # ống dưới
        top_pipe = pipe_surface.get_rect(midtop=(550, random_pipe_pos - 650))  # ống trên
    return bot_pipe, top_pipe


# di chuyển ống sang bên trái trả lại một list mới
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def daw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # lật ống theo chiều oy
            screen.blit(flip_pipe, pipe)


# check va chạm
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            can_score = True
            game_over = pygame.image.load('FileGame/assets/gameover.png').convert_alpha()
            game_over_rectt = game_over.get_rect(center=(216, 384))
            screen.blit(game_over, game_over_rectt)
            return False

        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            hit_sound.play()

            can_score = True
            game_over = pygame.image.load('FileGame/assets/gameover.png').convert_alpha()
            game_over_rectt = game_over.get_rect(center=(216, 384))
            screen.blit(game_over, game_over_rectt)
            return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)



def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False

            if pipe.centerx < 0:
                can_score = True


# pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FileGame/04B_19.ttf', 40)

# tạo các biến cho trò chơi
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
# chèn backgourd
bg = pygame.image.load(
    'FileGame/assets/background-night.png').convert()  # convert đổi file hình ảnh thành file nhẹ hơn để pygame load nhanh hơn
bg = pygame.transform.scale2x(bg)  # nhân đôi backgourd
# chèn sàn
floor = pygame.image.load('FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# tạo chim
bird_down = pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha()
bird_mid = pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
# bird = pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))
# tạo timer cho bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 216)
# tạo cột
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# tạo timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1700)
pipe_height = [500, 300, 400]

# tạo màn  hình kết thúc
game_over_surface = pygame.image.load('FileGame/assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216, 384))
screen.blit(game_over_surface, game_over_rect)

# chèn âm thanh
flap_sound = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('FileGame/sound/sfx_point.wav')
score_sound_countdown = 100
score_event = pygame.USEREVENT + 2
pygame.time.set_timer(score_event, 100)
# while loop của trò chơi
while True:

    for event in pygame.event.get():
        # nhấn phím thoát khỏi game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # thoát hệ thống

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    screen.blit(bg, (0, 0))  # thêm background vào của sổ game
    if game_active:
        # chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement  # di chuyển xuống dưới
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # ống
        pipe_list = move_pipe(pipe_list)
        daw_pipe(pipe_list)
        pipe_score_check()
        score_display('main game')

    else:

        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')
    # sàn
    floor_x_pos -= 1  # di chuyển lùi lại phía bên trái
    draw_floor()  # vẽ ống lên màn hình

    if floor_x_pos <= -432:
        floor_x_pos = 0
    screen.blit(floor, (floor_x_pos, 650))

    pygame.display.update()
    clock.tick(90)

