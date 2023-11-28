##################################################
## Class to control the game, game state and events
import pygame
import pygame.freetype
import random
import string
import time
import MSCell as Cell
import MSUberCell as UCell

# Used to render text to the screen
FONT_NAME = pygame.freetype.get_default_font()
focus_cell = None
TEXT_FONT = None

MS_WIN = "You Won"
MS_LOSE = "You Lost"
MS_IN_PROGRESS = 'In Progress'

class MSGame:
    GAME_STATE = {MS_WIN, MS_LOSE, MS_IN_PROGRESS}

    # Member variables
    _grid = None
    _cell_width = 20
    _border_width = 0
    _border_height = 0
    _grid_width = 0
    _grid_height = 0
    _focus_cell = None

    _total_mines = 1
    _mines_remaining = 1
    _non_mine_cells = 1

    _start_time = 0
    _game_size = "medium"
    _player_name = "ABC"
    _elapsed_time = 0

    # This is the drawing surface/screen the game is displayed on
    _screen = None

    _game_running = False
    _game_interactive = True

    def __init__(self, gamesize):
        print(FONT_NAME)
        global TEXT_FONT
        TEXT_FONT = pygame.freetype.SysFont(FONT_NAME, 0)

        # Set up the game variables
        self._cell_width = 20
        self._border_width = 50
        self._border_height = 50

        self._start_time = time.time()
        self._game_size = gamesize
        self._player_name = self.generate_player_name()

        # The starting point of the grid pattern.
        grid_start_x = self._border_width // 2
        grid_start_y = self._border_height // 2
        num_mines = 0
        if gamesize == "small":
            self._grid_width = 10
            self._grid_height = 10
            num_mines = 10
        elif gamesize == "medium":
            self._grid_width = 20
            self._grid_height = 20
            num_mines = 50
        else:
            self._grid_width = 40
            self._grid_height = 40
            num_mines = 100

        self._total_mines = num_mines
        self._non_mine_cells = (self._grid_width * self._grid_height) - num_mines
        self._mines_remaining = num_mines

        window_width = (self._grid_width * self._cell_width) + self._border_width
        window_height = (self._grid_height * self._cell_width) + self._border_height
        self._screen = pygame.display.set_mode([window_width, window_height])

        # Given way to make a rectangle.  Can access these variables with grid_rect.x etc.
        self._grid_rect = pygame.Rect(grid_start_x, grid_start_y,
                                      (self._grid_width * self._cell_width),
                                      (self._grid_height * self._cell_width))

        # Finally indicate the game is ready to run.
        self._game_running = True

        # generate the grid
        self._grid = []
        for row in range(self._grid_height):
            row_cells = []
            for col in range(self._grid_width):
                cell_color = Cell.color_table['empty cell']
                cell_rect = (self._grid_rect.x + col * self._cell_width,
                             self._grid_rect.y + row * self._cell_width,
                             self._cell_width, self._cell_width)
                cell_covered = True
                cell_focus = False
                # Make the cell's rectangle data
                # TODO: Make a change to use the child class instead.
                cell = None
                if ((row+col) % 2) == 0:
                    cell = Cell.MSCell(cell_color, cell_rect, 0, TEXT_FONT)
                else:
                    cell = UCell.MSUberCell(cell_color, cell_rect, 0, TEXT_FONT)
                row_cells.append(cell)
            self._grid.append(row_cells)

        # TODO LAB 2:  Randomly assign mines to various cells
        # num_read = read_mines2("mine_location_in2.txt", grid)
        # if num_read == 0:
        num_mines = self.assign_mines(num_mines)
        self.assign_cell_values()
        self._focus_cell = None
    # end of MSGame __init__


    # Public Getter method to see if the game is still running
    def is_game_running(self):
        return self._game_running

    def get_game_size(self):
        return self._game_size

    # will generate a player name - 3 random uppercase letters
    def generate_player_name(self):
        return ''.join(random.choices(string.ascii_uppercase, k=3))

    def get_player_name(self):
        return self._player_name

    def update_mine_count(self):
        num_flags = 0
        num_blanks = 0
        for row in self._grid:
            for cell in row:
                if(cell.is_flagged()):
                    num_flags += 1
                if (not cell.has_mine()) and cell.is_covered():
                    num_blanks += 1
        self._mines_remaining = max(self._total_mines - num_flags, 0)
        self._non_mine_cells = num_blanks

        # If all non-mine cells are clicked, then you win the game.
        if self._non_mine_cells <= 0:
            self._game_interactive = False


    def get_game_state(self):
        if self._non_mine_cells <= 0:
            return MS_WIN
        elif not self._game_interactive:
            return MS_LOSE
        else:
            return MS_IN_PROGRESS

    # Randomly choose locations where mines will be placed.
    def assign_mines(self, num_mines):
        random.seed()
        mines_made = 0
        while mines_made < num_mines:
            rand_row = random.randrange(0, self._grid_height, 1)
            rand_col = random.randrange(0, self._grid_width, 1)

            if not self.has_mine(rand_row, rand_col):
                mines_made += 1
                cell: Cell.MSCell = self._grid[rand_row][rand_col]
                cell.set_value(9) # 9 would mean a mine since 9 can NEVER be a legitimate value
                #cell[2] = BOMB_TXT
        return mines_made

    # Helper function: Determines if a cell at a given row and column has a mine
    # This function also handles cases when the row and column are invalid values
    def has_mine(self, row_idx, col_idx):
        if row_idx < 0 or col_idx < 0 or row_idx >= self._grid_width or col_idx >= self._grid_height:
            return False
        else:
            cell: Cell.MSCell = self._grid[row_idx][col_idx]
            return cell.has_mine()#[2] == BOMB_TXT


    # Helper function: Update the mine count for a PARTICULAR cell
    # and change the value stored in that cell in the end.  Return the count value
    def update_cell_count(self, row_idx, col_idx):
        cell: Cell.MSCell = self._grid[row_idx][col_idx]
        assert(not cell.has_mine())#cell[2] is not BOMB_TXT)
        assert(row_idx >= 0 and row_idx < self._grid_width)
        mine_count = 0
        for row_off in range(-1, 2):
            for col_off in range(-1, 2):
                if row_off != 0 or col_off != 0:
                    if self.has_mine(row_idx + row_off, col_idx + col_off):
                        mine_count += 1
        if mine_count == 0:
            cell.set_value(mine_count)
        else:
            cell.set_value(mine_count)
        return mine_count
   
    # ask all 8 cells surrounding each cell whether they have a bomb.  Invalid row and
    # column positions are handled by the has_mine function.
    # Made a function for testing each individual cell as well.
    def assign_cell_values(self):
        for row_idx in range(self._grid_height):
            for col_idx in range(self._grid_width):
                cell = self._grid[row_idx][col_idx]
                if not cell.has_mine():
                    self.update_cell_count(row_idx, col_idx)

    def find_cell_pos(self, cell: Cell.MSCell) -> tuple:
        for row_pair in enumerate(self._grid):
            for cell_pair in enumerate(row_pair[1]):
                if cell == cell_pair[1]:
                    return (row_pair[0], cell_pair[0])


    # HELPER FUNCTION: will take each element in list to_reveal
    # and reveal the cell at the position (a pair of values)
    # If that cell is blank then add adjacent cells to to_reveal
    # Remove the first element of to_reveal
    def uncover_cells(self, to_reveal: list):
        assert(len(to_reveal) > 0)
        cell_pos: tuple = to_reveal[0]
        curr_row = cell_pos[0]
        curr_col = cell_pos[1]
        current_cell: Cell.MSCell = self._grid[curr_row][curr_col]

        # Reveal the cell AND remove it from the list
        current_cell.set_covered(False)
        to_reveal.pop(0)

        if current_cell.has_mine():
            self._game_interactive = False

        elif current_cell.is_blank():
            # Add all adjacent covered cells to the list
            min_row = max(0, curr_row -1)
            max_row = min(self._grid_height, curr_row + 2)
            min_col = max(0, curr_col -1)
            max_col = min(self._grid_width, curr_col + 2)
            for i_row in range(min_row, max_row):
                for j_col in range(min_col, max_col):
                    to_add_pos = (i_row, j_col)
                    cell_toadd: Cell.MSCell = self._grid[i_row][j_col]
                    if cell_toadd.is_covered() and (to_add_pos not in to_reveal):
                        to_reveal.append(to_add_pos)


    # FUNCTION: When you click a cell to reveal what is underneath
    # any cell that is blank should reveal all adjacent cells to it.
    # Each of those adjacent cells may also reveal other cells.  So I make a
    # list of cells to show and add to the list for each blank cell.  This shows
    # all connected blank cells.
    def reveal_cell(self, cell: Cell.MSCell):
        cell_pos = self.find_cell_pos(cell)
        reveal_indexes = [cell_pos]
        reveal_count = 0
        while len(reveal_indexes) > 0:
            self.uncover_cells(reveal_indexes)
            reveal_count += 1
            #print("Reveal list:", reveal_indexes)
            #Emergency stop when trying this out
            if(reveal_count > self._grid_height * self._grid_width):
                return reveal_count
        return reveal_count

    # Helper function for printing out the entire grid
    def print_grid_values(self):
        for row in self._grid:
            row_text = ''
            for cell in row:
                row_text += cell.get_value()
            print(row_text)


    # Paint the outline of the shapes and the grid outline.
    # This handles ALL drawing tasks in the program.
    def draw_game(self):
        gridrect = self._grid_rect
        border_width = self._border_width
        border_height = self._border_height
        grid = self._grid
        screen = self._screen

        # Fill the screen with white
        screen.fill((255, 255, 255))

        # TODO
        # Keep for earlier versions of the project
        # Draw the main game frame
        # Should be drawing a single HUGE gray rect
        border_rect = pygame.Rect(0, 0,
                                 gridrect.width + (border_width * 2),
                                 gridrect.height + (border_height * 2))
        pygame.draw.rect(screen, (150, 150, 150, 255), border_rect, 0)

        pygame.draw.rect(screen, (150, 150, 255, 255), gridrect, 0)

        # Draw the grid
        for row in grid:
            for cell in row:
                cell.draw_cell(screen)

        # Displays mines remaining
        mine_text = f"Mines Left: {self._mines_remaining}"
        TEXT_FONT.render_to(self._screen, (10, 10), mine_text, (0, 0, 0), size=15)

        game_state_text = f"State: {self.get_game_state()}"
        TEXT_FONT.render_to(self._screen, (240, 10), game_state_text, (0, 0, 0), size=15)

        self._elapsed_time = int(time.time() - self._start_time)
        time_text = f"Time: {self._elapsed_time}s"
        TEXT_FONT.render_to(self._screen, (10, 40), time_text, (0, 0, 0), size=15)

        pygame.display.flip()


    # Helper function to detect what cell the mouse is over.  Return a reference to the cell
    # being moved over.
    def current_mouse_cell(self, event):
        assert(event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP)
        mouse_pos = pygame.mouse.get_pos()
        # cells have the format [cell_color, cell_rect, EMPTY_TXT, cell_covered, cell_focus]
        for row in self._grid:
            for cell in row:
                if cell.intersect_pt(mouse_pos):
                    return cell
        return None

    def store_top_times(self):
        top_times = {}
        try:
            with open('top_times.text', 'r') as file:
                for line in file:
                    time_won, grid_size, player = line.strip().split(',')
                    if grid_size not in top_times:
                        top_times[grid_size] = []
                    top_times[grid_size].append((int(time), player))
        except FileNotFoundError:
            pass

        curr_grid_size = self.get_game_size()
        if curr_grid_size not in top_times:
            top_times[curr_grid_size] = []
        top_times[curr_grid_size].append((self._elapsed_time, self.get_player_name()))

        for grid_size, times in top_times.items():
            top_times[grid_size] = sorted(times)[:10]

        with open('top_times.txt', 'w') as file:
            for grid_size, times in top_times.items():
                for time_won, player in time_won:
                    file.write(f"{time_won}, {grid_size}, {player}\n")



    # Returns true if the game continues and false if quitting.
    # We will change this soon enough when we do object oriented programming
    def handleUIEvent(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            # Handle case of mouse-over (need to update current and previous cells.
            # Need to make grid global (unfortunately)
            if self._game_interactive:
                curr_focus_cell = self.current_mouse_cell(event)
                if curr_focus_cell is not self._focus_cell:
                    if curr_focus_cell is not None:
                        curr_focus_cell.set_in_focus(True)

                    if self._focus_cell is not None:
                        self._focus_cell.set_in_focus(False)
                    self._focus_cell = curr_focus_cell
            return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self._game_interactive:
                curr_focus_cell = self.current_mouse_cell(event)
                if curr_focus_cell is not None:
                    if event.button == pygame.BUTTON_RIGHT:
                        # toggle the user flagging of the cell
                        curr_focus_cell.toggle_flag()
                    # Click the cell to reveal underneath
                    elif event.button == pygame.BUTTON_LEFT:
                        # Reveal the cell (easy for now)
                        self.reveal_cell(curr_focus_cell)
                        #curr_focus_cell.set_covered(False)

            # In all cases, we should re-draw the grid
            # after checking the number of bombs remaining
            self.update_mine_count()

            if self.get_game_state() == MS_WIN:
                self.store_top_times()

            return True
        elif event.type == pygame.QUIT:
            self._game_running = False
            return False

        else:
            return True
# End of MSGame class
