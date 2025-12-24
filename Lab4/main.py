import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple

Grid = List[List[int]]

def sample_sudoku() -> Grid:
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]


class SudokuCSP:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.domains: Dict[Tuple[int, int], List[int]] = {}
        self.assignment: Dict[Tuple[int, int], int] = {}
        self.stats_nodes = 0

        for r in range(9):
            for c in range(9):
                if grid[r][c] != 0:
                    self.assignment[(r, c)] = grid[r][c]
                    self.domains[(r, c)] = [grid[r][c]]
                else:
                    self.domains[(r, c)] = list(range(1, 10))

    def is_consistent(self, var: Tuple[int, int], val: int) -> bool:
        r, c = var
        if any(self.assignment.get((r, i), val + 1) == val for i in range(9)):
            return False
        if any(self.assignment.get((i, c), val + 1) == val for i in range(9)):
            return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if self.assignment.get((i, j), val + 1) == val:
                    return False
        return True

    def forward_check(self, var: Tuple[int, int], val: int) -> bool:
        r, c = var
        temp = {}
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.assignment:
                    if val in self.domains[(i, j)] and (i == r or j == c or (i // 3 == r // 3 and j // 3 == c // 3)):
                        if len(self.domains[(i, j)]) == 1:
                            return False
                        temp[(i, j)] = self.domains[(i, j)][:]
                        self.domains[(i, j)].remove(val)
        return True

    def restore_domains(self, var: Tuple[int, int], val: int, backup: Dict[Tuple[int, int], List[int]]):
        for k, v in backup.items():
            self.domains[k] = v[:]

    def select_unassigned_var(self) -> Tuple[int, int]:
        unassigned = [v for v in self.domains if v not in self.assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def solve(self) -> bool:
        self.stats_nodes = 0
        return self._backtrack()

    def _backtrack(self) -> bool:
        self.stats_nodes += 1
        if len(self.assignment) == 81:
            return True

        var = self.select_unassigned_var()
        for val in self.domains[var]:
            if self.is_consistent(var, val):
                self.assignment[var] = val
                backup = {}
                for i in range(9):
                    for j in range(9):
                        if (i, j) not in self.assignment:
                            if val in self.domains[(i, j)] and (
                                    i == var[0] or j == var[1] or (i // 3 == var[0] // 3 and j // 3 == var[1] // 3)):
                                backup[(i, j)] = self.domains[(i, j)][:]
                                self.domains[(i, j)].remove(val)
                                if not self.domains[(i, j)]:
                                    break
                else:
                    if self._backtrack():
                        return True
                # restore
                for k, v in backup.items():
                    self.domains[k] = v[:]
                del self.assignment[var]
        return False

    def get_solution(self) -> Grid:
        solution = [[0] * 9 for _ in range(9)]
        for (r, c), val in self.assignment.items():
            solution[r][c] = val
        return solution


def visualize_sudoku(grid: Grid):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))
    ax.grid(True, color='black', linewidth=1)

    for i in range(0, 10, 3):
        ax.axhline(i, color='black', linewidth=2)
        ax.axvline(i, color='black', linewidth=2)

    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                ax.text(c + 0.5, 8.5 - r, str(grid[r][c]), ha='center', va='center', fontsize=16)

    ax.axis('off')
    plt.show()


def generate_simple_sudoku(n_clues=20) -> Grid:
    import random
    grid = [[0] * 9 for _ in range(9)]
    count = 0
    while count < n_clues:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        val = random.randint(1, 9)
        if grid[r][c] == 0:
            grid[r][c] = val
            count += 1
    return grid


def main():
    puzzle = sample_sudoku()
    print("Вхідний Sudoku:")
    visualize_sudoku(puzzle)

    solver = SudokuCSP(puzzle)
    if solver.solve():
        print(f"Знайдено рішення! Вузлів перевірено: {solver.stats_nodes}")
        solution = solver.get_solution()
        visualize_sudoku(solution)
    else:
        print("Рішення не знайдено.")


if __name__ == "__main__":
    main()
