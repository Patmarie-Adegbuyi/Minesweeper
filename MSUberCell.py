import pygame.draw_py

import MSCell

UFLAG_BLANK = ''
UFLAG_UNKNOWN = '??'
UFLAG_MINE = '!!'

class MSUberCell(MSCell.MSCell):
    _sprite_color = MSCell.color_table['gray']

    def __init__(self, back_color, bound, value: int, font):
        MSCell.MSCell.__init__(self, back_color, bound, value, font)
        self.set_value(value)
        self._cell_flag == UFLAG_BLANK

    #########################
    # Setter Methods
    def set_value(self, val: int):
        MSCell.MSCell.set_value(self, val)

        if val >= 9:
            self._sprite_color = MSCell.color_table['mine-c']
        elif val == 8:
            self._sprite_color = MSCell.color_table['eight-c']
        elif val == 7:
            self._sprite_color = MSCell.color_table['seven-c']
        elif val == 6:
            self._sprite_color = MSCell.color_table['six-c']
        elif val == 5:
            self._sprite_color = MSCell.color_table['five-c']
        elif val == 4:
            self._sprite_color = MSCell.color_table['four-c']
        elif val == 3:
            self._sprite_color = MSCell.color_table['three-c']
        elif val == 2:
            self._sprite_color = MSCell.color_table['two-c']
        elif val == 1:
            self._sprite_color = MSCell.color_table['one-c']
        else:
            self._sprite_color = MSCell.color_table['gray']

    def is_flagged(self):
        return MSCell.MSCell.is_flagged(self) or self._cell_flag == UFLAG_MINE


    # Helper function to get the sprite color
    # becomes more obvious when you make the child class.
    def get_sprite_color(self):
        if self._is_covered:
            if self._cell_flag == UFLAG_BLANK:
                return MSCell.color_table['gray']
            elif self._cell_flag == UFLAG_UNKNOWN:
                return MSCell.color_table['bold_outline']
            else:
                return MSCell.color_table['red']
        else:
            return self._sprite_color


    # The shown "sprite" on the top of each cell
    # These are not set but instead toggled between
    def toggle_flag(self):
        if self._cell_flag == UFLAG_BLANK:
            self._cell_flag = UFLAG_MINE
        elif self._cell_flag == UFLAG_MINE:
            self._cell_flag = UFLAG_UNKNOWN
        else:
            self._cell_flag = UFLAG_BLANK
        return self._cell_flag

    # FUNCTION FOR DRAWING CELL
    def draw_cell(self, screen):
        MSCell.MSCell.draw_cell(self, screen)
        # For uncovered bombs, draw a big X across the cell.
        if self.has_mine() and not self.is_covered():
            bound = self._cell_dim

            up_left = (bound[0], bound[1])
            up_right = (bound[0] + bound[2], bound[1])
            bottom_left = (bound[0], bound[1] + bound[3])
            bottom_right = (bound[0] + bound[2], bound[1] + bound[3])
            # Draw the big X across the entire cell bound.
            pygame.draw_py.draw_line(screen, MSCell.color_table['red'], up_left, bottom_right, 4)
            pygame.draw_py.draw_line(screen, MSCell.color_table['red'], up_right, bottom_left, 4)
