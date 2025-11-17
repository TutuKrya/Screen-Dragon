import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Screen Dragon")

# Цвета
BACKGROUND = (10, 10, 40)  # Темно-синий фон
DRAGON_BODY = (220, 60, 60)  # Тело дракона
DRAGON_BELLY = (255, 150, 150)  # Живот
DRAGON_WINGS = (0, 0, 0)  # Крылья
DRAGON_ACCENT = (255, 200, 50)  # Рога и шипы
DRAGON_EYES = (80, 255, 150)  # Глаза
DRAGON_EYES_GLOW = (100, 255, 170, 100)  # Свечение глаз

# Позиции частей дракона (будем обновлять их отдельно)
dragon_parts = {
    'head': [WIDTH // 2, HEIGHT // 2],
    'body': [],
    'tail': []
}

DRAGON_SPEED = 0.08 # Скорость движения
TAIL_SEGMENTS = 8  # Количество сегментов хвоста
SEGMENT_DISTANCE = 15  # Расстояние между сегментами

def draw_detailed_dragon(surface, head_x, head_y, body_segments, tail_segments, mouse_x, mouse_y):
    """Рисует детализированного дракона с хвостом, который следует за движением"""

    # Вычисляем направление взгляда дракона
    dx = mouse_x - head_x
    dy = mouse_y - head_y
    direction = math.atan2(dy, dx)

    # Размеры
    body_width = 60
    body_height = 35
    head_radius = 28

    # Рисуем хвост (сегменты)
    for i, (seg_x, seg_y) in enumerate(tail_segments):
        size = 1.0 - (i / len(tail_segments)) * 0.7
        color_scale = 1.0 - (i / len(tail_segments)) * 0.3
        seg_color = (
            int(DRAGON_BODY[0] * color_scale),
            int(DRAGON_BODY[1] * color_scale),
            int(DRAGON_BODY[2] * color_scale)
        )
        pygame.draw.circle(surface, seg_color, (int(seg_x), int(seg_y)), int(12 * size))

    # Рисуем тело (сегменты)
    for i, (seg_x, seg_y) in enumerate(body_segments):
        size = 0.8 - (i / len(body_segments)) * 0.3
        pygame.draw.ellipse(surface, DRAGON_BODY,
                           (seg_x - body_width*size/2, seg_y - body_height*size/2,
                            body_width*size, body_height*size))

    # Рисуем живот (более светлый)
    for i, (seg_x, seg_y) in enumerate(body_segments):
        if i < len(body_segments) - 2:  # Не рисуем живот на последних сегментах
            belly_size = 0.6 - (i / len(body_segments)) * 0.3
            pygame.draw.ellipse(surface, DRAGON_BELLY,
                               (seg_x - body_width*belly_size/3, seg_y - body_height*belly_size/4,
                                body_width*belly_size/1.5, body_height*belly_size/2))

    # Рисуем голову
    pygame.draw.circle(surface, DRAGON_BODY, (int(head_x), int(head_y)), head_radius)

    # Рисуем морду
    muzzle_length = 20
    muzzle_x = head_x + math.cos(direction) * muzzle_length
    muzzle_y = head_y + math.sin(direction) * muzzle_length
    muzzle_radius = head_radius * 0.6
    pygame.draw.circle(surface, DRAGON_BODY, (int(muzzle_x), int(muzzle_y)), int(muzzle_radius))

    # Рисуем глаза
    eye_offset = 8
    eye_radius = 7
    left_eye_x = head_x + math.cos(direction - 0.3) * eye_offset
    left_eye_y = head_y + math.sin(direction - 0.3) * eye_offset
    right_eye_x = head_x + math.cos(direction + 0.3) * eye_offset
    right_eye_y = head_y + math.sin(direction + 0.3) * eye_offset

    # Свечение глаз
    pygame.draw.circle(surface, DRAGON_EYES_GLOW, (int(left_eye_x), int(left_eye_y)), eye_radius + 3)
    pygame.draw.circle(surface, DRAGON_EYES_GLOW, (int(right_eye_x), int(right_eye_y)), eye_radius + 3)

    # Глаза
    pygame.draw.circle(surface, DRAGON_EYES, (int(left_eye_x), int(left_eye_y)), eye_radius)
    pygame.draw.circle(surface, DRAGON_EYES, (int(right_eye_x), int(right_eye_y)), eye_radius)

    # Зрачки
    pupil_radius = 3
    pygame.draw.circle(surface, (0, 0, 0), (int(left_eye_x), int(left_eye_y)), pupil_radius)
    pygame.draw.circle(surface, (0, 0, 0), (int(right_eye_x), int(right_eye_y)), pupil_radius)

    # Рисуем крылья
    wing_amplitude = math.sin(pygame.time.get_ticks() * 0.01) * 15  # Анимация взмахов
    wing_points_left = [
        (head_x - 25, head_y),
        (head_x - 60, head_y - 40 + wing_amplitude),
        (head_x - 35, head_y - 20),
        (head_x - 20, head_y - 10)
    ]
    wing_points_right = [
        (head_x - 25, head_y),
        (head_x - 60, head_y + 40 - wing_amplitude),
        (head_x - 35, head_y + 20),
        (head_x - 20, head_y + 10)
    ]

    pygame.draw.polygon(surface, DRAGON_WINGS, wing_points_left)
    pygame.draw.polygon(surface, DRAGON_WINGS, wing_points_right)

    # Рисуем рога
    horn_length = 25
    left_horn_x = head_x + math.cos(direction - 0.8) * horn_length
    left_horn_y = head_y + math.sin(direction - 0.8) * horn_length
    right_horn_x = head_x + math.cos(direction + 0.8) * horn_length
    right_horn_y = head_y + math.sin(direction + 0.8) * horn_length

    pygame.draw.line(surface, DRAGON_ACCENT, (head_x, head_y), (left_horn_x, left_horn_y), 4)
    pygame.draw.line(surface, DRAGON_ACCENT, (head_x, head_y), (right_horn_x, right_horn_y), 4)

    # Рисуем шипы на спине
    for i, (seg_x, seg_y) in enumerate(body_segments[:-3]):  # Шипы только на первых сегментах
        spike_size = 10 - (i / len(body_segments)) * 6
        if spike_size > 3:
            spike_dir = direction + math.pi / 2  # Перпендикулярно направлению
            spike_x = seg_x + math.cos(spike_dir) * spike_size
            spike_y = seg_y + math.sin(spike_dir) * spike_size
            pygame.draw.line(surface, DRAGON_ACCENT, (seg_x, seg_y), (spike_x, spike_y), 3)

# Инициализация сегментов тела и хвоста
body_segments = [[WIDTH // 2, HEIGHT // 2] for _ in range(5)]
tail_segments = [[WIDTH // 2, HEIGHT // 2] for _ in range(TAIL_SEGMENTS)]

# Главный цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем позицию мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Обновляем позицию головы (плавно следует за мышкой)
    head_x, head_y = body_segments[0]
    head_x += (mouse_x - head_x - 25) * DRAGON_SPEED
    head_y += (mouse_y - head_y - 25) * DRAGON_SPEED
    body_segments[0] = [head_x, head_y]

    # Обновляем сегменты тела (каждый следует за предыдущим)
    for i in range(1, len(body_segments)):
        prev_x, prev_y = body_segments[i-1]
        curr_x, curr_y = body_segments[i]
        body_segments[i] = [
            curr_x + (prev_x - curr_x) * DRAGON_SPEED * 2,
            curr_y + (prev_y - curr_y) * DRAGON_SPEED * 2
        ]

    # Обновляем хвост (следует за последним сегментом тела)
    tail_segments[0] = body_segments[-1][:]  # Первый сегмент хвоста следует за телом

    for i in range(1, len(tail_segments)):
        prev_x, prev_y = tail_segments[i-1]
        curr_x, curr_y = tail_segments[i]
        tail_segments[i] = [
            curr_x + (prev_x - curr_x) * DRAGON_SPEED * 3,
            curr_y + (prev_y - curr_y) * DRAGON_SPEED * 3
        ]

    # Заливка фона
    screen.fill(BACKGROUND)

    # Рисуем дракона
    draw_detailed_dragon(screen, head_x, head_y, body_segments, tail_segments, mouse_x, mouse_y)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

pygame.quit()
sys.exit()