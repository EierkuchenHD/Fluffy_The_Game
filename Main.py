import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
import os

# Constants
FPS = 60

# Precomputed Constants
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 190
JUMP_COUNT_MAX = 11
RUNNING_VELOCITY = 5

# Function to initialize the game window
def initialize_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fluffy: The Game | FPS: 0")  # Initial caption with FPS placeholder
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "icon.ico")
    if os.path.exists(icon_path):  # Check if icon file exists
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    return screen, WIDTH, HEIGHT

# Function to load game assets
def load_assets():
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        script_dir = sys._MEIPASS
    else:
        # Running as a script
        script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        player_img = pygame.image.load(os.path.join(script_dir, "data", "basilisk.png"))
        player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    except FileNotFoundError:
        raise FileNotFoundError("The image file 'basilisk.png' is missing.")

    try:
        jump_sound = pygame.mixer.Sound(os.path.join(script_dir, "data", "boing.ogg"))
    except FileNotFoundError:
        raise FileNotFoundError("The sound file 'boing.ogg' is missing.")

    font = pygame.font.Font(None, 100)  # Font for "FLUFFY!" text
    small_font = pygame.font.Font(None, 30)  # Font for "Total Jumps" text
    return player_img, jump_sound, font, small_font

def show_error_message(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)

# Function to handle player movement
def move_player(keys, player_x, player_vel, WIDTH, player_width, player_img, player_flipped):
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
        if player_flipped:
            player_img = pygame.transform.flip(player_img, True, False)
            player_flipped = False
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_vel
        if not player_flipped:
            player_img = pygame.transform.flip(player_img, True, False)
            player_flipped = True
    return player_x, player_img, player_flipped

# Function to handle player jumping
def jump(player_y, is_jumping, keys, jump_sound, text, font, jump_count, total_jumps):
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            jump_sound.play()
            text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            text = font.render("FLUFFY!", True, text_color)
            total_jumps += 1  # Increment total jumps
    else:
        if jump_count >= -JUMP_COUNT_MAX:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = JUMP_COUNT_MAX
    return player_y, is_jumping, text, jump_count, total_jumps

# Function to draw game elements on the screen
def draw(screen, text, text_rect, player_img, player_x, player_y, total_jumps_text):
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    screen.blit(player_img, (player_x, player_y))
    screen.blit(total_jumps_text, (10, 10))  # Position of total jumps text
    pygame.display.update()  # Update the display


def main():
    screen, WIDTH, HEIGHT = initialize_game()
    try:
        player_img, jump_sound, font, small_font = load_assets()
    except FileNotFoundError as e:
        show_error_message("Asset Error", str(e))
        pygame.quit()
        sys.exit()

    player_x, player_y = WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT
    player_vel = RUNNING_VELOCITY
    is_jumping = False
    jump_count = JUMP_COUNT_MAX
    player_flipped = False
    text = font.render("FLUFFY!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    total_jumps = 0  # Initialize total jumps counter
    total_jumps_text = small_font.render("Total Jumps: 0", True, (255, 255, 255))  # Initial total jumps text

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player_x, player_img, player_flipped = move_player(keys, player_x, player_vel, WIDTH, PLAYER_WIDTH, player_img, player_flipped)
        player_y, is_jumping, text, jump_count, total_jumps = jump(player_y, is_jumping, keys, jump_sound, text, font, jump_count, total_jumps)
        total_jumps_text = small_font.render(f"Total Jumps: {total_jumps}", True, (255, 255, 255))  # Update total jumps text
        draw(screen, text, text_rect, player_img, player_x, player_y, total_jumps_text)

        # Update FPS in the window caption
        pygame.display.set_caption(f"Fluffy: The Game | FPS: {int(clock.get_fps())}")

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
