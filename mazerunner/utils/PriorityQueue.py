class PriorityQueue:
    """ Priority queue which is represented as a balanced binary heap. The items are ordered according to their
    comparator, that is n <= d for every node n and its descendants d. Thus, if the queue is non-empty, the item with
    the lowest value is stored at queue[0] and is returned by get().

    Implementation of a priority queue as python's lib/queue Priority Queue does not allow for items to be removed
    unless they popped from the front of the queue. This implementation is a translated from the java implementation
    util/PriorityQueue.java in openjdk8 which is release under GPL.

    Accessible here as at 13 Sept 2018:
    http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/687fd7c7986d/src/share/classes/java/util/PriorityQueue.java
    """

    def __init__(self):
        self.queue = []
        self.size = 0

    def put(self, item):
        """
        Add the specified item to the priority queue. The running time of this operation is O(log(n)).
        :param item: The item to add
        :return: None
        """
        if self.size == 0:
            self.queue.append(item)
            self.size += 1
        else:
            self.size += 1
            self.sift_up(self.size, item)

    def get(self):
        """
        Returns the item at the front of the priority queue and reorders the heap such that the invariant is maintained.
        The running time of this operation is O(log(n)).
        :return: The item at the front of the priority queue
        """
        if self.size == 0:
            return None
        self.size -= 1
        item = self.queue[0]
        last_item = self.queue[self.size]
        self.queue.remove(last_item)
        if self.size:
            self.sift_down(0, last_item)
        return item

    def sift_up(self, index, item):
        """
        Inserts the given item at the given index and moves it up the heap until it is greater than or equal to its
        parent or becomes the root and as such the heap invariant is preserved.
        :param index: The position at which the item is inserted
        :param item: The item to insert
        :return: None
        """
        while index > 0:
            parent_index = (index - 1) >> 1
            parent = self.queue[parent_index]
            if parent < item:
                break
            self.add_at(parent, index)
            index = parent_index
        self.add_at(item, index)

    def sift_down(self, index, item):
        """
        Inserts the given item at the given index and moves it down the heap until it is less than or equal to its
        parent and as such the heap invariant is preserved.
        :param index: The index at which to insert the item
        :param item: The item to insert
        :return: None
        """
        half_index = self.size >> 1
        while index < half_index:
            child_index = (index << 1) + 1
            child = self.queue[child_index]
            right_index = child_index + 1
            if right_index < self.size and child > self.queue[right_index]:
                child_index = right_index
                child = self.queue[child_index]
            if item <= child:
                break
            self.queue[index] = child
            index = child_index
        self.queue[index] = item

    def delete(self, item):
        """
        Removes the first occurrence of the given item from the priority queue, if it is present. The running time of
        this operation is O(n + log(n)).
        :param item: The item to remove
        :return: None
        """
        try:
            index = self.queue.index(item)
            self.size -= 1
            if self.size == index:
                self.queue.remove(item)
            else:
                last_item = self.queue[self.size]
                self.queue.remove(last_item)
                self.sift_down(index, last_item)
                if self.queue[index] == last_item:
                    self.sift_up(index, last_item)
        except ValueError:
            return None

    def contains(self, item):
        """
        Returns True if the given item appears in the priority queue. The running time of this operation is O(n).
        :param item: the item to to be checked for
        :return: True if the item is contained in this priority queue
        """
        return item in self.queue

    def clear(self):
        """
        Removes all items from this priority queue.
        :return: None
        """
        self.size = 0
        del self.queue[:]

    def __repr__(self):
        return str(self.queue)

    def add_at(self, item, index):
        """
        Adds the given item to the queue array at the given index. Used to avoid IndexErrors when adding to the end of
        the queue.
        :param item: The item to add to the queue
        :param index: The index at which to add the item
        :return: None
        """
        if index >= self.size:
            self.queue.append(item)
        else:
            self.queue[index] = item

    def empty(self):
        """
        Returns true if this priority queue is empty.
        :return: True if this priority queue is empty
        """
        return self.size == 0
