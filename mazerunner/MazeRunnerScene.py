from PyQt5.QtCore import QRectF, QLineF, QCoreApplication
from PyQt5.QtWidgets import QGraphicsScene

import mazerunner.Config as Config
from mazerunner.MazeRunner import MazeRunner


class MazeRunnerScene(QGraphicsScene):
    """ Defines the maze runner scene """

    def __init__(self):
        super().__init__()
        self.runner = MazeRunner(self)
        self.path = []

    def init_grid(self):
        """ Initialise the grid display """
        Config.set_runner_cell_dimension()
        width = Config.RUNNER_MAZE_COLUMNS * Config.RUNNER_CELL_DIMENSION
        height = Config.RUNNER_MAZE_ROWS * Config.RUNNER_CELL_DIMENSION
        self.setSceneRect(0, Config.WINDOW_HEIGHT * Config.MAZE_WINDOW_VERTICAL_OFFSET_FACTOR, width, height)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        cells = self.runner.get_cells()
        for cell in cells:
            lines = cell.get_wall_display()
            for line in lines:
                cell.add_line_object(self.addLine(line, Config.CELL_WALL_PEN))
            fill = cell.get_fill_display()
            if len(fill) > 0:
                cell.set_rect_object(self.addRect(fill[0], fill[1], fill[2]))

    def update_grid(self):
        """ For any cell which has been changed since the last update, delete its items and redraw it to its current
        state. """
        for cell in self.runner.cells:
            if cell.has_changed():
                old_lines = cell.get_line_objects()
                for line in old_lines:
                    self.removeItem(line)
                old_rect_display = cell.get_rect_object()
                if old_rect_display is not None:
                    self.removeItem(old_rect_display)

                new_rect_display = cell.get_fill_display()
                if len(new_rect_display) > 0:
                    cell.set_rect_object(self.addRect(new_rect_display[0], new_rect_display[1], new_rect_display[2]))
                cell.clear_line_objects()
                new_lines = cell.get_wall_display()
                for line in new_lines:
                    cell.add_line_object(self.addLine(line, Config.CELL_WALL_PEN))
                cell.changed = False

    def add_rect(self, cell, pen, brush):
        """ Add a filling rect to the scene for the given cell with the given pen and brush. """
        rect = QRectF(cell.get_x() * Config.RUNNER_CELL_DIMENSION + 1, cell.get_y() * Config.RUNNER_CELL_DIMENSION + 1,
                      Config.RUNNER_CELL_DIMENSION - 1, Config.RUNNER_CELL_DIMENSION - 1)
        self.rects.append(self.addRect(rect, pen, brush))

    def delete_grid(self):
        """ Deletes all items. """
        for cell in self.runner.cells:
            old_lines = cell.get_line_objects()
            for line in old_lines:
                self.removeItem(line)
            old_rect_display = cell.get_rect_object()
            if old_rect_display is not None:
                self.removeItem(old_rect_display)
        for line in self.path:
            self.removeItem(line)
        del self.path[:]

    def draw_path(self, path):
        """ Draws a line connecting each of the cells in the given path. """
        for cell, next_cell in zip(path[:-1], path[1:]):
            side_length = Config.RUNNER_CELL_DIMENSION
            first_xc = (cell.get_x() + 0.5) * side_length  # x position of first center
            first_yc = (cell.get_y() + 0.5) * side_length  # y position of first center
            second_xc = (next_cell.get_x() + 0.5) * side_length  # x position of second center
            second_yc = (next_cell.get_y() + 0.5) * side_length  # y position of second center
            self.path.append(self.addLine(QLineF(first_xc, first_yc, second_xc, second_yc), Config.CELL_WALL_PEN))

    def update_scene(self, path=None):
        """ Update the display. If a path is provided, it will also be drawn. """
        self.update_grid()
        if path is not None:
            self.draw_path(path)
        self.update()
        QCoreApplication.processEvents()

    def load_maze_on_click(self):
        """ Attempt to load a maze from a file and draw it on screen. Returns true if successfully loaded, false if not.
        """
        Config.set_runner_running(False)
        self.delete_grid()
        self.runner.reset_search()
        if self.runner.load_maze():
            self.init_grid()
            return True
        else:
            return False

    def start_search_on_click(self, search_option):
        """ Prepare the solver to start a new search and start it. """
        Config.set_runner_running(False)
        self.delete_grid()
        self.runner.reset_search()
        self.init_grid()
        Config.set_runner_running()
        self.runner.start_search(search_option)
