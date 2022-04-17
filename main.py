import random as rnd
from menu import *
from objects import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()


class Game:
    def __init__(self):
        self.running = False
        self.playing = False
        self.resume = False
        self.game_completed = False
        self.sound = True

        self.LeftKey = False
        self.RightKey = False
        self.UpKey = False
        self.DownKey = False
        self.EnterKey = False
        self.EscKey = False
        self.show_hitbox = False
        self.mouse_pressed = False
        self.mouse_pos = (0, 0)
        self.from_tutor_to_menu = False

        self.window_width = 1280
        self.window_height = 720
        self.screen_size = (self.window_width, self.window_height)
        self.screen = pygame.display.set_mode(
            self.screen_size,
            pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        pygame.display.set_caption("Be a smart car v1.0")
        pygame.display.set_icon(pygame.image.load(resource_path("resources/icon/icon.ico")))
        self.clock = pygame.time.Clock()
        self.fps = 120
        self.frames_count = 0
        self.bonus_way = 0
        self.bonus_type = 0
        self.time_default = 1000
        self.score = 0
        self.time_count = self.time_default
        self.time_str = ""
        self.score_str = ""

        self.Black_color = (0, 0, 0)
        self.Font_color = (0, 220, 220)
        self.Line_color = (240, 2, 244)
        self.Good_color = (28, 255, 165)
        self.Well_color = (255, 252, 36)
        self.font = resource_path('resources/font/nk110.ttf')
        self.background = pygame.image.load(resource_path('resources/backgrounds/background.jpg'))
        self.tutorial_screen = pygame.image.load(resource_path('resources/backgrounds/tutorial.jpg'))
        self.rect = self.background.get_rect()
        self.sound_menu_press = pygame.mixer.Sound(resource_path('resources/sound/menu_press.ogg'))
        self.sound_menu_select = pygame.mixer.Sound(resource_path('resources/sound/menu_select.ogg'))
        self.sound_bonus = pygame.mixer.Sound(resource_path('resources/sound/bonus.ogg'))
        self.sound_game_start = pygame.mixer.Sound(resource_path('resources/sound/game_start.ogg'))
        self.sound_game_lost = pygame.mixer.Sound(resource_path('resources/sound/game_lost.ogg'))
        self.sound_game_win = pygame.mixer.Sound(resource_path('resources/sound/game_win.ogg'))
        self.sound_excellent = pygame.mixer.Sound(resource_path('resources/sound/excellent.ogg'))
        self.sound_music = pygame.mixer.Sound(resource_path('resources/sound/mativve_life-on-synthwave.ogg'))
        self.sound_game_start.set_volume(0.3)
        self.sound_game_lost.set_volume(0.2)
        self.sound_game_win.set_volume(0.2)
        self.sound_excellent.set_volume(0.1)
        self.sound_menu_press.set_volume(0.5)
        self.sound_menu_select.set_volume(0.5)
        self.sound_bonus.set_volume(0.5)
        self.main_menu = MainMenu(self)
        self.tutor_menu = TutorialMenu(self)
        self.curr_menu = self.main_menu

        self.entities = pygame.sprite.Group()
        self.lines = pygame.sprite.Group()
        self.lines.add(MovingLine(self, 0))
        self.lines.add(MovingLine(self, 53))
        self.lines.add(MovingLine(self, 144))
        self.lines.add(MovingLine(self, 289))
        self.player = Player(self)
        self.entities.add(self.player)

    def run(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.curr_menu.display_menu()
            else:
                self.loop()

    def events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.main_menu.run_display = False
                self.tutor_menu.run_display = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    self.RightKey = True
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    self.LeftKey = True
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    self.UpKey = True
                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    self.DownKey = True
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER or e.key == pygame.K_SPACE:
                    self.EnterKey = True
                if e.key == pygame.K_ESCAPE:
                    self.EscKey = True
                    if self.playing and not self.game_completed:
                        self.playing = False
                        self.resume = True
                        self.EscKey = False
                        if self.sound:
                            self.sound_menu_press.play()
                if e.key == pygame.K_h:
                    self.show_hitbox = not self.show_hitbox
                if e.key == pygame.K_m:
                    self.sound = not self.sound
                    if not self.sound:
                        self.sound_off()

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_d or e.key == pygame.K_RIGHT:
                    self.RightKey = False
                if e.key == pygame.K_a or e.key == pygame.K_LEFT:
                    self.LeftKey = False
                if e.key == pygame.K_w or e.key == pygame.K_UP:
                    self.UpKey = False
                if e.key == pygame.K_s or e.key == pygame.K_DOWN:
                    self.DownKey = False
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER or e.key == pygame.K_SPACE:
                    self.EnterKey = False
                if e.key == pygame.K_ESCAPE:
                    self.EscKey = False

        self.mouse_pressed = pygame.mouse.get_pressed()[0]
        self.mouse_pos = pygame.mouse.get_pos()

    def reset_keys(self):
        self.LeftKey = False
        self.RightKey = False
        self.UpKey = False
        self.DownKey = False
        self.EnterKey = False
        self.EscKey = False

    def sound_off(self):
        self.sound_game_start.stop()
        self.sound_game_lost.stop()
        self.sound_game_win.stop()
        self.sound_excellent.stop()
        self.sound_menu_press.stop()
        self.sound_menu_select.stop()
        self.sound_bonus.stop()

    def draw_text(self, text, size, x, y, color, centered):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.x = x
            text_rect.y = y
        self.screen.blit(text_surface, text_rect)

    def time_to_string(self):
        if self.time_count < 0:
            return "0000"
        if self.time_count < 10:
            return "000" + str(self.time_count)
        elif self.time_count < 100:
            return "00" + str(self.time_count)
        elif self.time_count < 1000:
            return "0" + str(self.time_count)
        else:
            return str(self.time_count)

    def score_to_string(self):
        if self.score < 0:
            return "000%"
        elif self.score < 10:
            return "00" + str(self.score) + "%"
        elif self.score < 100:
            return "0" + str(self.score) + "%"
        else:
            return "100%"

    def game_over(self):
        self.game_completed = True
        self.sound_music.stop()
        if self.sound:
            self.screen.blit(self.background, self.rect)
        for line in self.lines:
            self.screen.blit(line.image, line.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.time_str = self.time_to_string()
        self.draw_text(self.time_str, 100, 30, 0, self.Font_color, False)
        self.score_str = self.score_to_string()
        self.draw_text(self.score_str, 100, self.window_width - 230, 0, self.Font_color, False)
        if self.score < 60:
            self.draw_text('Не сдал.', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 , self.Font_color, True)
            if self.sound:
                self.sound_game_lost.play()
        elif self.score < 71:
            self.draw_text('Cдал!', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 , self.Font_color, True)
            self.draw_text('Оценка: удовлетворительно', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 + 100, self.Font_color, True)
            if self.sound:
                self.sound_game_win.play()
        elif self.score < 85:
            self.draw_text('Cдал!', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 , self.Font_color, True)
            self.draw_text('Оценка: хорошо', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 + 100, self.Good_color, True)
            if self.sound:
                self.sound_game_win.play()
        else:
            self.draw_text('Cдал!', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 , self.Font_color, True)
            self.draw_text('Оценка: отлично!', 100, self.window_width / 2, self.window_height / 2 - self.window_height / 3 + 100, self.Well_color, True)
            if self.sound:
                self.sound_excellent.play()
        if self.EnterKey or self.EscKey or self.mouse_pressed:
            for e in self.entities:
                if isinstance(e, Bonus):
                    e.remove(self.entities)
            self.time_count = self.time_default
            self.score = 0
            self.playing = False
            self.resume = False
            self.EnterKey = False
            self.EscKey = False
            self.game_completed = False
            if self.sound:
                self.sound_menu_press.play()
        pygame.display.flip()
        if self.mouse_pressed:
            pygame.time.wait(300)

    def loop(self):
        self.sound_game_start.stop()
        self.sound_music.play()
        while self.playing:
            self.clock.tick(self.fps)
            self.frames_count += 1
            self.events()
            self.screen.fill(self.Black_color)
            self.screen.blit(self.background, self.rect)
            self.time_str = self.time_to_string()
            self.draw_text(self.time_str, 100, 30, 0, self.Font_color, False)
            self.score_str = self.score_to_string()
            self.draw_text(self.score_str, 100, self.window_width - 230, 0, self.Font_color, False)

            if self.frames_count % 60 == 0:
                self.lines.add(MovingLine(self))
                self.time_count -= 1

            if self.frames_count % 300 == 0 and not self.game_completed:
                self.bonus_way = rnd.randint(1, 3)
                self.bonus_type = rnd.randint(1, 6)
                self.entities.add(Bonus(self, self.bonus_way, self.bonus_type))
                self.entities.remove(self.player)
                self.entities.add(self.player)

            for line in self.lines:
                self.screen.blit(line.image, line.rect)
                line.update()
                if line.rect.y > self.window_height + 100:
                    line.remove(self.lines)

            for e in self.entities:
                self.screen.blit(e.image, e.rect)
                if isinstance(e, Bonus):
                    e.update()
                    if e.rect.y > self.window_height - 100:
                        e.remove(self.entities)
                    if e.rect.y == 520:
                        e.remove(self.entities)
                        e.add(self.entities)

            self.player.update(self.LeftKey, self.RightKey)

            if self.time_count <= 0 or self.score >= 100:
                if self.time_count < 0:
                    self.time_count = 0
                if self.score > 100:
                    self.score = 100
                self.game_over()
            pygame.display.flip()


game = Game()
game.run()
