class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self, root):
        self.root = Node(root)

    def preorder(self, start, records):
        if start is not None:
            records.append(start.value)  # Root
            records = self.preorder(start.left, records)  # Left subtreer
            records = self.preorder(start.right, records)  # Right subtree
        return records

    def postorder(self, start, records):
        if start is not None:
            records = self.postorder(start.left, records)  # Left subtreer
            records = self.postorder(start.right, records)  # Right subtree
            records.append(start.value)  # Root
        return records


tree = Tree(5)
tree.root.left = Node(3)  # type: ignore
tree.root.right = Node(4)  # type: ignore
tree.root.left.left = Node(2)  # type: ignore
tree.root.left.right = Node(8)  # type: ignore
print(tree.preorder(tree.root, []))
print(tree.postorder(tree.root, []))


#       5
#      / \
#     3  4
#    /   \
#   2     8
#  / \
