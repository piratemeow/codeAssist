
import random
import sys

def print_board(board):
    for row in board:
        print("|".join(row))
    print("-" * 7)

def check_win(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_player_move(board, player, args):
    if args:
        try:
            move_str = args.pop(0)
            row, col = map(int, move_str.split())
            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
                return row, col
            else:
                print(f"Invalid move provided: {move_str}. Player {player} cannot make this move.")
                sys.exit(1) # Exit if move is invalid
        except (ValueError, IndexError):
            print(f"Invalid argument format: {args[0] if args else 'empty'}. Player {player} needs valid row and col.")
            sys.exit(1) # Exit if argument format is invalid
    else:
        while True:
            try:
                move_str = input(f"Player {player}, enter your move (row and column, e.g., '0 0'): ")
                row, col = map(int, move_str.split())
                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
                    return row, col
                else:
                    print("This move is not valid. Try again.")
            except ValueError:
                print("Invalid input. Please enter row and column as numbers separated by a space.")

def get_computer_move(board, player):
    print(f"Player {player} (computer) is thinking...")
    
    # 1. Check if computer can win in the next move
    for r in range(2, -1, -1):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = player
                if check_win(board, player):
                    board[r][c] = " "  # backtrack
                    return r, c
                board[r][c] = " "  # backtrack

    # 2. Check if player can win in the next move and block it
    opponent = "X" if player == "O" else "O"
    for r in range(2, -1, -1):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = opponent
                if check_win(board, opponent):
                    board[r][c] = " " # backtrack
                    return r, c
                board[r][c] = " "  # backtrack

    # 3. Try to take the center if available
    if board[1][1] == " ":
        return 1, 1

    # 4. Try to take a corner if available
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = [corner for corner in corners if board[corner[0]][corner[1]] == " "]
    if available_corners:
        return random.choice(available_corners)

    # 5. Take any available side
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    available_sides = [side for side in sides if board[side[0]][side[1]] == " "]
    if available_sides:
        return random.choice(available_sides)

    # Should not reach here if there are empty cells, but as a fallback
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                return r, c

def play_game(player_moves=None):
    if player_moves is None:
        player_moves = [] # Ensure it's a mutable list

    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    random.shuffle(players)
    
    player_order = players[0]
    computer_order = players[1]

    print(f"Player X goes first, Player O goes second.")
    print(f"You are Player {player_order}. The computer is Player {computer_order}.")

    current_player = "X"
    move_count = 0
    total_cells = 9

    while True:
        print_board(board)
        if current_player == player_order:
            row, col = get_player_move(board, current_player, player_moves)
        else:
            row, col = get_computer_move(board, current_player)
        
        board[row][col] = current_player
        move_count += 1

        if check_win(board, current_player):
            print_board(board)
            if current_player == player_order:
                print("Congratulations! You win!")
            else:
                print("Computer wins!")
            return "win" # Indicate game result
        
        if move_count == total_cells and not check_win(board, current_player):
            print_board(board)
            print("It's a draw!")
            return "draw" # Indicate game result
        
        current_player = "O" if current_player == "X" else "X"
    return "ongoing" # Should not be reached in normal play

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Moves are provided as command line arguments
        moves_from_args = sys.argv[1:]
        play_game(moves_from_args)
    else:
        # Interactive mode
        while True:
            result = play_game()
            if result == "win" or result == "draw":
                play_again = input("Play again? (yes/no): ").lower()
                if play_again != "yes":
                    break
        print("Thanks for playing!")

