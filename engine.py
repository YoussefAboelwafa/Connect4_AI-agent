import math
import random
import time

ROW_COUNT = 6
COLUMN_COUNT = 7

tree = []
min_tree = {}


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
    for row in range(5, -1, -1):
        if state[row*7 + col] == '0':
            newstate = state[:row*7+col] + str(piece)[0] + state[row*7+col + 1:]
            break
    return newstate
def is_valid_location(state, col):
    return state[col] == '0'
def get_valid_locations(state):
    locations = []
    for col in range(7):
        if is_valid_location(state, col):
            locations.append(col)
    return locations
def get_score(state, col, piece, depth, option):
    next_state = drop_piece(state, col, piece)
    if option == 1:
        new_dict = {
            next_state: {
                "depth": depth - 1,
                "piece": piece % 2 + 1,
                "value": 0,
                "childs": [], }
        }
        value = minimax(next_state, depth - 1, piece % 2 + 1, False, new_dict)
        new_dict[next_state]['value'] = value
        min_tree[state]["childs"].append(new_dict)
        return value
    else:
        new_dict = {
            next_state: {
                "depth": depth - 1,
                "piece": piece % 2 + 1,
                "value": 0,
                "childs": [], }
        }
        value = minimax_alpha_beta(next_state, depth - 1, -math.inf, math.inf, piece % 2 + 1, False, new_dict)
        new_dict[next_state]['value'] = value
        min_tree[state]["childs"].append(new_dict)
        return value
def minimax_heuristic(state, player):
    # return 100
    board = convert_from_string_to_grid(state)
    num_of_four = count_window(board, 4, player)
    num_of_three = count_window(board, 3, player)
    num_of_two = count_window(board, 2, player)

    num_of_four_opp = count_window(board, 4, player % 2 + 1)
    # num_of_three_opp = count_window(board, 3, player % 2 + 1)
    # num_of_two_opp = count_window(board, 2, player % 2 + 1)

    # num_of_fail_loase=fail_loses(board,4,player%2+1)
    
    
    if (
        num_of_four == 0
        and num_of_three == 0
        and num_of_two == 0
        and num_of_four_opp == 0
        # and num_of_three_opp == 0
    ):
        return 0
    return (
        (10**10) * num_of_four
        # + 1000 * num_of_three
        # + 100 * num_of_two
        # - 1 * num_of_two_opp
        # - (10**6) * num_of_three_opp
        - (10**8) * num_of_four_opp
        # + 1000 * count_potential_future_wins(board, player)
        # -10000 * count_potential_future_wins(board, player % 2+1)
    )
def count_window(board, window, player):
    number_of_windows = 0
    # Hirozontal windows
    for i in range(6):
        for j in range(7 - window + 1):
            if board[i][j: j + window].count(player) == window and board[i][j: j + window].count(player%2+1)==0:
                number_of_windows += 1
    # Vertical windows
    for i in range(6 - window + 1):
        for j in range(7):
            arr=[board[i + k][j] for k in range(window)]
            if arr.count(player) == window and arr.count(player%2+1)==0:
                number_of_windows += 1
    # Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            arr=[board[i + k][j + k] for k in range(window)]
            if arr.count(player) == window and arr.count(player%2+1)==0:
                number_of_windows += 1
    # Negative Diagonal windows
    for i in range(6 - window + 1):
        for j in range(7 - window + 1):
            arr=[board[i + window - 1 - k][j + k] for k in range(window)]
            if arr.count(player) == window and arr.count(player%2+1)==0:
                number_of_windows += 1
    return number_of_windows
def evaluate_window(window, piece):
    opponent_piece = '1' if piece == '2' else '2'
    score = 0
    if window.count('2') == 4:
        score += 100000
    elif window.count('2') == 3 and window.count('0') == 1:
        score += 100
    if window.count('2') == 2 and window.count('0') == 2:
        score += 2
    
    if window.count('1') == 4:
        score -= 10000
    elif window.count('1') == 3 and window.count('0') == 1:
        score -= 500
    elif window.count('1') == 2 and window.count('0') == 2:
        score -= 1
    return score
def score_position(state, piece):
    rows = ROW_COUNT
    cols = COLUMN_COUNT
    score = 0
    center_array = [state[r * cols + cols // 2] for r in range(rows)]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score horizontal
    for r in range(rows):
        for c in range(cols - 3):
            start = r * cols + c
            window = state[start:start + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(cols):
        for r in range(rows - 3):
            start = r * cols + c
            window = state[start:start + 4 * cols:cols]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            start = r * cols + c
            window = [state[start - i * (cols - 1)] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonals
    for r in range(3, rows):
        for c in range(3, cols):
            start = r * cols + c
            window = [state[start - i * (cols + 1)] for i in range(4)]
            score += evaluate_window(window, piece)

    return score
def is_terminal(state):
    # Check for draw
    if '0' not in state:
        return True
    return False
def minimax(state, depth, piece, maximizingPlayer, tree):
    global NODE_EXPANDED
    NODE_EXPANDED+=1
    
    if depth == 0 or is_terminal(state) :
        value = score_position(state, piece)
        return value
    valid_location = get_valid_locations(state)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "piece": piece % 2 + 1,
                    "value": 0,
                    "childs": [],}
            }
            value = max(value, minimax(
                child, depth - 1, piece % 2 + 1, False, new_dict))
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value
    else:
        value = math.inf
        for col in valid_location:

            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "piece": piece % 2 + 1,
                    "value": 0,
                    "childs": [], }
            }
            value = min(value, minimax(
                child, depth - 1, piece % 2 + 1, True, new_dict))
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value
def minimax_alpha_beta(state, depth, alpha, beta, piece, maximizingPlayer,tree):
    global NODE_EXPANDED
    NODE_EXPANDED+=1
    if depth == 0 or is_terminal(state):
        return score_position(state, piece)
    valid_location = get_valid_locations(state)
    if maximizingPlayer:
        value = -math.inf
        for col in valid_location:

            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "piece": piece % 2 + 1,
                    "value": 0,
                    "childs": [], }
            }
            value = max(
                value, minimax_alpha_beta(
                    child, depth - 1, alpha, beta, piece % 2 + 1, False,new_dict)
            )
            alpha = max(alpha, value)
            if beta <= alpha:
                break
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value
    else:
        value = math.inf
        for col in valid_location:
            child = drop_piece(state, col, piece)
            new_dict = {
                child: {
                    "depth": depth - 1,
                    "piece": piece % 2 + 1,
                    "value": 0,
                    "childs": [], }
            }

            value = min(
                value, minimax_alpha_beta(
                    child, depth - 1, alpha, beta, piece % 2 + 1, True,new_dict)
            )
            beta = min(beta, value)
            if beta <= alpha:
                break
            new_dict[child]["value"] = value
            tree[state]["childs"].append(new_dict)
        return value
def agent(grid, depth, option):
    global NODE_EXPANDED
    NODE_EXPANDED = 0
    min_tree.clear()
    state = convert_from_grid_to_string(grid)
    min_tree[state] = {
        "depth": depth,
        "piece": 1,
        "value": 0,
        "childs": [],
    }
    valid_moves = get_valid_locations(state)
    scores = dict(
        zip(
            valid_moves,
            [get_score(state, col, 2, depth, option) for col in valid_moves],
        )
    )
    max_cols = [key for key in scores.keys() if scores[key] ==
                max(scores.values())]

    # print("max cols are", max_cols)
    res = random.choice(max_cols)
    min_tree[state]["value"] = scores[res]
    return res, min_tree ,NODE_EXPANDED

def print_tree(tree, indent=0):
    state = list(tree.keys())[0]
    print("    " * indent + f"{state} | Depth: {tree[state]['depth']}, Piece: {tree[state]['piece']}, Value: {tree[state]['value']}")
    childs = tree[state]['childs']
    for child in childs:
        print_tree(child, indent+1)


board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [1, 2, 1, 2, 0, 2, 2],
    [1, 2, 2, 1, 1, 2, 1],
]

def main():
    start = time.time()
    Res=agent(board, 9, 2)
    print(Res[0] , Res[2])
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()