import tkinter as tk
from random import random, choice as rand_choice
from typing import List, Optional, Dict, Tuple

Position = Tuple[int, int]


class Board:
    class Square:

        @staticmethod
        def up_range(pos: Position) -> List[Position]:
            row, col = pos
            return [(i, col) for i in range(row - 1, -1, -1)]

        @staticmethod
        def down_range(pos: Position) -> List[Position]:
            row, col = pos
            return [(i, col) for i in range(row + 1, 4)]

        @staticmethod
        def right_range(pos: Position) -> List[Position]:
            row, col = pos
            return [(row, i) for i in range(col + 1, 4)]

        @staticmethod
        def left_range(pos: Position) -> List[Position]:
            row, col = pos
            return [(row, i) for i in range(col - 1, -1, -1)]

        def __init__(self, position: Position, number: Optional[int] = None) -> None:
            self._ranges: Dict[str, List[Position]] = dict()
            self.number: int = number
            self.position: Position = position

        @property
        def number(self) -> int:
            return self._number

        @number.setter
        def number(self, num) -> None:
            self._number: int = num

        @property
        def position(self) -> Position:
            return self._position

        @position.setter
        def position(self, position: Position) -> None:
            self._position: Position = position
            self._ranges.update({"up": self.up_range(position), "down": self.down_range(position),
                                 "left": self.left_range(position), "right": self.right_range(position)})

        @property
        def ranges(self) -> Dict[str, List[Position]]:
            return self._ranges

        def update_num(self) -> None:
            self._number *= 2
            if self._number > 2048:
                raise ValueError("Value {} should be less or equal to 2048.".format(self._number))

        def spawn(self) -> None:
            if random() < 0.1:
                self._number: int = 4
            else:
                self._number: int = 2

        def __str__(self) -> str:
            return str(self._number)

    def __init__(self, square_labels, verbose: bool = False) -> None:
        self._POSITIONS_TO_LABELS: Dict[Position, tk.Label] = square_labels
        self._squares: Dict[Position, Board.Square] = dict()
        self._empty_positions: List[Position] = list(self._POSITIONS_TO_LABELS.keys()).copy()
        self._occupied_positions: List[Position] = []
        self._verbose: bool = verbose

    def get_square(self, row: int, col: int) -> Optional[Square]:
        if (row, col) in self._squares:
            return self._squares[(row, col)]
        else:
            return None

    def add_square(self, square: Square) -> None:
        self._POSITIONS_TO_LABELS[square.position]['text'] = square.number
        self._squares[square.position]: Board.Square = square
        self._empty_positions.remove(square.position)
        self._occupied_positions.append(square.position)

    def remove_square(self, square: Square) -> None:
        self._POSITIONS_TO_LABELS[square.position]['text'] = ""
        self._squares.pop(square.position)
        self._occupied_positions.remove(square.position)
        self._empty_positions.append(square.position)

    def move_square(self, target: Position, square: Square) -> None:
        old: Position = square.position
        square.position = target

        self._POSITIONS_TO_LABELS[old]['text'] = ""
        self._POSITIONS_TO_LABELS[target]['text'] = square.number

        self._squares.pop(old)
        self._squares.update({target: square})
        self._occupied_positions.remove(old)
        self._empty_positions.append(old)
        self._occupied_positions.append(target)
        self._empty_positions.remove(target)

    def spawn(self) -> None:

        pos: Position = rand_choice(self._empty_positions)
        square: Board.Square = self.Square(pos)
        square.spawn()
        self.add_square(square)
        if self._verbose:
            print("Spawned a square with number {} at position {}".format(square.number, square.position))

    def update_board(self, direction: str) -> bool:
        played = False
        if self._verbose:
            print("Updating board.")

        if self._verbose:
            print("Started looping through registered squares.")

        # dictionary of order of positions to scan while moving squares
        direction_switcher: Dict[str, List[Position]] = \
            {"down": [(row, col) for row in range(2, -1, -1) for col in range(0, 4, 1)],
             "up": [(row, col) for row in range(1, 4, 1) for col in range(0, 4, 1)],
             "left": [(row, col) for row in range(0, 4, 1) for col in range(1, 4, 1)],
             "right": [(row, col) for row in range(0, 4, 1) for col in range(2, -1, -1)]}

        pos: Position
        for pos in direction_switcher[direction]:

            if pos in self._squares:
                square: Board.Square = self._squares[pos]
            else:
                continue

            target_pos: Position
            for target_pos in square.ranges[direction]:

                if self._verbose:
                    print("Checking position: {}".format(square.position))
                    print("Number in square: {}".format(square.number))
                    print("Target position: {}".format(target_pos))

                if target_pos in self._empty_positions:
                    # Target position is empty
                    if self._verbose:
                        print("Target position {} is empty.".format(target_pos))

                    self.move_square(target_pos, square)
                    played = True

                else:
                    bumped_square: Board.Square = self._squares[target_pos]
                    if bumped_square.number == square.number:
                        # Target position contains a square with the same number
                        if self._verbose:
                            print("Target position {} is occupied with the same number {}"
                                  .format(target_pos, bumped_square.number))

                        bumped_square.update_num()
                        self._POSITIONS_TO_LABELS[target_pos]['text'] = bumped_square.number
                        self.remove_square(square)
                        played = True
                    else:
                        # Target position contains a square with a different number
                        if self._verbose:
                            print("Target position {} is occupied with a different number {}"
                                  .format(target_pos, bumped_square.number))
                        break
        return played
