import tkinter as tk
import random

class CaroExpectimax:
    def __init__(self, root):
        self.root = root
        self.root.title("Expectimax - X (Max) vs O (Random/Expectimax)")
        self.board = [' ' for _ in range(9)]
        self.turn = 'X'
        
        # UI Setup
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)
        self.board_frame = tk.Frame(main_frame)
        self.board_frame.grid(row=0, column=0)
        self.buttons = [tk.Button(self.board_frame, text='', font=('Arial', 20), width=5, height=2, state=tk.DISABLED) 
                        for _ in range(9)]
        for i, btn in enumerate(self.buttons): btn.grid(row=i//3, column=i%3)
            
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

    def expectimax(self, b, depth, is_maximizing):
        winner = self.check_winner(b)
        if winner == 'X': return 10 - depth
        if winner == 'O': return depth - 10
        if winner == 'Tie': return 0

        # Lấy danh sách các ô trống
        empty_cells = [i for i, val in enumerate(b) if val == ' ']

        if is_maximizing:
            max_eval = -float('inf')
            for i in empty_cells:
                b[i] = 'X'
                eval = self.expectimax(b, depth + 1, False)
                b[i] = ' '
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            # Nút CHANCE (Expectimax): Tính trung bình cộng của các nhánh
            total_eval = 0
            for i in empty_cells:
                b[i] = 'O'
                val = self.expectimax(b, depth + 1, True)
                b[i] = ' '
                total_eval += val
            
            avg_eval = total_eval / len(empty_cells)
            return avg_eval

    def play_turn(self):
        winner = self.check_winner(self.board)
        if winner:
            self.result_label.config(text=f"Kết quả: {winner if winner != 'Tie' else 'Hòa!'}")
            return

        move = -1
        self.log(f"--- Lượt {self.turn} ---")
        
        if self.turn == 'X':
            # X chơi kiểu Max (Minimax)
            best_score = -float('inf')
            for i in [i for i, v in enumerate(self.board) if v == ' ']:
                self.board[i] = 'X'
                score = self.expectimax(self.board, 0, False)
                self.board[i] = ' '
                self.log(f"X thử ô {i}, Score dự đoán: {score:.2f}")
                if score > best_score: best_score, move = score, i
        else:
            # O chơi kiểu Expectimax (Tính kỳ vọng)
            best_score = float('inf')
            for i in [i for i, v in enumerate(self.board) if v == ' ']:
                self.board[i] = 'O'
                score = self.expectimax(self.board, 0, True)
                self.board[i] = ' '
                self.log(f"O thử ô {i}, Expectation: {score:.2f}")
                if score < best_score: best_score, move = score, i
        
        self.board[move] = self.turn
        self.buttons[move].config(text=self.turn)
        self.log(f"-> {self.turn} chọn ô {move} (Score: {best_score:.2f})\n")
        
        self.turn = 'O' if self.turn == 'X' else 'X'
        self.root.after(800, self.play_turn)

root = tk.Tk()
game = CaroExpectimax(root)
root.mainloop()