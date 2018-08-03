from mazerunner.solvers.UninformedSolver import UninformedSolver


class DFSSolver(UninformedSolver):
    """ Solver which implements a Depth First Search. The fringe nodes are stored in a stack which means a single path
    is exhausted before the search backtracks to search shallower cells. The path produced by dfs is not guaranteed to
     be optimal. """

    def __init__(self, runner):
        UninformedSolver.__init__(self, runner)

    def get_next_cell(self):
        """ Returns the cell at the top of the stack (end of the queue). """
        return self.queue.pop()
