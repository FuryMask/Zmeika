import pygame
import random
import time

class HungerSnake:
    def __init__(self, screen_width, screen_height, cell_size=30):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.grid_width = screen_width // cell_size
        self.grid_height = screen_height // cell_size
        self.reset()
        
    def reset(self):
        self.snake = [(self.grid_width//2, self.grid_height//2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.generate_food()
        self.game_over = False
        self.win = False
        self.last_eat_time = time.time()
        
    def generate_food(self):
        while True:
            food = (random.randint(0, self.grid_width-1), random.randint(0, self.grid_height-1))
            if food not in self.snake:
                return food
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.next_direction = (1, 0)
            elif event.key == pygame.K_r:
                self.reset()
    
    def update(self):
        if self.game_over or self.win:
            return
            
        current_time = time.time()
        if current_time - self.last_eat_time > 5:
            self.game_over = True
            return
            
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or 
            new_head[1] < 0 or new_head[1] >= self.grid_height or 
            new_head in self.snake):
            self.game_over = True
            return
            
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.food = self.generate_food()
            self.last_eat_time = time.time()
            if len(self.snake) == self.grid_width * self.grid_height:
                self.win = True
        else:
            self.snake.pop()
    
    def draw(self, screen):
        screen.fill((50, 150, 50))
        
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (60, 160, 60), rect, 1)
        
        time_left = 5 - (time.time() - self.last_eat_time)
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Время до голода: {max(0, time_left):.1f}с", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        
        for i, (x, y) in enumerate(self.snake):
            color = (30, 90, 200) if i == 0 else (60, 120, 255)
            rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (20, 70, 180), rect, 2)
        
        food_rect = pygame.Rect(self.food[0]*self.cell_size, self.food[1]*self.cell_size, 
                              self.cell_size, self.cell_size)
        pygame.draw.rect(screen, (255, 50, 50), food_rect)
        pygame.draw.rect(screen, (200, 30, 30), food_rect, 2)