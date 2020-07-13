from PyQt5.QtGui import QPen, QColor, QBrush

""" Store global constants. """
# Dimensions of the program window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAZE_WINDOW_WIDTH_REDUCTION_FACTOR = 0.90
MAZE_WINDOW_HEIGHT_REDUCTION_FACTOR = 0.80
MAZE_WINDOW_VERTICAL_OFFSET_FACTOR = -0.025

# Default dimensions of the maze
DEFAULT_MAZE_COLUMNS = 24
DEFAULT_MAZE_ROWS = 12
DEFAULT_CELL_DIMENSION = 50

# Values for the random sample solver
SAMPLE_MAX_NODES = 1200
SAMPLE_MAX_DISTANCE = 100

# Pens for drawing cell walls
CELL_WALL_PEN = QPen(QColor(0, 0, 0), 1)
CELL_PATH_PEN = QPen(QColor(41, 182, 246), 2)
CELL_VISITED_PEN = QPen(QColor(128, 222, 234), 1)
CELL_QUEUE_PEN = QPen(QColor(41, 182, 246), 1)
CELL_CURRENT_PEN = QPen(QColor(25, 118, 210), 1)
CELL_START_PEN = QPen(QColor(239, 83, 80), 1)
CELL_END_PEN = QPen(QColor(102, 187, 106), 1)

# Pen for drawing sampler path
SAMPLER_PATH_PEN = QPen(QColor(102, 187, 106), 2)

# Brushes for filling cells
CELL_VISITED_BRUSH = QBrush(QColor(128, 222, 234))
CELL_QUEUE_BRUSH = QBrush(QColor(41, 182, 246))
CELL_CURRENT_BRUSH = QBrush(QColor(25, 118, 210))
CELL_START_BRUSH = QBrush(QColor(239, 83, 80))
CELL_END_BRUSH = QBrush(QColor(102, 187, 106))


def set_window_dimensions(width, height):
    """ Sets the dimensions of the main window. """
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    WINDOW_WIDTH = width
    WINDOW_HEIGHT = height
