import numpy as np


def to_solver_board(board):
    solver_board = np.full((9, 9), '')
    for i in board.shape[0]:
        for j in board.shape[1]:
            if board[i][j] == 0:
                solver_board[i][j] = '123456789'
            else:
                solver_board[i][j] = str(board[i][j])
    return solver_board


def solve(board, check_contradictions=True):
    """

    :param board:
    :param check_contradictions: If True, the solver will not assume that the sudoku is consistent
                                 and throw a ValueError if a contradiction is found.
    :return:
    """
    for i in range(9):
        for j in range(9):
            if len(board[i][j]) == 1:

