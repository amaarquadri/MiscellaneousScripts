"""
These are all unique miracle sudoku boards. On top of regular sudoku rules, they satisfy the knights move constraint,
kings move constraint, and non-consecutive constraint. Each of these boards can be rotated, reflected, or have the
digits reversed, resulting in 16 particular solutions for each of these. The one exception is the 3rd board which has an
extra symmetry whereby a 180 degree rotation gives the same result as reversing the digits. This results in only 8
particular solutions. Thus, there are a total of 4 * 16 + 1 * 8 = 72 particular solutions.

I've done a complete computer search (using depth first search) and found that there are only 72 possible completed miracle sudoku boards (which reduces to just 5 if you don't include reflections, rotations, and reversing the digits 1 to 9). So it's not that surprising that a solution is possible given just 2 digits. I checked and unfortunately none of the boards can be uniquely determined from a single digit.
"""
MIRACLE_SOLUTIONS = [[[1, 4, 7, 5, 8, 2, 9, 3, 6],
                      [5, 8, 2, 9, 3, 6, 4, 7, 1],
                      [9, 3, 6, 4, 7, 1, 8, 2, 5],
                      [4, 7, 1, 8, 2, 5, 3, 6, 9],
                      [8, 2, 5, 3, 6, 9, 7, 1, 4],
                      [3, 6, 9, 7, 1, 4, 2, 5, 8],
                      [7, 1, 4, 2, 5, 8, 6, 9, 3],
                      [2, 5, 8, 6, 9, 3, 1, 4, 7],
                      [6, 9, 3, 1, 4, 7, 5, 8, 2]],

                     # https://www.youtube.com/watch?v=yKf9aUIxdb4&ab_channel=CrackingTheCryptic
                     [[4, 8, 3, 7, 2, 6, 1, 5, 9],
                      [7, 2, 6, 1, 5, 9, 4, 8, 3],
                      [1, 5, 9, 4, 8, 3, 7, 2, 6],
                      [8, 3, 7, 2, 6, 1, 5, 9, 4],
                      [2, 6, 1, 5, 9, 4, 8, 3, 7],
                      [5, 9, 4, 8, 3, 7, 2, 6, 1],
                      [3, 7, 2, 6, 1, 5, 9, 4, 8],
                      [6, 1, 5, 9, 4, 8, 3, 7, 2],
                      [9, 4, 8, 3, 7, 2, 6, 1, 5]],

                     # https://www.youtube.com/watch?v=Tv-48b-KuxI&t=241s&ab_channel=CrackingTheCryptic
                     [[9, 4, 8, 3, 7, 2, 6, 1, 5],
                      [3, 7, 2, 6, 1, 5, 9, 4, 8],
                      [6, 1, 5, 9, 4, 8, 3, 7, 2],
                      [4, 8, 3, 7, 2, 6, 1, 5, 9],
                      [7, 2, 6, 1, 5, 9, 4, 8, 3],
                      [1, 5, 9, 4, 8, 3, 7, 2, 6],
                      [8, 3, 7, 2, 6, 1, 5, 9, 4],
                      [2, 6, 1, 5, 9, 4, 8, 3, 7],
                      [5, 9, 4, 8, 3, 7, 2, 6, 1]],

                     [[2, 5, 8, 6, 9, 3, 1, 4, 7],
                      [6, 9, 3, 1, 4, 7, 5, 8, 2],
                      [1, 4, 7, 5, 8, 2, 9, 3, 6],
                      [5, 8, 2, 9, 3, 6, 4, 7, 1],
                      [9, 3, 6, 4, 7, 1, 8, 2, 5],
                      [4, 7, 1, 8, 2, 5, 3, 6, 9],
                      [8, 2, 5, 3, 6, 9, 7, 1, 4],
                      [3, 6, 9, 7, 1, 4, 2, 5, 8],
                      [7, 1, 4, 2, 5, 8, 6, 9, 3]],

                     [[2, 5, 8, 6, 9, 3, 1, 4, 7],
                      [7, 1, 4, 2, 5, 8, 6, 9, 3],
                      [3, 6, 9, 7, 1, 4, 2, 5, 8],
                      [8, 2, 5, 3, 6, 9, 7, 1, 4],
                      [4, 7, 1, 8, 2, 5, 3, 6, 9],
                      [9, 3, 6, 4, 7, 1, 8, 2, 5],
                      [5, 8, 2, 9, 3, 6, 4, 7, 1],
                      [1, 4, 7, 5, 8, 2, 9, 3, 6],
                      [6, 9, 3, 1, 4, 7, 5, 8, 2]]]
