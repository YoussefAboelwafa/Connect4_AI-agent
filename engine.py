import math
from GUI import *
import random
import time


ROW_COUNT = 6
COLUMN_COUNT = 7


tree=[]
min_tree={}

def print_as_board(grid):
    for i in range(0, 6):
        for j in range(0, 7):
            print(grid[i][j], end=" ")
        print()
    print()

def convert_from_string_to_grid(state):
    grid = [[0] * 7 for _ in range(6)]
    for i in range(0, 6):
        for j in range(0, 7):
            grid[i][j] = int(state[i * 7 + j])
    return grid


def convert_from_grid_to_string(grid):
    state = ""
    for i in range(0, 6):
        for j in range(0, 7):
            state += str(grid[i][j])
    return state


def drop_piece(state, col, piece):
    grid = convert_from_string_to_grid(state)
    for row in range(5, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = piece
            break
    return convert_from_grid_to_string(grid)


def get_valid_locations(state):
    locations = []
    for col in range(7):
        if is_valid_location(state, col):
            locations.append(col)
    return locations


def is_valid_location(state, col):
    grid = convert_from_string_to_grid(state)
    return grid[0][col] == 0


def get_score(state, col, piece, depth, option):
    next_state = drop_piece(state, col, piece)
 
    if option == 1:
        new_dict={
                next_state:{
                "depth":depth - 1,
                "piece":piece % 2 + 1,
                "value":0,
                "childs":[],}
            }
        

        value = minimax(next_state, depth - 1, piece, False,new_dict)
        new_dict[next_state]['value']=value
        min_tree[state]["childs"].append(new_dict)
        return value
    else:
        return minimax_alpha_beta(
            next_state, depth - 1, -math.inf, math.inf, piece, False
        )


def count_potential_future_wins(board, player):
    potential_wins = 0
    for col in range(COLUMN_COUNT):
        if is_valid_location(convert_from_grid_to_string(board), col):
            future_state = drop_piece(convert_from_grid_to_string(board), col, player)
            if is_terminal(future_state):
                potential_wins += 1
    return potential_wins

    


# heuristic function
def minimax_heuristic(state, player):
    board = convert_from_string_to_grid(state)

    num_of_four = count_window(board, 4, player)
    num_of_three = count_window(board, 3, player)
    num_of_two = count_window(board, 2, player)

    num_of_four_opp = count_window(board, 4, player % 2 + 1)
    num_of_three_opp = count_window(board, 3, player % 2 + 1)
    num_of_two_opp = count_window(board, 2, player % 2 + 1)
    num_of_fail_loase=fail_loses(board,4,player%2+1)

    # print(num_of_fail_loase)

    if (
        num_of_four == 0
        and num_of_three == 0
        and num_of_two == 0
        and num_of_four_opp == 0
        and num_of_three_opp == 0
    ):
        return 0
    return (
        (10**10) * num_of_four
        + 1000 * num_of_three
        + 100 * num_of_two
        - 1 * num_of_two_opp
        - (10**6) * num_of_three_opp
        + 1000 * count_potential_future_wins(board, player)
        -100000000 *count_potential_future_wins(board,player%2+1)

    )

def fail_loses(board, window, player):
    number_of_windows = 0
    # Hirozontal windows
    for i in range(6):
        for j in range(7 - window + 1):
            if board[i][j : j + window].count(player) == window-1 and board[i][j : j + window].count(player%2+1)==1 :
                number_of_windows += 1
    # Vertical windows
    for i in range(6 - window + 1):
        for j in range(7):
            arr=[board[i + k][j] for k in range(window)]
            if arr.count(player) == window-1 and arr.count(player%2+1)==1 :
                number_of_windows += 1
    # Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            arr= [board[i + k][j + k] for k in range(window)]
            if arr.count(player) == window-1 and arr.count(player%2+1)==1:
                number_of_windows += 1
    # Negative Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            arr =[board[i + window - 1 - k][j + k] for k in range(window)]
            if arr.count(
                player
            ) == window-1 and arr.count(player%2+1)==1:
                number_of_windows += 1
    return number_of_windows

def count_window(board, window, player):
    number_of_windows = 0
    # Hirozontal windows
    for i in range(6):
        for j in range(7 - window + 1):
            if board[i][j : j + window].count(player) == window:
                number_of_windows += 1
    # Vertical windows
    for i in range(6 - window + 1):
        for j in range(7):
            if [board[i + k][j] for k in range(window)].count(player) == window:
                number_of_windows += 1
    # Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            if [board[i + k][j + k] for k in range(window)].count(player) == window:
                number_of_windows += 1
    # Negative Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            if [board[i + window - 1 - k][j + k] for k in range(window)].count(
                player
            ) == window:
                number_of_windows += 1
    return number_of_windows


def is_terminal(state):
    board = convert_from_string_to_grid(state)
    # check for draw
    if list(board[0]).count(0) == 0:
        return True
    # check for horizontal win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3]
                and board[r][c] != 0
            ):
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]
                and board[r][c] != 0
            ):
                return True

    # Check positive slope diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c]
                == board[r + 1][c + 1]
                == board[r + 2][c + 2]
                == board[r + 3][c + 3]
                and board[r][c] != 0
            ):
                return True

    # Check negative slope diagonal

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c]
                == board[r - 1][c + 1]
                == board[r - 2][c + 2]
                == board[r - 3][c + 3]
                and board[r][c] != 0
            ):
                return True


def minimax(state, depth, piece, maximizingPlayer,tree):
    if depth == 0 or is_terminal(state):
        value=minimax_heuristic(state, piece)
        return value
    valid_location = get_valid_locations(state)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict={
                child:{
                "depth":depth - 1,
                "piece":piece % 2 + 1,
                "value":0,
                "childs":[],}
            }
            value = max(value, minimax(child, depth - 1, piece, False,new_dict))
            new_dict[child]["value"]=value
            tree[state]["childs"].append(new_dict)
        return value
    else:
        value = math.inf
        for col in valid_location:

            child = drop_piece(state, col, piece % 2 + 1)
            new_dict={
                child:{
                "depth":depth - 1,
                "piece":piece % 2 + 1,
                "value":0,
                "childs":[],}
            }
            value = min(value, minimax(child, depth - 1, piece, True,new_dict))
            new_dict[child]["value"]=value
            tree[state]["childs"].append(new_dict)
        return value



def minimax_alpha_beta(state, depth, alpha, beta, piece, maximizingPlayer):
    if depth == 0 or is_terminal(state):
        return minimax_heuristic(state, piece)

    valid_location = get_valid_locations(state)

    if maximizingPlayer:
        value = -math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            value = max(
                value, minimax_alpha_beta(child, depth - 1, alpha, beta, piece, False)
            )
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece % 2 + 1)
            value = min(
                value, minimax_alpha_beta(child, depth - 1, alpha, beta, piece, True)
            )
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def agent(grid, depth, option):
    min_tree.clear()
    state = convert_from_grid_to_string(grid)
    min_tree[state]={
            "depth": depth,
            "piece": 1,
            "value": 0,
            "childs":[],
    }

    valid_moves = get_valid_locations(state)
    scores = dict(
        zip(
            valid_moves,
            [get_score(state, col, 2, depth, option) for col in valid_moves],
        )
    )
    # print(scores)
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    res=random.choice(max_cols)
    min_tree[state]["value"]=scores[res]
    return res, min_tree


board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [1, 2, 1, 2, 0, 2, 2],
    [1, 2, 2, 1, 1, 2, 1],
]


def print_tree(tree, indent=0):
    state=list(tree.keys())[0]
    
    print("    " * indent + f"{state} | Depth: {tree[state]['depth']}, Piece: {tree[state]['piece']}, Value: {tree[state]['value']}")
    childs=tree[state]['childs']
    for child in childs:
        print_tree(child,indent+1)


    # print()
    # for key,node in tree.keys(), tree.values():
    #     print(key)
    #     print(node)
    #     # print("    " * indent + f"{node['state']} | Depth: {node['depth']}, Piece: {node['piece']}, Value: {node['value']}")
    #     if 'childs' in node:
            
    #         print_tree(node['childs'], indent + 1)


def main():
    start = time.time()
    print(agent(board, 2, 1))
    end = time.time()
    # print(end - start)
    # print(len(tree))
    # print_as_tree(tree=tree)
    # print(min_tree)
    # min_tree.keys()
    # print(min_tree)
    # print_tree(min_tree)


if __name__ == "__main__":
    main()



