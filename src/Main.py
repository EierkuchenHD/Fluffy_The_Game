import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox
import os
from Player import Player
from SFX import SFX
from Options import Options

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 800
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 190
JUMP_COUNT_MAX = 11
RUNNING_VELOCITY = 5

class Main:
    @staticmethod
    def initialize_game():
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fluffy: The Game | FPS: 0")  # Initial caption with FPS placeholder
        Main.set_game_icon()
        return screen

    @staticmethod
    def set_game_icon():
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "icon.ico")
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)

    @staticmethod
    def load_assets():
        script_dir = Main.get_script_directory()
        player_img = Main.load_image(script_dir, "data", "basilisk.png")
        player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
        sfx = SFX()
        font = pygame.font.Font(None, 100)
        small_font = pygame.font.Font(None, 30)
        return player_img, sfx, font, small_font

    @staticmethod
    def get_script_directory():
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        else:
            return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def load_image(script_dir, *path_parts):
        path = os.path.join(script_dir, *path_parts)
        if not os.path.exists(path):
            raise FileNotFoundError(f"The image file '{os.path.basename(path)}' is missing.")
        return pygame.image.load(path)

    @staticmethod
    def show_error_message(title, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)

    @staticmethod
    def handle_jumping(player_y, is_jumping, keys, sfx, text, font, jump_count, total_jumps):
        if not is_jumping and keys[pygame.K_SPACE]:
            is_jumping = True
            sfx.play_jump_sound()
            text_color = Main.random_color()
            text = font.render("FLUFFY!", True, text_color)
            total_jumps += 1
        elif is_jumping:
            player_y, jump_count, is_jumping = Main.perform_jump(player_y, jump_count, is_jumping)
        return player_y, is_jumping, text, jump_count, total_jumps

    @staticmethod
    def random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    @staticmethod
    def perform_jump(player_y, jump_count, is_jumping):
        if jump_count >= -JUMP_COUNT_MAX:
            neg = 1 if jump_count >= 0 else -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jump_count = JUMP_COUNT_MAX
            is_jumping = False
        return player_y, jump_count, is_jumping

    @staticmethod
    def draw_screen(screen, text, text_rect, player, total_jumps_text, options):
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        player.draw(screen)
        screen.blit(total_jumps_text, (10, 10))
        options.draw_options_menu(screen)
        pygame.display.update()

    @staticmethod
    def main():
        screen = Main.initialize_game()
        try:
            player_img, sfx, font, small_font = Main.load_assets()
        except FileNotFoundError as e:
            Main.show_error_message("Asset Error", str(e))
            pygame.quit()
            sys.exit()

        player = Player(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, player_img)
        is_jumping = False
        jump_count = JUMP_COUNT_MAX
        text = font.render("FLUFFY!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        total_jumps = 0
        total_jumps_text = small_font.render("Total Jumps: 0", True, (255, 255, 255))

        options = Options(WIDTH, HEIGHT)
        clock = pygame.time.Clock()

        running = True
        while running:
            running = Main.handle_events(options)
            keys = pygame.key.get_pressed()
            player.move(keys, WIDTH)
            player.y, is_jumping, text, jump_count, total_jumps = Main.handle_jumping(player.y, is_jumping, keys, sfx, text, font, jump_count, total_jumps)
            total_jumps_text = small_font.render(f"Total Jumps: {total_jumps}", True, (255, 255, 255))
            Main.draw_screen(screen, text, text_rect, player, total_jumps_text, options)
            pygame.display.set_caption(f"Fluffy: The Game | FPS: {int(clock.get_fps())}")
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

    @staticmethod
    def handle_events(options):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    options.toggle_options()
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    options.handle_events()
        return True

if __name__ == "__main__":
    Main.main()
