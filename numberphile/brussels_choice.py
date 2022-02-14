# https://youtu.be/AeqK96UX3rA
class Node:
    def __init__(self, value, parent=None):
        self.value = value  # int
        self.parent = parent
        self.distance_to_root = parent.distance_to_root + 1 if parent is not None else 0
        self.children = None

    def __str__(self):
        children_str = ('[' + ', '.join([str(child) for child in self.children]) + ']') \
            if self.children is not None else 'None'
        return f'Node({self.value}, {children_str})'

    def print_indented(self, indent=0):
        print('  ' * indent, self.value, sep='')
        if self.children is not None:
            for child in self.children:
                child.print_indented(indent + 1)

    def verify_distance_to_root(self):
        # should be identical to self.distance_to_root
        if self.parent is None:
            return 0
        return 1 + self.parent.steps_to_root()

    def get_root(self):
        return self.parent if self.parent is not None else self

    def check_optimal(self, value, distance_to_beat):
        """
        If you want to check optimality across the entire tree, this should be called from the root.
        If there is a tie, then False is still returned to avoid duplicates in the tree.
        If another node is found that is worse that distance_to_beat, it is pruned from the tree.

        :param value: The value to search for.
        :param distance_to_beat: The distance_to_root that must be beaten.
        :return: True if and only if this Node and all its children cannot beat the provided distance_to_beat.
        """
        if self.value == value:

        if self.distance_to_root > distance_to_beat:
            return True  # neither me nor my children can beat it
        if self.value == value:
            return False  # I beat (or tied) it
        if self.distance_to_root == distance_to_beat:
            return True  # my children cannot beat it, so no point checking

        if self.distance_to_root + 1 == distance_to_beat and self.children is None:
            return True  # my children would tie it, but have not been created yet

        # optimal if and only if all my children say its optimal
        return all([child.check_optimal(value, distance_to_beat) for child in self.children])

    def extend(self):
        children = set()
        value_str = str(self.value)
        for i in range(len(value_str)):
            for j in range(i + 1, len(value_str) + 1):
                prefix = value_str[:i]
                inner_str = value_str[i:j]
                suffix = value_str[j:]

                inner_value = int(inner_str)
                leading_zeros = len(inner_str) - len(str(inner_value))
                if leading_zeros > 0:
                    # skip substrings with leading zeros
                    continue

                children.add(int(prefix + str(2 * inner_value) + suffix))
                if inner_value % 2 == 0:
                    children.add(int(prefix + str(inner_value // 2) + suffix))

        root = self.get_root()
        self.children = [Node(value, parent=self) for value in children
                         if root.check_optimal(value, self.distance_to_root + 1)]

    def extend_generation(self, count=1):
        if count == 0:
            return
        if self.children is None:
            self.extend()
            # noinspection PyTypeChecker
            for child in self.children:
                child.extend_generation(count - 1)
        else:
            for child in self.children:
                child.extend_generation(count)

    def search(self, target):
        if self.value == target:
            return self
        if self.children is None:
            return None

        search_results = list(filter(lambda node: node is not None, [child.search(target) for child in self.children]))
        if len(search_results) == 0:
            return None
        if len(search_results) > 1:
            raise Exception('Duplicate nodes found!')
        return search_results[0]

    def search_until_found(self, target):
        node = self.search(target)
        while node is None:
            self.extend_generation()
            node = self.search(target)
        return node

    def get_sequence_to_root(self):
        if self.parent is None:
            return str(self.value)
        return f'{self.value} -> {self.parent.get_sequence_to_root()}'


def main():
    nodes = []
    root_1 = Node(1)
    root_5 = Node(5)
    for i in range(1, 100):
        if i % 5 == 0:
            nodes.append(root_5.search_until_found(i))
        else:
            nodes.append(root_1.search_until_found(i))
    print(nodes)
    for node in nodes:
        print(node.get_sequence_to_root())


if __name__ == '__main__':
    main()
