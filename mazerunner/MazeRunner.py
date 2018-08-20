from PyQt5.QtWidgets import QFileDialog

from mazerunner.RunnerCell import RunnerCell
from mazerunner.solvers.AStarSolver import AStarSolver
from mazerunner.solvers.BFSSolver import BFSSolver
from mazerunner.solvers.BiBFSSolver import BiBFSSolver
from mazerunner.solvers.BiDFSSolver import BiDFSSolver
from mazerunner.solvers.DFSSolver import DFSSolver
from mazerunner.solvers.GreedySolver import GreedySolver


class MazeRunner:
    """ Generates a maze using depth first search. """

    def __init__(self, display):
        self.display = display
        self.cells = []
        # Class instance of solver, is set in start_search
        self.solver = None
        self.running = False
        self.paused = False
        self.solved = False

    def start_search(self, search_option):
        """ Calls the appropriate search function based on the search option. """
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
        if y > 0 and not self.cells[self.get_cell_index(x, y - 1)].get_walls().get('bottom'):
            cells.append(self.cells[self.get_cell_index(x, y - 1)])
        # Right
        if x < self.display.get_columns() - 1 and not cell.get_walls().get('right'):
            cells.append(self.cells[self.get_cell_index(x + 1, y)])
        # Below
        if y < self.display.get_rows() - 1 and not cell.get_walls().get('bottom'):
            cells.append(self.cells[self.get_cell_index(x, y + 1)])
        # Left, check cell to the left's right wall
        if x > 0 and not self.cells[self.get_cell_index(x - 1, y)].get_walls().get('right'):
            cells.append(self.cells[self.get_cell_index(x - 1, y)])
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
            self.display.set_maze_dimensions(columns, rows)

            x, y = 0, 0
            for line in lines[1:]:
                line = line.strip()
                cell = RunnerCell(x, y, int(line[0]), int(line[1]), self)
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
        """ Returns the cells. """
        return self.cells

    def get_running(self):
        """ Returns the running status. """
        return self.running

    def set_running(self, value):
        """ Sets the running flag to the given value. """
        self.running = value

    def get_paused(self):
        """ Returns the paused status. """
        return self.paused

    def set_paused(self, value):
        """ Sets the paused flag to the given value. """
        self.paused = value

    def get_solved(self):
        """ Returns the solved status. """
        return self.solved

    def get_columns(self):
        """ Returns the number of columns in the grid. """
        return self.display.get_columns()

    def get_rows(self):
        """ Returns the number of rows in the grid. """
        return self.display.get_rows()

    def get_cell_dimension(self):
        """ Returns the side length of a cell in the grid. """
        return self.display.get_cell_dimension()

    def get_cell_index(self, x, y):
        """ Returns the array index for the cell at position (x, y). """
        return y * self.display.get_columns() + x
