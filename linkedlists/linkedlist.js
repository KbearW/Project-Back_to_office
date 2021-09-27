"use strict";

// A node in a linked list.
class Node {
  constructor(data) {
    this.data = data;
    this.next = null;
  }
}

// A linked list
class LinkedList {
  constructor() {
    this.head = null;
    this.tail = null;
  }

  // Append `data` to the end of the list
  append(data) {
    const newNode = new Node(data);

    if (this.head === null) {
      this.head = newNode;
    }

    if (this.tail !== null) {
      this.tail.next = newNode;
    }

    this.tail = newNode;
  }

  // Print the items in the list
  print() {
    let current = this.head;
    while (current !== null) {
      console.log(current.data);

      current = current.next;
    }
  }

  // Find a node containing `data`
  find(data) {
    let current = this.head;

    while (current !== null) {
      if (current.data === data) {
        return current;
      }

      current = current.next;
    }
  }
}
