import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
SNAKE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Create the window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_SIZE // 2, WINDOW_SIZE // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.food = None
        self.place_food()

    def get_head_position(self):
        return self.positions[0]

    def place_food(self):
        while True:
            x = random.randint(0, GRID_COUNT - 1) * GRID_SIZE
            y = random.randint(0, GRID_COUNT - 1) * GRID_SIZE
            if (x, y) not in self.positions:
                self.food = (x, y)
                break

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_SIZE),
               (cur[1] + (y * GRID_SIZE)) % WINDOW_SIZE)

        if new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def eat(self):
        if self.get_head_position() == self.food:
            self.length += 1
            self.score += 1
            self.place_food()
            return True
        return False

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color,
                           (p[0], p[1], GRID_SIZE, GRID_SIZE))
        
        # Draw food
        pygame.draw.rect(surface, RED,
                        (self.food[0], self.food[1], GRID_SIZE, GRID_SIZE))

def draw_grid(surface):
    for y in range(0, WINDOW_SIZE, GRID_SIZE):
        for x in range(0, WINDOW_SIZE, GRID_SIZE):
            r = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRAY, r, 1)

def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    surface.blit(text, (10, 10))

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    snake = Snake()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        game_over = False
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            screen.fill(BLACK)
            draw_grid(screen)
            
            if not snake.update():
                game_over = True
            
            snake.eat()
            snake.draw(screen)
            draw_score(screen, snake.score)
        else:
            # Game Over screen
            font = pygame.font.Font(None, 48)
            game_over_text = font.render('Game Over!', True, WHITE)
            score_text = font.render(f'Final Score: {snake.score}', True, WHITE)
            restart_text = font.render('Press SPACE to restart', True, WHITE)
            
            screen.blit(game_over_text, 
                       (WINDOW_SIZE // 2 - game_over_text.get_width() // 2, 
                        WINDOW_SIZE // 2 - 60))
            screen.blit(score_text, 
                       (WINDOW_SIZE // 2 - score_text.get_width() // 2, 
                        WINDOW_SIZE // 2))
            screen.blit(restart_text, 
                       (WINDOW_SIZE // 2 - restart_text.get_width() // 2, 
                        WINDOW_SIZE // 2 + 60))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()