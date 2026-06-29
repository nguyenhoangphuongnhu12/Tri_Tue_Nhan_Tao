import tkinter as tk

class CaroAlphaBetaDetailed:
    def __init__(self, root):
        self.root = root
        self.root.title("Alpha-Beta Detailed Log")
        self.board = [' ' for _ in range(9)]
        self.turn = 'X'
        
        # --- UI Setup ---
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)
        
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.grid(row=0, column=0)
        
        self.buttons = [tk.Button(self.board_frame, text='', font=('Arial', 20), width=5, height=2, state=tk.DISABLED) 
                        for _ in range(9)]
        for i, btn in enumerate(self.buttons):
            btn.grid(row=i//3, column=i%3)
            
        self.log_text = tk.Text(main_frame, width=60, height=20)
        self.log_text.grid(row=0, column=1, padx=10)
        
        self.result_label = tk.Label(root, text="Bắt đầu...", font=('Arial', 14, 'bold'), fg='blue')
        self.result_label.pack(pady=10)
        
        self.root.after(1000, self.play_turn)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def check_winner(self, b):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for c in win_coords:
            if b[c[0]] == b[c[1]] == b[c[2]] and b[c[0]] != ' ': return b[c[0]]
        return 'Tie' if ' ' not in b else None

    def minimax_ab(self, b, depth, alpha, beta, is_maximizing):
        winner = self.check_winner(b)
        if winner == 'X': return 10 - depth
        if winner == 'O': return depth - 10
        if winner == 'Tie': return 0

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'X'
                    eval = self.minimax_ab(b, depth + 1, alpha, beta, False)
                    b[i] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    # Log chi tiết giá trị alpha/beta tại nút này
                    if beta <= alpha:
                        self.log(f"   [CẮT TỈA] depth {depth}: beta({beta}) <= alpha({alpha})")
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'O'
                    eval = self.minimax_ab(b, depth + 1, alpha, beta, True)
                    b[i] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        self.log(f"   [CẮT TỈA] depth {depth}: beta({beta}) <= alpha({alpha})")
                        break
            return min_eval

    def play_turn(self):
        winner = self.check_winner(self.board)
        if winner:
            self.result_label.config(text=f"Kết quả: {winner if winner != 'Tie' else 'Hòa!'}")
            return

        best_score = -float('inf') if self.turn == 'X' else float('inf')
        move = -1
        
        self.log(f"--- Lượt {self.turn} (Alpha-Beta) ---")
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.turn
                # Truyền alpha/beta vào hàm tính toán
                score = self.minimax_ab(self.board, 0, -float('inf'), float('inf'), self.turn == 'O')
                self.board[i] = ' '
                self.log(f"Thử ô {i}, Score dự đoán: {score}")
                
                if self.turn == 'X':
                    if score > best_score: best_score, move = score, i
                else:
                    if score < best_score: best_score, move = score, i
        
        self.board[move] = self.turn
        self.buttons[move].config(text=self.turn)
        self.log(f"-> Chốt ô {move} (Score: {best_score})\n")
        
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.root.after(800, self.play_turn)

root = tk.Tk()
game = CaroAlphaBetaDetailed(root)
root.mainloop()