import pygame
import sys
from ui import MainMenu, PauseMenu, WinMenu, GameOverMenu
from classic import ClassicSnake
from hunger import HungerSnake

def main():
    pygame.init()
    screen_width, screen_height = 900, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    
    main_menu = MainMenu(screen_width, screen_height)
    pause_menu = PauseMenu(screen_width, screen_height)
    win_menu = WinMenu(screen_width, screen_height)
    game_over_menu = GameOverMenu(screen_width, screen_height)
    
    current_game = None
    game_mode = None
    paused = False
    show_win = True
    show_game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not current_game:
                result = main_menu.handle_events(event)
                if result == "play":
                    main_menu.show_mode_select = True
                elif result == "quit":
                    running = False
                elif result == "classic":
                    current_game = ClassicSnake(screen_width, screen_height)
                    game_mode = "classic"
                    main_menu.show_mode_select = False
                elif result == "hunger":
                    current_game = HungerSnake(screen_width, screen_height)
                    game_mode = "hunger"
                    main_menu.show_mode_select = False
            elif show_win:
                result = win_menu.handle_events(event)
                if result == "restart":
                    if game_mode == "classic":
                        current_game = ClassicSnake(screen_width, screen_height)
                    else:
                        current_game = HungerSnake(screen_width, screen_height)
                    show_win = False
                elif result == "quit":
                    current_game = None
                    show_win = False
            elif show_game_over:
                result = game_over_menu.handle_events(event)
                if result == "restart":
                    if game_mode == "classic":
                        current_game = ClassicSnake(screen_width, screen_height)
                    else:
                        current_game = HungerSnake(screen_width, screen_height)
                    show_game_over = False
                elif result == "quit":
                    current_game = None
                    show_game_over = False
            elif paused:
                result = pause_menu.handle_events(event)
                if result == "resume":
                    paused = False
                elif result == "quit":
                    current_game = None
                    paused = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                
                current_game.handle_events(event)
        
        if not current_game:
            main_menu.draw(screen)
        elif show_win:
            current_game.draw(screen)
            win_menu.draw(screen)
        elif show_game_over:
            current_game.draw(screen)
            game_over_menu.draw(screen)
        elif paused:
            current_game.draw(screen)
            pause_menu.draw(screen)
        else:
            current_game.update()
            current_game.draw(screen)
            
            if current_game.win:
                show_win = True
            elif current_game.game_over:
                show_game_over = True
        
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()