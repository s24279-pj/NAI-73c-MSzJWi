from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

def make_board():
    board = [['0'] * 8 for _ in range(8)]

    for row in [0, 1, 2]:
        for col in range(8):
            if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                board[row][col] = 'W'

    for row in [5, 6, 7]:
        for col in range(8):
            if (col % 2 == 0 and row % 2 == 1) or (col % 2 == 1 and row % 2 == 0):
                board[row][col] = 'B'

    return board

def print_board(board):
    print('   ',*range(8))
    print('  ',' -'*8) # Wydrukowanie indeksów kolumn
    for i in range(len(board)):
        print(i, '|', ' '.join(board[i])) #drukowanie wierszy wraz z ich indeksami


def main():
    board = make_board()
    print_board(board)

if __name__ == '__main__':
    main()
