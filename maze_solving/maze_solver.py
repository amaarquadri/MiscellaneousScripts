import numpy as np
from collections import defaultdict

WALL_CHAR = 'W'
EMPTY_CHAR = '.'
START_CHAR = 'S'
END_CHAR = '1'
PATH_CHAR = 'X'


class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.neighbours = []


def parse_maze(file):
    with open(file) as f:
        data = f.readlines()
    data = np.array([list(line.strip().upper()) for line in data])
    walls = data == WALL_CHAR
    start = tuple(np.argwhere(data == START_CHAR)[0])
    end = tuple(np.argwhere(data == END_CHAR)[0])
    return walls, start, end


def create_graph(walls, start, end):
    nodes = np.array([[Node(i, j) for j in range(walls.shape[1])] for i in range(walls.shape[0])])

    for i in range(nodes.shape[0] - 1):
        for j in range(nodes.shape[1]):
            if not walls[i, j] and not walls[i + 1, j]:
                nodes[i, j].neighbours.append(nodes[i + 1, j])
                nodes[i + 1, j].neighbours.append(nodes[i, j])

    for i in range(nodes.shape[0]):
        for j in range(nodes.shape[1] - 1):
            if not walls[i, j] and not walls[i, j + 1]:
                nodes[i, j].neighbours.append(nodes[i, j + 1])
                nodes[i, j + 1].neighbours.append(nodes[i, j])
    return nodes[start], nodes[end]


def a_star(start_node, end_node):
    def dist(node_1, node_2):
        return abs(node_1.i - node_2.i) + abs(node_1.j - node_2.j)

    open_set = {start_node}  # set of nodes being considered
    came_from = {}  # maps nodes to the node that they originated from which had the least cost

    g_score = defaultdict(lambda: np.inf)  # maps nodes to the distance it takes to reach that node from the start node
    g_score[start_node] = 0

    f_score = defaultdict(lambda: np.inf)  # maps nodes to their g_score + the heuristic from that node to the end node
    f_score[start_node] = dist(start_node, end_node)

    while len(open_set) > 0:
        current_node = min(open_set, key=lambda node: f_score[node])
        if current_node == end_node:
            path = [current_node]
            while current_node is not start_node:
                current_node = came_from[current_node]
                path.insert(0, current_node)
            return path
        open_set.remove(current_node)
        for neighbour_node in current_node.neighbours:
            tentative_g_score = g_score[current_node] + dist(current_node, neighbour_node)
            if tentative_g_score < g_score[neighbour_node]:
                came_from[neighbour_node] = current_node
                g_score[neighbour_node] = tentative_g_score
                f_score[neighbour_node] = g_score[neighbour_node] + dist(neighbour_node, end_node)
                open_set.add(neighbour_node)

    return None


def write_solution(walls, path):
    # noinspection PyTypeChecker
    solution = np.full_like(walls, EMPTY_CHAR, dtype=str)
    solution[walls] = WALL_CHAR
    solution[path[0].i, path[0].j] = START_CHAR
    solution[path[-1].i, path[-1].j] = END_CHAR
    for node in path[1:-1]:
        solution[node.i, node.j] = PATH_CHAR

    return '\n'.join([''.join(solution[i, :]) for i in range(solution.shape[0])])


def main():
    walls, start, end = parse_maze('large_maze.txt')
    start_node, end_node = create_graph(walls, start, end)
    path = a_star(start_node, end_node)
    if path is None:
        print('No solution possible!')
    print(write_solution(walls, path))


if __name__ == '__main__':
    main()
