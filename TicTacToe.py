import copy

X = "x"
O = "o"
EMPTY = "_"

def winner(board):
    winnr = check_win(board)
    if( winnr == 1):
        return X
    elif(winnr == -1):
        return O
    else:
        return None


def new_board():
    return [["_", "_", "_"], 
            ["_", "_", "_"],
            ["_", "_", "_"]]

def draw_board(board):
    for i in range(3):
        print(board[i])
    print()    

def find_move(board):
    possible_moves = actions(board)
    curplayer = player(board)
    best_move = (-1, -1)

    if(curplayer == X):
        maxscore = -1000
        for i, j in possible_moves:
            temp_board = result(board, (i,j))
            curscore = minimax(temp_board, -1000, 1000)
            if(curscore > maxscore):
                best_move = (i, j)
                maxscore = curscore

    else:
        minscore = 1000
        for i, j in possible_moves:
            temp_board = result(board, (i,j))
            curscore = minimax(temp_board, -1000, 1000)
            if(curscore < minscore):
                best_move = (i, j)
                minscore = curscore
    return best_move

def scoring_func(board, depth):
    if(winner(board) == X):
        return 10 - depth
    elif(winner(board) == O):
        return depth - 10
    else:
        return 0

def minimax(board, alpha, beta, depth = 0):
    if(isterminal(board)):
        return scoring_func(board, depth)

    curplayer = player(board)  
    available_moves = actions(board)

    if(curplayer == X):
        maxscore = -1000
        for i, j in available_moves:
            temp_board = result(board, (i,j))
            maxscore = max(maxscore, minimax(temp_board, alpha, beta, depth=depth+1))
            alpha = max(maxscore, alpha)
            if beta<=alpha:
                break
        return maxscore

    else:
        minscore = 1000
        for i, j in available_moves:
            temp_board = result(board, (i,j))
            minscore = min(minscore, minimax(temp_board, alpha, beta, depth=depth+1)) 
            beta = min(beta, minscore)
            if beta<=alpha:
                break
        return minscore



def check_win(board):
    #check rows and columns
    for i in range(3):
        if(board[0][i] == board[1][i] == board[2][i] != EMPTY):
            return 1 if board[0][i] == X else -1
        
        if(board[i][0] == board[i][1] == board[i][2] != EMPTY):
            return 1 if board[i][0] == X else -1
    
    #check diagonals
    if(board[1][1] != EMPTY):
        if(board[0][0] == board[1][1] == board[2][2]):
            return 1 if board[1][1] == X else -1

        if(board[0][2] == board[1][1] == board[2][0]):
            return 1 if board[1][1] == X else -1    

    return 0

def isterminal(board):
    if check_win(board):
        return True

    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True               

def player(board):
    total_count = 0

    for i in range(3):
        for j in range(3):
            if(board[i][j] != EMPTY):
                total_count += 1   
    
    return X if total_count%2 == 0 else O

def actions(board):
    action_set = set()
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                action_set.add((i,j))

    return action_set

def result(board, action):
    copied_board = copy.deepcopy(board)
    (i, j) = action
    copied_board[i][j] = player(board)
    return copied_board

def main():
    choice = input("Would you like to play as X or O:").lower()
    board = new_board()

    if(choice == O):
        best_move = find_move(board)
        board = result(board, best_move)

    draw_board(board)

    while True:
        move = ""
        while True:
            move =tuple([int(x) for x in input("Enter your move:").split()])
            print(move)
            if(move in actions(board)):
                break
            else:
                print("INVALID move.\n")
            break   

        board = result(board, move)
        if(isterminal(board)):
            game_result = winner(board)
            if game_result:
                print(f"The winner is {game_result}")
            else:
                print("It is a tie")
            break   

        draw_board(board)
        print("Computer thinking...\n")

        best_move = find_move(board)
        board = result(board, best_move)
        if(isterminal(board)):
            game_result = winner(board)
            if game_result:
                print(f"The winner is {game_result}\n")
                break
            else:
                print("It is a tie")
                break
        draw_board(board)
    draw_board(board)


if __name__ == "__main__":
    main()