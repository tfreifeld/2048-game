from random import choice as rand_choice
from random import random


class Board:
    class PositionList:

        def __init__(self, full):
            if full:
                self._positions = [(row, col) for row in range(4) for col in range(4)]
            else:
                self._positions = []

        def update(self, pos):
            self._positions.append(pos)
            self._positions.sort()

        def remove(self, pos):
            self._positions.remove(pos)
            self._positions.sort()

        def get_positions(self):
            return self._positions

        def __contains__(self, position):
            return position in self._positions

    class Square:

        def __init__(self, number, position) -> None:
            self._number = number
            self._position = position

        def update(self) -> None:
            self._number *= 2
            if self._number > 2048:
                raise ValueError("Value {} should be less or equal to 2048.".format(self._number))

        def set(self, num) -> None:
            self._number = num

        def get_num(self) -> int:
            return self._number

        def spawn(self):
            if random() < 0.1:
                self._number = 4
            else:
                self._number = 2

        def __str__(self) -> str:
            return str(self._number)

    def __init__(self, verbose=False) -> None:
        self._BOARD = [[self.Square(0, (col, row)) for col in range(4)] for row in range(4)]
        self._POSITIONS = [(row, col) for row in range(4) for col in range(4)]

        self._empty_positions = self.PositionList(True)
        self._occupied_positions = self.PositionList(False)

        self._up_range = lambda row, col: [(i, col) for i in range(row, -1, -1)]
        self._down_range = lambda row, col: [(i, col) for i in range(row, 4)]
        self._left_range = lambda row, col: [(row, i) for i in range(col, -1, -1)]
        self._right_range = lambda row, col: [(row, i) for i in range(col, 4)]

        self._verbose = verbose

    def get_square(self, row: int, col: int) -> Square:
        return self._BOARD[row][col]

    def update_board(self, direction) -> None:
        if self._verbose:
            print("Updating board.")

        # down example
        for row in range(2,-1, -1):

            while


        for pos in reversed(self._occupied_positions.get_positions()):
            # Iterate through reversed positions so the closer ones to the direction of movement will move first
            curr = self.get_square(*pos)

            # Create a list of potential target positions for the current examined square
            potential_positions = [tuple(x + y * i for x, y in zip(pos, offset)) for i in range(1, 4)]
            potential_positions = [(x, y) for (x, y) in potential_positions if 0 <= x <= 3 and 0 <= y <= 3]

            if self._verbose:
                print("Currently examining position {} with number {}."
                      .format(pos, curr.get_num()))
                print("Current occupied positions: {}".format(self._occupied_positions.get_positions()))
                print("Current empty positions: {}".format(self._empty_positions.get_positions()))
                print("List of potential positions: {}".format(potential_positions))

            for option_pos in potential_positions:

                option_square = self.get_square(*option_pos)

                if self._verbose:
                    print("Examining option_pos: {} containing number: {}."
                          .format(option_pos, option_square.get_num()))

                if option_pos in self._empty_positions:
                    # Target is empty
                    if self._verbose:
                        print("Position {} found empty".format(option_pos))

                    option_square.set(curr.get_num())
                    self._empty_positions.remove(option_pos)
                    self._occupied_positions.update(option_pos)
                    curr.set(0)
                    self._empty_positions.update(pos)
                    self._occupied_positions.remove(pos)
                    break
                elif option_square.get_num() == curr.get_num():
                    # Target has the same number as current examined square
                    if self._verbose:
                        print("Position {} found containing the same number as examined square."
                              .format(option_pos))

                    option_square.update()
                    curr.set(0)
                    self._occupied_positions.remove(pos)
                    self._empty_positions.update(pos)
                    break
                else:
                    # Target has a different number than the current examined square
                    if self._verbose:
                        print("Position {} found containing a different number than as examined square."
                              .format(option_pos))

    def spawn(self) -> None:
        row, col = rand_choice(self._empty_positions.get_positions())
        self._empty_positions.remove((row, col))
        self.get_square(row, col).spawn()
        self._occupied_positions.update((row, col))

    def print(self):
        for row in self._BOARD:
            for square in row:
                print(square, end=" ")
            print()


board = Board(verbose=True)
directions = {"w": "up", "d": "right", "s": "down", "a": "left"}
board.spawn()
board.spawn()
board.print()
choice = input()

while choice != 'q':
    if choice in directions:
        board.update_board(directions.get(choice))
        board.spawn()
        board.print()
    choice = input()
