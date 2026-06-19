# https://github.com/nguyenhoangphuongnhu12/Tri_Tue_Nhan_Tao
# Nguyễn Hoàng Phương Như - 24110042
# THUẬT TOÁN CSP - AC-3
import tkinter as tk
from tkinter import scrolledtext

# =========================================================
# DỮ LIỆU
# =========================================================
REGION_POLYGONS = {
    "P1": [150, 300, 250, 300, 270, 420, 160, 420], "P2": [150, 180, 280, 180, 250, 300, 150, 300],
    "P3": [250, 300, 380, 300, 380, 420, 270, 420], "P4": [280, 180, 420, 180, 380, 300, 250, 300],
    "P5": [420, 180, 600, 180, 550, 320, 380, 300], "P6": [380, 300, 550, 320, 500, 450, 380, 420],
    "P7": [380, 420, 500, 450, 450, 550, 340, 520], "P8": [550, 320, 680, 350, 650, 520, 500, 450],
    "P9": [500, 450, 650, 520, 580, 650, 450, 550], "P10": [160, 420, 270, 420, 250, 560, 150, 520],
    "P11": [270, 420, 380, 420, 340, 520, 250, 560], "P12": [250, 560, 340, 520, 450, 550, 380, 680]
}

LABEL_COORDS = {
    "P1": (205, 360, "①"), "P2": (215, 240, "②"), "P3": (320, 360, "③"), "P4": (330, 240, "④"),
    "P5": (485, 240, "⑤"), "P6": (450, 365, "⑥"), "P7": (415, 470, "⑦"), "P8": (595, 420, "⑧"),
    "P9": (545, 540, "⑨"), "P10": (205, 480, "⑩"), "P11": (310, 480, "⑪"), "P12": (355, 600, "⑫")
}

NEIGHBORS = {
    "P1": ["P2", "P3", "P10"], "P2": ["P1", "P4"], "P3": ["P1", "P4", "P6", "P7", "P11"],
    "P4": ["P2", "P3", "P6", "P5"], "P5": ["P4", "P6", "P8"], "P6": ["P4", "P5", "P3", "P7", "P8", "P9"],
    "P7": ["P3", "P6", "P9", "P11", "P12"], "P8": ["P5", "P6", "P9"],
    "P9": ["P6", "P7", "P8", "P11", "P12"], "P10": ["P1", "P11", "P12"],
    "P11": ["P3", "P7", "P9", "P10", "P12"], "P12": ["P10", "P11", "P9", "P7"]
}

COLOR_MAP = {"Đỏ": "#ff6666", "Xanh lá": "#4bd24b", "Xanh dương": "#4696ff", "Vàng": "#ffeb46"}

# =========================================================
# THUẬT TOÁN CSP
# =========================================================
class MapColoringCSP:
    def __init__(self, regions, neighbors, colors, log_func):
        self.domains = {r: list(colors) for r in regions}
        self.neighbors = neighbors
        self.assignment = {}
        self.log_func = log_func # Hàm này dùng để in log lên giao diện

    def ac3(self):
        self.log_func("--- BẮT ĐẦU THUẬT TOÁN AC-3 ---")
        queue = [(xi, xj) for xi in self.neighbors for xj in self.neighbors[xi]]
        
        # In danh sách cung cần xét 
        self.log_func(f"Khởi tạo hàng đợi với {len(queue)} cung.")
        
        while queue:
            xi, xj = queue.pop(0)
            self.log_func(f"Xét Arc ({xi}, {xj})")
            
            if self.revise(xi, xj):
                self.log_func(f"  -> Đã sửa đổi Domain({xi}), hiện tại: {self.domains[xi]}")
                for xk in self.neighbors[xi]:
                    if xk != xj: 
                        queue.append((xk, xi))
            else:
                self.log_func(f"  -> Không có giá trị nào cần xóa cho Arc ({xi}, {xj})")
        
        self.log_func("--- KẾT THÚC AC-3 ---\n")

    def revise(self, xi, xj):
        revised = False
        for x in list(self.domains[xi]):
            # Kiểm tra xem có vi phạm ràng buộc không
            if len(self.domains[xj]) == 1 and x == self.domains[xj][0]:
                self.domains[xi].remove(x)
                revised = True
        return revised

    def solve(self, callback):
        # 1. Chạy AC-3 trước
        self.ac3()
        # 2. Sau đó mới chạy Backtracking
        self.log_func("--- BẮT ĐẦU BACKTRACKING ---")
        return self._backtrack(callback)

    def _backtrack(self, callback):
        if len(self.assignment) == len(self.domains): return self.assignment
        r = min([k for k in self.domains if k not in self.assignment], key=lambda k: len(self.domains[k]))
        for c in list(self.domains[r]):
            if all(self.assignment.get(n) != c for n in self.neighbors[r]):
                callback(r, c, "TRY")
                self.assignment[r] = c
                callback(r, c, "ADVANCE")
                res = self._backtrack(callback)
                if res: return res
                callback(r, c, "BACKTRACK")
                del self.assignment[r]
        return None

# =========================================================
# GIAO DIỆN CHÍNH
# =========================================================
def main():
    root = tk.Tk()
    root.title("MAP COLORING - AC3 & BACKTRACKING")
    root.geometry("1200x750")
    root.configure(bg="#1e1e1e")

    main_frame = tk.Frame(root, bg="#1e1e1e")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_frame, width=700, height=600, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_text(400, 30, text="CSP - AC-3", font=("Segoe UI", 16, "bold"), fill="#ffcc00")

    log_frame = tk.Frame(main_frame, bg="#1e1e1e")
    log_frame.pack(side="right", fill="y", padx=(10, 0))
    
    tk.Label(log_frame, text="TIẾN TRÌNH THUẬT TOÁN", font=("Segoe UI", 11, "bold"), bg="#1e1e1e", fg="#00ffcc").pack(anchor="w")
    log_area = scrolledtext.ScrolledText(log_frame, width=50, height=30, bg="#000", fg="#00ffcc", font=("Consolas", 10))
    log_area.pack(pady=5)

    res_area = tk.Text(root, height=4, bg="#000", fg="#fff", font=("Consolas", 11))
    res_area.pack(fill="x", padx=10, pady=(0, 10))

    def log(msg):
        log_area.insert("end", msg + "\n")
        log_area.see("end")

    # Tính offset để căn giữa
    all_x = [p[i] for p in REGION_POLYGONS.values() for i in range(0, len(p), 2)]
    all_y = [p[i] for p in REGION_POLYGONS.values() for i in range(1, len(p), 2)]
    offset_x, offset_y = 350 - (sum(all_x)/len(all_x)), 300 - (sum(all_y)/len(all_y))
    def adj(poly): return [poly[i] + (offset_x if i%2==0 else offset_y) for i in range(len(poly))]

    poly_ids = {r: canvas.create_polygon(adj(p), fill="#e0e0e0", outline="#fff", width=2) for r, p in REGION_POLYGONS.items()}
    for r, (lx, ly, txt) in LABEL_COORDS.items(): 
        canvas.create_text(lx + offset_x, ly + offset_y, text=txt, font=("Arial", 12, "bold"))

    # Truyền hàm log vào CSP
    csp = MapColoringCSP(REGION_POLYGONS.keys(), NEIGHBORS, COLOR_MAP.keys(), log)
    history = []

    def callback(r, c, t):
        history.append((r, c, t))
        log(f"Backtracking: {t} {r} -> {c}")

    final = csp.solve(callback)
    res_area.insert("end", f"KẾT QUẢ: {final}")

    def animate(i):
        if i < len(history):
            r, c, t = history[i]
            if t == "ADVANCE": canvas.itemconfig(poly_ids[r], fill=COLOR_MAP[c])
            elif t == "BACKTRACK": canvas.itemconfig(poly_ids[r], fill="#e0e0e0")
            root.after(100, lambda: animate(i + 1))

    root.after(500, lambda: animate(0))
    root.mainloop()

if __name__ == "__main__": main()