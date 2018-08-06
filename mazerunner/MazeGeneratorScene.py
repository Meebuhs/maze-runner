from PyQt5.QtCore import QCoreApplication, QRectF
from PyQt5.QtWidgets import QGraphicsScene

import mazerunner.Config as Config
from mazerunner.MazeGenerator import MazeGenerator


class MazeGeneratorScene(QGraphicsScene):
    """ Defines the maze generator scene """

    def __init__(self):
        super().__init__()
        self.generator = MazeGenerator(self)

    def init_grid(self):
        """ Initialise the grid display """
        # Define the dimensions of the scene
        width = Config.GENERATOR_MAZE_COLUMNS * Config.GENERATOR_CELL_DIMENSION
        height = Config.GENERATOR_MAZE_ROWS * Config.GENERATOR_CELL_DIMENSION
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
        rect = QRectF(cell.get_x() * Config.GENERATOR_CELL_DIMENSION + 1,
                      cell.get_y() * Config.GENERATOR_CELL_DIMENSION + 1,
                      Config.GENERATOR_CELL_DIMENSION - 1, Config.GENERATOR_CELL_DIMENSION - 1)
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
        """ Update the display. """
        self.update_grid()
        self.update()
        QCoreApplication.processEvents()

    def start_generation_on_click(self):
        """ Start maze generation """
        Config.set_generator_running(False)
        self.delete_grid()
        Config.set_generator_cell_dimension()
        self.generator = MazeGenerator(self)
        self.init_grid()
        self.update_scene()
        Config.set_generator_running()
        self.generator.generate()

    def save_maze_on_click(self):
        """ Save the generated maze to a file """
        self.generator.save_maze()
