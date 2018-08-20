from math import floor

from PyQt5.QtCore import QCoreApplication, QRectF
from PyQt5.QtWidgets import QGraphicsScene

import mazerunner.Config as Config
from mazerunner.MazeGenerator import MazeGenerator


class MazeGeneratorScene(QGraphicsScene):
    """ Defines the maze generator scene """

    def __init__(self):
        super().__init__()
        self.columns = Config.DEFAULT_MAZE_COLUMNS
        self.rows = Config.DEFAULT_MAZE_ROWS
        self.cell_dimension = Config.DEFAULT_CELL_DIMENSION
        self.render_progress = True
        self.generator = MazeGenerator(self)

    def init_grid(self):
        """ Initialise the grid display """
        # Define the dimensions of the scene
        width = self.columns * self.cell_dimension
        height = self.rows * self.cell_dimension
        self.setSceneRect(0, Config.WINDOW_HEIGHT * Config.MAZE_WINDOW_VERTICAL_OFFSET_FACTOR, width, height)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        cells = self.generator.get_cells()
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
        for cell in self.generator.cells:
            if cell.has_changed():
                # Remove old display items
                old_lines = cell.get_line_objects()
                for line in old_lines:
                    self.removeItem(line)
                old_rect_display = cell.get_rect_object()
                if old_rect_display is not None:
                    self.removeItem(old_rect_display)
                # Get the new display items and add them
                new_rect_display = cell.get_fill_display()
                if len(new_rect_display) > 0:
                    cell.set_rect_object(self.addRect(new_rect_display[0], new_rect_display[1], new_rect_display[2]))
                cell.clear_line_objects()
                new_lines = cell.get_wall_display()
                for line in new_lines:
                    cell.add_line_object(self.addLine(line, Config.CELL_WALL_PEN))
                cell.changed = False

    def add_rect(self, cell, pen, brush):
        rect = QRectF(cell.get_x() * self.cell_dimension + 1, cell.get_y() * self.cell_dimension + 1,
                      self.cell_dimension - 1, self.cell_dimension - 1)
        self.rects.append(self.addRect(rect, pen, brush))

    def set_visible(self, visible=True):
        """ Sets the visibility of the lines """
        for line in self.lines:
            line.setVisible(visible)

    def delete_grid(self):
        """ Deletes all items for every cell. """
        for cell in self.generator.cells:
            old_lines = cell.get_line_objects()
            for line in old_lines:
                self.removeItem(line)
            old_rect_display = cell.get_rect_object()
            if old_rect_display is not None:
                self.removeItem(old_rect_display)

    def update_scene(self):
        """ If rendering is not suppressed or if the runner has finished, the display is updated. """
        if self.render_progress or self.generator.get_finished():
            self.update_grid()
            self.update()
            QCoreApplication.processEvents()

    def start_generation_on_click(self):
        """ Start maze generation """
        self.generator.set_running(False)
        self.delete_grid()
        self.set_cell_dimension()
        self.generator = MazeGenerator(self)
        self.init_grid()
        self.update_scene()
        self.generator.set_running(True)
        self.generator.generate()

    def save_maze_on_click(self):
        """ Save the generated maze to a file """
        self.generator.save_maze()

    def get_columns(self):
        """ Returns the number of columns in the grid. """
        return self.columns

    def get_rows(self):
        """ Returns the number of rows in the grid. """
        return self.rows

    def get_cell_dimension(self):
        """ Returns the side length of a cell in the grid. """
        return self.cell_dimension

    def set_maze_dimensions(self, columns, rows):
        """ Sets the dimensions of the maze to the given columns and rows. """
        self.columns = columns
        self.rows = rows
        self.set_cell_dimension()

    def set_cell_dimension(self):
        """ Calculates an appropriate cell side length which allows the grid to be drawn on screen. This is not executed the
        scene is currently processing. """
        if not self.generator.get_running():
            self.cell_dimension = min(
                floor(Config.WINDOW_WIDTH * Config.MAZE_WINDOW_WIDTH_REDUCTION_FACTOR / self.columns),
                floor(Config.WINDOW_HEIGHT * Config.MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR / self.rows))

    def set_render_progress(self, value):
        """ Sets the render flag to the given value. """
        self.render_progress = value
