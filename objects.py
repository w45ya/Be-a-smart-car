import pygame
import pyganim
import sys
import os

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.width = 350
        self.height = 200
        self.x = self.game.window_width / 2 - self.width /2
        self.y = self.game.window_height - self.height - 40
        self.velocity = 0
        self.max_speed = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #self.image.set_colorkey((255, 255, 255))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, left, right):
        if left:
            self.velocity -= self.max_speed
        if right:
            self.velocity += self.max_speed
        if not (left or right):
            self.velocity = 0
        if self.velocity > self.max_speed:
            self.velocity = self.max_speed
        if self.velocity < -self.max_speed:
            self.velocity = -self.max_speed
        self.rect.x += self.velocity
        if self.rect.x <= 20:
            self.rect.x = 20
        if self.rect.x >= self.game.window_width - self.width - 20:
            self.rect.x = self.game.window_width - self.width - 20


class MovingLine(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.width = self.game.window_width
        self.height = 7
        self.speed = 0
        self.x = 0
        self.y = 290
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.game.Line_color)
        self.image.set_alpha(200)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.speed += self.rect.y / 30000
        self.rect.y += self.speed
