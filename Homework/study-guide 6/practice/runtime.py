def string_compare(s1, s2):
    """Given two strings, figure out if they are exactly the same (without using ==).

    """

    if len(s1) != len(s2):
        return False

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False

    return True


def has_exotic_animals(animals):
    """Determine whether a list of animals contains exotic animals."""

    if "hippo" in animals or "platpypus" in animals:
        return True
    else:
        return False


def sum_zero_1(numbers):
    """Find pairs of integers that sum to zero."""

    result = []

    # Hint: the following line, "s = set(numbers)", is O(n) ---
    # we'll learn exactly why later
    s = set(numbers)

    for x in s:
        if -x in s:
            result.append((-x, x))

    return result


def sum_zero_2(numbers):
    """Find pairs of integers that sum to zero. """

    result = []

    for x in numbers:
        for y in numbers:
            if x == -y:
                result.append((x, y))
    return result


def sum_zero_3(numbers):
    """Find pairs of integers that sum to zero.

    This version gets rid of duplicates (it won't add (1, -1) if (-1, 1) already there.

    """

    result = []

    for x in numbers:
        for y in numbers:
            if x == -y and (x, y) not in result and (y, x) not in result:
                result.append((x, y))
    return result
