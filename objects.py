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
        self.hitbox_image = pygame.Surface((self.width, self.height / 2 - self.height / 3))
        self.hitbox_image.fill((255, 0, 0))
        self.hitbox = pygame.Rect(self.x, self.y + self.height / 2, self.width / 2, self.height)
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

        if self.game.show_hitbox:
            self.hitbox_image.set_colorkey((0, 0, 0))
        else:
            self.hitbox_image.set_colorkey((255, 0, 0))

        self.game.screen.blit(self.hitbox_image, self.hitbox)
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y + self.height / 2
        self.colide(self.game)

    def colide(self, game):
        for e in game.entities:
            if pygame.sprite.collide_rect(self, e):
                if isinstance(e, Bonus) and self.hitbox.colliderect(e):
                    self.game.score += 50
                    game.entities.remove(e)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, game, way, type):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.size = 32
        self.way = way
        if self.way == 1:
            self.x = self.game.window_width / 2 - self.size / 2 - 50
        elif self.way == 2:
            self.x = self.game.window_width / 2 - self.size / 2
        elif self.way == 3:
            self.x = self.game.window_width / 2 - self.size / 2 + 75
        self.y = self.game.window_height / 2 - 100
        self.speed = 0
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.image = pygame.image.load(resource_path('resources/test.png'))
        self.size += 1
        self.speed = self.rect.y / 175
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        if self.way == 1:
            self.rect = pygame.Rect(self.rect.x - self.speed, self.rect.y, self.size, self.size)
        elif self.way == 2:
            self.rect = pygame.Rect(self.game.window_width / 2 - self.size / 2, self.rect.y, self.size, self.size)
        elif self.way == 3:
            self.rect = pygame.Rect(self.rect.x + self.speed, self.rect.y, self.size, self.size)
        self.rect.y += self.speed


class MovingLine(pygame.sprite.Sprite):
    def __init__(self, game, h=0):
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
        self.rect = pygame.Rect(self.x, self.y + h, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.speed += self.rect.y / 30000
        self.rect.y += self.speed
