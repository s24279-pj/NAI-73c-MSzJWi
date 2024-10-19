from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

def make_board():
    board = [[' '] * 8 for _ in range(8)]

    for row in [0, 1, 2]:
        for col in range(8):
            if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                board[row][col] = 'W'

    for row in [5, 6, 7]:
        for col in range(8):
            if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                board[row][col] = 'B'

    return board

def print_board(board):
    print('   ',*range(8))
    print('  ',' -'*8) # Wydrukowanie indeksów kolumn
    for i in range(len(board)):
        print(i, '|', ' '.join(board[i])) #drukowanie wierszy wraz z ich indeksami

def move(board, current_player, move_direction, checker_row, checker_column):

    if current_player == "white":
        match move_direction:
            case "left":
                board[checker_row][checker_column] = " "  # Czyści aktualnie zajmowane pole
                board[checker_row + 1][checker_column - 1] = "W"  # Wypełnia nowe pole (ruch w lewo)
            case "right":
                board[checker_row][checker_column] = " "  # Czyści aktualnie zajmowane pole
                board[checker_row + 1][checker_column + 1] = "W"  # Wypełnia nowe pole (ruch w prawo)
    elif current_player == "black":
        match move_direction:
            case "left":
                board[checker_row][checker_column] = " "
                board[checker_row - 1][checker_column - 1] = "B"
            case "right":
                board[checker_row][checker_column] = " "
                board[checker_row - 1][checker_column + 1] = "B"


def choose_and_validate_move(board, current_player, move_count_w, move_count_b):
    checker = "W" if current_player == "white" else "B"
    move_count = move_count_w if current_player == "white" else move_count_b

    position_row = sorted(set(
        row for row in range(len(board))
        for col in range(len(board[row])) if board[row][col] == checker
    ))

    print("Wybierz pionka: ")

    if current_player == "white":
        if move_count == 0:  # Sprawdzenie, czy to pierwszy ruch
            print("Dostępne wiersze (X):", max(position_row))
            while True:
                x = int(input("X (boczne wartości) z możliwych do wyboru: "))
                if x == max(position_row):
                    break
        else:
            print("Dostępne wiersze (X):", position_row)
            while True:
                x = int(input("X (boczne wartości) z możliwych do wyboru: "))
                if x in position_row:
                    break
    elif current_player == "black":
        if move_count == 0:  # Sprawdzenie, czy to pierwszy ruch
            print("Dostępne wiersze (X):", min(position_row))
            while True:
                x = int(input("X (boczne wartości) z możliwych do wyboru: "))
                if x == min(position_row):
                    break
        else:
            print("Dostępne wiersze (X):", position_row)
            while True:
                x = int(input("X (boczne wartości) z możliwych do wyboru: "))
                if x in position_row:
                    break

    position_col = sorted(set(
        col for col in range(len(board[x])) if board[x][col] == checker
    ))

    print("Dostępne kolumny (Y):", position_col)
    while True:
        y = int(input("Y (górne wartości) z możliwych do wyboru: "))
        if y in position_col:
            break

    print("Wybierz kierunek ruchu: ")
    while True:
        direction = input("left/right: ")
        if direction == "left" and y == 0:
            print("Nie można poruszyć się w lewo, wyjście poza plansze")
        elif direction == "right" and y == 7:
            print("Nie można poruszyć się w prawo, wyjście poza plansze")
        elif direction in ["left", "right"]:
            break

    return direction, x, y


def main():
    board = make_board()
    print_board(board)
    move_count_w = 0  # Licznik ruchów dla białego gracza
    move_count_b = 0  # Licznik ruchów dla czarnego gracza
    current_player = "white"

    while True:  # Pętla gry
        print(f"Ruch gracza: {current_player}")
        direction, x, y = choose_and_validate_move(board, current_player, move_count_w, move_count_b)
        move(board, current_player, direction, x, y)
        print_board(board)

        # Zwiększ licznik ruchów
        if current_player == "white":
            move_count_w += 1
        else:
            move_count_b += 1

        # Zamień gracza po każdym ruchu
        current_player = "black" if current_player == "white" else "white"


if __name__ == '__main__':
    main()