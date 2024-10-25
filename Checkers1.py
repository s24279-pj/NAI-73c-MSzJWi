## WELCOME to simplified Checkers game.
# Rules and instruction you can find here: https://github.com/s24279-pj/NAI-73c-MSzJWi
# Have fun.

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

def make_board(): # Początkowe ustawienie pionków na planszy
    """Inicjalizuje i zwraca początkową planszę do gry z rozmieszczeniem pionków:
    'W' dla gracza białego i 'B' dla gracza czarnego.
    """
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
    """Wyświetla planszę do gry wraz z indeksami kolumn i wierszy.
    
    Args:
        board (list): Plansza do gry, reprezentowana jako lista list.
    """
    print('   ',*range(8))
    print('  ',' -'*8) # Wydrukowanie indeksów kolumn
    for i in range(len(board)):
        print(i, '|', ' '.join(board[i])) #drukowanie wierszy wraz z ich indeksami


class Checkers(TwoPlayerGame):
    def __init__(self, players):
        """Inicjalizuje grę w warcaby z początkowym ustawieniem planszy,
        punktacją i wyznaczeniem obecnego gracza.
        
        Args:
            players (list): Lista graczy, zawierająca gracza człowieka oraz AI.
        """
        self.players = players
        self.board = make_board()
        self.current_player = 1
        self.white_points = 0
        self.black_points = 0

    def show(self):
        """Wyświetla bieżący stan planszy oraz aktualną punktację dla obu graczy."""

        print_board(self.board)
        print(f"Punkty: Białego gracza: {self.white_points}, Czarnego gracza: {self.black_points}")
    
    def possible_moves(self):
        """Generuje i zwraca listę dostępnych ruchów dla obecnego gracza.
        
        Returns:
            list: Lista dostępnych ruchów w formacie (kierunek, x, y).
        """
        moves = []
        checker = 'W' if self.current_player == 1 else 'B'
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == checker:
                    if self.can_move_left(x, y):
                        moves.append(("left", x, y))
                    if self.can_move_right(x, y):
                        moves.append(("right", x, y))
        return moves

    def can_move_left(self, x, y):
        """Sprawdza, czy obecny gracz może wykonać ruch w lewo z podanej pozycji.
        
        Args:
            x (int): Współrzędna wiersza.
            y (int): Współrzędna kolumny.
            
        Returns:
            bool: True, jeśli ruch w lewo jest możliwy, False w przeciwnym razie.
        """
        if self.current_player == 1:  # Gracz biały
            if y > 1 and x < 6 and self.board[x + 2][y - 2] == ' ' and self.board[x + 1][y - 1] == 'B':
                return True
            if y > 0 and self.board[x + 1][y - 1] == ' ':
                return True
        else:  # Gracz czarny
            if y > 1 and x > 1 and self.board[x - 2][y - 2] == ' ' and self.board[x - 1][y - 1] == 'W':
                return True
            if y > 0 and self.board[x - 1][y - 1] == ' ':
                return True
        return False

    def can_move_right(self, x, y):
        """Sprawdza, czy obecny gracz może wykonać ruch w prawo z podanej pozycji.
        
        Args:
            x (int): Współrzędna wiersza.
            y (int): Współrzędna kolumny.
            
        Returns:
            bool: True, jeśli ruch w prawo jest możliwy, False w przeciwnym razie.
        """
        if self.current_player == 1:  # Gracz biały
            if y < 6 and x < 6 and self.board[x + 1][y + 1] == 'B' and self.board[x + 2][y + 2] == ' ':
                return True
            if y < 7 and self.board[x + 1][y + 1] == ' ':
                return True
        else:  # Gracz czarny
            if y < 6 and x > 1 and self.board[x - 1][y + 1] == 'W' and self.board[x - 2][y + 2] == ' ':
                return True
            if y < 7 and self.board[x - 1][y + 1] == ' ':
                return True
        return False

    # wykonanie ruchu, przekazując zbior ruchow move[]
    def make_move(self, move):
        """Wykonuje ruch pionka zgodnie z określonym kierunkiem i pozycją początkową.
        
        Args:
            move (tuple): Krotka zawierająca kierunek ruchu ('left' lub 'right') oraz współrzędne (x, y).
        """
        direction, x, y = move
        if direction == "left":
            if self.current_player == 1 and y > 1 and self.board[x + 1][y - 1] == 'B' and self.board[x + 2][y - 2] == ' ':
                self.board[x + 1][y - 1] = " "
                self.move_piece(x, y, x + 2, y - 2)
                self.white_points += 1  # Punkt za zbicie przeciwnika
            elif self.current_player == 2 and y > 1 and self.board[x - 1][y - 1] == 'W' and self.board[x - 2][y - 2] == ' ':
                self.board[x - 1][y - 1] = " "
                self.move_piece(x, y, x - 2, y - 2)
                self.black_points += 1  # Punkt za zbicie przeciwnika
            else:
                self.move_piece(x, y, x + (1 if self.current_player == 1 else -1), y - 1)

        elif direction == "right":
            if self.current_player == 1 and y < 6 and self.board[x + 1][y + 1] == 'B' and self.board[x + 2][y + 2] == ' ':
                self.board[x + 1][y + 1] = " "
                self.move_piece(x, y, x + 2, y + 2)
                self.white_points += 1  # Punkt za zbicie przeciwnika
            elif self.current_player == 2 and y < 6 and self.board[x - 1][y + 1] == 'W' and self.board[x - 2][y + 2] == ' ':
                self.board[x - 1][y + 1] = " "
                self.move_piece(x, y, x - 2, y + 2)
                self.black_points += 1  # Punkt za zbicie przeciwnika
            else:
                self.move_piece(x, y, x + (1 if self.current_player == 1 else -1), y + 1)

    #funkcja zmieniajaca polozenie pionka na tablicy
    def move_piece(self, old_x, old_y, new_x, new_y):
        """Przesuwa pionek na nowe miejsce na planszy, dodaje punkt za dotarcie na koniec planszy.
        
        Args:
            old_x (int): Poprzednia współrzędna wiersza.
            old_y (int): Poprzednia współrzędna kolumny.
            new_x (int): Nowa współrzędna wiersza.
            new_y (int): Nowa współrzędna kolumny.
        """
        checker = 'W' if self.current_player == 1 else 'B'

        # Sprawdzenie, czy dochodzimy do końca planszy
        if (self.current_player == 1 and new_x == 7) or (self.current_player == 2 and new_x == 0):
            if self.current_player == 1:
                self.white_points += 1
            else:
                self.black_points += 1

        self.board[old_x][old_y] = ' '  # Czyszczenie starego pola
        self.board[new_x][new_y] = checker  # Przesunięcie pionka

    #pobranie aktualnego gracza
    def get_current_player(self):
        """Zwraca aktualnego gracza jako biały lub czarny.
        
        Returns:
            str: 'white' dla gracza białego, 'black' dla gracza czarnego.
        """
        return "white" if self.current_player == 1 else "black"
    
    def is_over(self):
        """Sprawdza, czy gra dobiegła końca (brak pionków przeciwnika lub możliwych ruchów).
        
        Returns:
            bool: True, jeśli gra się skończyła, False w przeciwnym razie.
        """
        return not self.possible_moves() or \
            not any('W' in row for row in self.board) or \
            not any('B' in row for row in self.board)

    def scoring(self):
        """Oblicza wynik gry na podstawie liczby punktów każdego gracza.
        
        Returns:
            int: Różnica punktów między graczami.
        """
        return self.white_points - self.black_points

    def play(self):
        """Rozpoczyna rozgrywkę w trybie naprzemiennego wykonywania ruchów gracza człowieka i AI.
        Wyświetla wyniki na zakończenie gry.
        """
        print_board(self.board)
        while not self.is_over():
            print(f"Ruch gracza: {'Biały' if self.current_player == 1 else 'Czarny'}")
            if self.current_player == 1:  # Gracz człowiek, białe pionki
                available_moves = self.possible_moves()
                print("Dostępne ruchy:")
                for i, move in enumerate(available_moves):
                    direction, x, y = move
                    print(f"{i + 1}: Pionek na ({x}, {y}), ruch w {direction}")
                while True:
                    move_index = input("Wybierz numer ruchu: ")
                    if move_index.isdigit() and 0 < int(move_index) < len(available_moves):
                        move_index = int(move_index) - 1
                        break
                    else:
                        print("Nieprawidłowy numer ruchu. Wybierz ponownie.")
                self.make_move(available_moves[move_index])
            else:  # Gracz AI
                move = self.players[1].ask_move(self)
                self.make_move(move)

            self.show()
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1


if __name__ == "__main__":
    ai_algo = Negamax(3)
    game = Checkers([Human_Player(), AI_Player(ai_algo)])
    game.play()


    if game.white_points > game.black_points:
        print("GRACZ Z BIAŁYMI PIONKAMI WYGRYWA")
    else:
        print("GRACZ Z CZARNYMI PIONKAMI WYGRYWA")
