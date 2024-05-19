import pygame

class Player:
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.flipped = False
        self.velocity = 5  # Default velocity for the player

    def move(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right(screen_width)

    def move_left(self):
        if self.x > 0:
            self.x -= self.velocity
            self.flip_image(False)

    def move_right(self, screen_width):
        if self.x < screen_width - self.width:
            self.x += self.velocity
            self.flip_image(True)

    def flip_image(self, flip_right):
        if self.flipped != flip_right:
            self.img = pygame.transform.flip(self.img, True, False)
            self.flipped = flip_right

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
