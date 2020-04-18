import tkinter as tk
from typing import Dict, Tuple

from game import Board
from game import Position


def gui_setup() -> Tuple[tk.Tk, Dict[Position, tk.Label]]:
    window: tk.Tk = tk.Tk()
    frame_board: tk.Frame = tk.Frame(master=window)
    frame_board.pack(fill=tk.BOTH, expand=True)
    window.bind("<Left>", left_pressed)
    window.bind("<Right>", right_pressed)
    window.bind("<Up>", up_pressed)
    window.bind("<Down>", down_pressed)

    square_labels: Dict[Position, tk.Label] = dict()
    for i in range(4):

        frame_board.columnconfigure(i, weight=1)
        frame_board.rowconfigure(i, weight=1)

        for j in range(4):
            # Setup the square frame
            frame_square: tk.Frame = tk.Frame(master=frame_board, borderwidth=1, relief=tk.RAISED)
            frame_square.grid(row=i, column=j, sticky="nsew")
            # Setup the square's content
            label: tk.Label = tk.Label(master=frame_square)
            label.pack(padx=20, pady=10)

            # Add square frame to the list
            square_labels[(i, j)] = label
    return window, square_labels


def setup_game(square_labels: Dict[Position, tk.Label]) -> None:
    global board
    board = Board(square_labels)
    board.spawn()
    board.spawn()


def left_pressed(_: tk.Event) -> None:
    if board.update_board("left"):
        board.spawn()


def right_pressed(_: tk.Event) -> None:
    if board.update_board("right"):
        board.spawn()


def up_pressed(_: tk.Event) -> None:
    if board.update_board("up"):
        board.spawn()


def down_pressed(_: tk.Event) -> None:
    if board.update_board("down"):
        board.spawn()


def main():
    window: tk.Tk
    square_labels: Dict[Position, tk.Label]
    window, square_labels = gui_setup()
    setup_game(square_labels)
    window.mainloop()


board = None
main()
