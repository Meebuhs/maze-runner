from mazerunner.solvers.BidirectionalUninformedSolver import BidirectionalUninformedSolver


class BiBFSSolver(BidirectionalUninformedSolver):
    """ Solver which implements a Bidirectional Breadth First Search. One search commences forward from the start cell
    and the other backwards from the goal. The search terminates when a cell has been visited by both the forward and
    backward search. Since bfs is used for both searches, the cell at which they intersect is guaranteed to have the
    shortest path to each end and thus the solution is guaranteed to be optimal. """

    def __init__(self, runner):
        BidirectionalUninformedSolver.__init__(self, runner)

    def get_next_cell(self, queue):
        """ Returns the cell at the front of the queue. """
        return queue.pop(0)
