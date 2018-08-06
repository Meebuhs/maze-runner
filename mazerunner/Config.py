from math import floor

from PyQt5.QtGui import QPen, QColor, QBrush

""" Store global constants """
# Dimensions of the program window
global WINDOW_WIDTH
WINDOW_WIDTH = 1280
global WINDOW_HEIGHT
WINDOW_HEIGHT = 720
global MAZE_WINDOW_WIDTH_REDUCTION_FACTOR
MAZE_WINDOW_WIDTH_REDUCTION_FACTOR = 0.90
global MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR
MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR = 0.80
global MAZE_WINDOW_VERTICAL_OFFSET_FACTOR
MAZE_WINDOW_VERTICAL_OFFSET_FACTOR = -0.025

# Default dimensions of the maze
global DEFAULT_MAZE_COLUMNS
DEFAULT_MAZE_COLUMNS = 24
global DEFAULT_MAZE_ROWS
DEFAULT_MAZE_ROWS = 12
global DEFAULT_CELL_DIMENSION
DEFAULT_CELL_DIMENSION = 50

# Runner dimensions of the maze
global RUNNER_MAZE_COLUMNS
RUNNER_MAZE_COLUMNS = DEFAULT_MAZE_COLUMNS
global RUNNER_MAZE_ROWS
RUNNER_MAZE_ROWS = DEFAULT_MAZE_ROWS
global RUNNER_CELL_DIMENSION
RUNNER_CELL_DIMENSION = DEFAULT_CELL_DIMENSION

# Generator dimensions of the maze
global GENERATOR_MAZE_COLUMNS
GENERATOR_MAZE_COLUMNS = DEFAULT_MAZE_COLUMNS
global GENERATOR_MAZE_ROWS
GENERATOR_MAZE_ROWS = DEFAULT_MAZE_ROWS
global GENERATOR_CELL_DIMENSION
GENERATOR_CELL_DIMENSION = DEFAULT_CELL_DIMENSION

# Pens for drawing cell walls
global CELL_WALL_PEN
CELL_WALL_PEN = QPen(QColor(0, 0, 0), 1)
global CELL_VISITED_PEN
CELL_VISITED_PEN = QPen(QColor(128, 222, 234), 1)
global CELL_QUEUE_PEN
CELL_QUEUE_PEN = QPen(QColor(41, 182, 246), 1)
global CELL_CURRENT_PEN
CELL_CURRENT_PEN = QPen(QColor(25, 118, 210), 1)
global CELL_START_PEN
CELL_START_PEN = QPen(QColor(239, 83, 80), 1)
global CELL_END_PEN
CELL_END_PEN = QPen(QColor(102, 187, 106), 1)

# Brushes for filling cells
global CELL_VISITED_BRUSH
CELL_VISITED_BRUSH = QBrush(QColor(128, 222, 234))
global CELL_QUEUE_BRUSH
CELL_QUEUE_BRUSH = QBrush(QColor(41, 182, 246))
global CELL_CURRENT_BRUSH
CELL_CURRENT_BRUSH = QBrush(QColor(25, 118, 210))
global CELL_START_BRUSH
CELL_START_BRUSH = QBrush(QColor(239, 83, 80))
global CELL_END_BRUSH
CELL_END_BRUSH = QBrush(QColor(102, 187, 106))

# Flags for restricting cell dimension resize
global GENERATOR_RUNNING
GENERATOR_RUNNING = False
global RUNNER_RUNNING
RUNNER_RUNNING = False


def set_generator_running(value=True):
    """ Sets the generator running flag to value, true by default. """
    global GENERATOR_RUNNING
    GENERATOR_RUNNING = value


def set_runner_running(value=True):
    """ Sets the runner running flag to value, true by default. """
    global RUNNER_RUNNING
    RUNNER_RUNNING = value


def get_runner_running():
    """ Gets the runner running flag. """
    return RUNNER_RUNNING


def set_window_dimensions(width, height, scene=None):
    """ Sets the dimensions of the main window. """
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    WINDOW_WIDTH = width
    WINDOW_HEIGHT = height
    set_cell_dimension(scene)


def set_maze_dimensions(columns, rows, scene):
    """ Sets the dimensions of the maze to the given columns and rows. """
    if scene == 'runner':
        global RUNNER_MAZE_COLUMNS
        global RUNNER_MAZE_ROWS
        RUNNER_MAZE_COLUMNS = columns
        RUNNER_MAZE_ROWS = rows
    elif scene == 'generator':
        global GENERATOR_MAZE_COLUMNS
        global GENERATOR_MAZE_ROWS
        GENERATOR_MAZE_COLUMNS = columns
        GENERATOR_MAZE_ROWS = rows
    set_cell_dimension(scene)


def set_cell_dimension(scene):
    """ Calls the appropriate cell dimension method based on the scene from which it's called. """
    if scene == 'runner':
        set_runner_cell_dimension()
    elif scene == 'generator':
        set_generator_cell_dimension()


def set_runner_cell_dimension():
    """ Calculates an appropriate cell side length which allows the grid to be drawn on screen. This is not executed the
    scene is currently processing"""
    if not RUNNER_RUNNING:
        global RUNNER_CELL_DIMENSION
        RUNNER_CELL_DIMENSION = min(floor(WINDOW_WIDTH * MAZE_WINDOW_WIDTH_REDUCTION_FACTOR / RUNNER_MAZE_COLUMNS),
                                    floor(WINDOW_HEIGHT * MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR / RUNNER_MAZE_ROWS))


def set_generator_cell_dimension():
    """ Calculates an appropriate cell side length which allows the grid to be drawn on screen. This is not executed the
    scene is currently processing"""
    if not GENERATOR_RUNNING:
        global GENERATOR_CELL_DIMENSION
        GENERATOR_CELL_DIMENSION = min(
            floor(WINDOW_WIDTH * MAZE_WINDOW_WIDTH_REDUCTION_FACTOR / GENERATOR_MAZE_COLUMNS),
            floor(WINDOW_HEIGHT * MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR / GENERATOR_MAZE_ROWS))
