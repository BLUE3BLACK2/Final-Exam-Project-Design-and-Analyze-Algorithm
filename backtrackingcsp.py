import time
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class VisualWheresMyCatBacktracking:
    def __init__(self, n, delay=0.1):
        self.N = n
        self.board = np.zeros((n, n), dtype=int)

        self.node_expansions = 0
        self.backtracks_count = 0
        self.start_time = 0
        
        self.delay = delay
        self.animate = self.N <= 15 
        
        self.cmap = ListedColormap(['#FFFFFF', '#0A192F', '#60A5FA']) 

        if self.animate:
            plt.ion()
        
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.fig.canvas.manager.set_window_title(f"Where's My Cat - Backtracking {self.N}x{self.N}")

    def draw_board(self, current_row=-1, current_col=-1, status="idle"):
        if not self.animate and status != "final":
            return

        self.ax.clear()
        vis_grid = np.copy(self.board)
        
        if current_row != -1 and current_col != -1 and status in ["evaluating", "backtrack"]:
            vis_grid[current_row][current_col] = 2
            
        self.ax.matshow(vis_grid, cmap=self.cmap, vmin=0, vmax=2)
        
        self.ax.set_xticks(np.arange(-0.5, self.N, 1))
        self.ax.set_yticks(np.arange(-0.5, self.N, 1))
        self.ax.grid(color='black', linestyle='-', linewidth=1)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        current_time = time.perf_counter() - self.start_time if self.start_time > 0 else 0
        title_text = (f"Algorithm: Backtracking | Grid: {self.N}x{self.N}\n"
                      f"Nodes Evaluated: {self.node_expansions} | Backtracks: {self.backtracks_count}\n"
                      f"Time Elapsed: {current_time:.4f} seconds")
        
        self.ax.set_title(title_text, fontsize=12, pad=15, loc='left', fontweight='bold')
        
        if self.animate and status != "final":
            plt.draw()
            plt.pause(self.delay)

    def is_safe(self, row, col):
        for i in range(row):
            if self.board[i][col] == 1:
                return False

        directions = [(-1, -1), (-1, 0), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.N and 0 <= c < self.N:
                if self.board[r][c] == 1:
                    return False
        return True

    def solve_backtracking(self, row):
        if row >= self.N:
            return True

        kolom_tersedia = list(range(self.N))
        random.shuffle(kolom_tersedia)

        for col in kolom_tersedia:
            self.node_expansions += 1
            self.draw_board(row, col, "evaluating")

            if self.is_safe(row, col):
                self.board[row][col] = 1 
                self.draw_board(row, col, "placed") 

                if self.solve_backtracking(row + 1):
                    return True

                self.board[row][col] = 0
                self.backtracks_count += 1
                self.draw_board(row, col, "backtrack") 

        return False

    def run_experiment(self):
        print(f"\n--- Memulai Visualisasi Backtracking {self.N}x{self.N} ---")
        self.start_time = time.perf_counter()
        
        success = self.solve_backtracking(0)
        
        end_time = time.perf_counter()

        self.draw_board(status="final")

        if success:
            print("Status: Solusi Ditemukan!")
            if self.animate:
                plt.ioff()
            plt.show()
        else:
            print("Status: Solusi Tidak Ditemukan.")
            
        print(f"Total Nodes       : {self.node_expansions}")
        print(f"Total Backtracks  : {self.backtracks_count}")
        print(f"Waktu Eksekusi    : {end_time - self.start_time:.6f} detik")
        print("-" * 50)

if __name__ == "__main__":
    print("Pilih ukuran grid 'Where's My Cat':")
    print("1. Grid 5 x 5 (Full Animasi)")
    print("2. Grid 50 x 50 (Hanya Hasil Akhir)")
    
    pilihan = input("Masukkan pilihan (1 atau 2): ")
    
    if pilihan == '1':
        game_5x5 = VisualWheresMyCatBacktracking(5, delay=0.15) 
        game_5x5.run_experiment()
    elif pilihan == '2':
        game_50x50 = VisualWheresMyCatBacktracking(50)
        game_50x50.run_experiment()
    else:
        print("Pilihan tidak valid.")