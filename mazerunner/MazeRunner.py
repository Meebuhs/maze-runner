from pathlib import Path

from PyQt5.QtWidgets import QFileDialog

from mazerunner.RunnerCell import RunnerCell
from mazerunner.solvers.AStarSolver import AStarSolver
from mazerunner.solvers.BFSSolver import BFSSolver
from mazerunner.solvers.BiBFSSolver import BiBFSSolver
from mazerunner.solvers.BiDFSSolver import BiDFSSolver
from mazerunner.solvers.DFSSolver import DFSSolver
from mazerunner.solvers.GreedySolver import GreedySolver
from mazerunner.solvers.RandomSampleSolver import RandomSampleSolver


class MazeRunner:
    """ Generates a maze using depth first search. """

    def __init__(self, display):
        self.display = display
        self.cells = []
        # References to the sample solvers display items for cleanup
        self.sample_display_items = []
        # Class instance of solver, is set in start_search
        self.solver = None
        self.running = False
        self.paused = False
        self.solved = False
        self.start_cell = None
        self.goal_cell = None

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
        elif search_option == 'Random Sampling':
            self.solver = RandomSampleSolver(self)
        self.solver.start()

    def reset_search(self):
        """ Resets the status of all cells to allow a new search to begin. """
        self.solved = False
        if self.sample_display_items:
            for item in self.sample_display_items:
                self.display.removeItem(item)
            self.sample_display_items = []
        for cell in self.cells:
            cell.reset()

    def get_neighbours(self, cell):
        """ Returns a list of cells which are adjacent to cell. """
        cells = []
        x = cell.x
        y = cell.y

        # Above, check cell above's bottom wall
        if y > 0 and not self.cells[self.get_cell_index(x, y - 1)].walls.get('bottom'):
            cells.append(self.cells[self.get_cell_index(x, y - 1)])
        # Right
        if x < self.display.columns - 1 and not cell.walls.get('right'):
            cells.append(self.cells[self.get_cell_index(x + 1, y)])
        # Below
        if y < self.display.rows - 1 and not cell.walls.get('bottom'):
            cells.append(self.cells[self.get_cell_index(x, y + 1)])
        # Left, check cell to the left's right wall
        if x > 0 and not self.cells[self.get_cell_index(x - 1, y)].walls.get('right'):
            cells.append(self.cells[self.get_cell_index(x - 1, y)])
        return cells

    def load_maze(self):
        """ Load a maze from a file. The expected format for the file has the dimensions of the maze on the first line
        in the format "columns rows" (two integers separated by a space). Then there are columns x rows lines, each
        containing 2 binary digits indicating whether the cell has a bottom or right wall. In total the file will have
        columns x rows + 1 lines
        """
        # Allow user to select filename
        dialog = QFileDialog()
        path = Path('./mazes')
        filename = dialog.getOpenFileName(dialog, "Load maze", str(path.resolve()), '*.txt')[0]
        if not filename:
            # No filename chosen
            return False

        self.display.delete_grid()
        self.reset_search()
        del self.cells[:]

        with open(filename, 'r') as file:
            lines = file.readlines()
            columns, rows = [int(x) for x in lines[0].split()]
            self.display.set_maze_dimensions(columns, rows)

            x, y = 0, 0
            for line in lines[1:]:
                line = line.strip()
                cell = RunnerCell(x, y, int(line[0]), int(line[1]), self.display)
                self.cells.append(cell)

                x = (x + 1) % columns
                if not x:
                    y = (y + 1)

        if len(self.cells) != columns * rows:
            return False
        return True

    def recommence(self):
        """ Recommence the solver. """
        self.solver.recommence()

    def initialise_start_and_goal_cells(self):
        """ Sets the start cell to be the upper leftmost cell, and the goal cell to be the lower rightmost. """
        self.start_cell = self.cells[0]
        self.start_cell.start = True
        self.goal_cell = self.cells[
            self.get_cell_index(self.display.columns - 1, self.display.rows - 1)]
        self.goal_cell.end = True

    def get_cell_index(self, x, y):
        """ Returns the array index for the cell at position (x, y). """
        return y * self.display.columns + x
