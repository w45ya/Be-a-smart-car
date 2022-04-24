from objects import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.window_width / 2
        self.mid_h = self.game.window_height / 2
        self.rect = self.game.background.get_rect()
        self.run_display = True
        self.title = pygame.image.load(resource_path('resources/menu/title.png'))

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
        self.button_continue = pygame.image.load(resource_path('resources/menu/button_continue.png'))
        self.cursor1 = pygame.image.load(resource_path('resources/menu/cursor1.png'))
        self.cursor2 = pygame.image.load(resource_path('resources/menu/cursor2.png'))
        self.cursor3 = pygame.image.load(resource_path('resources/menu/cursor3.png'))
        self.cursor4 = pygame.image.load(resource_path('resources/menu/cursor4.png'))

        self.state = 1
        self.previous_state = 1
        self.state_changed = 0
        self.current_cursor = self.cursor1

    def display_menu(self):
        self.run_display = True
        self.game.sound_game_lost.stop()
        self.game.sound_game_win.stop()
        self.game.sound_excellent.stop()
        if self.game.sound and not self.game.resume and not self.game.from_tutor_to_menu:
            self.game.sound_game_start.play()
        if self.game.from_tutor_to_menu:
            self.game.from_tutor_to_menu = False
        while self.run_display:
            self.game.events()
            self.check_input()
            self.game.screen.fill(self.game.Black_color)
            self.game.screen.blit(self.game.background, self.rect)
            self.game.screen.blit(self.title, self.rect)
            if not self.game.resume:
                self.game.screen.blit(self.button_play, self.rect)
                if self.state == 1:
                    self.current_cursor = self.cursor1
            else:
                self.game.screen.blit(self.button_continue, self.rect)
                if self.state == 1:
                    self.current_cursor = self.cursor4
            self.game.screen.blit(self.button_how, self.rect)
            if self.game.sound:
                self.game.screen.blit(self.button_sound1, self.rect)
            else:
                self.game.screen.blit(self.button_sound0, self.rect)
            self.game.screen.blit(self.current_cursor, self.rect)
            self.blit_screen()
            if self.game.mouse_pressed:
                pygame.time.wait(150)

    def move_cursor(self):
        self.previous_state = self.state
        if 320 <= self.game.mouse_pos[0] <= 960 and 230 <= self.game.mouse_pos[1] <= 340 and pygame.mouse.get_rel() != (0, 0):
            self.state = 1
            self.state_changed = self.previous_state - self.state
            if self.state_changed != 0:
                if not self.game.resume:
                    self.current_cursor = self.cursor1
                else:
                    self.current_cursor = self.cursor4
                if self.game.sound:
                    self.game.sound_menu_select.play()
        if 320 <= self.game.mouse_pos[0] <= 960 and 341 <= self.game.mouse_pos[1] <= 479 and pygame.mouse.get_rel() != (0, 0):
            self.state = 2
            self.state_changed = self.previous_state - self.state
            if self.state_changed != 0:
                self.current_cursor = self.cursor2
                if self.game.sound:
                    self.game.sound_menu_select.play()
        if 320 <= self.game.mouse_pos[0] <= 960 and 480 <= self.game.mouse_pos[1] <= 590 and pygame.mouse.get_rel() != (0, 0):
            self.state = 3
            self.state_changed = self.previous_state - self.state
            if self.state_changed != 0:
                self.current_cursor = self.cursor3
                if self.game.sound:
                    self.game.sound_menu_select.play()
        if self.game.DownKey:
            if self.state == 1:
                self.current_cursor = self.cursor2
                self.state = 2
            elif self.state == 2:
                self.current_cursor = self.cursor3
                self.state = 3
            elif self.state == 3:
                if not self.game.resume:
                    self.current_cursor = self.cursor1
                else:
                    self.current_cursor = self.cursor4
                self.state = 1
            if self.game.sound:
                self.game.sound_menu_select.play()
        if self.game.UpKey:
            if self.state == 1:
                self.current_cursor = self.cursor3
                self.state = 3
            elif self.state == 2:
                if not self.game.resume:
                    self.current_cursor = self.cursor1
                else:
                    self.current_cursor = self.cursor4
                self.state = 1
            elif self.state == 3:
                self.current_cursor = self.cursor2
                self.state = 2
            if self.game.sound:
                self.game.sound_menu_select.play()

    def check_input(self):
        self.move_cursor()
        if self.game.EnterKey or self.game.mouse_pressed:
            if self.state == 1:
                self.game.playing = True
                self.run_display = False
            elif self.state == 2:
                self.game.curr_menu = self.game.tutor_menu
                self.run_display = False
            elif self.state == 3:
                self.game.sound = not self.game.sound
                if not self.game.sound:
                    self.game.sound_off()
                if self.game.sound:
                    self.game.screen.blit(self.button_sound1, self.rect)
                    if self.game.resume:
                        self.game.sound_music.play()
                else:
                    self.game.screen.blit(self.button_sound0, self.rect)
            if self.game.sound:
                self.game.sound_menu_press.play()
        if self.game.EscKey:
            self.game.playing = True
            self.run_display = False
            self.game.reset_keys()
            if self.game.sound:
                self.game.sound_menu_press.play()


class TutorialMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events()
            if self.game.EnterKey or self.game.EscKey or self.game.mouse_pressed:
                if self.game.sound:
                    self.game.sound_menu_press.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.reset_keys()
            self.game.screen.blit(self.game.tutorial_screen, self.rect)
            self.blit_screen()
            self.game.from_tutor_to_menu = True
            if self.game.mouse_pressed:
                pygame.time.wait(150)
