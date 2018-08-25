from math import floor

from PyQt5.QtCore import QRectF, QLineF, QCoreApplication, Qt
from PyQt5.QtWidgets import QGraphicsScene

import mazerunner.Config as Config
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

        cells = self.runner.cells
        for cell in cells:
            lines = cell.lines
            for line in lines:
                cell.add_line_item(self.addLine(line, Config.CELL_WALL_PEN))
            fill = cell.get_fill_rect()
            if len(fill) > 0:
                cell.rect_item = self.addRect(fill[0], fill[1], fill[2])

    def start_search_on_click(self, search_option):
        """ Prepare the solver to start a new search and start it. """
        self.runner.running = False
        self.delete_grid()
        self.runner.reset_search()
        self.init_grid()
        self.runner.running = True
        self.runner.start_search(search_option)

    def update_grid(self):
        """ For any cell which has been changed since the last update, delete its items and redraw it to its current
        state. """
        for cell in self.runner.cells:
            if cell.changed:
                old_lines = cell.line_items
                for line in old_lines:
                    self.removeItem(line)
                old_rect_display = cell.rect_item
                if old_rect_display is not None:
                    self.removeItem(old_rect_display)

                new_rect_display = cell.get_fill_rect()
                if len(new_rect_display) > 0:
                    cell.rect_item = self.addRect(new_rect_display[0], new_rect_display[1], new_rect_display[2])
                cell.clear_line_items()
                new_lines = cell.lines
                for line in new_lines:
                    cell.add_line_item(self.addLine(line, Config.CELL_WALL_PEN))
                cell.changed = False

    def add_rect(self, cell, pen, brush):
        """ Add a filling rect to the scene for the given cell with the given pen and brush. """
        rect = QRectF(cell.x * self.cell_dimension + 1, cell.y * self.cell_dimension + 1,
                      self.cell_dimension - 1, self.cell_dimension - 1)
        self.rects.append(self.addRect(rect, pen, brush))

    def delete_grid(self):
        """ Deletes all items. """
        for cell in self.runner.cells:
            old_lines = cell.line_items
            for line in old_lines:
                self.removeItem(line)
            old_rect_display = cell.rect_item
            if old_rect_display is not None:
                self.removeItem(old_rect_display)
        for line in self.path:
            self.removeItem(line)
        del self.path[:]

    def draw_path(self, path):
        """ Draws a line connecting each of the cells in the given path. """
        for cell, next_cell in zip(path[:-1], path[1:]):
            first_xc = (cell.x + 0.5) * self.cell_dimension  # x position of first center
            first_yc = (cell.y + 0.5) * self.cell_dimension  # y position of first center
            second_xc = (next_cell.x + 0.5) * self.cell_dimension  # x position of second center
            second_yc = (next_cell.y + 0.5) * self.cell_dimension  # y position of second center
            self.path.append(self.addLine(QLineF(first_xc, first_yc, second_xc, second_yc), Config.CELL_WALL_PEN))

    def update_scene(self, path=None):
        """ If rendering is not suppressed or if the runner has finished, the display is updated. If a path is provided,
        it will also be drawn. """
        if self.render_progress or self.runner.solved:
            self.update_grid()
            if path is not None:
                self.draw_path(path)
            self.update()
            QCoreApplication.processEvents()

    def load_maze_on_click(self):
        """ Attempt to load a maze from a file and draw it on screen. Returns true if successfully loaded, false if not.
        """
        self.runner.running = False
        self.delete_grid()
        self.runner.reset_search()
        if self.runner.load_maze():
            self.init_grid()
            self.runner.initialise_start_and_goal_cells()
            self.maze_loaded = True
        else:
            self.maze_loaded = False

    def set_maze_dimensions(self, columns, rows):
        """ Sets the dimensions of the maze to the given columns and rows. """
        self.columns = columns
        self.rows = rows
        self.set_cell_dimension()

    def set_cell_dimension(self):
        """ Calculates an appropriate cell side length which allows the grid to be drawn on screen. This is not executed the
        scene is currently processing. """
        if not self.runner.running:
            self.cell_dimension = min(
                floor(Config.WINDOW_WIDTH * Config.MAZE_WINDOW_WIDTH_REDUCTION_FACTOR / self.columns),
                floor(Config.WINDOW_HEIGHT * Config.MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR / self.rows))

    def mousePressEvent(self, event):
        """ Bind the mouse presses to start and goal cell selection. """
        if self.maze_loaded and not self.runner.running:
            x = event.scenePos().x()
            y = event.scenePos().y()
            if 0 <= x <= self.columns * self.cell_dimension and 0 <= y <= self.rows * self.cell_dimension:
                if event.button() == Qt.LeftButton:
                    self.set_start_cell(x, y)
                elif event.button() == Qt.RightButton:
                    self.set_goal_cell(x, y)

    def set_start_cell(self, x, y):
        """ Sets the start cell for the search. """
        index = self.calculate_cell_index_from_coordinates(x, y)
        self.runner.start_cell.start = False
        self.runner.start_cell = self.runner.cells[index]
        self.runner.start_cell.start = True

        self.update_grid()
        self.update()
        QCoreApplication.processEvents()

    def set_goal_cell(self, x, y):
        """ Sets the goal cell for the search. """
        index = self.calculate_cell_index_from_coordinates(x, y)
        self.runner.goal_cell.goal = False
        self.runner.goal_cell = self.runner.cells[index]
        self.runner.goal_cell.goal = True

        self.update_grid()
        self.update()
        QCoreApplication.processEvents()

    def calculate_cell_index_from_coordinates(self, x, y):
        """ Returns the index of the cell which contains the point x, y. """
        cell_x = floor(x / self.cell_dimension)
        cell_y = floor(y / self.cell_dimension)

        return self.runner.get_cell_index(cell_x, cell_y)
