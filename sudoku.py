# -*- coding: utf-8 -*-
import tkinter as tk
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True
def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False
def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None
def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))
def solve():
    sudoku_board = []
    for i in range(9):
        row = []
        for j in range(9):
            entry = entries[i][j].get()
            if entry:
                row.append(int(entry))
            else:
                row.append(0)
        sudoku_board.append(row)
    if solve_sudoku(sudoku_board):
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(sudoku_board[i][j]))
    else:
        result_label.config(text="No solution found.")
root = tk.Tk()
root.title("Sudoku Solver")
entries = []
for i in range(9):
    row_entries = []
    for j in range(9):
        entry = tk.Entry(root, width=3, font=('Helvetica', 16))
        entry.grid(row=i, column=j)
        row_entries.append(entry)
    entries.append(row_entries)
solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.grid(row=9, column=4, pady=10)
result_label = tk.Label(root, text="")
result_label.grid(row=10, columnspan=9)
root.mainloop()
