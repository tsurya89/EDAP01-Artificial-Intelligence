import numpy as np

class Othello:
    def __init__(self):
        # Initialize the starting state of the board itself
        self.board = np.zeros((8, 8), dtype=str)
        self.board[3][3] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"
        self.board[4][4] = "W"

        # Lists to keep track of the locations of black/white pieces, to be updated 
        # and used to compute possible moves
        self.white_locations = [(3, 3), (4, 4)]
        self.black_locations = [(3, 4), (4, 3)]


    def make_move(self,  player, row, col): # To actually change the board
        # check if legal move
        self.board[row][col] = player
        # Update the locations lists

    def update_board(board,  player, row, col,): # Used to calculate the utility of a move
        board = board.copy()
        board[row][col] = player

    def possible_moves(self, player):
        list_of_possible_moves = {}
        opp_locations = None
        # Can only put a white down adjacent / diagonal to a black piece
        if player == "W":
            opp_locations = self.black_locations.copy()
        elif player == "B":
            opp_locations = self.white_locations.copy()
        for location in opp_locations:
            above = (location[0] - 1, location[1])
            below = (location[0] + 1, location[1])
            left = (location[0], location[1] - 1)
            right = (location[0], location[1] + 1)
            upper_right_diag = (location[0] + 1, location[1] + 1)
            lower_right_diag = (location[0] - 1, location[1] + 1)
            upper_left_diag = (location[0] + 1, location[1] - 1)
            lower_left_diag = (location[0] - 1, location[1] - 1)
            potential_moves = [above, below,
                                left, right,
                                upper_right_diag, lower_right_diag,
                                upper_left_diag, lower_left_diag]
            for move in potential_moves:
                if (self.board[move[0]][move[1]] == '' and move[0] < 8 and move[1] < 8):
                    list_of_possible_moves.add(move)
        return list_of_possible_moves
            
        

    def print_board(self):
        print(self.board)
    

class human_player:
    def __init__(self):
        pass

class computer_player:
    def __init__(self):
        pass

def flip(move, locations, player): #move = (row, col), locations = [(white_locations), (black_locations)], 0/1 return list of locations flipped
    return sum(check_col(move, locations, player), 
               check_row(move, locations, player), 
               check_diagonal(move, locations, player))
    
def check_col(move, locations, player):
    total = ()
    row, col = move
    counter = 0
    
    #check above
    curr_col = col - 1
    while curr_col >= 0:
        if (curr_col, row) in locations[player]:
            pass     
        curr_col -= 1

    #check below
    curr_col = col + 1
    while curr_col < 8:
        curr_col += 1
        

    return total

def check_row(move, locations, player):
    total = ()
    # check left

    # check right

    return total

def check_diagonal(move, locations, player):
    total = ()

    return total


def main():
    op = input("Choose colour, ’B’ for black, ’W’ for white: ")

    # Validate input as B or W
    while op.upper() not in "BW":
        op = input("Choose colour, ’B’ for black, ’W’ for white: ")
        
    # Black always goes first

    game = Othello()
    game.print_board()
    
    # Play game
    curr_player = 0
    # -1 as human player
    # 1 as computer

    if op == "B":
        curr_player = -1
    else:
        curr_player = 1

    # TODO while game not done
    for _ in range(5):
        if curr_player == -1:
            row = input("Row: ")
            col = input("Column: ")
            game.make_move(op, row, col)
            curr_player = 1
        else:
            # make computer move
            curr_player = -1
            game.update_board()
        


if __name__ == '__main__': 
    main()
