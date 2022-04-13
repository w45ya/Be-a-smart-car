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
        self.show_hitbox = False

        self.window_width = 1280
        self.window_height = 720
        self.screen_size = (self.window_width, self.window_height)
        self.screen = pygame.display.set_mode(
            self.screen_size,
            pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        pygame.display.set_caption("Be a smart car (indev)")
        self.font = pygame.font.get_default_font()
        self.clock = pygame.time.Clock()
        self.fps = 120
        self.frames_count = 0
        self.way = 0

        self.Back_color = (0, 70, 70)
        self.Font_color = (0, 70, 70)
        self.Line_color = (240, 2, 244)
        self.Title_color = (106, 186, 151)
        self.background = pygame.image.load(resource_path('resources/backgrounds/background.png'))
        self.rect = self.background.get_rect()

        self.main_menu = MainMenu(self)
        self.tutor_menu = TutorialMenu(self)
        self.curr_menu = self.main_menu

        self.entities = pygame.sprite.Group()
        self.lines = pygame.sprite.Group()
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
                    if self.playing:
                        self.playing = False
                        self.resume = True
                if e.key == pygame.K_h:
                    self.show_hitbox = not self.show_hitbox
                if e.key == pygame.K_g:
                    self.sound = not self.sound

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

    def reset_keys(self):
        self.LeftKey = False
        self.RightKey = False
        self.UpKey = False
        self.DownKey = False
        self.EnterKey = False

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def loop(self):
        while self.playing:
            self.clock.tick(self.fps)
            self.frames_count += 1
            self.events()

            self.screen.fill(self.Back_color)
            self.screen.blit(self.background, self.rect)

            if self.frames_count % 60 == 0:
                moving_line = MovingLine(self)
                self.lines.add(moving_line)

            if self.frames_count % 500 == 0:
                self.way = rnd.randint(1,3)
                test_item = Bonus(self, self.way, 1)
                self.entities.add(test_item)

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

            self.player.update(self.LeftKey, self.RightKey)

            pygame.display.flip()


game = Game()
game.run()
