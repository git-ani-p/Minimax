# TODOs
# Finish the Minimax work
# Optimize --> Move variables to global
# Benchmark Board as an object

import math
import random
import time
import sys
import copy

from collections import namedtuple

DEPTH = 2 # Just to start with, should not be too bad to look two moves into the future considering the branching factor of Othello


BOARD_WIDTH = 8
BOARD_HEIGHT = 8

ID = int(input())
OPP_ID = 1 - ID

size = int(input())                                                                 #Unnecessary


#String notations
NEUTRAL_SIGN = '.'
MY_SIGN = str(ID)
OPP_SIGN = str(OPP_ID)

# Map reference notations
NEUTRAL = -1
MINE = ID
OPPONENT = OPP_ID


board = [ [ -1 for j in range(BOARD_WIDTH) ] for i in range(BOARD_HEIGHT) ]         # Game map

temp_board = board                                                                  # modified board on playouts




Direction = namedtuple('Direction', ['x', 'y'])

directions = [
    Direction(0, -1),            #North
    Direction(1, -1),            #North East
    Direction(1, 0),             #East
    Direction(1, 1),             #South East
    Direction(0, 1),             #South
    Direction(-1, 1),            #South West
    Direction(-1, 0),            #West
    Direction(-1, -1),           #North West
]






def fill_board(board):                                                                   # Fill the board using the input
    grid = board

    for i in range(BOARD_HEIGHT):

        line = input()

        for j in range(BOARD_WIDTH):
            if line[j] != NEUTRAL_SIGN:

                if line[j] == MY_SIGN:
                    grid[i][j] = MINE

                else:
                    grid[i][j] = OPPONENT

    return grid


def evaluate_playout(playout_board):
    opp_score = 0
    my_score = 0

    for i in range(BOARD_HEIGHT):

        for j in range(BOARD_WIDTH):

            if playout_board[i][j] == MINE:
                my_score += 1

            elif playout_board == OPPONENT:
                opp_score += 1

    if my_score + opp_score == BOARD_WIDTH * BOARD_HEIGHT:

        if my_score > BOARD_HEIGHT * BOARD_WIDTH // 2:
            return double('inf')

        else:
            return double('inf') * -1

    return my_score - opp_score                                         # Zero sum --> evaluate_me + evaluate_him = 0




def game_over(playout_board):

    for i in range(BOARD_HEIGHT):

        for j in range(BOARD_WIDTH):

            if playout_board == NEUTRAL:
                return False

    return True



# Is it better than having objects? Nested fors vs object creation --> Benchmarking required.
# A piece is a tuple --> (x, y)
def get_pieces(game_board, player):

    my_pieces = []

    for i in range(BOARD_HEIGHT):

        for j in range(BOARD_WIDTH):

            if game_board[i][j] == player:
                my_pieces.append( ( j, i ) )

    return my_pieces

#Action is a tuple --> (x, y)
def get_actions(game_board, player):

    my_pieces = get_pieces(game_board, player)

    actions = []

    for piece in my_pieces:
        #Iterate through the directions and see if there is a chain that I can capture

        for direction in directions:

            count = 0

            x = piece[0]
            y = piece[1]

            while True:

                # Move in that direction
                x += direction.x
                y += direction.y

                #Out of board
                if x < 0 or x > BOARD_WIDTH - 1:
                    break

                if y < 0 or y > BOARD_HEIGHT - 1:
                    break

                location = temp_board[y][x] #Piece type

                # If it is a neutral cell, we need to stop and check if we can place here
                if location == NEUTRAL:

                    #Should capture a piece and avoid repeats.
                    if count > 0 and location not in actions:

                        actions.append( ( x, y ) )

                    break

                #If a piece is on that cell
                else:

                    #Cannot capture my own
                    if location == MINE:
                        break

                    #Capture a piece
                    else:
                        count += 1

    return actions





def play_move(temp_board, x, y, owner):

    to_flip = [] # An array of tuples (x, y) to give the positions to flip

    for direction in directions:
        #Start from placement each time
        start_x = x
        start_y = y

        pieces_to_add = []       # An array of opponent pieces to flip only if the end is mine.

        #Flip all possible in that direction
        while True:
            # Move in that direction
            start_x += direction.x
            start_y += direction.y

            #Out of board
            if x < 0 or x > BOARD_WIDTH - 1:
                break

            if y < 0 or y > BOARD_HEIGHT - 1:
                break
 
            location = temp_board[y][x] #Piece type

            if location == NEUTRAL:  # Dont move ahead if it is an empty square
                break

            if location == owner:  # If I hit my piece, return aall of the opponent`s pieces till there
                to_flip.extend(pieces_to_add)

            else:
                pieces_to_add.append( (start_x, start_y) )

    for piece in to_flip:

        temp_board[y][x] ^= 1  #Change its owner

    return temp_board


# Search algorithm, two turns into the future for the time being
# It is a minimax, so it will always converge.


def minimax(temp_board, depth, maximizing_player):

    #I am done creating the tree, or there are no future actions
    # game_over() is needed as I dont want the bot to go into the recursive steps and have a coin toss between infinity and -infinity based on whose turn it is.
    if depth == 0 or game_over(temp_board):

        return evaluate_playout(temp_board)

    


    #Is it my turn? I want to maximize my score...
    elif maximizing_player:
        best_score = -1 * double('inf')

        actions = get_actions(temp_board, MINE)

        for action in actions:

            playout_board = play(temp_board, action[0], action[1], MINE)

            score = minimax(playout_board, depth - 1, False)

            if score > best_score:

                best_score = score


                if depth == DEPTH:
                    global best
                    best = good


        

        return best_score

    #Opponent wants my score to be as low as possible
    else:
        best_score = double('inf')

        actions = get_actions(temp_board, OPPONENT)

        for action in actions:

            playout_board = play(temp_board, action[0], action[1], OPPONENT)

            score = minimax(playout_board, depth - 1, True)

            if score < best_score:
                best_score = score

        return best_score
    
        





while True:

    best = None  # The first move that I should make



    start = time.time()   #Benchmarker


    board = fill_board(board)
    temp_board = board          #Search copy


    action_count = int(input()) # Unnecessary, can be commented out if this is not given as an input
    
    
    for i in range(action_count):
        input()

    minimax(temp_board, DEPTH, MINE)

    print(best)























