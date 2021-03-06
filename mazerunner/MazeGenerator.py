from pathlib import Path
from random import randint
from time import time

from mazerunner.GeneratorCell import GeneratorCell


class MazeGenerator:
    """ Uses a Depth First Search to generate a maze. Starting with a full grid and setting the current cell as the top
    left, the algorithm moves the current cell to a neighbouring cell and the wall between them is removed. By
    continuing this process until there are no cells left unvisited, the resulting maze is guaranteed to be connected.
    """

    def __init__(self, display):
        self.display = display
        self.cells = create_cells(self.display.columns, self.display.rows, self.display)
        self.current_cell = self.cells[0]
        self.current_cell.visited = True
        # Set a cell as next, this is replaced with another cell before it is accessed
        self.next_cell = self.cells[1]
        self.visited_cells = []
        self.running = False
        self.paused = False
        self.finished = False

    def generate(self):
        """ Start the depth first search algorithm to generate the maze. """
        while True:
            if not self.running or self.paused:
                break
            self.next_cell = self.select_neighbours(self.current_cell)
            if self.next_cell:
                self.visited_cells.append(self.current_cell)
                self.next_cell.visited = True
                self.next_cell.in_queue = False
                remove_walls(self.current_cell, self.next_cell)
                self.current_cell = self.next_cell
                self.display.update_scene()
            elif len(self.visited_cells) > 0:
                self.current_cell = self.visited_cells.pop()
            else:
                self.running = False
                self.finished = True
                self.display.update_scene()
                break

    def recommence(self):
        """ Recommence the maze generation. """
        self.generate()

    def select_neighbours(self, cell):
        """ Checks the neighbouring cells and if there exists at least one unvisited neighbour, one is selected randomly
        and returned. Otherwise None is returned. """
        unvisited = []
        neighbours = self.get_neighbours(cell)
        for neighbour in neighbours:
            if not neighbour.visited:
                unvisited.append(neighbour)
                neighbour.in_queue = True
        if len(unvisited) > 0:
            return unvisited[randint(0, len(unvisited) - 1)]
        else:
            return None

    def get_neighbours(self, cell):
        """ Returns all neighbouring cells of a cell in an array. """
        neighbours = []
        x = cell.x
        y = cell.y

        if y > 0:  # Above
            neighbours.append(self.cells[self.get_cell_index(x, y - 1)])
        if x < self.display.columns - 1:  # Right
            neighbours.append(self.cells[self.get_cell_index(x + 1, y)])
        if y < self.display.rows - 1:  # Below
            neighbours.append(self.cells[self.get_cell_index(x, y + 1)])
        if x > 0:  # Right
            neighbours.append(self.cells[self.get_cell_index(x - 1, y)])
        return neighbours

    def save_maze(self):
        """ Saves the maze to a file. The format for the file has the dimensions of the maze on the first line
        in the format "columns rows" (two integers separated by a space). Then there are columns x rows lines, each
        containing a 4 bit number. The lines are the cells in order where a 1 indicates a wall (ordered top right
        bottom left). In total the file will have columns x rows + 1 lines
        """
        path = Path('./mazes')
        if not path.exists():
            path.mkdir(parents=True)
        filename = "maze-{}x{}-{}.txt".format(self.display.columns, self.display.rows, time())
        file = path / filename
        with open(file, 'w') as file:
            # Write the maze dimensions
            file.write("{} {}".format(self.display.columns, self.display.rows))
            for cell in self.cells:
                # Output string will be a two bit number, where a 1 represents a wall in that position.
                # Ordered bottom, right.
                output = ''
                walls = ['bottom', 'right']
                for wall in walls:
                    if cell.walls.get(wall):
                        output += str(1)
                    else:
                        output += str(0)
                file.write("\n{}".format(output))

    def get_cell_index(self, x, y):
        """ Returns the array index for the cell at position (x, y). """
        return y * self.display.columns + x


def create_cells(columns, rows, parent):
    """ Creates an array of cells of length columns x rows. The cell at position (x, y) (origin top left, increasing
     toward bottom right) appears in the array at index y * rows + x.
    """
    cells = []
    for y in range(rows):
        for x in range(columns):
            cell = GeneratorCell(x, y, parent)
            cells.append(cell)
    return cells


def remove_walls(current_cell, next_cell):
    """ Determines the direction travelled and removes the walls between two given cells"""
    dx = current_cell.x - next_cell.x
    dy = current_cell.y - next_cell.y

    if dx == 1:  # Moved left, remove other cells right wall
        next_cell.set_wall('right', False)
    elif dx == -1:  # Moved right, remove this cells right wall
        current_cell.set_wall('right', False)
    elif dy == 1:  # Moved down, remove this cells bottom wall
        next_cell.set_wall('bottom', False)
    elif dy == -1:  # Moved up, remove other cells bottom wall
        current_cell.set_wall('bottom', False)
