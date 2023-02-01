'''/////////////////////////////////////////////////////////
File name: myplayer.py
File function:

The Blocks Puzzle is a simplified version
of Tetris with a simple set of rules:

The game is played on a rectangular board with fixed
width and height.
A sequence of rectangular blocks must be placed on the
board. The blocks cannot be rotated.
Every block can be placed anywhere on the board as long
as the space is not occupied.
After placing a block, all completed rows and columns
are cleared.

In this file, there is an implementation of an online
algorithm for the Block Puzzle. The algorithm will read
a sequence of blocks, i.e. (w, h)-pairs representing
rectangles, and will place them on the board. Since the
algorithm must be online, the location for each block
must be computed without knowing the following blocks
in the sequence.

Date: 09_03_2021
/////////////////////////////////////////////////////////'''

###########################################################
#                         IMPORTS
###########################################################
from gameboard import *

###########################################################
#                        CONSTANTS
###########################################################

###########################################################
#                          TYPES
###########################################################

###########################################################
#                         CLASSES
###########################################################
class MyPlayer:
    #************************************
    # Private variables
    #************************************

    #************************************
    # Processes and Functions
    #************************************
    '''----------------------------------------------------
    * Name: __init__
    * Function: Init of the class.
    * Parameters: self: Instance of the class.
    *             width: Width of the board.
    *             height: Height of the board.
    *             method: Method the user wants to apply.
    *             Only two methods are available (simple
    *             and expert). Simple method is the
    *             predetermined. Precondition: the method
    *             asked to be implemented must be avaiable,
    *             otherwise the function gives an assertion
    *             error.
    * Return: -
    ----------------------------------------------------'''
    def __init__(self, width, height, method = 'simple'):
        # If the method asked to be implemented is not avaiable, the user cannot play.
        assert method in ['simple', 'expert'], 'The method you want to apply is not available.'
        # The board will be simulated by a board of the class GameBoard (see the
        # gameboard.py file to get more information about the class).
        self._myboard = GameBoard(Shape(width, height))
        # The method to be implemented is the one given.
        self._method = method

    '''----------------------------------------------------
    * Name: __str__
    * Function: Returns the string representation of the
    *           object (the board, in this case). Returns
    *           a human-readable format, which is good
    *           for logging or to display some
    *           information about the object.
    * Parameters: self: Instance of the class.
    * Return: A string.
    ----------------------------------------------------'''
    def __str__(self):
        # Calling the __str__ method from GameBoard class.
        return self._myboard.__str__()

    '''----------------------------------------------------
    * Name: place_block
    * Function: Allocates a block of the shape asked on
    *           the position it must be. Also, if a whole
    *           row or column is full, it clears all
    *           tockens on it.
    * Parameters: self: Instance of the class.
    *             location: Location where the block
    *             must be.
    *             shape: Shape of the block.
    * Return: The board itself.
    ----------------------------------------------------'''
    def place_block(self, location, shape):
        # Calling the put method from the
        # GameBoard class (see the gameboard.py file to
        # get more information). The algorithm is O(w x h), with
        # w the width of the shape given and h its height.
        self._myboard.put(location, shape)

        # If a whole row or column is full we want to clear it.
        # Calling the methods clear_rows and clear_columns
        # from GameBoard class and give them the list of the full rows
        # and columns we need to clear (they can be obtained by the full_rows
        # and full_columns methods from GameBoard class).

        # The clear_rows algorithm is O(r x w), with r the length of the list
        # of full rows given and w the width of the board.
        # The full_rows algorithm is O(h), with h the height of the board.
        self._myboard.clear_rows(self._myboard.full_rows())

        # The clear_columns algorithm is O(c x h), with c the length of the
        # list of full columns given and h the height of the board.
        # The full_columns algorithm is O(w), with w the width of the board.
        self._myboard.clear_columns(self._myboard.full_columns())

        return self

    '''----------------------------------------------------
    * Name: play
    * Function: Given a board and a new block, finds a
    *           location to place the block. The way
    *           it does it depends on the method applied.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape, which
    *                    it means it has positive width
    *                    and height with integer values.
    *                    (this precondition is checked by
    *                    the is_legal method).
    *                    It represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def play(self, block):
        if self._method == 'simple':
            return self._simple(block)
        else:
            return self._expert(block)

    '''----------------------------------------------------
    * Name: is_legal
    * Function: Cheks if the object given is a block with
    *           its properties (if it is a tuple Shape with
    *           width and height). In case the block is a
    *           Shape, the function also checks that its
    *           width and height are positive integers.
    * Parameters: self: Instance of the class.
    *             block: Object we need to check if it
    *             is a block with its properties.
    * Return: True if the object is a tuple Shape
    *         well defined.
    *         False otherwise.
    ----------------------------------------------------'''
    def is_legal(self, block):
        # Checking if block is type Shape
        is_Shape = isinstance(block, Shape)
        # Checking if width and height are integers
        is_Width_Integer = isinstance(block.width, int)
        is_Height_Integer = isinstance(block.height, int)
        are_Integers = is_Width_Integer and is_Height_Integer
        # Checking if width and height are positive.
        is_Width_Positive = block.width > 0
        is_Height_Positive = block.height > 0
        are_Positives = is_Width_Positive and is_Height_Positive

        return are_Integers and are_Positives and is_Shape

    #************************************
    # Private functions
    #************************************
    '''----------------------------------------------------
    * Name: _simple
    * Function: Given a board and a new block, finds a
    *           location to place the block. From all
    *           the possible locations for a block, picks
    *           the one with the lowest row. In case
    *           several locations are possible in the
    *           same row, pick the one with the lowest
    *           column.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _simple(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # The algorithm is O(w x h), with w the width of the board and h its
        # height.
        i = -1
        # We search an empty spot starting from the lower-left corner and ending
        # to the upper-right one.
        while not found_place and i < board_shape.height:
            i += 1
            j = -1
            while not found_place and j < board_shape.width:
                j += 1
                # If we find an empty spot where the block can be placed,
                # we stop searching a place for it an return the location found.
                # The algorithm of the method is_empty (from GameBoard class) is
                # O(w x h), with w the width of the block given and h its height.
                found_place = self._myboard.is_empty(Location(i, j), block)
        return Location(i, j) if found_place else None

    '''----------------------------------------------------
    * Name: _expert
    * Function: Given a board and a new block, finds a
    *           location to place the block. It searches
    *           for the best location using the
    *           _searching_priorizing_columns method.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _expert(self, block):
        # Some methods have been tested; the one selected
        # is the better one. Anyway, they can be tried:
        # return self._simple_into_two_halves(block)
        # return self._simple_into_two_halves_inverted(block)
        # return self._simple_into_four_quarters(block)
        # return self._looking_for_completing_rows_and_columns(block)
        # return self._searching_priorizing_rows(block)
        return self._searching_priorizing_columns(block)

    #************************************
    # Functions I tried to construct
    # for the expert algoithm.
    #************************************
    '''----------------------------------------------------
    * Name: _simple_into_two_halves
    * Function: Given a board and a new block, finds a
    *           location to place the block. It uses the
    *           simple algorithm but dividing the matrix
    *           into two halves and working with each one
    *           separately. - Not useful; there is no
    *           difference.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _simple_into_two_halves(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # The following algorithm is the same used with the simple method but,
        # insted of searching a positiong along the whole matrix, we first
        # look for a position at the lowest half and then at the upper one.
        # I first thought it could make a better optimization of the space,
        # but at the end it allocates the same amount of blocks than the
        # simple algorithm.
        i = -1
        while not found_place and i <= board_shape.height / 2:
            i += 1
            j = -1
            while not found_place and j <= board_shape.width:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)
        while not found_place and i <= board_shape.height:
            i += 1
            j = -1
            while not found_place and j <= board_shape.width:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)

    '''----------------------------------------------------
    * Name: _simple_into_two_halves
    * Function: Given a board and a new block, finds a
    *           location to place the block. It uses the
    *           simple algorithm but dividing the matrix
    *           into two halves and working with each one
    *           separately. For the upper half, it starts
    *           searching for a location from the top.
    *           - Not useful; the difference is rather small.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _simple_into_two_halves_inverted(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # The following algorithm is the same used with the simple method but,
        # insted of searching a positiong along the whole matrix, we first
        # look for a position at the lowest half and then at the upper one but,
        # in difference of the _simple_into_two_halves method, starting by its
        # top. I first thought it could make a better optimization of the space,
        # but at the end it only allocates a few more blocks for some boards
        # than the simple algorithm and, in several cases, the same amount.
        i = -1
        while not found_place and i < board_shape.height / 2:
            i += 1
            j = -1
            while not found_place and j <= board_shape.width:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)
        i = board_shape.height + 1
        while not found_place and i >= int(board_shape.height / 2):
            i -= 1
            j = board_shape.width + 1
            while not found_place and j >= 0:
                j -= 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)

    '''----------------------------------------------------
    * Name: _simple_into_four_quarters
    * Function: Given a board and a new block, finds a
    *           location to place the block. It uses the
    *           simple algorithm but dividing the matrix
    *           into four quarters and working with each one
    *           separately.
    *           - Not useful; it can be even worst.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _simple_into_four_quarters(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # The following algorithm is the same used with the simple method but,
        # insted of searching a positiong along the whole matrix, we first
        # look for a position at the lower-left quarter, then at the lower-right
        # one, then at the upper-left one and, finally, at the upper-right quarter.
        # Again, I first thought it could make a better optimization of the space,
        # but at the end it only allocates a few more blocks for two boards
        # than the simple algorithm and, in the other cases, a much smaller
        # amount.
        i = -1
        while not found_place and i <= board_shape.height / 2:
            i += 1
            j = -1
            while not found_place and j <= board_shape.width / 2:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)
        i = -1
        while not found_place and i <= board_shape.height / 2:
            i += 1
            j = int(board_shape.width / 2) - 1
            while not found_place and j <= board_shape.width:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)
        while not found_place and i <= board_shape.height:
            i += 1
            j = -1
            while not found_place and j <= board_shape.width / 2:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        if found_place:
            return Location(i, j)
        i = int(board_shape.height / 2) - 1
        while not found_place and i <= board_shape.height:
            i += 1
            j = int(board_shape.width / 2) - 1
            while not found_place and j <= board_shape.width:
                j += 1
                found_place = self._myboard.is_empty(Location(i, j), block)
        return Location(i, j) if found_place else None

    '''----------------------------------------------------
    * Name: _searching_priorizing_columns
    * Function: Given a board and a new block, finds a
    *           location to place the block. It searches
    *           for the columns almost full and checks if
    *           the block can be placed on them in order
    *           to complete them and make some new space.
    *           - Useful: it works better for almost all
    *             cases, except one that is the same as
    *             the simple method. It is generally better
    *             than _searching_priorizing_rows.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _searching_priorizing_columns(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # We obtain the total tockens of the board's rows and columns
        # by using the row_counters and column_counters methods from the
        # GameBoard class.
        column_counter = self._myboard.column_counters()
        # We obtain the positions of the rows and columns starting from
        # the ones with more tockens on them.
        column_positions_ordered = sorted(range(len(column_counter)), key=lambda k: column_counter[k])[::-1]

        j = 0 # Index of column_positions_ordered.
        while j < len (column_positions_ordered) and not found_place:
            # Position of the row we are working with.
            i_pos = 0
            # Position of the column we are working with.
            j_pos = column_positions_ordered[j]
            # Width of the board
            i_max = board_shape.width
            # Poisition of the highest row the block can be placed given its
            # dimensions.
            j_max = j_pos + block.height if (j_pos + block.height) <= board_shape.height else board_shape.height
            # For each position possible of the board given the dimensions
            # of the block, we check if it fits.
            while j_pos < j_max and not found_place:
                while i_pos < i_max and not found_place:
                    found_place = self._myboard.is_empty(Location(i_pos, j_pos), block)
                    i_pos += 1
                j_pos += 1
            j += 1
        # Returning the location if the block can be placed somewhere, None otherwise.
        return Location(i_pos -1 , j_pos - 1) if found_place else None

    '''----------------------------------------------------
    * Name: _searching_priorizing_rows
    * Function: Given a board and a new block, finds a
    *           location to place the block. It searches
    *           for the rows almost full and checks if
    *           the block can be placed on them in order
    *           to complete them and make some new space.
    *           - Useful: it works better for almost all
    *             cases, except one that is the same as
    *             the simple method.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _searching_priorizing_rows(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # We obtain the total tockens of the board's rows
        # by using the row_counters method from the GameBoard class.
        row_counter = self._myboard.row_counters()
        # We obtain the positions of the rows starting from
        # the ones with more tockens on them.
        row_positions_ordered = sorted(range(len(row_counter)), key=lambda k: row_counter[k])[::-1]

        i = 0 # Index of row_positions_ordered.
        while i < len(row_positions_ordered) and not found_place:
            # Position of the row we are working with.
            i_pos = row_positions_ordered[i]
            # Position of the column we are working with.
            j_pos = 0
            # Poisition of the highest column the block can be placed given its
            # dimensions.
            i_max = i_pos + block.width if (i_pos + block.width) <= board_shape.width else board_shape.width
            # Height of the board.
            j_max = board_shape.height
            # For each position possible of the board given the dimensions
            # of the block, we check if it fits.
            while i_pos < i_max and not found_place:
                while j_pos < j_max and not found_place:
                    found_place = self._myboard.is_empty(Location(i_pos, j_pos), block)
                    j_pos += 1
                i_pos += 1
            i += 1
        # Returning the location if the block can be placed somewhere, None otherwise.
        return Location(i_pos -1 , j_pos - 1) if found_place else None

    '''----------------------------------------------------
    * Name: _looking_for_completing_rows_and_columns
    * Function: Given a board and a new block, finds a
    *           location to place the block. It searches
    *           for the rows and columns almost full and
    *           checks if the block can be placed on them
    *           in order to complete the row/column and
    *           clear it all to have more space to allocate
    *           new blocks.
    *           - Not useful, it only works better for some
    *             boards; sometimes it can be even worst.
    * Parameters: self: Instance of the class.
    *             block: An object of type Shape. It
    *                    represents a set of united
    *                    tockens that need to be placed.
    * Return: The best location to put the given block.
    ----------------------------------------------------'''
    def _looking_for_completing_rows_and_columns(self, block):
        # Accessing to the board width and height by the get_shape method
        # of the class GameBoard (check on the gameboard.py file the
        # implementation of this method).
        board_shape = self._myboard.get_shape()
        found_place = False # This bolean variable tells if a place
        # to allocate the block has been found or not.
        # We obtain the total tockens of the board's rows and columns
        # by using the row_counters and column_counters methods from the
        # GameBoard class.
        row_counter = self._myboard.row_counters()
        column_counter = self._myboard.column_counters()
        # We obtain the positions of the rows and columns starting from
        # the ones with more tockens on them.
        row_positions_ordered = sorted(range(len(row_counter)), key=lambda k: row_counter[k])#[::-1]
        column_positions_ordered = sorted(range(len(column_counter)), key=lambda k: column_counter[k])#[::-1]

        i = 0 # Index of row_positions_ordered.
        j = 0 # Index of column_positions_ordered.
        while i < len(row_positions_ordered) and not found_place:
            # Position of the row we are working with.
            i_pos = row_positions_ordered[i]
            while j < len(column_positions_ordered) and not found_place:
                # Position of the column we are working with.
                j_pos = column_positions_ordered[j]
                # Poisition of the lowest column the block can be placed given its
                # dimensions.
                i_min = i_pos - block.width if (i_pos - block.width) >= 0 else i_pos
                # Poisition of the highest column the block can be placed given its
                # dimensions.
                i_max = i_pos + block.width if (i_pos + block.width) <= board_shape.width else board_shape.width
                # Poisition of the lowest row the block can be placed given its
                # dimensions.
                j_min = j_pos - block.height if (j_pos - block.height) >= 0 else j_pos
                # Poisition of the highest row the block can be placed given its
                # dimensions.
                j_max = j_pos + block.height if (j_pos + block.height) <= board_shape.height else board_shape.height
                # We start searching from the bottom of the possible spaces
                # ending to the largest position possible.
                i_pos = i_min
                j_pos = j_min
                while i_pos < i_max and not found_place:
                    while j_pos < j_max and not found_place:
                        if i_pos >= 0 and (row_counter[i_pos] + block.width) <= board_shape.width:
                            if j_pos >= 0 and (column_counter[j_pos] + block.height) <= board_shape.height:
                                found_place = self._myboard.is_empty(Location(i_pos, j_pos), block)
                        j_pos += 1
                    i_pos += 1
                j += 1
            i += 1
        # If the block fits somewhere we return its location, None otherwise.
        return Location(i_pos -1 , j_pos - 1) if found_place else None
