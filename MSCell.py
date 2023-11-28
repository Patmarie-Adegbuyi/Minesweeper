import pygame
import pygame.freetype

BOMB_TXT = '*'
EMPTY_TXT = ''
FLAG_BLANK = ''
FLAG_UNKNOWN = '?'
FLAG_MINE = 'M'


# TODO: Add more colours for the cells
color_table = {'red':(255, 0, 0, 255), 'empty cell':(250, 250, 250, 255),
               'gray':(150, 150, 150, 255), 'cell cover': (220, 220, 220, 255),
               'outline':(200, 200, 200, 255), 'bold_outline':(50, 50, 50, 255),
               'one-c':(0, 100, 0, 255), 'two-c':(100, 100, 0, 255),
               'three-c': (0, 100, 100, 255), 'four-c': (100, 255, 100, 255),
               'five-c': (255, 100, 100, 255), 'six-c': (255, 255, 100, 255),
               'seven-c': (255, 0, 255, 255), 'eight-c': (100, 255, 255, 255),
               'mine-c': (255, 0, 0, 255)}

class MSCell:


    # Hidden or "hidden" member variables
    _cell_dim = (0,0,0,0)
    _cell_color = color_table['gray']
    _cell_value = EMPTY_TXT
    _cell_flag = FLAG_BLANK
    _is_covered = True
    _in_focus = False
    _font = None


    def __init__(self, back_color, bound, value: int, font):
        self._cell_dim = bound
        self._cell_color = back_color
        self.set_value(value)
        #self._cell_value = value
        self._is_covered = True
        self._in_focus = False
        self._font = font

    #################
    # Getter Methods
    def has_mine(self):
        return self._cell_value == BOMB_TXT

    def get_value(self) -> int:
        if self._cell_value == BOMB_TXT:
            return 9
        elif self._cell_value == EMPTY_TXT:
            return 0
        else:
            return str(self._cell_value)

    # Function to identify if the cell is empty.  
    def is_blank(self):
        return self._cell_value == EMPTY_TXT

    def is_flagged(self):
        return self._cell_flag == FLAG_MINE

    def is_covered(self):
        return self._is_covered

    #########################
    # Setter Methods
    def set_value(self, val: int):
        if val >= 9:
            self._cell_value = BOMB_TXT
        elif val <= 0:
            self._cell_value = EMPTY_TXT
        else:
            # Also needs to change the color of the text in this case.
            self._cell_value = str(val)

    # Turn on/off the indicator that the cell is in focus (mouse is over it)
    def set_in_focus(self, in_focus: bool):
        self._in_focus = in_focus

    # ONLY uncover a cell if it is not flagged as a mine or a potential mine.
    def set_covered(self, covered: bool):
        if self._cell_flag == FLAG_BLANK:
            self._is_covered = covered


    # The shown "sprite" on the top of each cell
    # These are not set but instead toggled between
    def toggle_flag(self):
        if self._cell_flag == FLAG_BLANK:
            self._cell_flag = FLAG_MINE
        elif self._cell_flag == FLAG_MINE:
            self._cell_flag = FLAG_UNKNOWN
        else:
            self._cell_flag = FLAG_BLANK
        return self._cell_flag

    # FUNCTION FOR DRAWING CELL
    def draw_cell(self, screen):
        # Cell format is [cell_color, cell_rect, text, cell_covered, cell_focus]
        border_rect = pygame.Rect(self._cell_dim[0], self._cell_dim[1],
                                  self._cell_dim[2], self._cell_dim[3])
        cell_text = self.get_sprite()
        sprite_color = self.get_sprite_color()
        back_color = self._cell_color

        # Covered cell:
        if self._is_covered == True:
            back_color = color_table['cell cover']

        pygame.draw.rect(screen, back_color, border_rect, 0)

        # Now draw the outline around.  Drawn differently if in focus
        outline_color = color_table['outline']
        if self._in_focus == True:
            outline_color = color_table['bold_outline']

        pygame.draw.rect(screen, outline_color, border_rect, 2)
        assert (pygame.freetype.get_init())

        # Draw the text to the screen
        self._font.render_to(screen, self._cell_dim, cell_text,
                             sprite_color, size=20)

    # TODO: Add helper function to get the sprite color
    # becomes more obvious when you make the child class.
    def get_sprite_color(self):
        if self._is_covered:
            return color_table['red']
        else:
            return color_table['one-c']

    def get_sprite(self):
        if self._is_covered:
            return self._cell_flag
        else:
            return self._cell_value


    def intersect_pt(self, pt) -> bool:
        rect = self._cell_dim
        pt_in_rect: bool = (rect[0] < pt[0])
        pt_in_rect = pt_in_rect and (rect[0] + rect[2] > pt[0])
        pt_in_rect = pt_in_rect and (rect[1] < pt[1])
        pt_in_rect = pt_in_rect and (rect[1] + rect[3] > pt[1])
        return pt_in_rect
