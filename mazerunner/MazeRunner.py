from PyQt5.QtWidgets import QFileDialog

import mazerunner.Config as Config
from mazerunner.RunnerCell import RunnerCell, get_index
from mazerunner.solvers.AStarSolver import AStarSolver
from mazerunner.solvers.BFSSolver import BFSSolver
from mazerunner.solvers.BiBFSSolver import BiBFSSolver
from mazerunner.solvers.BiDFSSolver import BiDFSSolver
from mazerunner.solvers.DFSSolver import DFSSolver
from mazerunner.solvers.GreedySolver import GreedySolver


class MazeRunner:
    """ Generates a maze using depth first search """

    def __init__(self, display):
        self.display = display
        self.cells = []
        # Class instance of solver, is set in start_search
        self.solver = None
        self.solved = False

    def start_search(self, search_option):
        """ Calls the appropriate search function based on searchOption """
        if search_option == 'Breadth First Search':
            self.solver = BFSSolver(self)
        elif search_option == 'Bidirectional BFS':
            self.solver = BiBFSSolver(self)
        elif search_option == 'Depth First Search':
            self.solver = DFSSolver(self)
        elif search_option == 'Bidirectional DFS':
            self.solver = BiDFSSolver(self)
        elif search_option == 'Greedy Best First':
            self.solver = GreedySolver(self)
        elif search_option == 'A*':
            self.solver = AStarSolver(self)
        self.solver.start()

    def reset_search(self):
        """ Resets the status of all cells to allow a new search to begin. """
        self.solved = False
        for cell in self.cells:
            cell.reset()

    def get_neighbours(self, cell):
        """ Returns a list of cells which are adjacent to cell. """
        cells = []
        x = cell.get_x()
        y = cell.get_y()

        # Above, check cell above's bottom wall
        if y > 0 and not self.cells[get_index(x, y - 1)].get_walls().get('bottom'):
            cells.append(self.cells[get_index(x, y - 1)])
        # Right
        if x < Config.RUNNER_MAZE_COLUMNS - 1 and not cell.get_walls().get('right'):
            cells.append(self.cells[get_index(x + 1, y)])
        # Below
        if y < Config.RUNNER_MAZE_ROWS - 1 and not cell.get_walls().get('bottom'):
            cells.append(self.cells[get_index(x, y + 1)])
        # Left, check cell to the left's right wall
        if x > 0 and not self.cells[get_index(x - 1, y)].get_walls().get('left'):
            cells.append(self.cells[get_index(x - 1, y)])
        return cells

    def load_maze(self):
        """ Load a maze from a file. The expected format for the file has the dimensions of the maze on the first line
        in the format "columns rows" (two integers separated by a space). Then there are columns x rows lines, each
        containing a 4 bit number. The lines are the cells in order where a 1 indicates a wall (ordered top right
        bottom left). In total the file will have columns x rows + 1 lines
        """
        self.display.delete_grid()
        del self.cells[:]
        # Allow user to select filename
        dialog = QFileDialog()
        filename = dialog.getOpenFileName(dialog, "Load maze", '.\\mazes\\', '*.txt')[0]
        if not filename:
            # No filename chosen
            return False

        with open(filename, 'r') as file:
            lines = file.readlines()
            columns, rows = [int(x) for x in lines[0].split()]
            Config.set_maze_dimensions(columns, rows, 'runner')

            x, y = 0, 0
            for line in lines[1:]:
                line = line.strip()
                cell = RunnerCell(x, y, int(line[0]), int(line[1]))
                self.cells.append(cell)

                x = (x + 1) % columns
                if not x:
                    y = (y + 1) % rows

        if len(self.cells) != columns * rows:
            return False
        return True

    def recommence(self):
        """ Recommence the solver. """
        self.solver.recommence()

    def get_cells(self):
        """ Returns the cells """
        return self.cells

    def get_solved(self):
        """ Returns the solved status for the runner """
        return self.solved
