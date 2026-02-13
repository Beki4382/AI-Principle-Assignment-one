

from typing import List, Set


def solve_n_queens(n: int) -> List[List[int]]:
    
    solutions = []
    
    # Sets to track occupied columns and diagonals
    cols: Set[int] = set()           # Occupied columns
    diag1: Set[int] = set()          # Main diagonals (row - col)
    diag2: Set[int] = set()        # Current solution being built   # Anti-diagonals (row + col)
    
    current_solution: List[int] = []
    
    def backtrack(row: int) -> None:
        
        if row == n:
            # All queens placed successfully
            solutions.append(current_solution.copy())
            return
        
        for col in range(n):
            # Check if this position is safe
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Place the queen
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            current_solution.append(col)
            
            # Recurse to the next row
            backtrack(row + 1)
            
            # Backtrack: remove the queen
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            current_solution.pop()
    
    backtrack(0)
    return solutions


def solve_n_queens_one(n: int) -> List[int]:
    
    cols: Set[int] = set()
    diag1: Set[int] = set()
    diag2: Set[int] = set()
    solution: List[int] = []
    
    def backtrack(row: int) -> bool:
        if row == n:
            return True
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            solution.append(col)
            
            if backtrack(row + 1):
                return True
            
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            solution.pop()
        
        return False
    
    backtrack(0)
    return solution


def print_board(solution: List[int]) -> None:
    
    n = len(solution)
    print("+" + "---+" * n)
    for row in range(n):
        row_str = "|"
        for col in range(n):
            if solution[row] == col:
                row_str += " Q |"
            else:
                row_str += "   |"
        print(row_str)
        print("+" + "---+" * n)


def count_solutions(n: int) -> int:
    
    count = [0]  # Using list to allow modification in nested function
    
    cols: Set[int] = set()
    diag1: Set[int] = set()
    diag2: Set[int] = set()
    
    def backtrack(row: int) -> None:
        if row == n:
            count[0] += 1
            return
        
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1)
            
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return count[0]


def is_valid_solution(solution: List[int]) -> bool:
    
    n = len(solution)
    
    # Check columns (each column should be unique)
    if len(set(solution)) != n:
        return False
    
    # Check diagonals
    for i in range(n):
        for j in range(i + 1, n):
            # Same diagonal if |row_diff| == |col_diff|
            if abs(i - j) == abs(solution[i] - solution[j]):
                return False
    
    return True


if __name__ == "__main__":
    n = 4
    print(f"Solving {n}-Queens Problem")
    print("=" * 40)
    
    solutions = solve_n_queens(n)
    print(f"\nTotal solutions for N={n}: {len(solutions)}")
    print(f"\nSolutions (column positions for each row):")
    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i}: {sol}")
        print_board(sol)
        print(f"Valid: {is_valid_solution(sol)}")
        print()
    
   
    
    