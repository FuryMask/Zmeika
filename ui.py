import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 200, 255), hover_color=(150, 220, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, (50, 150, 200), self.rect, 3, border_radius=12)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.buttons = [
            Button(screen_width//2 - 110, screen_height//2, 220, 60, "Играть"),
            Button(screen_width//2 - 110, screen_height//2 + 80, 220, 60, "Выйти")
        ]
        self.mode_buttons = [
            Button(screen_width//2 - 160, screen_height//2, 320, 60, "Классический"),
            Button(screen_width//2 - 160, screen_height//2 + 80, 320, 60, "Режим голода")
        ]
        self.show_mode_select = False

    def draw(self, screen):
        screen.fill((173, 216, 230))
        title = self.font_large.render("Змейка", True, (50, 120, 180))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 100))
        
        if self.show_mode_select:
            for button in self.mode_buttons:
                button.draw(screen, self.font_medium)
        else:
            for button in self.buttons:
                button.draw(screen, self.font_medium)

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.show_mode_select:
            for button in self.mode_buttons:
                button.check_hover(mouse_pos)
            for i, button in enumerate(self.mode_buttons):
                if button.is_clicked(mouse_pos, event):
                    return ["classic", "hunger"][i]
        else:
            for button in self.buttons:
                button.check_hover(mouse_pos)
            for i, button in enumerate(self.buttons):
                if button.is_clicked(mouse_pos, event):
                    return ["play", "quit"][i]
        return None

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 48)
        self.buttons = [
            Button(screen_width//2 - 110, screen_height//2 - 10, 220, 60, "Продолжить"),
            Button(screen_width//2 - 110, screen_height//2 + 80, 220, 60, "Выйти")
        ]
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        panel = pygame.Rect(self.screen_width//2 - 150, self.screen_height//2 - 150, 300, 300)
        pygame.draw.rect(screen, (230, 240, 250), panel, border_radius=15)
        pygame.draw.rect(screen, (100, 180, 220), panel, 4, border_radius=15)
        
        title = self.font.render("Пауза", True, (50, 120, 180))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, panel.y + 50))
        
        for button in self.buttons:
            button.draw(screen, self.font)

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
        for i, button in enumerate(self.buttons):
            if button.is_clicked(mouse_pos, event):
                return ["resume", "quit"][i]
        return None

class WinMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.buttons = [
            Button(screen_width//2 - 110, screen_height//2 + 70, 220, 65, "Сыграть ещё"),
            Button(screen_width//2 - 110, screen_height//2 + 160, 220, 65, "Выйти")
        ]
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        panel = pygame.Rect(self.screen_width//2 - 250, self.screen_height//2 - 200, 500, 450)
        pygame.draw.rect(screen, (255, 255, 200), panel, border_radius=20)
        pygame.draw.rect(screen, (220, 180, 60), panel, 5, border_radius=20)
        
        title = self.font_large.render("Поздравляем!", True, (220, 140, 40))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, panel.y + 60))
        
        subtitle = self.font_medium.render("Вы победили!", True, (200, 120, 30))
        screen.blit(subtitle, (self.screen_width//2 - subtitle.get_width()//2, panel.y + 140))
        
        for button in self.buttons:
            button.draw(screen, self.font_medium)

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
        for i, button in enumerate(self.buttons):
            if button.is_clicked(mouse_pos, event):
                return ["restart", "quit"][i]
        return None

class GameOverMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.buttons = [
            Button(screen_width//2 - 110, screen_height//2 + 70, 220, 65, "Повторить"),
            Button(screen_width//2 - 110, screen_height//2 + 160, 220, 65, "Выйти")
        ]
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        panel = pygame.Rect(self.screen_width//2 - 250, self.screen_height//2 - 200, 500, 450)
        pygame.draw.rect(screen, (255, 200, 200), panel, border_radius=20)
        pygame.draw.rect(screen, (220, 80, 80), panel, 5, border_radius=20)
        
        title = self.font_large.render("Игра окончена", True, (220, 60, 60))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, panel.y + 60))
        
        subtitle = self.font_medium.render("Вы проиграли!", True, (200, 50, 50))
        screen.blit(subtitle, (self.screen_width//2 - subtitle.get_width()//2, panel.y + 140))
        
        for button in self.buttons:
            button.draw(screen, self.font_medium)

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
        for i, button in enumerate(self.buttons):
            if button.is_clicked(mouse_pos, event):
                return ["restart", "quit"][i]
        return None