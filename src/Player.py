import pygame

class Player:
    def __init__(self, x, y, width, height, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = img
        self.flipped = False

    def move(self, keys, vel, WIDTH):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= vel
            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
                self.flipped = False
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += vel
            if not self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
                self.flipped = True

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
