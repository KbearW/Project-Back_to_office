"""A pancake-themed demonstration of stacks.

See stack.py for the implementation of the Stack class imported here.
"""

from stack import Stack


class PancakeStack(Stack):
    """A stack of pancakes."""

    def __repr__(self):
        """A more helpful representation of the PancakeStack."""

        return "<PancakeStack NEXT: {pancake} REMAINING: {num}>".format(
            pancake=self.peek(), num=self.length())

    def eat_next_pancake(self):
        """Remove a pancake from the plate and acknowledge its deliciousness."""

        print("Mmmm, {to_eat} pancakes are tasty!".format(to_eat=self.pop()))

    def empty(self):
        """Clear all pancakes from the plate. Note their tastiness."""

        while not self.is_empty():
            print("There goes the {to_eat} pancake...delicious.".format(
                to_eat=self.pop()))

        self.print_empty_plate()

    def check_next_pancake(self):
        """Display the pancake at the top of the stack."""

        next_pancake = self.peek()
        if next_pancake:
            print("You'll eat a {to_eat} pancake next. Yum!".format(
                to_eat=next_pancake))

        else:
            self.print_empty_plate()

    def check_plate(self):
        """Print an ASCII-art representation of the pancake stack."""

        if not self.is_empty():
            print()
            print("     ({top})    <--- Top of Stack".format(
                top=self._list[-1]))

            for pancake in self._list[-2::-1]:
                print("     ({next_pancake})    ".format(next_pancake=pancake))

            print("\________________________/")
            print()

        else:
            self.print_empty_plate()

    def print_empty_plate(self):
        """Show an ASCII-art representation of a plate with no pancakes."""

        print()
        print("Your plate is empty...just looking at it makes me sad. T.T")
        print("See? \________________________/")
        print()


def run_pancake_shop(pancakes=None):
    """REPL for our stack-based pancake diner."""

    if pancakes:
        plate = PancakeStack(pancakes)

    else:
        plate = PancakeStack()

    print("\nWelcome to Balloonicorn's Diner! We only serve pancakes here.")

    while True:
        print("\nDo you want to: ")
        print("O)rder a pancake, E)at a pancake, C)heck your plate, or L)eave?")
        choice = input("> ").upper()

        if choice == "O":
            flavor = input("\nWhat flavor do you want to order? ")
            plate.push(flavor)

        elif choice == "E":
            plate.eat_next_pancake()

        elif choice == "C":
            plate.check_plate()

        elif choice == "L":
            print("\nHope you enjoyed the pancakes. Don't forget to pay up. :)")
            break

        else:
            print("You can't do that at this diner!")


if __name__ == "__main__":

    run_pancake_shop()
