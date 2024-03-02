import pygame
import sys
import random
from Cell import Cell

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
NUM_MINES = 40

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

#Initialize game objects
mineClicked = False
font = pygame.font.Font(None, 36)
cells = {}

for y in range(GRID_HEIGHT):
    for x in range(GRID_WIDTH):
        cells[(x, y)] = Cell(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

#chooses specified amount of unique random cells
mines = random.sample(list(cells.keys()), k=NUM_MINES)

#set randomly chosen cells to mines and update their surrounding cells
for pos in mines:
    cells[pos].isMine = True
    for h in range(pos[1] - 1, pos[1] + 2):
        for w in range(pos[0] - 1, pos[0] + 2):
            if (w, h) in cells and not cells[(w, h)].isMine:
                cells[(w, h)].surroundingMines += 1

def revealSurroundings(cell):
    if not cell.displayNum:
        cell.displayNum = True
        if cell.surroundingMines == 0:
            for h in range(cell.pos[1] - 1, cell.pos[1] + 2):
                for w in range(cell.pos[0] - 1, cell.pos[0] + 2):
                    neighbor = cells.get((w, h))
                    print("gets here")
                    if neighbor and not neighbor.displayNum:
                        revealSurroundings(neighbor)
 
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not mineClicked:
            mouse_pos = pygame.mouse.get_pos()
            for cell in cells.values():
                if cell.rect.collidepoint(mouse_pos):
                    #if left click
                    if event.button == 1:
                        if cell.isMine:
                            print("mine clicked")
                            mineClicked = True
                        elif not cell.isFlagged:
                            print(cell.surroundingMines)
                            if cell.surroundingMines == 0:
                                revealSurroundings(cell)
                            cell.displayNum = True
                    elif event.button == 3:
                        if cell.isFlagged:
                            cell.isFlagged = False
                        else:
                            cell.isFlagged = True

    # Fill background
    screen.fill(WHITE)

    # Draw grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell = cells[(x, y)]
            
            if mineClicked and cell.isMine:
                cell.surface.fill(BLACK)
                screen.blit(cell.surface, cell.rect)

            if cell.isFlagged:
                cell.surface.fill(RED)
                screen.blit(cell.surface, cell.rect)
                
            else:
                pygame.draw.rect(screen, GRAY, cell.rect, 1)
                if cell.displayNum:
                    cell.surface.fill(DARK_GRAY)
                    screen.blit(cell.surface, cell.rect)
                    if cell.surroundingMines > 0:
                        num_surface = font.render(str(cell.surroundingMines), True, WHITE)
                        screen.blit(cell.surface, cell.rect)
                        screen.blit(num_surface, cell.rect)
                    

    # Update display
    pygame.display.flip()