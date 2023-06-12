import pygame
import random

GRID_SIZE = 32
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
CROSS = [(GRID_SIZE // 2 - 2 + x, GRID_SIZE // 2) for x in range(5)] + [(GRID_SIZE // 2, GRID_SIZE // 2 - 2 + y) for y in range(5)]
START_POINTS = [(0, GRID_SIZE // 2), (GRID_SIZE // 2, 0), (GRID_SIZE - 1, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE - 1)]
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Block:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

score = 0

def check_and_change(grid):
    global score
    for y in range(len(grid) - 1):
        for x in range(len(grid[0]) - 1):
            if (grid[y][x] == grid[y][x + 1] == grid[y + 1][x] == grid[y + 1][x + 1] and
                grid[y][x] is not None and grid[y][x] != (255, 255, 0)):
                grid[y][x] = grid[y][x + 1] = grid[y + 1][x] = grid[y + 1][x + 1] = (255, 255, 0)
                score += 10
    return grid

def draw_grid(grid, screen):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = grid[y][x]
            if color is not None:
                pygame.draw.rect(screen, color, pygame.Rect(x * 25, y * 25, 25, 25))

def draw_block(block, screen):
    pygame.draw.rect(screen, block.color, pygame.Rect(block.x * 25, block.y * 25, 25, 25))

def handle_input(block, fast_fall, pause):
    global score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = not pause
            if not pause: 
                if event.key == pygame.K_LEFT:
                    block.x -= 1 if block.direction in [(0, 1), (0, -1)] else 0
                    block.y -= 1 if block.direction in [(1, 0), (-1, 0)] else 0
                elif event.key == pygame.K_RIGHT:
                    block.x += 1 if block.direction in [(0, 1), (0, -1)] else 0
                    block.y += 1 if block.direction in [(1, 0), (-1, 0)] else 0
                elif event.key == pygame.K_SPACE:
                    fast_fall = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False

    return fast_fall, pause


def update_block_position(block, grid, fast_fall, SPEED):
    if fast_fall and (0 <= block.x + block.direction[0] < GRID_SIZE and 0 <= block.y + block.direction[1] < GRID_SIZE and grid[int(block.y + block.direction[1])][int(block.x + block.direction[0])] is None):
        block.x += block.direction[0] * SPEED * 10
        block.y += block.direction[1] * SPEED * 10
    elif (0 <= block.x + block.direction[0] < GRID_SIZE and 0 <= block.y + block.direction[1] < GRID_SIZE and grid[int(block.y + block.direction[1])][int(block.x + block.direction[0])] is None):
        block.x += block.direction[0] * SPEED
        block.y += block.direction[1] * SPEED
    else:
        fast_fall = False
        if 0 <= block.x < GRID_SIZE and 0 <= block.y < GRID_SIZE and grid[int(block.y)][int(block.x)] is None:
            grid[int(block.y)][int(block.x)] = block.color
        grid = check_and_change(grid)
        start_point = random.choice(START_POINTS)
        direction = DIRECTIONS[START_POINTS.index(start_point)]
        block = Block(*start_point, random.choice(COLORS), direction)
        
        # Check if any blocks are one grid space from the edge
        for y in range(GRID_SIZE):
            if grid[y][0] is not None or grid[y][GRID_SIZE - 1] is not None:
                return True, block, grid
        
        for x in range(GRID_SIZE):
            if grid[0][x] is not None or grid[GRID_SIZE - 1][x] is not None:
                return True, block, grid
        
        # Check if any blocks have come to rest one grid space from any edge
        for y in range(1, GRID_SIZE - 1):
            if grid[y][1] is not None or grid[y][GRID_SIZE - 2] is not None:
                return True, block, grid
        
        for x in range(1, GRID_SIZE - 1):
            if grid[1][x] is not None or grid[GRID_SIZE - 2][x] is not None:
                return True, block, grid
        
    return fast_fall, block, grid

def display_game_over(screen):
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(GRID_SIZE * 12.5, GRID_SIZE * 12.5))
    screen.blit(game_over_text, text_rect)

def main():
    pygame.init()
    WINDOW_SIZE = [800, 800]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for x, y in CROSS:
        grid[y][x] = (125, 125, 125)

    start_point = random.choice(START_POINTS)
    direction = DIRECTIONS[START_POINTS.index(start_point)]
    block = Block(*start_point, random.choice(COLORS), direction)

    SPEED = GRID_SIZE / (8 * 60)

    running = True
    fast_fall = False

    pause = False
    game_over = False
    while running:
        fast_fall, pause = handle_input(block, fast_fall, pause)
        
        if not pause:
            screen.fill((0, 0, 0))
            draw_grid(grid, screen)
            draw_block(block, screen)
        
            if not game_over:
                fast_fall, block, grid = update_block_position(block, grid, fast_fall, SPEED)
            
            if game_over:
                display_game_over(screen)
        
            # Display the score in the upper right corner of the grid
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(score), True, (255, 255, 255))
            screen.blit(score_text, (650, 10))

        pygame.display.flip()
        clock.tick(60)

        if not game_over:
            for y in range(GRID_SIZE):
                if grid[y][0] is not None:
                    grid[y][0] = None
                if grid[y][GRID_SIZE - 1] is not None:
                    grid[y][GRID_SIZE - 1] = None
            
            for x in range(GRID_SIZE):
                if grid[0][x] is not None:
                    grid[0][x] = None
                if grid[GRID_SIZE - 1][x] is not None:
                    grid[GRID_SIZE - 1][x] = None
        
        # Check if any blocks are one grid space from the edge
        for y in range(GRID_SIZE):
            if grid[y][0] is not None or grid[y][GRID_SIZE - 1] is not None:
                game_over = True
                break
        
        if game_over:
            continue
        
        for x in range(GRID_SIZE):
            if grid[0][x] is not None or grid[GRID_SIZE - 1][x] is not None:
                game_over = True
                break

        if game_over:
            continue

        # Check if any blocks have come to rest one grid space from any edge
        for y in range(1, GRID_SIZE - 1):
            if grid[y][1] is not None or grid[y][GRID_SIZE - 2] is not None:
                game_over = True
                break
        
        if game_over:
            continue
        
        for x in range(1, GRID_SIZE - 1):
            if grid[1][x] is not None or grid[GRID_SIZE - 2][x] is not None:
                game_over = True
                break

        if game_over:
            continue

    pygame.quit()

if __name__ == '__main__':
    main()
