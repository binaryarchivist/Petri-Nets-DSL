class Node:
    def __init__(self, data=None):
        self.data = data
        self.subnodes = []
        self._current_iteration_index = -1

    def add_subnode(self, subnode):
        if isinstance(subnode, Node):
            self.subnodes.append(subnode)
        else:
            raise ValueError("Subnode must be an instance of Node class.")

    def __iter__(self):
        self._current_iteration_index = -1
        return self

    def __next__(self):
        if self._current_iteration_index + 1 < len(self.subnodes):
            self._current_iteration_index += 1
            current_subnode = self.subnodes[self._current_iteration_index]
            return current_subnode

        # Recursively iterate over subnodes
        for subnode in self.subnodes:
            try:
                return next(subnode)
            except StopIteration:
                continue

        raise StopIteration()

    def find_last_nodes(self):
        last_nodes = []
        if not self.subnodes:
            last_nodes.append(self)
        else:
            for subnode in self.subnodes:
                last_nodes.extend(subnode.find_last_nodes())
        return last_nodes

    def find_paths_to_last_nodes(self, current_path=None):
        if current_path is None:
            current_path = []

        current_path.append(self.data)
        paths_to_last_nodes = []

        if not self.subnodes:
            paths_to_last_nodes.append(current_path[:])

        for subnode in self.subnodes:
            paths_to_last_nodes.extend(subnode.find_paths_to_last_nodes(current_path))

        current_path.pop()

        return paths_to_last_nodes
    def __repr__(self):
        return f"Node(data={self.data}, subnodes={self.subnodes})"

