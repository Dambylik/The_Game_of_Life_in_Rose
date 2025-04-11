import pygame
import numpy as np
import random

# Rose color palette
COLORS = {
    'background': (25, 0, 15),          # Dark rose background
    'grid': (60, 20, 40),               # Subtle grid lines
    'cell_alive': (255, 105, 180),      # Hot pink for alive cells
    'cell_dying': (219, 112, 147),      # Pale violet red for dying cells
    'cell_born': (255, 182, 193),       # Light pink for newly born cells
    'text': (255, 240, 245)             # Lavender blush for text
}

# Rainbow colors for different figures
RAINBOW_COLORS = [
    (255, 0, 0),      # Red
    (255, 127, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (75, 0, 130),     # Indigo
    (148, 0, 211)     # Violet
]

# Predefined patterns for Game of Life
PATTERNS = {
    'glider': [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    'blinker': [
        [1, 1, 1]
    ],
    'toad': [
        [0, 1, 1, 1],
        [1, 1, 1, 0]
    ],
    'beacon': [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ],
    'pulsar': [
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
    ],
    'pentadecathlon': [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    ],
    'spaceship': [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0]
    ]
}

class GameOfLife:
    def __init__(self, width=800, height=600, cell_size=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        
        # Calculate grid dimensions
        self.cols = width // cell_size
        self.rows = height // cell_size
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game of Life - Rose & Rainbow Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        
        # Initialize grid
        self.grid = np.zeros((self.rows, self.cols))
        self.previous_grid = np.zeros((self.rows, self.cols))
        
        # For cell animation effects
        self.cell_states = np.zeros((self.rows, self.cols))  # 0: dead, 1: alive, 2: dying, 3: born
        
        # For rainbow figures
        self.cell_colors = {}  # Dictionary to store custom colors for cells
        self.rainbow_cycle = 0  # For cycling through rainbow colors
        
    def randomize_grid(self, probability=0.3):
        """Fill the grid with random alive cells based on probability"""
        self.grid = np.random.choice([0, 1], size=(self.rows, self.cols), p=[1-probability, probability])
        self.update_cell_states()
        # Clear any custom colors when randomizing
        self.cell_colors = {}
    
    def place_pattern(self, pattern_name, x, y, use_rainbow=True):
        """Place a predefined pattern at position (x,y) with optional rainbow colors"""
        if pattern_name not in PATTERNS:
            return False
            
        pattern = PATTERNS[pattern_name]
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        
        # Place the pattern on the grid
        for py in range(pattern_height):
            for px in range(pattern_width):
                grid_y = (y + py) % self.rows
                grid_x = (x + px) % self.cols
                
                if pattern[py][px] == 1:
                    self.grid[grid_y, grid_x] = 1
                    
                    # Assign a rainbow color to this cell if requested
                    if use_rainbow:
                        color_index = (px + py) % len(RAINBOW_COLORS)
                        self.cell_colors[(grid_y, grid_x)] = RAINBOW_COLORS[color_index]
        
        self.update_cell_states()
        return True
    
    def place_random_patterns(self, count=3):
        """Place random patterns at random locations with rainbow colors"""
        # Clear the grid first
        self.grid = np.zeros((self.rows, self.cols))
        self.cell_colors = {}
        
        for _ in range(count):
            pattern_name = random.choice(list(PATTERNS.keys()))
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            self.place_pattern(pattern_name, x, y)
        
        self.update_cell_states()
    
    def update_cell_states(self):
        """Update cell states for animation effects"""
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y, x] == 1 and self.previous_grid[y, x] == 0:
                    self.cell_states[y, x] = 3  # Born
                elif self.grid[y, x] == 1:
                    self.cell_states[y, x] = 1  # Alive
                elif self.grid[y, x] == 0 and self.previous_grid[y, x] == 1:
                    self.cell_states[y, x] = 2  # Dying
                else:
                    self.cell_states[y, x] = 0  # Dead
        
    def count_neighbors(self, grid, y, x):
        """Count live neighbors of a cell using toroidal boundary"""
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = (y + dy) % self.rows, (x + dx) % self.cols
                neighbors += grid[ny, nx]
        return neighbors
    
    def update(self):
        """Update grid based on Conway's Game of Life rules"""
        # Save current grid for animation purposes
        self.previous_grid = self.grid.copy()
        
        # Create new grid for the next generation
        next_grid = np.zeros((self.rows, self.cols))
        
        # Apply Game of Life rules
        for y in range(self.rows):
            for x in range(self.cols):
                neighbors = self.count_neighbors(self.grid, y, x)
                
                # Apply Conway's rules
                if self.grid[y, x] == 1:  # Cell is alive
                    if neighbors < 2 or neighbors > 3:
                        next_grid[y, x] = 0  # Dies: under/overpopulation
                    else:
                        next_grid[y, x] = 1  # Survives
                else:  # Cell is dead
                    if neighbors == 3:
                        next_grid[y, x] = 1  # Born: reproduction
        
        self.grid = next_grid
        self.update_cell_states()
    
    def draw(self):
        """Draw the grid on the screen"""
        self.screen.fill(COLORS['background'])
        
        # Draw grid lines
        for y in range(self.rows + 1):
            pygame.draw.line(self.screen, COLORS['grid'], 
                            (0, y * self.cell_size), 
                            (self.width, y * self.cell_size))
        for x in range(self.cols + 1):
            pygame.draw.line(self.screen, COLORS['grid'], 
                            (x * self.cell_size, 0), 
                            (x * self.cell_size, self.height))
        
        # Rainbow cycle effect (slowly shift colors)
        self.rainbow_cycle = (self.rainbow_cycle + 0.05) % len(RAINBOW_COLORS)
        
        # Draw cells
        for y in range(self.rows):
            for x in range(self.cols):
                if self.cell_states[y, x] == 0:  # Dead
                    continue  # Don't draw dead cells
                
                # Determine cell color
                if (y, x) in self.cell_colors:
                    # Use custom rainbow color for this cell
                    color_index = int((self.cell_colors[(y, x)][0] + self.rainbow_cycle) % len(RAINBOW_COLORS))
                    color = RAINBOW_COLORS[color_index]
                elif self.cell_states[y, x] == 1:  # Alive
                    color = COLORS['cell_alive']
                elif self.cell_states[y, x] == 2:  # Dying
                    color = COLORS['cell_dying']
                elif self.cell_states[y, x] == 3:  # Born
                    color = COLORS['cell_born']
                
                rect = pygame.Rect(
                    x * self.cell_size + 1, 
                    y * self.cell_size + 1, 
                    self.cell_size - 1, 
                    self.cell_size - 1
                )
                pygame.draw.rect(self.screen, color, rect)

    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Reset with random state
                if event.key == pygame.K_r:
                    self.randomize_grid()
                # Clear grid
                elif event.key == pygame.K_c:
                    self.grid = np.zeros((self.rows, self.cols))
                    self.cell_colors = {}  # Clear custom colors
                    self.update_cell_states()
                # Quit
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
                # Place random patterns
                elif event.key == pygame.K_p:
                    self.place_random_patterns(count=random.randint(3, 6))
                # Place specific patterns with shortcut keys
                elif event.key == pygame.K_1:
                    x, y = self.cols // 3, self.rows // 3
                    self.place_pattern('glider', x, y)
                elif event.key == pygame.K_2:
                    x, y = self.cols // 3, self.rows // 2
                    self.place_pattern('blinker', x, y)
                elif event.key == pygame.K_3:
                    x, y = self.cols // 2, self.rows // 2
                    self.place_pattern('toad', x, y)
                elif event.key == pygame.K_4:
                    x, y = self.cols // 2, self.rows // 3
                    self.place_pattern('beacon', x, y)
                elif event.key == pygame.K_5:
                    x, y = self.cols // 2, self.rows // 2
                    self.place_pattern('spaceship', x, y)
            
            # Toggle cells with mouse click or place pattern with right click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // self.cell_size, y // self.cell_size
                
                if event.button == 1:  # Left click
                    # Toggle the cell
                    if grid_y < self.rows and grid_x < self.cols:
                        self.grid[grid_y, grid_x] = 1 - self.grid[grid_y, grid_x]
                        self.update_cell_states()
                elif event.button == 3:  # Right click
                    # Place a random pattern at mouse position
                    pattern = random.choice(list(PATTERNS.keys()))
                    self.place_pattern(pattern, grid_x, grid_y)
                    
        return True
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Display instructions
        text_lines = [
            "Controls:",
            "Left-click: Toggle cells",
            "Right-click: Place random pattern",
            "P: Place multiple random patterns",
            "1-5: Place specific patterns",
            "R: Random cell pattern",
            "C: Clear grid",
            "Space: Pause/Resume",
            "Q/ESC: Quit"
        ]
        
        y_offset = 10
        for line in text_lines:
            text_surface = self.font.render(line, True, COLORS['text'])
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 22
            
    def run(self):
        """Main game loop"""
        # Start with random pattern
        self.randomize_grid()
        
        running = True
        paused = False
        
        while running:
            running = self.handle_events()
            
            # Check for pause toggle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                paused = not paused
                pygame.time.wait(200)  # Prevent space from toggling too quickly
            
            if not paused:
                self.update()
                
            self.draw()
            self.draw_ui()
            
            # Display pause status
            if paused:
                pause_text = self.font.render("PAUSED - Space to continue", True, COLORS['text'])
                self.screen.blit(pause_text, (self.width // 2 - 100, 10))
            
            pygame.display.flip()
            self.clock.tick(10)  # Control simulation speed
            
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife(800, 600, 10)
    game.run()
