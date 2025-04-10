import os

FILENAME = "game_state.txt"

positions_map = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2),
}

# color
class Colors:
    X = "\033[94m"  # Blue
    O = "\033[91m"  # Red
    END = "\033[0m"

def colored(symbol):
    if symbol == "X":
        return f"{Colors.X}{symbol}{Colors.END}"
    elif symbol == "O":
        return f"{Colors.O}{symbol}{Colors.END}"
    return " "

def display_board(board):
    print("\n   TIC TAC TOE")
    print("   Positions:")
    print("    1 | 2 | 3")
    print("   -----------")
    print("    4 | 5 | 6")
    print("   -----------")
    print("    7 | 8 | 9\n")

    print("   Game Board:")
    for i, row in enumerate(board):
        row_display = " | ".join(colored(cell) if cell != "-" else " " for cell in row)
        print(f"    {row_display}")
        if i < 2:
            print("   -----------")
    print()

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in zip(*board):
        if all(cell == player for cell in col):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != "-" for row in board for cell in row)

def save_game(board, player_symbol, player_turn):
    with open(FILENAME, 'w') as f:
        for row in board:
            f.write("".join(row) + "\n")
        f.write(f"{player_symbol}\n")
        f.write(f"Player Turn: {player_turn}\n")
        f.write("N\n")
    print("\n💾 Game state saved! Come back soon.\n")

def load_game():
    if not os.path.exists(FILENAME):
        print("🚫 No saved game found. Starting a new game.\n")
        return None

    with open(FILENAME, 'r') as f:
        lines = f.read().splitlines()
        board = [list(lines[i]) for i in range(3)]
        current_symbol = lines[3]
        turn_line = lines[4]
        player_turn = int(turn_line.split(":")[1].strip())

    print("✅ Game loaded successfully!\n")
    return board, current_symbol, player_turn

def start_new_game():
    board = [["-" for _ in range(3)] for _ in range(3)]
    current_symbol = "X"
    player_turn = 1
    return board, current_symbol, player_turn

def play_game():
    print("🎮 Welcome to Tic Tac Toe!")
    print("Player 1: " + Colors.X + "X" + Colors.END)
    print("Player 2: " + Colors.O + "O" + Colors.END + "\n")

    choice = input("📂 Do you want to load the previous game? (y/n): ").strip().lower()
    if choice == 'y':
        loaded = load_game()
        if loaded:
            board, current_symbol, player_turn = loaded
        else:
            board, current_symbol, player_turn = start_new_game()
    else:
        board, current_symbol, player_turn = start_new_game()

    while True:
        display_board(board)
        try:
            move = int(input(f"🧠 Player {player_turn} ({colored(current_symbol)}), choose a move (1-9) or 0 to save and quit: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1 and 9.")
            continue

        if move == 0:
            save_game(board, current_symbol, player_turn)
            break

        if move not in positions_map:
            print("🚫 Invalid move. Choose a position from 1 to 9.")
            continue

        row, col = positions_map[move]
        if board[row][col] != "-":
            print("⚠ That cell is already taken. Try another.")
            continue

        board[row][col] = current_symbol

        if check_winner(board, current_symbol):
            display_board(board)
            print(f"🎉 Player {player_turn} ({colored(current_symbol)}) wins! Congrats!")
            if os.path.exists(FILENAME):
                os.remove(FILENAME)
            break

        if is_draw(board):
            display_board(board)
            print("🤝 It's a draw! Good game!")
            if os.path.exists(FILENAME):
                os.remove(FILENAME)
            break

        # Switching players
        current_symbol = "O" if current_symbol == "X" else "X"
        player_turn = 2 if player_turn == 1 else 1

    print("👋 Thanks for playing!\n")

if __name__ == "__main__":
   play_game()

