import sys
import tkinter as tk
import os

import minesweeper as ms
import config


class GMineSweeper:

    def __init__(self, width, height, bombs):
        self.game = ms.make_game(width, height, bombs)
        self.game_win = tk.Tk()
        self.game_win.title('MineSweeper')
        self.label_state = tk.Label(self.game_win, text="RUNNING", fg="blue")
        iconpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
        self.img = [tk.PhotoImage(file=os.path.join(iconpath, "0.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "1.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "2.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "3.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "4.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "5.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "6.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "7.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "8.gif")),
                    tk.PhotoImage(file=os.path.join(iconpath, "9.gif")),  # unrevealed
                    tk.PhotoImage(file=os.path.join(iconpath, "10.gif")),  # bomb explosed
                    tk.PhotoImage(file=os.path.join(iconpath, "11.gif")),  # bomb discovered
                    tk.PhotoImage(file=os.path.join(iconpath, "12.gif")),  # flag
                    tk.PhotoImage(file=os.path.join(iconpath, "13.gif"))  # question
                    ]
        self.width, self.height = (ms.get_width(self.game), ms.get_height(self.game))
        self.button_grid = []
        for i in range(self.height):
            self.button_grid.insert(i, [])
            for j in range(self.width):
                button = tk.Button(self.game_win, padx=0, pady=0, width=19, height=19, image=self.img[9])
                button.grid(column=i, row=j)
                self.button_grid[i].insert(j, button)
                button.bind("<Button-1>", lambda event, i=i, j=j: self.right_click(i, j))
                button.bind("<Button-3>", lambda event, i=i, j=j: self.left_click(i, j))
        self.label_state.grid(columnspan=3)
        self.game_win.mainloop()

    def right_click(self, row, column):
        ms.reveal_cell(self.game, row, column)
        if ms.get_state(self.game) == ms.GameState.losing:
            self.label_state.config(text="LOSE", fg="red")
            self.disable_game()
        elif ms.get_state(self.game) == ms.GameState.wining:
            self.label_state.config(text="WIN", fg="green")
            self.disable_game()
        self.redraw(row, column)

    def left_click(self, row, column):
        cell = ms.get_cell(self.game, row, column)
        if ms.is_flaged(cell):
            ms.unset_flag(cell)
        else:
            ms.set_flag(cell)
        self.redraw(row, column)

    def redraw(self, row, column):
        for i in range(self.height):
            for j in range(self.width):
                cell = ms.get_cell(self.game, i, j)
                button = self.button_grid[i][j]
                if ms.is_revealed(cell):
                    if ms.is_bomb(cell):
                        new_img = self.img[10]
                        if row == i and column == j:
                            new_img = self.img[11]
                    else:
                        new_img = self.img[ms.number_of_bombs_in_neighborhood(cell)]
                    button.config(relief=tk.FLAT, image=new_img, command="")
                elif ms.is_flaged(cell):
                    button.config(image=self.img[12])
                else:
                    button.config(image=self.img[9])

    def disable_game(self):
        for line in self.button_grid:
            for button in line:
                button.config(state=tk.DISABLED)
                button.unbind("<Button-1>")
                button.unbind("<Button-3>")


if __name__ == '__main__':
    # TODO argparse
    try:
        config_file = sys.argv[1]
    except IndexError:
        app = GMineSweeper(10, 10, 10)
    else:
        h, w, b = config.rescue_basic_config(config_file)
        app = GMineSweeper(w, h, b)
