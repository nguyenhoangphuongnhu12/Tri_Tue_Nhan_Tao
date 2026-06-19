# https://github.com/nguyenhoangphuongnhu12/Tri_Tue_Nhan_Tao
# Nguyễn Hoàng Phương Như - 24110042
# THUẬT TOÁN CSP - MIN CONFLICTS
import tkinter as tk
from tkinter import scrolledtext
import random

# Dữ liệu
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

# THUẬT TOÁN CSP - CONFLICTS
class MinConflictsCSP:
    def __init__(self, regions, neighbors, colors, log_func):
        self.regions = regions
        self.neighbors = neighbors
        self.colors = list(colors)
        self.log = log_func
        self.assignment = {r: random.choice(self.colors) for r in regions}

    def count_conflicts(self, var, val):
        return sum(1 for n in self.neighbors[var] if self.assignment.get(n) == val)

def main():
    root = tk.Tk()
    root.title("MIN-CONFLICTS - MAP COLORING")
    root.geometry("1200x750")
    root.configure(bg="#1e1e1e")

    main_frame = tk.Frame(root, bg="#1e1e1e")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_frame, width=700, height=600, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_text(400, 30, text="CSP - MIN CONFLICTS", font=("Segoe UI", 16, "bold"), fill="#ffcc00")

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

    all_x = [p[i] for p in REGION_POLYGONS.values() for i in range(0, len(p), 2)]
    all_y = [p[i] for p in REGION_POLYGONS.values() for i in range(1, len(p), 2)]
    offset_x, offset_y = 350 - (sum(all_x)/len(all_x)), 300 - (sum(all_y)/len(all_y))
    
    poly_ids = {r: canvas.create_polygon([p[i] + (offset_x if i%2==0 else offset_y) for i in range(len(p))], fill="#e0e0e0", outline="#fff", width=2) for r, p in REGION_POLYGONS.items()}
    
    csp = MinConflictsCSP(REGION_POLYGONS.keys(), NEIGHBORS, COLOR_MAP.keys(), log)
    
    # Tô màu khởi tạo ban đầu cho toàn bộ bản đồ
    for r, color_name in csp.assignment.items():
        canvas.itemconfig(poly_ids[r], fill=COLOR_MAP[color_name])

    for r, (lx, ly, txt) in LABEL_COORDS.items(): 
        canvas.create_text(lx + offset_x, ly + offset_y, text=txt, font=("Arial", 12, "bold"))

    def run_min_conflicts(step):
        conflicted = [r for r in csp.regions if csp.count_conflicts(r, csp.assignment[r]) > 0]
        if not conflicted:
            log("--- HOÀN THÀNH: KHÔNG CÒN XUNG ĐỘT ---")
            res_area.insert("end", f"KẾT QUẢ CUỐI CÙNG: {csp.assignment}")
            return

        var = random.choice(conflicted)
        log(f"Bước {step}: Xét {var} (đang xung đột)")
        
        best_val = min(csp.colors, key=lambda c: csp.count_conflicts(var, c))
        
        log(f"  -> Thử các màu cho {var}...")
        for c in csp.colors:
            conf_count = csp.count_conflicts(var, c)
            log(f"     * Màu {c}: {conf_count} xung đột")
            
        csp.assignment[var] = best_val
        canvas.itemconfig(poly_ids[var], fill=COLOR_MAP[best_val])
        log(f"  -> CHỌN: {var} = {best_val}")
        
        root.after(500, lambda: run_min_conflicts(step + 1))

    root.after(1000, lambda: run_min_conflicts(0))
    root.mainloop()

if __name__ == "__main__": main()