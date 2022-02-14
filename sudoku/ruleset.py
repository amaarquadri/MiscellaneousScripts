class Ruleset:
    KNIGHTS_MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    KINGS_MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    ORTHOGONALLY_ADJACENT = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    def __init__(self, knights=True, kings=True, consecutive=True):
        self.knights = knights
        self.kings = kings
        self.consecutive = consecutive

    def verify(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0 and not self.verify_square(board, i, j):
                    return False
        return True

    def verify_index(self, board, idx):
        if idx == -1:
            return self.verify(board)

        return self.verify_square(board, idx // 9, idx % 9)

    def verify_square(self, board, i, j):
        value = board[i][j]

        # Sudoku rows and columns
        for target_i in range(0, 9):
            if i != target_i and value == board[target_i][j]:
                return False
        for target_j in range(0, 9):
            if j != target_j and value == board[i][target_j]:
                return False

        # Sudoku 3x3 box check
        i_box = 3 * (i // 3)
        j_box = 3 * (j // 3)
        for target_i in range(i_box, i_box + 3):
            for target_j in range(j_box, j_box + 3):
                if (target_i != i or target_j != j) and value == board[target_i][target_j]:
                    return False

        if self.knights or self.kings:
            targets = self.KNIGHTS_MOVES + self.KINGS_MOVES if self.knights and self.kings else \
                (self.KNIGHTS_MOVES if self.knights else self.KINGS_MOVES)
            for di, dj in targets:
                target_i, target_j = i + di, j + dj
                if 0 <= target_i < 9 and 0 <= target_j < 9 and value == board[target_i][target_j]:
                    return False

        # consecutive restriction check
        if self.consecutive:
            consecutive_numbers = list(filter(lambda v: 0 < v <= 9, [value + 1, value - 1]))
            for di, dj in self.ORTHOGONALLY_ADJACENT:
                target_i, target_j = i + di, j + dj
                if 0 <= target_i < 9 and 0 <= target_j < 9 and board[target_i][target_j] in consecutive_numbers:
                    return False

        return True


if __name__ == '__main__':
    test = [[4, 8, 3, 7, 2, 6, 1, 5, 9],
            [7, 2, 6, 1, 5, 9, 4, 8, 3],
            [1, 5, 9, 4, 8, 3, 7, 2, 6],
            [8, 3, 7, 2, 6, 1, 5, 9, 4],
            [2, 6, 1, 5, 9, 4, 8, 3, 7],
            [5, 9, 4, 8, 3, 7, 2, 6, 1],
            [3, 7, 2, 6, 1, 5, 9, 4, 8],
            [6, 1, 5, 9, 4, 8, 3, 7, 2],
            [9, 4, 8, 3, 7, 2, 6, 1, 5]]
    print(Ruleset().verify(test))
