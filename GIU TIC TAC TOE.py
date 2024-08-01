import tkinter as tk
from tkinter import messagebox

# Initialize the board and current player
board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

# Set these variables to define the player and AI symbols
player_symbol = 'O'  # The symbol for the human player
ai_symbol = 'X'      # The symbol for the AI

def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_draw(board):
    return all([cell != ' ' for row in board for cell in row])

def minimax(board, depth, is_maximizing, player, opponent):
    if check_winner(board, player):
        return 10 - depth
    if check_winner(board, opponent):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score = minimax(board, depth + 1, False, player, opponent)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = opponent
                    score = minimax(board, depth + 1, True, player, opponent)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def find_best_move(board, player, opponent):
    best_move = None
    best_score = float('-inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player
                score = minimax(board, 0, False, player, opponent)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def make_move(row, col):
    global current_player
    if board[row][col] == ' ' and not game_ended:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        if check_winner(board, current_player):
            messagebox.showinfo("Game Over", f"{current_player} wins!")
            disable_buttons()
            return
        if is_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
            return
        current_player = player_symbol if current_player == ai_symbol else ai_symbol
        if current_player == ai_symbol:
            status_label.config(text="AI's Turn")
            root.after(500, ai_move)  # Schedule AI move after 500 ms delay
        else:
            status_label.config(text="Your Turn")

def ai_move():
    move = find_best_move(board, ai_symbol, player_symbol)
    if move:
        row, col = move
        board[row][col] = ai_symbol
        buttons[row][col].config(text=ai_symbol)
        if check_winner(board, ai_symbol):
            messagebox.showinfo("Game Over", "AI wins!")
            disable_buttons()
            return
        if is_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
            return
        global current_player
        current_player = player_symbol
        status_label.config(text="Your Turn")

def disable_buttons():
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.DISABLED)

def reset_board():
    global board, current_player, game_ended
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    current_player = player_symbol
    game_ended = False
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', state=tk.NORMAL)

def create_gui():
    global buttons, status_label, current_player, root, game_ended
    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    status_label = tk.Label(root, text="Your Turn")
    status_label.pack()

    frame = tk.Frame(root)
    frame.pack()

    buttons = [[None]*3 for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(frame, text=' ', width=15, height=8, command=lambda r=row, c=col: make_move(r, c))
            buttons[row][col].grid(row=row, column=col)

    # Initialize game state
    global current_player, game_ended
    current_player = player_symbol
    game_ended = False

    # If AI starts the game
    if current_player == ai_symbol:
        root.after(500, ai_move)

    root.mainloop()

# Start the GUI
create_gui()
