# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 18:39:54 2024

@author: YS
"""

import tkinter as tk

def is_valid(board, row, col, num):
    """
    检查在给定的数独矩阵中，将数字num放入指定的行和列是否符合数独规则。

    参数：
    - board: 9x9的数独矩阵
    - row: 要放置数字的行索引
    - col: 要放置数字的列索引
    - num: 要放置的数字

    返回值：
    - 如果放置数字num在指定位置是合法的，则返回True；否则返回False。
    """
    # 检查同一行、同一列、3x3子格子是否存在相同数字
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(9):
        if board[row][i] == num or board[i][col] == num or board[start_row + i // 3][start_col + i % 3] == num:
            return False
    return True

def solve_sudoku(board):
    """
    解决数独问题的主要函数。使用回溯算法。

    参数：
    - board: 要解决的数独矩阵，其中0表示空格。

    返回值：
    - 如果找到了解决方案，则返回True；否则返回False。
    """
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
    """
    在数独矩阵中查找第一个空的单元格。

    参数：
    - board: 要查找空单元格的数独矩阵。

    返回值：
    - 如果找到了空单元格，则返回其行和列的索引；否则返回None。
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def format_solution(solution):
    """
    将解决方案格式化为九个3x3的矩阵。

    参数：
    - solution: 解决方案矩阵

    返回值：
    - 格式化后的解决方案字符串
    """
    formatted_solution = "求解的结果如下：\n"
    for i in range(9):
        if i % 3 == 0 and i != 0:
            formatted_solution += "-" * 29 + "\n"
        for j in range(9):
            if j % 3 == 0 and j != 0:
                formatted_solution += "  |  "
            formatted_solution += str(solution[i][j]) + " "
        formatted_solution += "\n"
    return formatted_solution

def is_valid_input(board):
    """
    检查数独输入的有效性。

    参数：
    - board: 要检查的数独矩阵。

    返回值：
    - 如果数独输入有效，则返回True；否则返回False。
    """
    # 检查每个元素是否为整数0到9
    for i in range(9):
        row = board[i]
        column = [board[j][i] for j in range(9)]
        for num in row + column:
            if num not in range(0, 10):
                return False
        if not is_valid_row(row) or not is_valid_row(column):
            return False

    # 检查每个3x3子格是否包含重复数字
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_row(square):
                return False

    return True

def is_valid_row(row):
    """
    检查给定行是否包含重复数字。

    参数：
    - row: 要检查的行。

    返回值：
    - 如果行有效（不包含重复数字），则返回True；否则返回False。
    """
    seen = set()
    for num in row:
        if num != 0:
            if num in seen:
                return False
            seen.add(num)
    return True

def solve(entries, solution_text, result_label):
    """
    处理用户点击"Solve"按钮的函数。将GUI输入的数独问题转换为数独矩阵，并解决该问题。

    参数：
    - entries: 输入框列表
    - solution_text: 显示解决方案的文本框
    - result_label: 显示结果的标签
    """
    # 从GUI输入框中获取数独矩阵
    sudoku_board = [[int(entries[i][j].get()) if entries[i][j].get() else 0 for j in range(9)] for i in range(9)]

    # 检查数独输入的有效性
    if not is_valid_input(sudoku_board):
        result_label.config(text="Invalid input.")
        return

    # 解决数独问题并显示解决方案或提示无解
    if solve_sudoku(sudoku_board):
        solution_text.delete(1.0, tk.END)  # 清空文本框
        formatted_solution = format_solution(sudoku_board)
        solution_text.insert(tk.END, formatted_solution)
        result_label.config(text="")
    else:
        result_label.config(text="No solution found.")
        solution_text.delete(1.0, tk.END)  # 清空文本框

def clear(entries, solution_text):
    """
    处理用户点击"Clear"按钮的函数。清除所有输入。

    参数：
    - entries: 输入框列表
    - solution_text: 显示解决方案的文本框
    """
    # 清空所有GUI输入框和解决方案文本框
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
    solution_text.delete(1.0, tk.END)  # 清空文本框

def gui():
    root = tk.Tk()
    root.title("Sudoku Solver")

    # 创建提示文本
    tk.Label(root, text="请在这里输入题目：").pack()

    # 创建输入框
    entries = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        frame = tk.Frame(root)
        frame.pack()
        for j in range(9):
            entries[i][j] = tk.Entry(frame, width=3, font=('Helvetica', 16))
            entries[i][j].pack(side=tk.LEFT)

    # 创建解决和清除按钮
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    solve_button = tk.Button(button_frame, text="Solve", command=lambda: solve(entries, solution_text, result_label))
    solve_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(button_frame, text="Clear", command=lambda: clear(entries, solution_text))
    clear_button.pack(side=tk.LEFT, padx=5)

    # 创建结果标签
    result_label = tk.Label(root, text="")
    result_label.pack()

    # 创建解决方案文本框
    solution_text = tk.Text(root, width=35, height=15, font=('Helvetica', 16))
    solution_text.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    gui()
