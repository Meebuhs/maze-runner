from math import floor

import mazerunner.Config as Config
from PyQt5.QtCore import QRectF, QLineF, QCoreApplication
from PyQt5.QtWidgets import QGraphicsScene
from mazerunner.MazeRunner import MazeRunner


class MazeRunnerScene(QGraphicsScene):
    """ Defines the maze runner scene. """

    def __init__(self):
        super().__init__()
        self.runner = MazeRunner(self)
        self.path = []
        self.columns = Config.DEFAULT_MAZE_COLUMNS
        self.rows = Config.DEFAULT_MAZE_ROWS
        self.cell_dimension = Config.DEFAULT_CELL_DIMENSION
        self.render_progress = True
        self.maze_loaded = False

    def init_grid(self):
        """ Initialise the grid display. """
        self.set_cell_dimension()
        width = self.columns * self.cell_dimension
        height = self.rows * self.cell_dimension
        self.setSceneRect(0, Config.WINDOW_HEIGHT * Config.MAZE_WINDOW_VERTICAL_OFFSET_FACTOR, width, height)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        cells = self.runner.get_cells()
        for cell in cells:
            lines = cell.get_lines()
            for line in lines:
                cell.add_line_item(self.addLine(line, Config.CELL_WALL_PEN))
            fill = cell.get_fill_rect()
            if len(fill) > 0:
                cell.set_rect_item(self.addRect(fill[0], fill[1], fill[2]))

    def start_search_on_click(self, search_option):
        """ Prepare the solver to start a new search and start it. """
        self.runner.set_running(False)
        self.delete_grid()
        self.runner.reset_search()
        self.init_grid()
        self.runner.set_running(True)
        self.runner.start_search(search_option)

    def update_grid(self):
        """ For any cell which has been changed since the last update, delete its items and redraw it to its current
        state. """
        for cell in self.runner.cells:
            if cell.has_changed():
                old_lines = cell.get_line_items()
                for line in old_lines:
                    self.removeItem(line)
                old_rect_display = cell.get_rect_item()
                if old_rect_display is not None:
                    self.removeItem(old_rect_display)

                new_rect_display = cell.get_fill_rect()
                if len(new_rect_display) > 0:
                    cell.set_rect_item(self.addRect(new_rect_display[0], new_rect_display[1], new_rect_display[2]))
                cell.clear_line_items()
                new_lines = cell.get_lines()
                for line in new_lines:
                    cell.add_line_item(self.addLine(line, Config.CELL_WALL_PEN))
                cell.changed = False

    def add_rect(self, cell, pen, brush):
        """ Add a filling rect to the scene for the given cell with the given pen and brush. """
        rect = QRectF(cell.get_x() * self.cell_dimension + 1, cell.get_y() * self.cell_dimension + 1,
                      self.cell_dimension - 1, self.cell_dimension - 1)
        self.rects.append(self.addRect(rect, pen, brush))

    def delete_grid(self):
        """ Deletes all items. """
        for cell in self.runner.cells:
            old_lines = cell.get_line_items()
            for line in old_lines:
                self.removeItem(line)
            old_rect_display = cell.get_rect_item()
            if old_rect_display is not None:
                self.removeItem(old_rect_display)
        for line in self.path:
            self.removeItem(line)
        del self.path[:]

    def draw_path(self, path):
        """ Draws a line connecting each of the cells in the given path. """
        for cell, next_cell in zip(path[:-1], path[1:]):
            first_xc = (cell.get_x() + 0.5) * self.cell_dimension  # x position of first center
            first_yc = (cell.get_y() + 0.5) * self.cell_dimension  # y position of first center
            second_xc = (next_cell.get_x() + 0.5) * self.cell_dimension  # x position of second center
            second_yc = (next_cell.get_y() + 0.5) * self.cell_dimension  # y position of second center
            self.path.append(self.addLine(QLineF(first_xc, first_yc, second_xc, second_yc), Config.CELL_WALL_PEN))

    def update_scene(self, path=None):
        """ If rendering is not suppressed or if the runner has finished, the display is updated. If a path is provided,
        it will also be drawn. """
        if self.render_progress or self.runner.get_solved():
            self.update_grid()
            if path is not None:
                self.draw_path(path)
            self.update()
            QCoreApplication.processEvents()

    def load_maze_on_click(self):
        """ Attempt to load a maze from a file and draw it on screen. Returns true if successfully loaded, false if not.
        """
        self.runner.set_running(False)
        self.delete_grid()
        self.runner.reset_search()
        if self.runner.load_maze():
            self.init_grid()
            self.maze_loaded = True
        else:
            self.maze_loaded = False

    def get_columns(self):
        """ Returns the number of columns in the grid. """
        return self.columns

    def get_rows(self):
        """ Returns the number of rows in the grid. """
        return self.rows

    def set_maze_dimensions(self, columns, rows):
        """ Sets the dimensions of the maze to the given columns and rows. """
        self.columns = columns
        self.rows = rows
        self.set_cell_dimension()

    def get_cell_dimension(self):
        """ Returns the side length of a cell in the grid. """
        return self.cell_dimension

    def set_cell_dimension(self):
        """ Calculates an appropriate cell side length which allows the grid to be drawn on screen. This is not executed the
        scene is currently processing. """
        if not self.runner.get_running():
            self.cell_dimension = min(
                floor(Config.WINDOW_WIDTH * Config.MAZE_WINDOW_WIDTH_REDUCTION_FACTOR / self.columns),
                floor(Config.WINDOW_HEIGHT * Config.MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR / self.rows))

    def set_render_progress(self, value):
        """ Sets the render flag to the given value. """
        self.render_progress = value
