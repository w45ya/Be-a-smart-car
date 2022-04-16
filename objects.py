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
        self.hitbox_image = pygame.Surface((self.width - 20, self.height / 2 - self.height / 3))
        self.hitbox_image.fill((255, 0, 0))
        self.hitbox = pygame.Rect(self.x + 10, self.y + self.height / 2, self.width - 20, self.height / 2 - self.height / 3)
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.image.load(resource_path('resources/sprites/car.png'))
        self.count = 1
        self.amplitude = 10
        self.text_timer = 0
        self.text_duration = 150
        self.text = ""

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
            self.game.screen.blit(self.hitbox_image, self.hitbox)

        self.hitbox.x = self.rect.x + 10
        self.hitbox.y = self.rect.y + self.height / 2

        self.count += 1
        if self.count > 60: self.count = 1
        if self.count == self.amplitude or self.count == self.amplitude * 2 or self.count == self.amplitude * 3:
            self.rect.y += 1
        if self.count == self.amplitude * 4 or self.count == self.amplitude * 5 or self.count == self.amplitude * 6:
            self.rect.y -= 1

        self.text_timer -= 1
        if self.text_timer > 0:
            self.game.draw_text(self.text, 70, self.game.window_width / 2, self.game.window_height / 2 - self.game.window_height / 4, self.game.Font_color, True)

        self.colide()

    def colide(self):
        for e in self.game.entities:
            if pygame.sprite.collide_rect(self, e):
                if isinstance(e, Bonus) and self.hitbox.colliderect(e.hitbox):
                    if e.type == 1:                   # Игры
                        self.game.time_count -= 100
                        self.text_timer = self.text_duration
                        self.text = "Время: -100 Готовность: +0%"
                    elif e.type == 2:                 # Фильмы
                        self.game.time_count -= 50
                        self.text_timer = self.text_duration
                        self.text = "Время: -50 Готовность: +0%"
                    elif e.type == 3:                 # Пиво
                        self.game.time_count -= 100
                        self.game.score -= 10
                        self.text_timer = self.text_duration
                        self.text = "Время: -100 Готовность: -10%"
                        if self.game.score < 0:
                            self.game.score = 0
                    elif e.type == 4:                 # Подготовка диплома
                        self.game.time_count -= 100
                        self.game.score += 10
                        self.text_timer = self.text_duration
                        self.text = "Время: -100 Готовность: +10%"
                    elif e.type == 5:                 # Обучение
                        self.game.time_count -= 50
                        self.game.score += 5
                        self.text_timer = self.text_duration
                        self.text = "Время: -50 Готовность: +5%"
                    elif e.type == 6:                 # Программирование
                        self.game.time_count -= 50
                        self.game.score += 5
                        self.text_timer = self.text_duration
                        self.text = "Время: -50 Готовность: +5%"
                    else: # тест
                        self.game.score += 100
                    self.game.entities.remove(e)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, game, way, type):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.size = 32
        self.way = way
        self.type = type
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

        self.hitbox_image = pygame.Surface((self.size, self.size / 2 - self.size / 3))
        self.hitbox_image.fill((255, 0, 0))
        self.hitbox = pygame.Rect(self.x, self.y + self.size / 2, self.size, self.size / 2 - self.size / 3)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.type == 1:
            self.image = pygame.image.load(resource_path('resources/sprites/antibonus1.png')) # Игры
        elif self.type == 2:
            self.image = pygame.image.load(resource_path('resources/sprites/antibonus2.png')) # Фильмы
        elif self.type == 3:
            self.image = pygame.image.load(resource_path('resources/sprites/antibonus3.png')) # Пиво
        elif self.type == 4:
            self.image = pygame.image.load(resource_path('resources/sprites/bonus1.png'))     # Подготовка диплома
        elif self.type == 5:
            self.image = pygame.image.load(resource_path('resources/sprites/bonus2.png'))     # Обучение
        elif self.type == 6:
            self.image = pygame.image.load(resource_path('resources/sprites/bonus3.png'))     # Программирование
        else:
            self.image = pygame.image.load(resource_path('resources/sprites/test.png'))
        self.size += 1
        self.speed = self.rect.y / 175
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.hitbox_image = pygame.transform.scale(self.hitbox_image, (self.size, int(self.size / 2 - self.size / 3)))
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y + self.size / 2, self.size, int(self.size / 2 - self.size / 3))

        if self.way == 1:
            self.rect = pygame.Rect(self.rect.x - self.speed, self.rect.y, self.size, self.size)
        elif self.way == 2:
            self.rect = pygame.Rect(self.game.window_width / 2 - self.size / 2, self.rect.y, self.size, self.size)
        elif self.way == 3:
            self.rect = pygame.Rect(self.rect.x + self.speed, self.rect.y, self.size, self.size)
        self.rect.y += self.speed

        if self.game.show_hitbox:
            self.game.screen.blit(self.hitbox_image, self.hitbox)


        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y + self.size / 2


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
        #self.image.set_alpha(200)
        self.rect = pygame.Rect(self.x, self.y + h, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.speed += self.rect.y / 30000
        self.rect.y += self.speed
