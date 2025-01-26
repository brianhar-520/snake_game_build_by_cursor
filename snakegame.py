import pygame
import random
import os
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors (macOS style)
COLORS = {
    'background': (28, 28, 30),
    'grid': (44, 44, 46),
    'snake': (10, 132, 255),
    'apple': (255, 69, 58),
    'text': (255, 255, 255)
}

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize font (SF Pro)
def init_font():
    try:
        font_path = '/System/Library/Fonts/SFNS.ttf'  # SF Pro path
        if not os.path.exists(font_path):
            font_path = '/System/Library/Fonts/SFNSDisplay.ttf'
        return pygame.font.Font(font_path, 24)
    except:
        return pygame.font.SysFont('arial', 24)

FONT = init_font()

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = RIGHT
        self.score = 0

    def update(self):
        current = self.positions[0]
        x, y = self.direction
        new_x = current[0] + x
        new_y = current[1] + y

        # Check wall collision
        if (new_x < 0 or new_x >= GRID_WIDTH or 
            new_y < 0 or new_y >= GRID_HEIGHT):
            return False

        new = (new_x, new_y)

        # Check self collision
        if new in self.positions[2:]:
            return False

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def get_head_position(self):
        return self.positions[0]

class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
        self.state = 'menu'  # menu, playing, game_over

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == 'menu':
                    if event.key == pygame.K_SPACE:
                        self.state = 'playing'
                elif self.state == 'playing':
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.direction = UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.direction = RIGHT
                elif self.state == 'game_over':
                    if event.key == pygame.K_SPACE:
                        self.snake.reset()
                        self.state = 'playing'
        return True

    def update(self):
        if self.state == 'playing':
            if not self.snake.update():
                self.state = 'game_over'
                return
            
            if self.snake.get_head_position() == self.apple.position:
                self.snake.length += 1
                self.snake.score += 1
                self.apple.randomize()

    def draw(self):
        screen.fill(COLORS['background'])

        if self.state == 'menu':
            text = FONT.render('PRESS SPACE TO START', True, COLORS['text'])
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(text, text_rect)

        elif self.state in ['playing', 'game_over']:
            # Draw apple
            x = self.apple.position[0] * GRID_SIZE
            y = self.apple.position[1] * GRID_SIZE
            pygame.draw.rect(screen, COLORS['apple'], 
                           (x, y, GRID_SIZE-2, GRID_SIZE-2))

            # Draw snake
            for position in self.snake.positions:
                x = position[0] * GRID_SIZE
                y = position[1] * GRID_SIZE
                pygame.draw.rect(screen, COLORS['snake'], 
                               (x, y, GRID_SIZE-2, GRID_SIZE-2))

            # Draw score
            score_text = FONT.render(f'SCORE: {self.snake.score}', 
                                   True, COLORS['text'])
            screen.blit(score_text, (10, 10))

            if self.state == 'game_over':
                text = FONT.render('GAME OVER - PRESS SPACE', True, COLORS['text'])
                text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                screen.blit(text, text_rect)

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        running = game.handle_input()
        game.update()
        game.draw()
        clock.tick(10)  # Fixed speed

    pygame.quit()

if __name__ == '__main__':
    main()
