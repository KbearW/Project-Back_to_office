class BinarySearchNode():
    """Binary tree node."""

    def __init__(self, data, left=None, right=None):
        self.data = data

        self.left = left
        self.right = right

    def __repr__(self):
        """Debugging-friendly representation."""

        return "<BinaryNode {data}>".format(data=self.data)

    def find(self, sought):
        """Return node with this data.

        Start here. Return None if not found.
        """

        current = self

        while current:

            print("checking ", current.data)

            if current.data == sought:
                return current

            elif sought < current.data:
                current = current.left

            elif sought > current.data:
                current = current.right


if __name__ == '__main__':
    # Create sample tree and search for nodes in it

    apple = BinarySearchNode("apple")
    ghost = BinarySearchNode("ghost")
    fence = BinarySearchNode("fence", apple, ghost)
    just = BinarySearchNode("just")
    jackal = BinarySearchNode("jackal", fence, just)
    zebra = BinarySearchNode("zebra")
    pencil = BinarySearchNode("pencil", None, zebra)
    mystic = BinarySearchNode("mystic")
    nerd = BinarySearchNode("nerd", mystic, pencil)
    money = BinarySearchNode("money", jackal, nerd)

    print("nerd = ", money.find("nerd"))     # should find
    print("banana = ", money.find("banana"))  # shouldn't find
