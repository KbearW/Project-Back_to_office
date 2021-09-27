# Linked list with Node/LinkedList classes


class Node(object):
    """Node in a linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return "<Node object. Data: {}; Next: {}>".format(
                                        self.data,
                                        self.next.data if self.next else None,
                                        )


class LinkedList(object):
    """Linked List using head and tail.

    Let's make a list:

        >>> ll = LinkedList()

        >>> ll.print_list()

        >>> ll.append(1)
        >>> ll.append(2)
        >>> ll.append(3)
        >>> ll.append(4)

        >>> ll.print_list()
        1
        2
        3
        4

    Test find:

        >>> ll.find(1)
        True

        >>> ll.find(3)
        True

        >>> ll.find(99)
        False

    Test remove:

        >>> ll.remove(99)

        >>> ll.remove(2)
        >>> ll.print_list()
        1
        3
        4
        >>> ll.tail.data
        4

        >>> ll.remove(4)
        >>> ll.print_list()
        1
        3
        >>> ll.tail.data
        3

        >>> ll.remove(1)
        >>> ll.print_list()
        3
        >>> ll.tail.data
        3

        >>> ll.remove(3)
        >>> ll.print_list()
        >>> ll.head
        >>> ll.tail

    """

    def __init__(self):
        self.head = None
        self.tail = None

    def __repr__(self):
        return "<Linked List. Head: {}; Tail: {}>".format(
                                        self.head.data if self.head else None,
                                        self.tail.data if self.head else None,
                                        )

    def append(self, data):
        """Append node with data to end of list."""

        new_node = Node(data)

        if self.head is None:
            self.head = new_node

        if self.tail is not None:
            # Did list start as empty?
            self.tail.next = new_node

        self.tail = new_node

    def print_list(self):
        """Print all items in the list."""

        current = self.head

        while current is not None:
            print(current.data)
            current = current.next

    def find(self, data):
        """Does this data exist in our list?"""

        current = self.head

        while current is not None:
            if current.data == data:
                return True

            current = current.next

        return False

    def remove(self, value):
        """Remove node with given value"""

        # If removing head, make 2nd item (if any) the new .head
        if self.head is not None and self.head.data == value:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return

        # Removing something other than head
        current = self.head

        while current.next is not None:

            if current.next.data == value:
                current.next = current.next.next
                if current.next is None:
                    # If removing last item, update .tail
                    self.tail = current
                return

            else:     # haven't found yet, keep traversing
                current = current.next


class LinkedListNoTail(object):
    """Linked List using head only.

        >>> ll = LinkedListNoTail()

        >>> ll.print_list()

        >>> ll.append_node(1)
        >>> ll.append_node(2)

        >>> ll.print_list()
        1
        2
    """

    def __init__(self):
        self.head = None

    def append_node(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head

            while current.next is not None:
                current = current.next

            current.next = new_node

    def print_list(self):
        """Print all items in the list."""

        current = self.head

        while current is not None:
            print(current.data)
            current = current.next


if __name__ == '__main__':
    ll = LinkedList()
    ll.append("apple")
    ll.append("berry")
    ll.append("cherry")
