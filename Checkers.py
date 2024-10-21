from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import random

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

    global white_points, black_points

    if current_player == "white":
        if checker_row == 6:
            board[checker_row][checker_column] = " "  # Czyści aktualnie zajmowane pole
            board[checker_row + 1][checker_column - 1] = " "  # Wypełnia nowe pole (ruch w lewo)
            print("DOTARŁEŚ DO KOŃCA PLANSZY, ZDOBYWASZ PUNKT")
            white_points += 1
        match move_direction:
            case "left":
                if board[checker_row + 1][checker_column - 1] == "W":
                    print("Nie można poruszyć się tym pionkiem w lewo, ponieważ stoi już tam Twój inny pionek")
                    game_loop(board, current_player)
                if board[checker_row + 1][checker_column - 1] == "B":  # Sprawdź zbicie
                    board[checker_row + 1][checker_column - 1] = "W"  # Zbij pionka
                    board[checker_row][checker_column] = " "
                    white_points += 1
                    print("Zdobywasz punkt")
                else:
                    board[checker_row][checker_column] = " "  # Czyści aktualnie zajmowane pole
                    board[checker_row + 1][checker_column - 1] = "W"  # Wypełnia nowe pole (ruch w lewo)
            case "right":
                if board[checker_row + 1][checker_column + 1] == "W":
                    print("Nie można poruszyć się tym pionkiem w prawo, ponieważ stoi już tam Twój inny pionek")
                    game_loop(board, current_player)
                if board[checker_row + 1][checker_column + 1] == "B":  # Sprawdź zbicie
                    board[checker_row + 1][checker_column + 1] = "W"  # Zbij pionka
                    board[checker_row][checker_column] = " "
                    white_points += 1
                    print("Zdobywasz punkt")
                else:
                    board[checker_row][checker_column] = " "  # Czyści aktualnie zajmowane pole
                    board[checker_row + 1][checker_column + 1] = "W"  # Wypełnia nowe pole (ruch w prawo)
    elif current_player == "black":
        if checker_row == 1:
            board[checker_row][checker_column] = " "  # Czyści aktualnie zajmowane pole
            print("DOTARŁEŚ DO KOŃCA PLANSZY, ZDOBYWASZ PUNKT")
            black_points += 1
        match move_direction:
            case "left":
                if board[checker_row - 1][checker_column - 1] == "B":
                    print("Nie można poruszyć się tym pionkiem w lewo, ponieważ stoi już tam Twój inny pionek")
                    game_loop(board, current_player)
                if board[checker_row - 1][checker_column - 1] == "W":  # Sprawdź zbicie
                    board[checker_row - 1][checker_column - 1] = "B"  # Zbij pionka
                    board[checker_row][checker_column] = " "
                    black_points += 1
                    print("Zdobywasz punkt")
                else:
                    board[checker_row][checker_column] = " "
                    board[checker_row - 1][checker_column - 1] = "B"
            case "right":
                if board[checker_row - 1][checker_column + 1] == "B":
                    print("Nie można poruszyć się tym pionkiem w prawo, ponieważ stoi już tam Twój inny pionek")
                    game_loop(board, current_player)
                if board[checker_row - 1][checker_column + 1] == "W":  # Sprawdź zbicie
                    board[checker_row - 1][checker_column + 1] = "B"  # Zbij pionka
                    board[checker_row][checker_column] = " "
                    black_points += 1
                    print("Zdobywasz punkt")
                else:
                    board[checker_row][checker_column] = " "
                    board[checker_row - 1][checker_column + 1] = "B"

def choose_and_validate_move(board, current_player):
    checker = "W" if current_player == "white" else "B"

    position_row = sorted(set(
        row for row in range(len(board))
        for col in range(len(board[row])) if board[row][col] == checker
    ))

    print("Wybierz pionka: ")

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

def game_loop(board, current_player):

    print(f"Ruch gracza: {current_player}")
    direction, x, y = choose_and_validate_move(board, current_player)
    move(board, current_player, direction, x, y)
    print_board(board)

    current_player = "black" if current_player == "white" else "white"
    # Zamień gracza po każdym ruchu
    return current_player

def main():
    global white_points, black_points
    white_points = 0
    black_points = 0
    board = make_board()
    print_board(board)
    current_player = random.choice(["white", "black"])

    while True:
        current_player = game_loop(board, current_player)
        if not any('W' in row for row in board) or not any('B' in row for row in board):
            if white_points > black_points:
                print("GRACZ Z BIAŁYMI PIONKAMI WYGRYWA")
                break
            else:
                print("GRACZ Z CZARNYMI PIONKAMI WYGRYWA")
                break


if __name__ == '__main__':
    main()