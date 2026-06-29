# https://github.com/nguyenhoangphuongnhu12/Tri_Tue_Nhan_Tao
# Nguyễn Hoàng Phương Như - 24110042
# THUẬT TOÁN MINIMAX

import tkinter as tk

class CaroAIvsAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI vs AI - Minimax Log")
        self.board = [' ' for _ in range(9)]
        self.turn = 'X'  # X đi trước
        
        # --- Giao diện ---
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)
        
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.grid(row=0, column=0)
        
        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text='', font=('Arial', 20), width=5, height=2, state=tk.DISABLED)
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
            
        self.log_text = tk.Text(main_frame, width=45, height=15)
        self.log_text.grid(row=0, column=1, padx=10)
        
        self.result_label = tk.Label(root, text="Đang bắt đầu...", font=('Arial', 14, 'bold'), fg='blue')
        self.result_label.pack(pady=10)
        
        # Bắt đầu game tự động sau 1 giây
        self.root.after(1000, self.play_turn)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def check_winner(self, b):
        win_coords = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for c in win_coords:
            if b[c[0]] == b[c[1]] == b[c[2]] and b[c[0]] != ' ': return b[c[0]]
        return 'Tie' if ' ' not in b else None

    def minimax(self, b, depth, is_maximizing):
        winner = self.check_winner(b)
        if winner == 'X': return 10 - depth
        if winner == 'O': return depth - 10
        if winner == 'Tie': return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'X'
                    score = self.minimax(b, depth + 1, False)
                    b[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'O'
                    score = self.minimax(b, depth + 1, True)
                    b[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def play_turn(self):
        winner = self.check_winner(self.board)
        if winner:
            self.result_label.config(text=f"Kết quả: {winner if winner != 'Tie' else 'Hòa!'}")
            return

        best_score = -float('inf') if self.turn == 'X' else float('inf')
        move = -1
        
        self.log(f"--- Đến lượt {self.turn} ---")
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.turn
                score = self.minimax(self.board, 0, self.turn == 'O')
                self.board[i] = ' '
                self.log(f"Thử ô {i}, Score dự đoán: {score}")
                
                if self.turn == 'X':
                    if score > best_score: best_score, move = score, i
                else:
                    if score < best_score: best_score, move = score, i
        
        # Thực hiện nước đi
        self.board[move] = self.turn
        self.buttons[move].config(text=self.turn)
        self.log(f"-> {self.turn} chọn ô {move} (Score: {best_score})\n")
        
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.root.after(800, self.play_turn)

root = tk.Tk()
game = CaroAIvsAI(root)
root.mainloop()