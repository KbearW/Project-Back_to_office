"""Double-ended queue.

Two implementations provided:

- doubly-linked list
- circular array.

"""

__author__ = "Joel Burton <joel@joelburton.com>"


class DNode(object):
    """Doubly-linked Node in a double-ended queue."""

    # Pre-declare only allowed attributes as a memory optimization
    __slots__ = ['data', 'next', 'prev']

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        return "<Node {data}>".format(data=self.data)


class DequeEmptyError(IndexError):
    """Attempt to dequeue an empty deque."""


class Deque(object):
    """Double-ended queue.

    Implemented as a doubly-linked list. This will be slower
    than using a Python list for small lists but when the list
    size is larger than ~5,000, it becomes faster to use, as
    it's expensive to pop items off the front of a Python list
    (this is a O(n) operation, whereas it's O(1) for a linked list.

    This is useful for studying how doubly-linked lists work but,
    should you want one in a real-world program, see the
    `collections.deque` object.
    """

    def __init__(self, inlist):
        self._head = None
        self._length = len(inlist)

        last = None
        for item in inlist:
            node = DNode(item, prev=last)
            if last:
                last.next = node
            if self._head is None:
                self._head = node
            last = node
        self._tail = last

    def __repr__(self):
        if not self._head:
            return "<Deque (empty)>"
        else:
            return "<Deque head={head} tail={tail} length={length}>".format(
                head=self._head.data, tail=self._tail.data, length=self._length)

    def append(self, item):
        """Add item to end of queue."""

        self._length += 1
        node = DNode(item, prev=self._tail)
        if self._tail:
            self._tail.next = node
            self._tail = node
        else:
            self._head = self._tail = node

    def appendleft(self, item):
        """Add item to start of deque."""

        self._length += 1
        node = DNode(item, next=self._head)
        if self._head:
            self._head.prev = node
            self._head = node
        else:
            self._head = self._tail = node

    def pop(self):
        """Remove item from end of deque and return it."""

        if not self._tail:
            raise DequeEmptyError()

        self._length -= 1
        node = self._tail
        self._tail = node.prev

        if not self._tail:
            self._head = None

        return node.data

    def popleft(self):
        """Remove item from start of deque and return it."""

        if not self._head:
            raise DequeEmptyError()

        self._length -= 1
        node = self._head
        self._head = node.next

        if not self._head:
            self._tail = None

        return node.data

    def length(self):
        """Return length of deque."""

        return self._length

    def empty(self):
        """Empty deque."""

        self._tail = self._head = None
        self._length = 0

    def is_empty(self):
        """Is deque empty?"""

        return not bool(self._length)


class ArrayDeque(object):
    """Dequeue.

    Implemented by using a standard Python list as a
    circular array--we loop around in it, and keep track of
    where the "front" currently is. This will usually perform
    better than a doubly-linked list.

    This is useful for studying how circular arrays work but,
    should you want one in a real-world program, see the
    `collections.deque` object --- this is a doubly-linked
    lists, but it will perform excellently, given that it
    is implemented in C.
    """

    def __init__(self, inlist):
        self._data = inlist          # underlying storage is list
        self._dlength = len(inlist)  # actual len of underlying list
        self._length = len(inlist)   # number of items in queue
        self._front = 0              # index in list of 1st queue item

    def __repr__(self):
        return "<ArrayDequeue head={head} length={length}>".format(
            head=self._data[self._front], length=self._length)

    def __iter__(self):
        """Allow iteration over list.

        __iter__ is a special method that, when defined,
        allows you to loop over a list, so you can say
        things like "for item in my_queue", and it will
        pop successive items off.
        """

        while True:
            try:
                yield self.popleft()
            except DequeEmptyError:
                raise StopIteration

    def _resize(self, capacity):
        """Grow underlying list to capacity."""

        old = self._data

        # Create new list of the right size
        self._data = [None] * capacity
        self._dlength = capacity

        # Walk current list, copying into new list
        walk = self._front
        for i in range(self._length):
            self._data[i] = old[walk]
            walk = (1 + walk) % len(old)

        # Since we put the first item at start of list,
        # our front is now 0 again
        self._front = 0

    def append(self, item):
        """Add item to end of queue."""

        if self._length == self._dlength:
            self._resize(2 * self._dlength)

        next_spot = (self._front + self._length) % self._dlength
        self._data[next_spot] = item
        self._length += 1

    def appendleft(self, item):
        """Add item to start of queue."""

        if self._length == self._dlength:
            self._resize(2 * self._dlength)

        self._front = (self._front - 1) % self._dlength
        self._data[self._front] = item
        self._length += 1

    def popleft(self):
        """Remove item from front of queue and return it."""

        if self._length == 0:
            raise DequeEmptyError()

        out = self._data[self._front]

        self._front = (self._front + 1) % self._dlength
        self._length -= 1

        return out

    def pop(self):
        """Remove item from end of queue and return it."""

        if self._length == 0:
            raise DequeEmptyError()

        out = self._data[
            (self._front + self._length - 1) % self._dlength]

        self._length -= 1

        return out

    def length(self):
        """Return length of queue."""

        return self._length

    def empty(self):
        """Empty queue."""

        self._data = []
        self._length = 0
        self._front = 0

    def is_empty(self):
        """Is queue empty?"""

        return self._length == 0


if __name__ == '__main__':
    fruits = ArrayDeque(["apple", "berry", "cherry"])
    fruits.append("durian")
    assert(fruits.length() == 4)
    assert(fruits.pop() == "durian")
    assert(fruits.length() == 3)
    fruits.appendleft("hello")
    assert(fruits.length() == 4)
    assert(fruits.popleft() == "hello")

    from timeit import timeit

    print("Time for our Deque class")
    print(timeit("q.pop(); q.append(1); q.popleft(); q.appendleft(2)",
                 "from deque import Deque; q=Deque(range(50000))"))

    print("Time for our ArrayDeque class")
    print(timeit("q.pop(); q.append(1); q.popleft(); q.appendleft(2)",
                 "from deque import ArrayDeque; q=ArrayDeque(range(50000))"))

    print("Time for native Python list as deque")
    print(timeit("q.append(1); q.pop(); q.insert(0, 0); q.pop(0)", "q=range(50000)"))

    print("Time for native Python deque as deque")
    print(timeit("q.append(1); q.pop(); q.appendleft(2); q.popleft()",
                 "from collections import deque; q=deque(range(50000))"))

