from mazerunner.solvers.BidirectionalUninformedSolver import BidirectionalUninformedSolver


class BiDFSSolver(BidirectionalUninformedSolver):
    """ Solver which implements a Bidirectional Depth First Search. One search commences forward from the start cell
    and the other backwards from the goal. The search terminates when a cell has been visited by both the forward and
    backward search. Since dfs is used for both searches, the solution produced by this search is not guaranteed to
    be optimal. """

    def __init__(self, runner):
        BidirectionalUninformedSolver.__init__(self, runner)

    def get_next_cell(self, queue):
        """ Returns the cell at the top of the stack (end of the queue). """
        return queue.pop()
