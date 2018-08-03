from mazerunner.solvers.UninformedSolver import UninformedSolver


class BFSSolver(UninformedSolver):
    """ Solver which implements a Breadth First Search. The fringe nodes are stored in a FIFO queue which means all
    cells at a certain depth from the start cell are searched before cells at a greater depth. Since the maze is
    unweighted and therefore the distance from the start cell increments monotonically from zero, the solution is
    guaranteed to be optimal. """

    def __init__(self, runner):
        UninformedSolver.__init__(self, runner)

    def get_next_cell(self):
        """ Return the cell at the front of the queue. """
        return self.queue.pop(0)
