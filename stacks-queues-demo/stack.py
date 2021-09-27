"""LIFO stack implemented using Python native list."""

__author__ = "Joel Burton <joel@joelburton.com>"


class StackEmptyError(IndexError):
    """Attempt to pop an empty stack."""


class Stack():
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

    def __init__(self, inlist=None):
        if inlist:
            self._list = inlist
        else:
            self._list = []

    def __repr__(self):
        if not self._list:
            return "<Stack (empty)>"
        else:
            return "<Stack tail={tail} length={length}>".format(
                tail=self._list[-1], length=len(self._list))

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

    def push(self, item):
        """Add item to end of stack."""

        self._list.append(item)

    def pop(self):
        """Remove item from end of stack and return it."""

        if not self._list:
            raise StackEmptyError()

        return self._list.pop()


    def length(self):
        """Return length of stack."""

        return len(self._list)

    def peek(self):
        """Return, but don't remove, top item."""

        if self.is_empty():
            return None

        return self._list[-1]

    def empty(self):
        """Empty stack."""

        self._list = []

    def is_empty(self):
        """Is stack empty?"""

        return not bool(self._list)


def are_parens_balanced(symbols):
      """Are parentheses balanced in expression?"""

      # make a stack
      parens = Stack()

      for char in symbols:

          if char == "(":
              parens.push(char)   # push onto stack

          elif char == ")":
              if parens.is_empty():
                  return False
              else:
                  parens.pop()      # pop from stack

      return parens.is_empty()

are_parens_balanced("((3+4)-(1+2))/(1+1)")


if __name__ == '__main__':
    fruits = Stack(["apple", "berry", "cherry"])
    fruits.push("durian")
    assert(fruits.length() == 4)
    assert(fruits.pop() == "durian")
    assert(fruits.length() == 3)

    from timeit import timeit

    print("Time for our Stack class")
    print(timeit("s.push(1); s.pop()", "from __main__ import Stack; s=Stack(list(range(50000)))"))

    print("Time for native Python list as stack")
    print(timeit("s.append(1); s.pop()", "s=(list(range(50000)))"))

    print("Time for native Python deque as stack")
    print(timeit("s.append(1); s.pop()", "from collections import deque; s=deque(list(range(50000)))"))
