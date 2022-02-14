from itertools import product
import numpy as np
from multiprocessing import Pool
import pickle
from sudoku.ruleset import Ruleset
from sudoku.solutions import MIRACLE_SOLUTIONS

"""
Generating all possible miracle sudoku grids using depth first search.
Regular sudoku rules plus:
Knight and king constraint
orthogonally adjacent squares cannot be consecutive
"""


def solver(board=np.zeros((9, 9)), idx=0, ruleset=Ruleset()):
    """
    Yields all possible solutions to a partially filled sudoku board under a given ruleset.
    All values up until idx are expected to already be filled in and be self consistent.
    All values at idx and after are either unfilled (i.e. zero) or are provided as part of the puzzle.

    :param board: The partially filled, self consistent board.
    :param idx: The first index (in the flattened board) that has not yet been filled as part of the solution.
    :param ruleset: A function which accepts partially completed boards and returns whether or not they are consistent.
                    If a second parameter, idx, is provided then only that position in the board needs to be checked for
                    consistency with the rest of the board.
    :return: Yields all possible solutions.
    """
    if idx == 81:
        # given board is already solved so just yield that and stop
        yield np.copy(board)
        return

    i, j = idx // 9, idx % 9

    if board[i, j] != 0:
        # This square was given as part of the puzzle, so skip over it
        yield from solver(np.copy(board), idx + 1, ruleset)
        return

    # Try all possibilities for this square
    for v in range(1, 10):
        board_copy = np.copy(board)
        board_copy[i, j] = v

        # If the value tried is consistent then recurse onto the next square
        if ruleset.verify_square(board_copy, i, j):
            yield from solver(board_copy, idx + 1, ruleset)


def check_puzzle_uniqueness(puzzle, expected_solution=None, ruleset=Ruleset()):
    # create a solution generator for this puzzle
    generator = solver(puzzle, ruleset=ruleset)

    try:
        solution = next(generator)
    except StopIteration as e:
        raise ValueError('No solution to puzzle') from e

    if expected_solution is not None and not np.all(solution == expected_solution):
        # The first found solution does not match the expected solution,
        # so there must be multiple solutions
        return False

    # Try generating a second solution
    try:
        next(generator)
    except StopIteration:
        # A second solution was not found so the puzzle is unique
        return True

    # A second solution was found
    return False


def generate_clue_indices(clue_count=1):
    clues = list(range(clue_count))
    while clues[-1] < 81:
        yield clues
        for i in range(clue_count):
            if i == (clue_count - 1) or (clues[i] + 1) < clues[i + 1]:
                clues[i] += 1
                break
            clues[i] = 0


def generate_puzzles(solutions, max_clues=2):
    """
    Generates puzzles from the given solutions.

    :param solutions: A list of all possible puzzle solutions.
    :param max_clues: The maximum allowed number of clues in the puzzle.
    :return: Yields all satisfactory puzzles.
    """
    for clue_count in range(1, max_clues + 1):
        for clues_indices in generate_clue_indices(clue_count):
            for clue_values in product(*[list(range(1, 10)) for _ in range(clue_count)]):
                puzzle = np.zeros((9, 9))
                for index, value in zip(clues_indices, clue_values):
                    puzzle[index // 9, index % 9] = value

                roi = puzzle != 0
                target = puzzle[roi]

                # check if puzzle exists in solutions
                sol = None
                for solution in solutions:
                    if np.all(solution[roi] == target):
                        if sol is not None:
                            # second solution found
                            break
                        sol = solution
                else:
                    # either 0 or 1 solutions found
                    if sol is not None:
                        # unique solution found
                        # for equivalent in get_equivalents(sol):
                        #     for desired_sol in np.array(MIRACLE_SOLUTIONS)[[0, 3, 4]]:
                        #         if np.all(equivalent == desired_sol):
                        print(clues_indices, clue_values)
                        yield puzzle, sol


def miracle_puzzle_finder(values, ruleset=Ruleset()):
    board = np.zeros((9, 9))
    board[0, 0] = values[0]
    board[0, 1] = values[1]

    if not ruleset.verify(board):
        return []

    # result = []
    # for solution in solver(board, ruleset=ruleset):
    #     print('solution found')
    #     for puzzle in generate_puzzles(solution):
    #         print(puzzle, solution)
    #         result.append((puzzle, solution))
    #     print('all puzzles found')
    # return result
    return list(solver(board, ruleset=ruleset))


def find_miracle_puzzles(threads=8):
    with Pool(threads) as pool:
        inputs = []
        for v1 in range(1, 10):
            for v2 in range(1, 10):
                inputs.append((v1, v2))
        data = pool.map(miracle_puzzle_finder, inputs)

    # flatmap
    data = [sol for sols in data for sol in sols]

    with open('miracle_sudoku_old.pickle', 'wb') as fout:
        pickle.dump(data, fout)

    print('Final data:', data)
    print(len(data))


def get_equivalents(board):
    result = []
    for rot in range(4):
        for flip in [True, False]:
            for reverse in [True, False]:
                b = np.rot90(board, rot)
                if flip:
                    b = np.fliplr(b)
                if reverse:
                    b = 10 - b
                result.append(b)
    return result


def filter_unique(solutions):
    unique_solutions = []
    for solution in solutions:
        for equivalent in get_equivalents(solution):
            for unique_solution in unique_solutions:
                if np.all(unique_solution == equivalent):
                    break
            else:
                continue
            break
        else:
            unique_solutions.append(solution)
    return unique_solutions


def main():
    with open('miracle_sudoku_old.pickle', 'rb') as fin:
        solutions = pickle.load(fin)
    # from sudoku.solutions import MIRACLE_SOLUTIONS
    # solutions = [b for miracle_solution in MIRACLE_SOLUTIONS[[0, 3, 4]] for b in get_equivalents(miracle_solution)]
    data = []
    for puzzle, solution in generate_puzzles(solutions):
        # print(puzzle)
        data.append((puzzle, solution))

    print('Final:', data)


if __name__ == '__main__':
    main()
