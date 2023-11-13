def minmax_heuristic(board, player):
    num_of_four = count_window(board,4,player)
    num_of_three= count_window(board,3,player)
    num_of_two= count_window(board,2,player)

    num_of_four_opp = count_window(board,4,player%2+1)
    num_of_three_opp= count_window(board,3,player%2+1)
    num_of_two_opp= count_window(board,2,player%2+1)
    print(
        "num_of_four: ", num_of_four,
        "num_of_three: ", num_of_three,
        "num_of_two: ", num_of_two,
        "num_of_four_opp: ", num_of_four_opp,
        "num_of_three_opp: ", num_of_three_opp,
        "num_of_two_opp: ", num_of_two_opp
    )

    if num_of_four == 0 and num_of_three == 0 and num_of_two == 0 and num_of_four_opp == 0 and num_of_three_opp == 0 and num_of_three == 0 and num_of_two_opp == 0:
        return 0
    return (10**6)*num_of_four+100*num_of_three+num_of_two-num_of_two_opp-100*num_of_three_opp-(10**6)*num_of_four_opp

def count_window(board,window,player):
    number_of_windows=0
    #Hirozontal windows
    for i in range(6):
        for j in range(7-window+1):
            if board[i][j:j+window].count(player)==window:
                number_of_windows+=1
    #Vertical windows
    for i in range(6-window+1):
        for j in range(7):
            if [board[i+k][j] for k in range(window)].count(player)==window:
                number_of_windows+=1
    #Diagonal windows
    for i in range(6-window+1):
        for j in range(7-window+1):
            if [board[i+k][j+k] for k in range(window)].count(player)==window:
                number_of_windows+=1
    #Negative Diagonal windows
    for i in range(6-window+1):
        for j in range(7-window+1):
            if [board[i+window-1-k][j+k] for k in range(window)].count(player)==window:
                number_of_windows+=1
    return number_of_windows



board=[ [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 2, 2, 0],
        [0, 0, 0, 2, 1, 1, 0],
        [0, 1, 2, 1, 2, 2, 2]]
def main():
    print(minmax_heuristic(board,2))
if __name__ == "__main__":
    main()
