#!/usr/bin/env python3

import pygame
import math
import os

# ASCII Splash
ascii_logo = r"""


░▒▓███████▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░░▒▓██████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓███████▓▒░░▒▓██████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░
R E T R O : R E V I V A L
        AcidWarp 2025 Edition - Terminal Warp Mode Active
                      Welcome to the past.
"""
print(ascii_logo)

# Constants
WIDTH, HEIGHT = 640, 480
FPS = 30

# Center window (just in case fullscreen fails or is toggled)
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("AcidWarp Revival - b145k0")
clock = pygame.time.Clock()

# Generate a sinusoidal color palette
palette = [
    (int(127 + 127 * math.sin(i * 0.024)),
     int(127 + 127 * math.sin(i * 0.024 + 2)),
     int(127 + 127 * math.sin(i * 0.024 + 4)))
    for i in range(256)
]

# === Warp effect functions ===
def plasma(x, y, t):
    return int((math.sin(x * 0.06 + t) +
                math.sin(y * 0.04 + t) +
                math.sin((x + y) * 0.02 + t)) * 42 + 128) % 256

def radial(x, y, t):
    cx, cy = WIDTH // 2, HEIGHT // 2
    dx, dy = x - cx, y - cy
    angle = math.atan2(dy, dx)
    dist = math.hypot(dx, dy)
    return int((math.sin(dist * 0.08 - t) + math.sin(angle * 5 + t)) * 64 + 128) % 256

def tunnel(x, y, t):
    cx, cy = WIDTH // 2, HEIGHT // 2
    dx, dy = x - cx, y - cy
    dist = math.hypot(dx, dy) + 1e-5
    angle = math.atan2(dy, dx)
    return int((math.sin(10 * angle + t) + math.cos(0.1 * dist + t)) * 64 + 128) % 256

# List of modes
modes = [plasma, radial, tunnel]
mode_index = 0

# === Render a single frame ===
def render(t, mode):
    surf = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = mode(x, y, t)
            surf.set_at((x, y), palette[c])
    return surf

# === Main visual loop ===
t = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                mode_index = (mode_index + 1) % len(modes)

    frame = render(t, modes[mode_index])
    screen.blit(frame, (0, 0))
    pygame.display.flip()
    t += 0.1
    clock.tick(FPS)

pygame.quit()

