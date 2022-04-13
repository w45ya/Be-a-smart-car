from objects import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.window_width / 2
        self.mid_h = self.game.window_height / 2
        self.rect = self.game.background.get_rect()
        self.run_display = True
        self.title = pygame.image.load(resource_path('resources/menu/title.png'))
        self.sound_menu_press = pygame.mixer.Sound(resource_path('resources/sound/menu_press.ogg'))
        self.sound_menu_select = pygame.mixer.Sound(resource_path('resources/sound/menu_select.ogg'))

    def blit_screen(self):
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.button_play = pygame.image.load(resource_path('resources/menu/button_play.png'))
        self.button_how = pygame.image.load(resource_path('resources/menu/button_how.png'))
        self.button_sound0 = pygame.image.load(resource_path('resources/menu/button_sound0.png'))
        self.button_sound1 = pygame.image.load(resource_path('resources/menu/button_sound1.png'))
        self.cursor1 = pygame.image.load(resource_path('resources/menu/cursor1.png'))
        self.cursor2 = pygame.image.load(resource_path('resources/menu/cursor2.png'))
        self.cursor3 = pygame.image.load(resource_path('resources/menu/cursor3.png'))

        self.state = 1
        self.current_cursor = self.cursor1

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.screen.fill(self.game.Back_color)
            self.game.screen.blit(self.game.background, self.rect)
            self.game.screen.blit(self.title, self.rect)
            self.game.screen.blit(self.button_play, self.rect)
            self.game.screen.blit(self.button_how, self.rect)
            if self.game.sound:
                self.game.screen.blit(self.button_sound1, self.rect)
            else:
                self.game.screen.blit(self.button_sound0, self.rect)
            self.game.screen.blit(self.current_cursor, self.rect)
            self.blit_screen()

    def move_cursor(self):
        if self.game.DownKey:
            if self.state == 1:
                self.current_cursor = self.cursor2
                self.state = 2
            elif self.state == 2:
                self.current_cursor = self.cursor3
                self.state = 3
            elif self.state == 3:
                self.current_cursor = self.cursor1
                self.state = 1
            self.sound_menu_select.play()
        if self.game.UpKey:
            if self.state == 1:
                self.current_cursor = self.cursor3
                self.state = 3
            elif self.state == 2:
                self.current_cursor = self.cursor1
                self.state = 1
            elif self.state == 3:
                self.current_cursor = self.cursor2
                self.state = 2
            self.sound_menu_select.play()

    def check_input(self):
        self.move_cursor()
        if self.game.EnterKey:
            self.sound_menu_press.play()
            if self.state == 1:
                self.game.playing = True
            elif self.state == 2:
                self.game.curr_menu = self.game.tutor_menu
            elif self.state == 3:
                self.game.sound = not self.game.sound
            self.run_display = False


class TutorialMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()

            if self.game.EnterKey:
                self.sound_menu_press.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            self.game.screen.blit(self.game.background, self.rect)
            self.game.screen.blit(self.title, self.rect)
            self.blit_screen()
