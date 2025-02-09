import numpy as np
import copy
import time
from math import log

CHANGE = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
HUMAN = 0
AB = 1

class Othello:
    def __init__(self, color):
        # Initialize the starting state of the board itself
        self.board = np.zeros((8, 8), dtype=str)
        for row in range (len(self.board)):
            for col in range (len(self.board[0])):
                self.board[row][col] = "▢"
        self.board[3][3] = "W"
        self.board[3][4] = "B"
        self.board[4][3] = "B"
        self.board[4][4] = "W"

        # Lists to keep track of the locations of black/white pieces, to be updated 
        # and used to compute possible moves
        self.white_locations = set([(3, 3), (4, 4)])
        self.black_locations = set([(3, 4), (4, 3)])

        # self.white_locations = set([
        #     (1,0), (1,3), (1,4), (1, 6), (1,7), 
        #     (2,0), (2,6), (2,7),
        #     (3,2), (3,3), (3,5), (3,6), (3,7),
        #     (4,3), (4,4), (4,6), (4,7),
        #     (5,1), (5,2), (5,3), (5,5), (5,6), (5,7),
        #     (6,1), (6,2), (6,4), (6,5), (6,6), (6,7),
        #     (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7)
        # ])

        # self.black_locations = set([
        #     (0,0),(0, 1), (0, 2), (0,3), (0,4), (0,5),
        #     (1, 1), (1,2), (1,5),
        #     (2, 1), (2,2), (2,3), (2,4), (2,5),
        #     (3,0), (3,1), (3,4),
        #     (4,0), (4,1), (4,2), (4,5),
        #     (5, 0), (5,4),
        #     (6,0), (6,3),
        #     (7,0)
        # ])

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
        print("If you want to pass, enter 'P'.")
        row = input("Row: ").strip()
        if row.upper() == 'P':
            return None
        
        col = input("Column: ").strip()
        if col.upper() == 'P':
            return None
        
        while (not row.isdigit()    # check if input is a digit
            or not col.isdigit()
            or int(row) < 0 or int(row) >= 8    # check within bounds
            or int(col) < 0 or int(col) >= 8
            or (int(row), int(col)) in self.locations[0]    # check if move already exists
            or (int(row), int(col))  in self.locations[1]):
            
            print("Invalid move.")
            row = input("Row: ").strip()
            if row.upper() == 'P':
                return None
        
            col = input("Column: ").strip()
            if col.upper() == 'P':
                return None

        return (int(row), int(col))

    def make_move(self, player, move): # To actually change the board
        if move == None:
            return
        row, col = move
        total_flips = self.flip((row, col), self.locations, player)
        # Flips are possible
        if len(total_flips) > 0:
            
            # Update locations lists
            self.locations[player].add(move)
            self.locations[player].update(total_flips)
            self.locations[abs(player - 1)] -= total_flips
            
            # Update the board representation
            for flipped in total_flips:
                flip_row, flip_col = flipped
                self.board[flip_row][flip_col] = self.color[player]
            self.board[row][col] = self.color[player]
            return
        
        
        else:
            #invalid do again
            print("Invalid move.")
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
                if (move[0] < 8 and move[1] < 8
                    and move[0] >= 0 and move[1] >= 0
                    and self.board[move[0]][move[1]] == "▢"):
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
        self.check(row+1, col-1, locations, curr_player, op_player, total, 6)
        self.check(row+1, col+1, locations, curr_player, op_player, total, 7)

        return total

    def check(self, row, col, locations, curr_player, op_player, total, index):
        possible_flips = set()
        counter = 0

        while (0 <= row < 8) and (0 <= col < 8):
            # if same piece found, if no op piece found - break, else add possible flips to total - break
            if (row, col) in locations[curr_player]:
                # print("Same piece found in ", row, col)
                if counter > 0:
                    # print(counter, " flipped")
                    total.update(possible_flips)
                break
            # if different piece found - add location to possible flips
            elif (row, col) in locations[op_player]:
                # print("Opponenet piece found in ", row, col)
                possible_flips.add((row, col))
                counter += 1
            # if empty - break
            else:
                # print("No more.")
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
        self.bad_spots = {(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                           (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
                           (2, 1), (3, 1), (4, 1), (5, 1),
                           (2, 6), (3, 6), (4, 6), (5, 6)}
        self.good_spots = {(0, 0), (0, 7), (7, 0), (7, 7)}
        self.okay_spots = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                           (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
                           (2, 0), (3, 0), (4, 0), (5, 0),
                           (2, 7), (3, 7), (4, 7), (5, 7)}

    def game_over(self, locations):
        if len(locations[0]) + len(locations[1]) == 64 or len(locations[0]) == 0 or len(locations[1]) == 0 or len(self.game.possible_moves(HUMAN, self.game.locations)) == 0 or len(self.game.possible_moves(AB, self.game.locations)) == 0:
            return HUMAN if len(locations[0]) > len(locations[1]) else AB        
        return -1
    # ***** Start of use of minimax algorithm with alpha-beta pruning *****
    # (find_best_move, min_player, max_player)
    def find_best_move(self, game):
        # copy of locations
        locations_copy = game.get_locations()
        best_score = -np.inf
        best_move = None
        for move in game.possible_moves(AB, locations_copy):
            score = self.min_player(self.update_board(locations_copy, AB, move), best_score, np.inf, 1) + self.eval(move)
            print(move, score)
            if score > best_score:
                best_score = score
                best_move = move
        print("Best move:", best_move)
        game.make_move(AB, best_move)

    # ALWAYS HUMAN
    def min_player(self, locations, alpha, beta, depth):
        winner = self.game_over(locations)
        if winner != -1:
            return 100 if winner == HUMAN else -100
        elif depth == self.max_depth: return len(locations[0])
        score = np.inf
        # need to fix this possible moves call because it won't work on the updated board 
        for move in self.game.possible_moves(HUMAN, locations): 
            score = min(score, self.max_player(self.update_board(locations, HUMAN, move), alpha, beta, depth+1)) + self.eval(move)
            beta = min(beta, score)
            if score <= alpha: break
        return score

    # ALWAYS AB
    def max_player(self, locations, alpha, beta, depth):
        winner = self.game_over(locations)
        if winner != -1:
            return 100 if winner == AB else -100        
        elif depth == self.max_depth: return len(locations[1])
        score = -np.inf
        for move in self.game.possible_moves(AB, locations): 
            score = max(score, self.min_player(self.update_board(locations, AB, move), alpha, beta, depth+1)) + self.eval(move)
            alpha = max(alpha, score)
            if score >= beta: break
        return score
    
    def eval(self, move):
        if move is None:
            return 0
        elif move in self.good_spots:
            return 10
        elif move in self.bad_spots:
            return -10
        elif move in self.okay_spots:
            return 5
        
        return 0
    
    def update_board(self, locations, player, move_to_simulate): # Used to calculate the utility of a move
        locations_copy = copy.deepcopy(locations)
        # "Make that move" and flip pieces that that move outflanks
        # Update locations lists
        total_flips = self.game.flip(move_to_simulate, locations_copy, player)
        locations_copy[player].add(move_to_simulate)
        locations_copy[player].update(total_flips)
        locations_copy[abs(player - 1)] -= total_flips
        return locations_copy
    
def main():   
    
    op = input("Choose colour, ’B’ for black, ’W’ for white: ").upper().strip()

    # Validate input as B or W
    while op not in "BW":
        op = input("Choose colour, ’B’ for black, ’W’ for white: ").upper().strip()
    
    time_limit = input("Time limit in seconds: ")
    try:
        time_limit = float(time_limit)
    except ValueError:
        time_limit = input("Time limit in seconds: ")

    time_limit = float(time_limit)
    depth = 1
    if time_limit <= 0.005:
        depth = 1
    elif time_limit <= 0.01:
        depth = 2
    elif time_limit <= 0.1:
        depth = 3
    elif time_limit <= 1:
        depth = 4
    elif time_limit <= 5:
        depth = 5
    elif time_limit <= 30:
        depth = 6
    elif time_limit <= 300:
        depth = 7
    else:
        depth = 2 + int(log(time_limit))
        
    print("DEPTH", depth)
    # Black always goes first

    game = Othello(op)
    game.print_board()

    comp = AlphaBeta(game, depth)
    
    # Play game
    # 0 as human player
    # 1 as computer
    if op == "B":
        curr_player = HUMAN
        print("You chose Black.")
    else:
        curr_player = AB
        print("You chose White.")

    winner = comp.game_over(game.locations)
    while winner == -1:
        if curr_player == HUMAN:
            game.make_move(HUMAN, game.get_user_input())
            curr_player = AB
        else:
            curr_player = HUMAN
            #timer start
            start_time = time.perf_counter()
            comp.find_best_move(game)
            end_time = time.perf_counter()
            print("AB took ", end_time - start_time)
            # time end
        winner = comp.game_over(game.locations)
        game.print_board()
    if (winner  == HUMAN):
        print("You won!")
    elif (winner == AB):
        print("Computer won!")
    else:
        print("Tie!")    

    print("Game over. You have", len(game.locations[HUMAN]), "and Computer has", len(game.locations[AB]))
 
    

if __name__ == '__main__': 
    main()