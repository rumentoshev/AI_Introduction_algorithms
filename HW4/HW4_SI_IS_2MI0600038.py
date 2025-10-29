

from typing import Any


class Board:
    def __init__(self):
        self.board = [[" "," "," "],
                      [" "," "," "],
                      [" "," "," "]]
        self.rounds = 0
    
    def print_board(self):
        print(f"     1   2   3 " )
        print("   -------------")
        for i in range(3):
            print(f"{i+1}  | {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]} |" )
            print("   -------------")

    def clean_board(self):
        self.board = [[" "," "," "],
                      [" "," "," "],
                      [" "," "," "]]
        self.rounds = 0

    def is_board_full(self):
        count = 0

        for row in range(3):
            for col in range(3):
                if self.board[row][col] != " ":
                    count += 1
        if count == 9:
            return True

        return False

    def who_wins(self,index_X,index_Y):
        return self.board[index_X,index_Y]

    def is_solved(self):
        #check rows for win
        for row in range(3):
            if ((self.board[row][0] == self.board[row][1] and
                self.board[row][1] == self.board[row][2]) and
                self.board[row][0] != " "):
                return self.board[row][0]
        
        #check cols for win
        for col in range(3):
            if ((self.board[0][col] == self.board[1][col] and
                self.board[2][col] == self.board[1][col]) and
                self.board[0][col] != " "):
                return self.board[0][col]

        #check diagonals for win
        if ((self.board[0][0] == self.board[1][1] and
            self.board[1][1] == self.board[2][2]) and
            self.board[1][1] != " "):
            return self.board[1][1]
        
        if ((self.board[0][2] == self.board[1][1] and
            self.board[1][1] == self.board[2][0]) and
            self.board[1][1] != " "):
            return self.board[1][1]
            
        if self.is_board_full():
            return "tie"


    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]
    
    def __setitem__(self, pos, value):
        x, y = pos
        self.board[x][y] = value
              
class Game:
    def __init__(self):
        self.board = Board()
    
    def minmax_algorithm(self,depth,isMax,a = -10000,b = 10000):

        res = self.board.is_solved()
        if res == "X":
            return -100000 + depth, None 
        elif res == "O":
            return 100000 - depth, None
        elif res == "tie":
            return 0, None

        best_move = None

        if isMax:
            value = -10000
            for row in range(3):
                for col in range(3):
                    if self.board[row, col] == " ":
                        self.board[row, col] = "O"
                        val, _ = self.minmax_algorithm(depth + 1, False, a, b)
                        self.board[row, col] = " "
                        if val > value:
                            value = val
                            best_move = [row, col]
                        a = max(a, value)
                        if a >= b:
                            break
            return value, best_move

        else:
            value = 10000
            for row in range(3):
                for col in range(3):
                    if self.board[row, col] == " ":
                        self.board[row, col] = "X"
                        val, _ = self.minmax_algorithm(depth + 1, True, a, b)
                        self.board[row, col] = " "
                        if val < value:
                            value = val
                            best_move = [row, col]
                        b = min(b, value)
                        if a >= b:
                            break
            return value, best_move
         
    
    def play_game(self):
        index_of_games = 1
        play_again_flag = True  
        while play_again_flag:
            print(f"This is game № {index_of_games}")
            index_of_games += 1
            while True:
                try:
                    first_player = int(input("Please select who starts first [0 - you, 1 - computer]: "))
                    if first_player in [0, 1]:
                        break
                    else:
                        print("Invalid input. Please enter 0 or 1.")
                except ValueError:
                    print("Invalid input. Please enter a number (0 or 1).")

            
            round = 0
            while round != 10:
                self.board.print_board()
                if first_player == 0:
                            #function
                    row = int(input("Plese enter row [1,3] : ")) -1
                    col = int(input("Plese enter col [1,3] : ")) - 1

                    #check if it is possible
                    self.board[row, col] = "X"
                    round += 1
                    first_player = 1
                else:
                    value, best_move = self.minmax_algorithm(round,True,-10000,10000)
                    self.board[best_move[0], best_move[1]] = "O"
                    round += 1
                    first_player = 0

                is_over = self.board.is_solved()
                if is_over != None:
                    self.board.print_board()
                    if is_over == "tie":
                        print("TIE")
                    else:   
                        print(f"{is_over} WINS")
                    break
            self.board.clean_board()
            while True:
                try:
                    play_again = int(input("Do you want to play again? [0 - NO, 1 - YES]: "))
                    if play_again in [0, 1]:
                        play_again_flag = bool(play_again)
                        break
                    else:
                        print("Invalid input. Please enter 0 or 1.")
                except ValueError:
                    print("Invalid input. Please enter a number (0 or 1).")
    
    
def main():
    game = Game()
    game.play_game()
if __name__ == "__main__":
    main()
