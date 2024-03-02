import pygame
import sys

class Options:
    def __init__(self, screen_width, screen_height):
        self.options_open = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.menu_items = ["General Settings", "Advanced Settings", "Credits", "Exit Menu"]
        self.selected_item = 0

        # Define colors
        self.color_white = (255, 255, 255)
        self.color_gray = (128, 128, 128)
        self.color_background = (200, 200, 200)

        # Define item dimensions and positions
        self.bg_x = screen_width // 4
        self.bg_y = screen_height // 4
        self.bg_width = screen_width // 2
        self.bg_height = screen_height // 2
        self.item_spacing = self.bg_height / len(self.menu_items)

    def toggle_options(self):
        self.options_open = not self.options_open

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.toggle_options()
                elif event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)

    def draw_options_menu(self, screen):
        if self.options_open:
            # Draw gray background
            bg_rect = pygame.Rect(self.bg_x, self.bg_y, self.bg_width, self.bg_height)
            pygame.draw.rect(screen, self.color_background, bg_rect)

            # Draw menu items
            for i, item in enumerate(self.menu_items):
                color = self.color_white if i == self.selected_item else self.color_gray
                text = self.font.render(item, True, color)
                # Center text vertically within the gray background
                text_rect = text.get_rect(center=(self.screen_width // 2, self.bg_y + i * self.item_spacing + self.item_spacing / 2))
                screen.blit(text, text_rect)
