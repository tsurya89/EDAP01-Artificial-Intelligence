import numpy as np
import copy
CHANGE = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [-1, 1], [1, 1]]
HUMAN = 0
AB = 1

class Othello:
    def __init__(self, color):
        # Initialize the starting state of the board itself
        self.board = np.zeros((8, 8), dtype=str)
        self.board[3][3] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"
        self.board[4][4] = "W"

        # Lists to keep track of the locations of black/white pieces, to be updated 
        # and used to compute possible moves
        self.white_locations = {(3, 3), (4, 4)}
        self.black_locations = {(3, 4), (4, 3)}

        # List of two sets
        if color == "B": # color = the color that the human player chose
            self.locations = [self.black_locations, self.white_locations]
            self.color = {0: "B", 1: "W"}
        else:
            self.locations = [self.white_locations, self.black_locations]
            self.color = {0: "W", 1: "B"}
        
        # TESTING
        # self.white_locations = {(3, 4), (4, 3), (2, 4), (2, 2)}
        # self.black_locations = {(3, 3), (4, 4), (4, 2)}

    def get_user_input(self):
        row = input("Row: ").strip()
        col = input("Column: ").strip()
        
        while (not row.isdigit()    # check if input is a digit
            or not col.isdigit()
            or int(row) < 0 or int(row) >= 8    # check within bounds
            or int(col) < 0 or int(col) >= 8
            or (int(row), int(col)) in self.locations[0]    # check if move already exists
            or (int(row), int(col))  in self.locations[1]):
            
            print("Invalid move.")
            row = input("Row: ").strip()
            col = input("Column: ").strip()

        return (int(row), int(col))

    def make_move(self, player, move): # To actually change the board
        row, col = move
        
        total_flips = self.flip((row, col), self.locations, player)
        # Flips are possible
        if len(total_flips) > 0:
            
            # Update locations lists
            self.locations[player].add(move)
            self.locations[player].update(total_flips)
            self.locations[abs(player - 1)] -= total_flips
            
            # Update the board representation
            for fliped in total_flips:
                row, col = fliped
                self.board[row][col] = self.color[player]

            self.board[row][col] = self.color[player]
            return
        
        else:
            #invalid do again
            self.make_move(player, self.get_user_input())
            return
            
    
 
    def possible_moves(self, player, locations):
        list_of_possible_moves = set()
        opp_locations = None
        # Can only put a white down adjacent / diagonal to a black piece
        opp_locations = locations[abs(player - 1)].copy()
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
                if (self.board[move[0]][move[1]] == '' and move[0] < 8 and move[1] < 8
                    and move[0] >= 0 and move[1] >= 0):
                    total_flips = self.flip((move), locations, player)
                    
                    # Flips are possible
                    if len(total_flips) > 0:
                        # # Update locations lists
                        # locations[player].update(move)
                        # locations[player].update(total_flips)
                        # locations[abs(player - 1)] -= total_flips
                        
                        # # Update the board representation
                        # self.board[move[0]][move[1]] = self.color[player]
                        # # FIX THIS to return updated locations based on the current move we are trying from possible moves.
                        list_of_possible_moves.add(move)
        return list_of_possible_moves
    
    def flip(self, move, locations, curr_player): #move = (row, col), locations, 0/1 return list of locations flipped
        total = set()  # set of how many turned
        row, col = move
        op_player = abs(curr_player - 1)

        #check row
        self.check(row-1, col, locations, curr_player, op_player, total, 0)
        self.check(row+1, col, locations, curr_player, op_player, total, 1)

        #check col
        self.check(row, col-1, locations, curr_player, op_player, total, 2)
        self.check(row, col+1, locations, curr_player, op_player, total, 3)

        #check diagonal
        self.check(row-1, col-1, locations, curr_player, op_player, total, 4)
        self.check(row-1, col+1, locations, curr_player, op_player, total, 5)
        self.check(row-1, col-1, locations, curr_player, op_player, total, 6)
        self.check(row+1, col+1, locations, curr_player, op_player, total, 7)

        return total

    def check(self, row, col, locations, curr_player, op_player, total, index):
        possible_flips = set()
        counter = 0

        while (0 <= row < 8) and (0 <= col < 8):
            # if same piece found, if no op piece found - break, else add possible flips to total - break
            if (row, col) in locations[curr_player]:
                print("Same piece found in ", row, col)
                if counter > 0:
                    print(counter, " flipped")
                    total.update(possible_flips)
                break
            # if different piece found - add location to possible flips
            elif (row, col) in locations[op_player]:
                print("Opponenet piece found in ", row, col)
                possible_flips.add((row, col))
                counter += 1
            # if empty - break
            else:
                print("No more.")
                possible_flips.clear()
                break
            # iterate
            row += CHANGE[index][0]
            col += CHANGE[index][1]
        
        return

    def print_board(self):
        print(self.board)
    
    def get_locations(self):
        return copy.deepcopy(self.locations)

class AlphaBeta:
    def __init__(self, game, max_depth=3):
        self.max_depth = max_depth
        self.game = game

    def game_over(self, locations, winner):
        if len(locations[0]) + len(locations[1]) == 64:
            winner = HUMAN if len(locations[0]) > len(locations[1]) else AB
            return True
    
    def find_best_move(self, game):
        # copy of locations
        locations_copy = game.get_locations()
        best_score = -np.inf
        best_move = None
        for move in game.possible_moves(AB, locations_copy):
            score = self.min_player(self.update_board(locations_copy, AB, move), best_score, np.inf, 1)
            if score > best_score:
                best_score = score
                best_move = move
        game.make_move(best_move)

    def min_player(self, locations, alpha, beta, depth):
        winner = -1
        if self.game_over(locations, winner):
            return 100 if winner == HUMAN else -100
        elif depth == self.max_depth: return len(locations[0])
        score = np.inf
        # need to fix this possible moves call because it won't work on the updated board 
        for move in self.game.possible_moves(HUMAN, locations): 
            score = min(score, self.max_player(self.update_board(locations, HUMAN, move), alpha, beta, depth+1))
            beta = min(beta, score)
            if score <= alpha: break
        return score

    def max_player(self, locations, alpha, beta, depth):
        winner = -1
        if self.game_over(locations, winner) :
            return 100 if winner == AB else -100        
        elif depth == self.max_depth: return len(locations[1])
        score = -np.inf
        for move in self.game.possible_moves(AB, locations): 
            score = max(score, self.max_player(self.update_board(locations, AB, move), alpha, beta, depth+1))
            alpha = max(alpha, score)
            if score >= beta: break
        return score
    
    def update_board(self, locations, player, move_to_simulate): # Used to calculate the utility of a move
        locations_copy = copy.deepcopy(locations)
        # "Make that move" and flip pieces that that move outflanks
        # Update locations lists
        total_flips = self.game.flip(move_to_simulate, locations_copy, player)
        locations_copy[player].update(move_to_simulate)
        locations_copy(total_flips)
        locations_copy[abs(player - 1)] -= total_flips
        return locations_copy

        

    
def main():   
    
    op = input("Choose colour, ’B’ for black, ’W’ for white: ").upper()

    # Validate input as B or W
    while op not in "BW":
        op = input("Choose colour, ’B’ for black, ’W’ for white: ").upper()
        
    # Black always goes first

    game = Othello(op)
    game.print_board()

    comp = AlphaBeta()
    
    # Play game

    # 0 as human player
    # 1 as computer
    if op == "B":
        curr_player = HUMAN
        print("You chose Black.")
    else:
        curr_player = AB
        print("You chose White.")

    # TODO while game not done
    for _ in range(5):
        if curr_player == 0:
            game.make_move(HUMAN, game.get_user_input())

            curr_player = 1
        else:
            # make computer move
            curr_player = 0
            comp.find_best_move(game)
        game.print_board()
            
    

if __name__ == '__main__': 
    main()
