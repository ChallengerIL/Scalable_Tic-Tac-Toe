import os
import numpy as np


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ValueTooBig(Error):
    """Raised when input is too big"""
    pass


class ValueTooSmall(Error):
    """Raised when input is too small"""
    pass


class Tic_Tac_Toe:

    def __init__(self, size):
        self.active = True
        self.choosing = True
        self.players_list = ["X", "O"]
        self.score_dict = {self.players_list[0]: 0, self.players_list[-1]: 0}
        self.move_num = 0
        self.current_row = 0
        self.size = size
        self.rows_total = self.size
        self.current_column = 0
        self.columns_total = self.size
        self.columns_delimiter = "|"
        self.row_delimiter = "-" * ((self.columns_total * 4) - 1)
        self.tracking_arr = np.chararray((self.rows_total, self.columns_total))
        self.tracking_arr[:] = " "

    def print_board(self):
        print("   Score")
        print(f"  {self.players_list[0]}-{self.score_dict[self.players_list[0]]} "
              f"{self.players_list[1]}-{self.score_dict[self.players_list[-1]]}")

        while self.current_row != self.rows_total:
            self.current_column = 0

            for value in self.tracking_arr[self.current_row, :]:
                if value == "":
                    value = " "
                else:
                    value = value.decode('UTF-8')

                cell = f" {value} "

                if self.columns_total - self.current_column > 1:
                    print(cell, end="")
                    print(self.columns_delimiter, end="")
                else:
                    print(cell)

                self.current_column += 1

            # Don't print after the final row
            if self.rows_total - self.current_row > 1:
                print(self.row_delimiter)

            self.current_row += 1

        self.current_row = 0

    def take_input(self, player):
        self.choosing = True

        while self.choosing:
            print(f"Player {player},")
            try:
                column = int(input("Choose a column: ")) - 1
                if column >= self.columns_total:
                    raise ValueTooBig
                elif column < 0:
                    raise ValueTooSmall
            except ValueError:
                print("Wrong input. Only numbers are allowed.")
            except ValueTooBig:
                print(f"Maximum allowed number is {self.columns_total}")
            except ValueTooSmall:
                print(f"Minimum allowed number is {1}")
            else:
                try:
                    row = int(input("Choose a row: ")) - 1
                    if row >= self.rows_total:
                        raise ValueTooBig
                    elif row < 0:
                        raise ValueTooSmall
                except ValueError:
                    print("Wrong input. Only numbers are allowed.")
                except ValueTooBig:
                    print(f"Maximum allowed number is {self.rows_total}")
                except ValueTooSmall:
                    print(f"Minimum allowed number is {1}")
                else:
                    if self.tracking_arr[row, column] == "":
                        self.tracking_arr[row, column] = player
                        self.check_win(player)
                        self.choosing = False
                    else:
                        print("The cell is taken. Pick a different one.")

    def check_win(self, player):
        for i in range(0, self.size):
            # Checks rows and columns for match
            rows_win = (self.tracking_arr[i, :] == player.encode()).all()
            cols_win = (self.tracking_arr[:, i] == player.encode()).all()

            if rows_win or cols_win:
                self.score_dict[player] += 1
                self.tracking_arr[:] = " "

        diag1_win = (np.diag(self.tracking_arr) == player.encode()).all()
        diag2_win = (np.diag(np.fliplr(self.tracking_arr)) == player.encode()).all()

        if diag1_win or diag2_win:
            self.score_dict[player] += 1
            self.tracking_arr[:] = " "

    def play(self):
        while self.active:
            try:
                for player in self.players_list:
                    clear()
                    self.print_board()
                    self.take_input(player)
            except KeyboardInterrupt:
                self.active = False


if __name__ == "__main__":
    game = Tic_Tac_Toe(size=3)
    game.play()
