import pygame
import pygame.freetype
import random

# Used to render text to the screen
FONT_NAME = pygame.freetype.get_default_font()
TEXT_FONT = None
BOMB_TXT = '*'
EMPTY_TXT = '--'

# the colour lookup dictionary
color_table = {'red': (255, 0, 0, 255),
               'empty cell': (250, 250, 250, 255),
               'gray': (150, 150, 150, 255),
               'cell cover': (150, 150, 150, 255),
               'outline': (200, 200, 200, 255),
               'one-c': (0, 150, 0, 255),
               'two-c': (150, 150, 0, 255),
               'three-c': (100, 100, 255, 255),
               'four-c': (100, 255, 100, 255)}


# Randomly choose locations where mines will be placed.
def assign_mines(grid, num_mines):
    random.seed()  # sets up random number generator
    mines_made = 0
    while mines_made < num_mines:
        # means rand_col is some whole number between 0 and the length of row 0 (grid is a list of rows).  The 1 indicates the distance between each number
        rand_row = random.randrange(0, len(grid), 1)
        rand_col = random.randrange(0, len(grid[0]), 1)

        # if we don't have a mine, then mines_made+1, and we add the mine to grid
        if not has_mine(grid, rand_row, rand_col):
            mines_made += 1
            cell = grid[rand_row][rand_col]
            cell[2] = BOMB_TXT  # looking at entire row and putting a bomb/mine inside ONE of them
    return mines_made


# Helper function: Determines if a cell at a given row and column has a mine
# This function also handles cases when the row and column are invalid values
def has_mine(grid, row_idx, col_idx):
    if row_idx < 0 or col_idx < 0 or row_idx >= len(grid) or col_idx >= len(grid[row_idx]):
        return False
    else:
        cell = grid[row_idx][col_idx]
        return cell[2] == BOMB_TXT


# Helper function: Update the mine count for a PARTICULAR cell
# and change the value stored in that cell in the end.  Return the count value
def update_cell_count(grid, row_idx, col_idx):
    cell = grid[row_idx][col_idx]
    mine_count = 0

    for row_offset in range(-1, 2):  # surroundings of row
        for col_offset in range(-1, 2):  # surroundings of columns
            if row_offset != 0 or col_offset != 0:
                # if the cell has a mine next to it or behind it, mine_count+1
                if has_mine(grid, row_idx + row_offset, col_idx + col_offset):
                    mine_count += 1
    if mine_count == 0:
        cell[2] = EMPTY_TXT
    else:
        cell[2] = str(mine_count)
    return mine_count


# I made a has_mine function to simplify logic
# then asked all 8 cells surrounding each cell whether they had a bomb.  Invalid row and
# column positions were handled by the has_mine function.
# Made a function for testing each individual cell as well.
def assign_cell_values(grid):
    # for each row and column in the grid, if it doesn't have a mine, update cell count
    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[row_idx])):
            if not has_mine(grid, row_idx, col_idx):
                update_cell_count(grid, row_idx, col_idx)


# drawing the grid to the screen
# Helper function for printing out the entire grid
def print_grid_values(grid):
    for row in grid:
        row_text = ''
        for cell in row:
            row_text += cell[2]
        print(row_text)


# FUNCTION FOR DRAWING CELL
def draw_cell(screen, cell):
    cell_dim = cell[1]
    border_rect = pygame.Rect(cell_dim[0], cell_dim[1],cell_dim[2], cell_dim[3])
    back_colour = cell[0]
    pygame.draw.rect(screen, back_colour, border_rect, 0)

    # drawing the outline of the cells
    outline_colour = color_table['outline']
    pygame.draw.rect(screen, outline_colour, border_rect, 2)

    # Finally you would draw the value for the cell
    if(cell[2] != EMPTY_TXT): # is the cell empty
       TEXT_FONT.render_to(screen, cell_dim, cell[2], color_table['one-c'], size=20)


# Paint the outline of the shapes and the grid outline.
# This handles ALL drawing tasks in the program.
def draw_game(screen, gridrect, border_width, border_height, grid):
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the main game frame
    # Should be drawing a single HUGE gray rect
    border_rect = pygame.Rect(0, 0,
                              gridrect.width + (border_width * 2),
                              gridrect.height + (border_height * 2))
    pygame.draw.rect(screen, (150, 150, 150, 255), border_rect, 0)

    pygame.draw.rect(screen, (150, 150, 255, 255), gridrect, 0)

    # draw cells one by one using nested for loops
    for row in grid:
        for cell in row:
            draw_cell(screen, cell)

    # Needed for all times you draw.
    pygame.display.flip()


# Returns true if the game continues and false if quitting.
# We will change this soon enough when we do object oriented programming
def handleUIEvent(event) -> bool:
    if event.type == pygame.QUIT:
        game_running = False
        return False
    else:
        return True


# This sets up the game board (depending on the gamesize variable)
# and sets up how to run the game by looping through paint and user interface (UI)
# handling events.
def main(gamesize):
    # New addition
    pygame.init()
    pygame.freetype.init()

    print(FONT_NAME)
    global TEXT_FONT
    TEXT_FONT = pygame.freetype.SysFont(FONT_NAME, 0)

    # Set up the game variables
    cellWidth = 20
    border_width = 50
    border_height = 50

    # The starting point of the grid pattern.
    grid_start_x = border_width // 2
    grid_start_y = border_height // 2
    num_mines = 0
    if gamesize == "small":
        gridWidth = 10
        gridHeight = 10
        num_mines = 5
    elif gamesize == "medium":
        gridWidth = 20
        gridHeight = 20
        num_mines = 20
    else:
        gridWidth = 40
        gridHeight = 40
        num_mines = 100

    window_width = (gridWidth * cellWidth) + border_width
    window_height = (gridHeight * cellWidth) + border_height
    screen = pygame.display.set_mode([window_width, window_height])

    # way to make a rectangle.  Can access these variables with grid_rect.x etc.
    grid_rect = pygame.Rect(grid_start_x, grid_start_y,
                            (gridWidth * cellWidth),
                            (gridHeight * cellWidth))

    # Finally indicate the game is ready to run.
    game_running = True
    grid = []
    # generate the grid
    for row in range(gridHeight):
        row_cells = []
        for col in range(gridWidth):
            cell_color = color_table['empty cell']
            cell_rect = (grid_rect.x + col * cellWidth,
                         grid_rect.y + row * cellWidth,
                         cellWidth, cellWidth)
            # Make the cell's rectangle data
            cell = [cell_color, cell_rect, EMPTY_TXT]
            row_cells.append(cell)
        grid.append(row_cells)

    # Randomly assign mines to various cells
    num_mines = assign_mines(grid, num_mines)
    assign_cell_values(grid)
    print_grid_values(grid)

    while game_running:
        for event in pygame.event.get():
            # Throwing all events at the MVC_Canvas class
            game_running = handleUIEvent(event)
            draw_game(screen, grid_rect, border_width, border_height, grid)

    pygame.freetype.quit()
    pygame.quit()


# End of main

# ----------Code to start everything---------------
main("medium")
