from math import sqrt


class SampleGraphNode:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.distance = float("inf")
        self.parent = None

    def distance_to(self, node):
        """ Returns the distance to the given node. """
        return sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    def __repr__(self):
        return "id:{}-({}, {})".format(self.id, self.x, self.y)

    def __lt__(self, other):
        """ Override the less than comparator with an arbitrary result, this is used to fix priority queue breaking
        when two nodes are the same distance from the goal. """
        return self.distance < other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def __cmp__(self, other):
        if self.distance > other.distance:
            return 1
        elif self.distance < other.distance:
            return -1
        else:
            return 0
