class StackEmptyError(IndexError):
    """Attempt to pop an empty stack."""


class Stack(object):
    """LIFO stack.

    Implemented using a Python list; since stacks just need
    to pop and push, a list is a good implementation, as
    these are O(1) for native Python lists. However, in cases
    where performance really matters, it might be best to
    use a Python list directly, as it avoids the overhead
    of a custom class.

    Or, for even better performance (& typically smaller
    memory footprint), you can use the `collections.deque`
    object, which can act like a stack.

    (We could also write our own LinkedList class for a
    stack, where we push things onto the head and pop things
    off the head (effectively reversing it), but that would be less
    efficient than using a built-in Python list or a
    `collections.deque` object)
    """

    def __init__(self):
        self._list = []

    def __repr__(self):
        if not self._list:
            return "<Stack (empty)>"
        else:
            return "<Stack tail=%s length=%d>" % (
                self._list[-1], len(self._list))

    def push(self, item):
        """Add item to end of stack."""

        self._list.append(item)

    def pop(self):
        """Remove item from end of stack and return it."""

        if not self._list:
            raise StackEmptyError()

        return self._list.pop()

    def __iter__(self):
        """Allow iteration over list.

        __iter__ is a special method that, when defined,
        allows you to loop over a list, so you can say things
        like "for item in my_stack", and it will pop
        successive items off.
        """

        while True:
            try:
                yield self.pop()
            except StackEmptyError:
                raise StopIteration

    def length(self):
        """Return length of stack::

            >>> s = Stack()
            >>> s.length()
            0

            >>> s.push("dog")
            >>> s.push("cat")
            >>> s.push("fish")

            >>> s.length()
            3
        """
        return len(self)

        
    def empty(self):
        """Empty stack::

            >>> s = Stack()
            >>> s.push("dog")
            >>> s.push("cat")
            >>> s.push("fish")

            >>> s.length()
            3

            >>> s.empty()

            >>> s.length()
            0
        """
        while not len(self):
            return True


    def is_empty(self):
        """Is stack empty?

            >>> s = Stack()

            >>> s.is_empty()
            True

            >>> s.push("dog")
            >>> s.push("cat")
            >>> s.push("fish")

            >>> s.is_empty()
            False
        """
        if len(self) >0:
            return False
        else:
            return True

if __name__ == "__main__":
    import doctest

    print()
    result = doctest.testmod()
    if not result.failed:
        print("ALL TESTS PASSED. GOOD WORK!")
    print()

