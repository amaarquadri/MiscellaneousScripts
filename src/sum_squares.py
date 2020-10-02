import numpy as np

# https://www.youtube.com/watch?v=G1m7goLCJDY


def generate_graph(n):
    squares = [k ** 2 for k in range(int(np.sqrt(2 * n - 1)))]
    edges = []
    for i in range(1, n + 1):
        edges.append([j for j in range(1, n + 1) if (i + j) in squares and i != j])
    return edges


def process():
    print(generate_graph(15))


if __name__ == '__main__':
    process()
