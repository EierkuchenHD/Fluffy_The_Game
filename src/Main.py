import pygame, sys, random, tkinter as tk
from tkinter import messagebox
import os
from Player import Player
from SFX import SFX
from Options import Options

# Constants
FPS = 60

# Precomputed Constants
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 190
JUMP_COUNT_MAX = 11
RUNNING_VELOCITY = 5

class Main:
    @staticmethod
    def initialize_game():
        pygame.init()
        WIDTH, HEIGHT = 800, 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fluffy: The Game | FPS: 0")  # Initial caption with FPS placeholder
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "icon.ico")
        if os.path.exists(icon_path):  # Check if icon file exists
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        return screen, WIDTH, HEIGHT

    @staticmethod
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

        sfx = SFX()

        font = pygame.font.Font(None, 100)  # Font for "FLUFFY!" text
        small_font = pygame.font.Font(None, 30)  # Font for "Total Jumps" text
        return player_img, sfx, font, small_font

    @staticmethod
    def show_error_message(title, message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)

    @staticmethod
    def jump(player_y, is_jumping, keys, sfx, text, font, jump_count, total_jumps):
        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
                sfx.play_jump_sound()
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

    @staticmethod
    def draw(screen, text, text_rect, player, total_jumps_text, options):
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        player.draw(screen)
        screen.blit(total_jumps_text, (10, 10))  # Position of total jumps text
        options.draw_options_menu(screen)  # Draw options menu
        pygame.display.update()  # Update the display

    @staticmethod
    def main():
        screen, WIDTH, HEIGHT = Main.initialize_game()
        try:
            player_img, sfx, font, small_font = Main.load_assets()
        except FileNotFoundError as e:
            Main.show_error_message("Asset Error", str(e))
            pygame.quit()
            sys.exit()

        player = Player(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, player_img)
        player_vel = RUNNING_VELOCITY
        is_jumping = False
        jump_count = JUMP_COUNT_MAX
        text = font.render("FLUFFY!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        total_jumps = 0  # Initialize total jumps counter
        total_jumps_text = small_font.render("Total Jumps: 0", True, (255, 255, 255))  # Initial total jumps text

        options = Options(WIDTH, HEIGHT)

        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        options.toggle_options()
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        options.handle_events()

            keys = pygame.key.get_pressed()
            player.move(keys, player_vel, WIDTH)
            player.y, is_jumping, text, jump_count, total_jumps = Main.jump(player.y, is_jumping, keys, sfx, text, font, jump_count, total_jumps)
            total_jumps_text = small_font.render(f"Total Jumps: {total_jumps}", True, (255, 255, 255))  # Update total jumps text
            Main.draw(screen, text, text_rect, player, total_jumps_text, options)

            # Update FPS in the window caption
            pygame.display.set_caption(f"Fluffy: The Game | FPS: {int(clock.get_fps())}")

            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main.main()
