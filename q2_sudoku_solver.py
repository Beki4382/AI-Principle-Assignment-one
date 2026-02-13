from typing import List, Tuple, Optional


def solve_sudoku(board: List[List[int]]) -> bool:
    
    empty_cell = find_empty(board)
    
    if empty_cell is None:
        return True
    
    row, col = empty_cell
    
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            
            
            if solve_sudoku(board):
                return True
            
            # Backtrack: remove the number if it didn't lead to a solution
            board[row][col] = 0
    
    # No valid number found, need to backtrack
    return False


def find_empty(board: List[List[int]]) -> Optional[Tuple[int, int]]:
   
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True


def print_board(board: List[List[int]]) -> None:
    
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        
        row_str = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            
            if board[i][j] == 0:
                row_str += " ."
            else:
                row_str += f" {board[i][j]}"
        
        print(row_str)


def is_valid_sudoku(board: List[List[int]]) -> bool:
  
    # Check all rows
    for row in board:
        if sorted([x for x in row if x != 0]) != sorted(set([x for x in row if x != 0])):
            return False
        if 0 in row:
            return False
    
    # Check all columns
    for col in range(9):
        column = [board[row][col] for row in range(9)]
        if sorted(column) != list(range(1, 10)):
            return False
    
    # Check all 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    box.append(board[i][j])
            if sorted(box) != list(range(1, 10)):
                return False
    
    return True


# Test the solution
if __name__ == "__main__":
    # Example from the problem
    board = [
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
    
    print("Original Sudoku Board:")
    print_board(board)
    print()
    
    if solve_sudoku(board):
        print("Solved Sudoku Board:")
        print_board(board)
        print()
        print(f"Solution is valid: {is_valid_sudoku(board)}")
    else:
        print("No solution exists for this Sudoku puzzle.")
    
    