'''/////////////////////////////////////////////////////////
File name: gameboard.py
File function: A board can be represented as a grid with
height h (number of rows) and width w (number of  columns).
The rows and columns are numbered from 0 to h−1 and from
0 to w−1, respectively. We will often refer to a w×h-board
as a board with width w and height h. Each square is
identified by a (row,column)-pair. The lower-left corner
of the board corresponds to square (0,0).
A class for the board is implemented in a way that exactly
the interface used in the Board notebook is available.
Date: 06_03_2021
/////////////////////////////////////////////////////////'''

###########################################################
#                         IMPORTS
###########################################################
# Library collections is needed to define Location and Shape tuples.
import collections

###########################################################
#                        CONSTANTS
###########################################################

###########################################################
#                          TYPES
###########################################################
# Tuple Location contains the coordenates of an exact position of the board.
Location = collections.namedtuple('Location', 'row column')
# Tuple Shape contains how high and wide is an object defined by this tuple.
Shape = collections.namedtuple('Shape', 'width height')

###########################################################
#                         CLASSES
###########################################################
class GameBoard:
    #************************************
    # Private constants
    #************************************
    _EMPTY = '\u2b1c' # Chain of characters that simulates a white square.
    _FULL  = '\u2b1b' # Chain of characters that simulates a black square.

    # In case that the squares aren't clearly visible in the terminal, this
    # other definition can be used:

    # _EMPTY = '0' # Equivalent to '\u2b1c' (an empty square).
    # _FULL  = '1' # Equivalent to '\u2b1b' (an occupied square).

    #************************************
    # Processes and Functions
    #************************************

    '''----------------------------------------------------
    * Name: __init__
    * Function: Init of the class.
    * Parameters: self: Instance of the class.
    *             shape: Shape of the board.
    * Return: -
    ----------------------------------------------------'''
    def __init__(self, shape):
        # The board shape will be the one given by the user
        # (wich is a tuple Shape).
        self._shape = shape
        # The board will be simulated by a matrix of size (width x height)
        # given by the tuple Shape. The matrix is initialized with empty
        # squares on all positions.
        self._board = [[self._EMPTY for x in range(self._shape.width)]
                        for y in range(self._shape.height)]

    '''----------------------------------------------------
    * Name: __str__
    * Function: Returns the string representation of the
    *           object (the board, in this case). Returns
    *           a human-readable format, which is good
    *           for logging or to display some
    *           information about the object.
    * Parameters: self: Instance of the class.
    * Return: A string that simulates the current status
    *         of the board.
    ----------------------------------------------------'''
    def __str__(self):
        chain = '' # This string will simulate the status of the board.
        # Starting from the upper-left corner and ending to the
        # lowest-right one, we want to print all the squares
        # of the board. So, before, we need to print the
        # highest rows. The algorithm is O(w x h), with w the
        # width of the board and h its height.
        for i in range(self._shape.height - 1, -1, -1):
            for j in range(0, self._shape.width):
                chain += self._board[i][j] # Adding the status of the sqaure.
            # At the end of each row, except the last one, we need to
            # add a line break, to start printing the following one.
            if i != 0: chain += '\n'
        return chain

    '''----------------------------------------------------
    * Name: __repr__
    * Function: Returns the object representation (the
    *           board, in this case) in string format.
    *           Returns an “official” string
    *           representation of the object, which can
    *           be used to construct the object again.
    * Parameters: self: Instance of the class.
    * Return: A string that gives to the user the exact
    *         position of the tockens on the board at
    *         the moment.
    ----------------------------------------------------'''
    def __repr__(self):
        # The string chain will be the one that gives the information wanted.
        # The first things it gives to the user are the dimensions of the board.
        chain = str(self._shape.width) + 'x' + str(self._shape.height) + ' board: {'
        initialized = False # This bolean variable is useful to check
        # if the chain already has, at least one, location; can
        # help with not having extra comas when printing the whole string.
        # Starting from the upper-left corner and ending to
        # the lowest-right one, if the square we are checking
        # at that moment is occupied, we add its coordenates
        # to the chain.
        # The algorithm is O(w x h), with w the width of the
        # board and h its height.
        for i in range(self._shape.height - 1, -1, -1):
            for j in range(0, self._shape.width):
                if self.is_full(Location(i,j)): # The is_full method is O(w x h),
                # with w the width of the shape given and h its height. So, as
                # we don't specify any shape, it will be Shape(1 x 1) and
                # the algorithm will be O (1 x 1).
                    if initialized:
                        chain += ', ' # We add a coma if we are going to add
                        # a location after another one.
                    chain += '(' + str(i) + ', ' + str(j) + ')'
                    initialized = True # Once we add a location, then we consider
                    # the chain has been initialized.
        chain += '}'
        return chain

    '''----------------------------------------------------
    * Name: get_shape
    * Function: Gives the shape of the board.
    * Parameters: self: Instance of the class.
    * Return: The shape of the class (the board).
    ----------------------------------------------------'''
    def get_shape(self):
        return self._shape

    '''----------------------------------------------------
    * Name: put
    * Function: Puts tockens on the board on the position/s
    *           that the user asks. Precondition: the
    *           position/s must be empty, otherwise
    *           the function gives an assertion error.
    * Parameters: self: Instance of the class.
    *             location: Coordenates x and y of the
    *                       position where the tocken
    *                       must be put.
    *             shape: Width and height of the blocks
    *                    of tockens that the user wants
    *                    to put on the board. If this
    *                    parameter is not specified,
    *                    the function considers a 1x1
    *                    tocken.
    * Return: The object itself (the board with the new
    *         tockens allocated).
    ----------------------------------------------------'''
    def put(self, location, shape = Shape(1, 1)):
        # Having an empty spot where the user wants to put a tocken(s)
        # is essential to keep going with the task.
        assert self.is_empty(location, shape), 'The locations you are trying to access are already occupied or out of bounds.'
        # If Shape = (1, 1), the algoithm is O(1).
        # Else, the algorithm is O(w x h), with w the width of the shape given
        # and h its height.
        for i in range(location.row, location.row + shape.height):
            for j in range(location.column, location.column + shape.width):
                # Putting a tocken on a location means to adjudicate,
                # to the value of the position, the chain of chars that
                # returns the black square.
                self._board[i][j] = self._FULL
        return self

    '''----------------------------------------------------
    * Name: is_empty
    * Function: Says if the position(s) given by the user
    *           is/are empty or not.
    * Parameters: self: Instance of the class.
    *             location: Coordenates x and y of the
    *                       position the user wants to
    *                       know if it is empty or not.
    *             shape: Width and height of the blocks
    *                    of tockens that the user wants
    *                    to remove from the board. If
    *                    this parameter is not specified
    *                    the function considers a 1x1
    *                    tocken.
    * Return: True if the position is empty.
    *         False otherwise.
    ----------------------------------------------------'''
    def is_empty(self, location, shape = Shape(1, 1)):
        # If Shape = (1, 1), the algoithm is O(1).
        # Else, the algorithm is O(w x h), with w the width of the shape given
        # and h its height.
        for i in range(location.row, location.row + shape.height):
            for j in range(location.column, location.column + shape.width):
                # If the value of i or j is out of the bounds of the board
                # we will consider that the spot is not empty, as out of
                # the board should be impossible to put a tocken.
                # If the spot is full we return it is not empty.
                if i >= self._shape.height or j >= self._shape.width or self._board[i][j] == self._FULL:
                    return False
        # If nothing has been returned yet, we return if the location given
        # is empty or not.
        return self._board[location.row][location.column] == self._EMPTY

    '''----------------------------------------------------
    * Name: is_full
    * Function: Says if the position(s) given by the user
    *           is/are occupied or not.
    * Parameters: self: Instance of the class.
    *             location: Coordenates x and y of the
    *                       position the user wants to
    *                       know if it is occupied or not.
    *             shape: Width and height of the set of
    *                    coordenates the user wants to
    *                    know if they are occupied or not.
    *                    If this parameter is not specified,
    *                    the function considers that
    *                    the user only wants to check
    *                    one only location, so shape is
    *                    1x1.
    * Return: True if the position(s) is/are occupied.
    *         False otherwise.
    ----------------------------------------------------'''
    def is_full(self, location, shape = Shape(1, 1)):
        # If Shape = (1, 1), the algoithm is O(1).
        # Else, the algorithm is O(w x h), with w the width of the shape given
        # and h its height.
        for i in range(location.row, location.row + shape.height):
            for j in range(location.column, location.column + shape.width):
                # If the value of i or j is out of the bounds of the board
                # we will consider that the spot is empty, as out of
                # the board should be impossible to remove a tocken that
                # does not exist.
                # If a spot is empty we return it is not full.
                if i >= self._shape.height or j >= self._shape.width or self._board[i][j] == self._EMPTY:
                    return False
        # If nothing has been returned yet, we return if the location given
        # is full or not.
        return self._board[location.row][location.column] == self._FULL

    '''----------------------------------------------------
    * Name: remove
    * Function: Removes a tocken from the position(s) the
    *           user asks. Precondition: there is/are
    *           tockens to be removed, otherwise it
    *           gives an assertion error.
    * Parameters: self: Instance of the class.
    *             location: Coordenates x and y of the
    *             position which tocken the user wants
    *             to remove.
    *             shape: Width and height of the block
    *                    of tockens that the user wants
    *                    to remove from the board. If
    *                    this parameter is not specified
    *                    the function considers a 1x1
    *                    tocken.
    * Return: The object itself (the board with the
    *         tockens asked removed).
    ----------------------------------------------------'''
    def remove(self, location, shape = Shape(1, 1)):
        # Having an full spot where the user wants to remove a tocken(s)
        # is essential to keep going with the task.
        assert self.is_full(location, shape), 'There are not tockens to be removed on the positions you are asking for.'
        # If Shape = (1, 1), the algoithm is O(1).
        # Else, the algorithm is O(w x h), with w the width of the shape given
        # and h its height.
        for i in range(location.row, location.row + shape.height):
            for j in range(location.column, location.column + shape.width):
                # Removing a tocken from a position means to adjudicate
                # to its value the chain of chars that returns a white square.
                self._board[i][j] = self._EMPTY
        return self

    '''----------------------------------------------------
    * Name: full_rows
    * Function: Looks for the rows with all squares
    *           occupied and gives its list.
    * Parameters: self: Instance of the class.
    * Return: A list of rows with all squares occupied.
    ----------------------------------------------------'''
    def full_rows(self, board = None, height = None, width = None):
        # If the call of full_rows is directly done the board has not been
        # transposed, so the variables take their predetermined values.
        if board is None: board = self._board
        if height is None: height = self._shape.height
        if width is None: width = self._shape.width

        rows = [] # This list will keep the number of the rows with all their
                  # squares occupied.
        # The algorithm is O(h), with h the height of the board.
        for i in range(0, height):
            # Having a full row occupied means having the value of the
            # black square repeated along the entire row. When this happens,
            # we keep in the list the value of the row.
            if board[i] == [self._FULL] * width:
                rows.append(i)
        return rows

    '''----------------------------------------------------
    * Name: full_columns
    * Function: Looks for the columns with all squares
    *           occupied and gives its list by transposing
    *           the board and calling the full_rows function.
    * Parameters: self: Instance of the class.
    * Return: A list of columns with all squares occupied.
    ----------------------------------------------------'''
    def full_columns(self):
        # To create an algorithm with lower runtime than
        # O(w x h), with w the width of the board and h its height,
        # transposing the board to apply a similar algorithm to the one applied
        # in the function full_rows is necessary.
        transposed_board = list(map(list, zip(*self._board)))
        # Then we just need to call the full_rows method with the board transposed.
        # Then, the algorithm will be O(w), with w the width of the board.
        return self.full_rows(transposed_board, self._shape.width, self._shape.height)

    '''----------------------------------------------------
    * Name: clear_rows
    * Function: Removes all tokens present in the rows
    *           that the user gives, regardless they
    *           are full or not. Precondition: the rows
    *           given exist.
    * Parameters: self: Instance of the class.
    *             rows: List of rows the user wants to
    *                   clear.
    * Return: The object itself (the board with all the
    *         squares of the rows given empty).
    ----------------------------------------------------'''
    def clear_rows(self, rows):
        # The algorithm is O(r x w), with r the length of the list of rows
        # given and w the width of the board.
        for i in rows:
            # If the row given is out of bounds we don't need to do anything.
            if i >= self._shape.width: pass
            # For each row, we adjudicate the value of the white square along all
            # its width.
            else:
                for j in range(0, self._shape.width):
                    self._board[i][j] = self._EMPTY
        return self

    '''----------------------------------------------------
    * Name: clear_columns
    * Function: Removes all tokens present in the columns
    *           that the user gives, regardless they
    *           are full or not. Precondition: the columns
    *           given must exist.
    * Parameters: self: Instance of the class.
    *             columns: List of columns the user wants
    *                      to clear.
    * Return: The object itself (the board with all the
    *         squares of the columns given empty).
    ----------------------------------------------------'''
    def clear_columns(self, columns):
        # The algorithm is O(c x h), with c the length of the list of columns
        # given and h the height of the board.
        for j in columns:
            # If the column given is out of bounds we don't need to do anything.
            if j >= self._shape.width: pass
            # For each column, we adjudicate the value of the white square along all
            # its height.
            else:
                for i in range(0, self._shape.height):
                    self._board[i][j] = self._EMPTY
        return self

    '''----------------------------------------------------
    * Name: row_counters
    * Function: Counts how many tockens are in each row
    *           and gives a list with the values.
    * Parameters: self: Instance of the class.
    * Return: A list that says how many tockens has
    *         each row.
    ----------------------------------------------------'''
    def row_counters(self):
        tockens = 0 # This variable will save the number of tockens on one row.
        row_counter = [] # This list will save the number of tockens on each row.
        # The algorithm is O(w x h), with w the width of the board and h its
        # height.
        for i in range (0, self._shape.height):
            for j in range (0, self._shape.width):
                # When we find a position with a black square, we add 1 to the
                # tockens variable.
                if self._board[i][j] == self._FULL:
                    tockens += 1
            # Once we have checked a full row, we save the number of tockens
            # on it in the list row_counter and reset the tockens
            # variable to zero, in order to start checking the following row.
            row_counter.append(tockens)
            tockens = 0
        return row_counter

    '''----------------------------------------------------
    * Name: column_counters
    * Function: Counts how many tockens are in each column
    *           and gives a list with that values.
    * Parameters: self: Instance of the class.
    * Return: A list that says how many tockens has
    *         each column.
    ----------------------------------------------------'''
    def column_counters(self):
        tockens = 0 # This variable will save the number of tockens on one column.
        column_counter = [] # This list will save the number of tockens on each column.
        # The algorithm is O(w x h), with w the width of the board and h its
        # height.
        for j in range (0, self._shape.width):
            for i in range (0, self._shape.height):
                # When we find a position with a black square, we add 1 to the
                # tockens variable.
                if self._board[i][j] == self._FULL:
                    tockens += 1
            # Once we have checked a full column, we save the number of tockens
            # on it in the list column_counter and reset the tockens
            # variable to zero, in order to start checking the following column.
            column_counter.append(tockens)
            tockens = 0
        return column_counter
