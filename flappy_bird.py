import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
BIRD_JUMP = -5
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Load bird image
bird_image = pygame.image.load('bird.png')

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.image = bird_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Keep bird on screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        
    def jump(self):
        self.velocity = BIRD_JUMP
        
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        
    def get_mask(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.Surface((50, HEIGHT))
        self.PIPE_BOTTOM = pygame.Surface((50, HEIGHT))
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randint(50, 300)
        self.top = self.height - 400
        self.bottom = self.height + PIPE_GAP
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, 50, self.height))
        # Draw bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, 50, HEIGHT - self.bottom))
        
    def collide(self, bird):
        bird_rect = bird.get_mask()
        top_pipe = pygame.Rect(self.x, 0, 50, self.height)
        bottom_pipe = pygame.Rect(self.x, self.bottom, 50, HEIGHT - self.bottom)
        
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe) or bird.y + bird.height >= HEIGHT

# Game class
class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('Arial', 32)
        self.game_over = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.bird.jump()
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()
                    
    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(Pipe())
                self.last_pipe = time_now
                
            # Update pipes and check for collisions
            for pipe in self.pipes:
                pipe.update()
                
                # Check if bird has passed the pipe
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    
                # Check for collisions
                if pipe.collide(self.bird):
                    self.game_over = True
                    
            # Remove pipes that are off screen
            self.pipes = [pipe for pipe in self.pipes if pipe.x > -50]
            
            # Check if bird hits the ground
            if self.bird.y + self.bird.height >= HEIGHT:
                self.game_over = True
                
    def draw(self):
        screen.fill(SKY_BLUE)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()
            
        # Draw bird
        self.bird.draw()
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to restart', True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 16))
            
        pygame.display.update()

# Main game loop
def main():
    game = Game()
    
    while True:
        clock.tick(FPS)
        
        game.handle_events()
        game.update()
        game.draw()

if __name__ == "__main__":
    main()