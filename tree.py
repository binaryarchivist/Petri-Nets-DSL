class Node:
    def __init__(self, data=None):
        self.data = data
        self.subnodes = []

    def add_subnode(self, subnode):
        if isinstance(subnode, Node):
            self.subnodes.append(subnode)
        else:
            raise ValueError("Subnode must be an instance of Node class.")

    def __repr__(self):
        return f"Node(data={self.data}, subnodes={self.subnodes})"

