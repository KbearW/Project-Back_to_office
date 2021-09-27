"""Example of using a queue to make a console "task manager"."""


class Queue(object):
    """A simple queue, implemented using a list."""

    # NOTE: this is a straightforward way to implement a
    # queue -- but it's also inefficient if you'll have
    # many items in the queue. For a more efficient queue
    # implementation, you could build a Queue class
    # yourself using a doubly-linked list, or you could use
    # the Queue class included in Python's standard library,
    # "collections.deque" ("deque" = "double-ended queue")

    def __init__(self):
        self._data = []

    def enqueue(self, item):
        """Add to end of queue."""

        self._data.append(item)

    def dequeue(self):
        """Remove from front of queue."""

        return self._data.pop(0)

    def peek(self):
        """Show first item in queue."""

        return self._data[0]

    def is_empty(self):
        """Is queue empty?"""

        return not self._data


task_queue = Queue()

while True:

    if task_queue.is_empty():
        next_task = None
    else:
        next_task = task_queue.peek()

    print("Next task:", next_task)

    command = input("A)dd task, D)o first task, or Q)uit? ")

    if command == "A":
        task = input("Task: ")
        task_queue.enqueue(task)

    elif command == "D":
        print("Completed:", task_queue.dequeue())

    elif command == "Q":
        break

    else:
        print("*** Invalid command; try again ***")

