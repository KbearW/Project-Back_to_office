"""FIFO queues implemented as linked list and circular array."""

__author__ = "Joel Burton <joel@joelburton.com>"


class Node():
    """Node in a queue."""

    # Pre-declare only allowed attributes as a memory optimization
    __slots__ = ['data', 'next']

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return "<Node {data}>".format(data=self.data)


class QueueEmptyError(IndexError):
    """Attempt to dequeue an empty queue."""


class Queue():
    """FIFO queue.

    Implemented as a linked list. This will be slower than
    using a Python list for small lists but when the list
    size is larger than ~5,000, it becomes faster to use,
    as it's expensive to pop items off the front of a Python
    list (this is a O(n) operation, whereas it's O(1) for
    a linked list.

    This is useful for studying how linked lists work but,
    should you want one in a real-world program, see the
    `collections.deque object` --- this is a
    doubly-linked lists, but it will perform excellently,
    given that it is implemented in C.
    """

    def __init__(self, inlist):
        self._tail = None
        self._length = len(inlist)

        prev = None
        for item in inlist[::-1]:
            node = Node(item, next=prev)
            if self._tail is None:
                self._tail = node
            prev = node
        self._head = prev

    def __repr__(self):
        if not self._head:
            return "<Queue (empty)>"
        else:
            return "<Queue head={head} tail={tail} length={length}>".format(
                head=self._head.data, tail=self._tail.data, length=self._length)

    def enqueue(self, item):
        """Add item to end of queue."""

        self._length += 1
        node = Node(item)
        if self._tail:
            self._tail.next = node
            self._tail = node
        else:
            self._head = self._tail = node

    def dequeue(self):
        """Remove item from front of queue and return it."""

        if not self._head:
            raise QueueEmptyError()

        self._length -= 1
        node = self._head
        self._head = self._head.next

        if not self._head:
            self._tail = None

        return node.data

    def __iter__(self):
        """Allow iteration over list.

        __iter__ is a special method that, when defined,
        allows you to loop over a list, so you can say things
        like "for item in my_queue", and it will pop
        successive items off.
        """

        while True:
            try:
                yield self.dequeue()
            except QueueEmptyError:
                raise StopIteration

    def length(self):
        """Return length of queue."""

        return self._length

    def peek(self):
        """Return, but don't remove, item at front of queue."""

        if self.is_empty():
            return None

        return self._head.data

    def empty(self):
        """Empty queue."""

        self._tail = self._head = None
        self._length = 0

    def is_empty(self):
        """Is queue empty?"""

        return not bool(self._length)


class ArrayQueue():
    """FIFO queue.

    Implemented by using a standard Python list as a circular
    array---we loop around in it, and keep track of where the
    "front" currently is. This will usually perform a bit
    better than a linked list.

    This is useful for studying how circular arrays work but,
    should you want one in a real-world program, see the
    `collections.deque` object --- this is a doubly-linked
    lists, but it will perform excellently, given that it is
    implemented in C.
    """

    def __init__(self, inlist):
        self._data = inlist          # underlying storage is a python list
        self._dlength = len(inlist)  # actual length of underlying python list
        self._length = len(inlist)   # number of items in queue
        self._front = 0              # index in list of first item in queue

    def __repr__(self):
        return "<ArrayQueue head={head} length={length}>".format(
            head=self._data[self._front], length=self._length)

    def __iter__(self):
        """Allow iteration over list.

        __iter__ is a special method that, when defined,
        allows you to loop over a list, so you can say things
        like "for item in my_queue", and it will pop
        successive items off.
        """

        while True:
            try:
                yield self.dequeue()
            except QueueEmptyError:
                raise StopIteration

    def enqueue(self, item):
        """Add item to end of queue."""

        if self._length == self._dlength:
            self._resize(2 * self._dlength)

        next_spot = (self._front + self._length) % self._dlength
        self._data[next_spot] = item
        self._length += 1

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

    def dequeue(self):
        """Remove item from front of queue and return it."""

        if self._length == 0:
            raise QueueEmptyError()

        out = self._data[self._front]

        self._front = (self._front + 1) % self._dlength
        self._length -= 1

        return out

    def length(self):
        """Return length of queue."""

        return self._length

    def peek(self):
        """Return, but don't remove, item at front of queue."""

        if self.is_empty():
            return None

        return self._data[self._front]

    def empty(self):
        """Empty queue."""

        self._data = []
        self._length = 0
        self._front = 0

    def is_empty(self):
        """Is queue empty?"""

        return self._length == 0


if __name__ == '__main__':
    fruits = Queue(["apple", "berry", "cherry"])
    fruits.enqueue("durian")
    assert(fruits.length() == 4)
    assert(fruits.dequeue() == "apple")
    assert(fruits.length() == 3)

    from timeit import timeit

    print("Time for our Queue class")
    print(timeit("q.dequeue(); q.enqueue(0)", "from __main__ import Queue; q=Queue(list(range(50000)))"))

    print("Time for our ArrayQueue class")
    print(timeit("q.dequeue(); q.enqueue(0)", "from __main__ import ArrayQueue; q=ArrayQueue(list(range(50000)))"))

    print("Time for native Python list as queue")
    print(timeit("q.append(1); q.pop(0)", "q=(list(range(50000)))"))

    print("Time for native Python deque as queue")
    print(timeit("q.append(1); q.popleft()", "from collections import deque; q=deque(list(range(50000)))"))
