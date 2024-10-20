from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

def make_board(): # Początkowe ustawienie pionków na planszy
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

## TO-DO
#logika poruszania się po planszy. --- do dodania jeszcze atak tutaj, czyli co się stanie, jak napotkasz innego pionka
def move(board, current_player, move_direction, checker_row, checker_column):
    if current_player == "white":
        if move_direction == "left":
            board[checker_row][checker_column] = " "  # Czyści pole
            board[checker_row + 1][checker_column - 1] = "W"  # Przesuwa się w lewo
        elif move_direction == "right":
            board[checker_row][checker_column] = " " 
            board[checker_row + 1][checker_column + 1] = "W"  # Przesuwa się w prawo
    elif current_player == "black":
        if move_direction == "left":
            board[checker_row][checker_column] = " "
            board[checker_row - 1][checker_column - 1] = "B"
        elif move_direction == "right":
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

class Checkers(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.board = make_board()
        self.current_player = 1
    
    #TO-DO chyba tutaj tez trzeba dodać atak
    # lista dostępnych ruchów dla AI
    def possible_moves(self):
        moves = []
        #ustawia literke gracza, zaleznie, który został wybrany
        current_player = 'W' if self.current_player == 1 else 'B'
        #direction - zmienna okreslająca, w która stone wykona się ruch, zalenie od gracza
        direction = 1 if self.current_player == 1 else -1
    
        #iteracja po kadym polu planszy
        for row in range(8):
            for col in range(8):
                #jeśli trafi na pole z oznaczeniem obecnego gracza
                if self.board[row][col] == current_player:
                    #sprawdza, czy mozliwy jest ruch w lewo
                    if col > 0 and self.board[row + direction][col - 1] == ' ':
                        moves.append((row, col, "left"))
                    #sprawdza, czy mozliwy jest ruch w prawo
                    if col < 7 and self.board[row + direction][col + 1] == ' ':
                        moves.append((row, col, "right"))

        return moves

    # wykonanie ruchu, przekazując funkcję move()
    def make_move(self, move):
        #sprawdzay, który gracz wykonuje ruch
        if isinstance(self.players[self.current_player - 1], AI_Player):
            #jesli AI, przekazuje do move "zapakowane" ponizsze zmienne 
            checker_row, checker_column, move_direction = move
        else:
            #jesli czlowiek, przekazuje te same zmienne do funcji walidujacej ruch gracza
            move_direction, checker_row, checker_column = choose_and_validate_move(self.board, self.get_current_player())

        #przypisanie aktuyalnego gracza do zmiennej
        current_player = "white" if self.current_player == 1 else "black"
        
        #wykonanie logiki ruchu z naszej funkcji move()
        move(self.board, current_player, move_direction, checker_row, checker_column)

    #pobranie aktualnego gracza
    def get_current_player(self):
        return "white" if self.current_player == 1 else "black"
    
    #koniec gry jest wtedy, gdy nie ma mozliwych ruchów
    def is_over(self):

    #liczy ilość pozostalych pionków - wygra ten co ma wiecej
    def scoring():
    
    #wyswietla plansze -- trzeba będzie jakoś ją wyświetlić po ruchu
    def show(self):
        print_board(self.board)


if __name__ == "__main__":
    ai_algo = Negamax(3)
    game = Checkers([Human_Player(), AI_Player(ai_algo)])
    game.play()
