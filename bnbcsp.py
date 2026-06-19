import time
import random
import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class VisualWheresMyCatBnB:
    def __init__(self, n, delay=0.1):
        self.N = n
        self.board = np.zeros((n, n), dtype=int)
        
        self.node_expansions = 0
        self.pruned_branches = 0
        self.start_time = 0
        
        self.delay = delay
        self.animate = self.N <= 15
        
        self.cmap = ListedColormap(['#FFFFFF', '#0A192F', '#60A5FA']) 

        if self.animate:
            plt.ion()
        
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.fig.canvas.manager.set_window_title(f"Where's My Cat - Branch and Bound {self.N}x{self.N}")

    def draw_board(self, current_row=-1, current_col=-1, status="idle"):
        if not self.animate and status != "final":
            return

        self.ax.clear()
        vis_grid = np.copy(self.board)
        
        if current_row != -1 and current_col != -1 and status == "evaluating":
            vis_grid[current_row][current_col] = 2
            
        self.ax.matshow(vis_grid, cmap=self.cmap, vmin=0, vmax=2)
        
        self.ax.set_xticks(np.arange(-0.5, self.N, 1))
        self.ax.set_yticks(np.arange(-0.5, self.N, 1))
        self.ax.grid(color='black', linestyle='-', linewidth=1)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        
        current_time = time.perf_counter() - self.start_time if self.start_time > 0 else 0
        title_text = (f"Algorithm: Branch & Bound | Grid: {self.N}x{self.N}\n"
                      f"Nodes Evaluated: {self.node_expansions} | Pruned Branches: {self.pruned_branches}\n"
                      f"Time Elapsed: {current_time:.4f} seconds")
        
        self.ax.set_title(title_text, fontsize=12, pad=15, loc='left', fontweight='bold')
        
        if self.animate and status != "final":
            plt.draw()
            plt.pause(self.delay)

    def is_safe(self, placement, new_row, new_col):
        for r, c in enumerate(placement):
            if c == new_col: 
                return False
            if abs(r - new_row) <= 1 and abs(c - new_col) <= 1: 
                return False
        return True

    def solve_bnb(self):
        pq = []
        heapq.heappush(pq, (0, random.random(), 0, []))
        
        while pq:
            cost, _, row, placement = heapq.heappop(pq)
            self.node_expansions += 1
            
            self.board.fill(0)
            for r, c in enumerate(placement):
                self.board[r][c] = 1
                
            if row == self.N:
                return True
                
            available_cols = list(range(self.N))
            random.shuffle(available_cols)
            
            for col in available_cols:
                self.draw_board(row, col, "evaluating")
                
                if self.is_safe(placement, row, col):
                    new_placement = placement + [col]
                    heuristic = self.N - (row + 1)
                    heapq.heappush(pq, (heuristic, random.random(), row + 1, new_placement))
                else:
                    self.pruned_branches += 1

        return False

    def run_experiment(self):
        print(f"\n--- Memulai Visualisasi Branch and Bound {self.N}x{self.N} ---")
        self.start_time = time.perf_counter()
        
        success = self.solve_bnb()
        
        end_time = time.perf_counter()
        self.draw_board(status="final")

        if success:
            print("Status: Solusi Ditemukan!")
            if self.animate:
                plt.ioff()
            plt.show()
        else:
            print("Status: Solusi Tidak Ditemukan.")
            
        print(f"Total Nodes Evaluated : {self.node_expansions}")
        print(f"Total Pruned Branches : {self.pruned_branches}")
        print(f"Waktu Eksekusi        : {end_time - self.start_time:.6f} detik")
        print("-" * 50)

if __name__ == "__main__":
    print("Pilih ukuran grid 'Where's My Cat':")
    print("1. Grid 5 x 5 (Full Animasi)")
    print("2. Grid 50 x 50 (Hanya Hasil Akhir)")
    
    pilihan = input("Masukkan pilihan (1 atau 2): ")
    
    if pilihan == '1':
        game_5x5 = VisualWheresMyCatBnB(5, delay=0.15) 
        game_5x5.run_experiment()
    elif pilihan == '2':
        game_50x50 = VisualWheresMyCatBnB(50)
        game_50x50.run_experiment()
    else:
        print("Pilihan tidak valid.")