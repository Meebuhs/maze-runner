from math import floor
from random import randint

from PyQt5.QtCore import QCoreApplication

import mazerunner.utils.Config as Config
from mazerunner.solvers.SampleGraphNode import SampleGraphNode
from mazerunner.utils.PriorityQueue import PriorityQueue


class RandomSampleSolver:
    """ Blind search algorithm which attempts to find a solution by taking a number of random samples of the search
    space. A graph is then constructed with these samples as nodes and Dijkstra's algorithm is used to find a path. """

    def __init__(self, runner):
        self.runner = runner
        self.max_nodes = 1000
        self.max_distance = 100
        # Current and goal cells, the cells assigned here are discarded once search is commenced
        self.id_counter = 0
        self.start_node = self.create_node(
            (self.runner.start_cell.x + 0.5) * self.runner.display.cell_dimension,
            (self.runner.start_cell.y + 0.5) * self.runner.display.cell_dimension)
        self.current_node = self.start_node
        self.goal_node = self.create_node(
            (self.runner.goal_cell.x + 0.5) * self.runner.display.cell_dimension,
            (self.runner.goal_cell.y + 0.5) * self.runner.display.cell_dimension)
        self.line_items = []
        self.ellipse_size = 6
        self.ellipse_items = []
        self.ellipse_items.append(
            self.runner.display.addEllipse(self.start_node.x - self.ellipse_size, self.start_node.y - self.ellipse_size,
                                           self.ellipse_size, self.ellipse_size, Config.CELL_QUEUE_PEN,
                                           Config.CELL_QUEUE_BRUSH))
        self.ellipse_items.append(
            self.runner.display.addEllipse(self.goal_node.x - self.ellipse_size, self.goal_node.y - self.ellipse_size,
                                           self.ellipse_size, self.ellipse_size, Config.CELL_QUEUE_PEN,
                                           Config.CELL_QUEUE_BRUSH))
        self.nodes = []
        self.adjacency_list = []
        self.queue = PriorityQueue()

    def create_node(self, x, y):
        """ Creates a new sample node. """
        node = SampleGraphNode(x, y, self.id_counter)
        self.id_counter += 1
        return node

    def start(self):
        """ Starts the solver. """
        self.initialize()
        self.run()

    def initialize(self):
        """ Performs the initialisation necessary for the search to run. Creates the nodes fro the the start and end
        cells.
        """
        self.nodes.append(self.current_node)
        self.nodes.append(self.goal_node)

    def run(self):
        """ Runs the solver. """
        self.sample()
        self.construct_adjacency_list()
        self.dijkstras_search()

    def sample(self):
        """ Creates the sample points from which a path will be constructed. """
        cell_dimension = self.runner.display.cell_dimension
        while len(self.nodes) < self.max_nodes:
            x = randint(0, self.runner.display.columns * cell_dimension)
            y = randint(0, self.runner.display.rows * cell_dimension)
            if abs(x % cell_dimension) > self.ellipse_size and abs(y % cell_dimension) > self.ellipse_size:
                self.nodes.append(self.create_node(x, y))
                self.ellipse_items.append(self.runner.display.addEllipse(x, y, self.ellipse_size, self.ellipse_size,
                                                                         Config.CELL_QUEUE_PEN,
                                                                         Config.CELL_QUEUE_BRUSH))
                self.runner.display.update()
                QCoreApplication.processEvents()

    def construct_adjacency_list(self):
        """ Constructs an adjacency list from the sample points. """
        for _ in range(len(self.nodes)):
            self.adjacency_list.append([])
        for node in self.nodes:
            for other_node in self.nodes:
                if node is not other_node and node.distance_to(other_node) <= self.max_distance:
                    if not self.has_path_collision(node, other_node):
                        self.adjacency_list[node.id] += [other_node]

    def has_path_collision(self, node, other_node):
        """ Returns true if a straight line path connecting node and other_node intersects with a cell wall. """
        cell_dimension = self.runner.display.cell_dimension
        cells_to_check = self.get_cells_to_check(node, other_node)
        for cell in cells_to_check:
            if cell.walls['bottom']:
                wall_x1 = cell.x * cell_dimension
                wall_x2 = (cell.x + 1) * cell_dimension
                wall_y1 = (cell.y + 1) * cell_dimension
                wall_y2 = (cell.y + 1) * cell_dimension
                if intersect((node.x, node.y), (other_node.x, other_node.y), (wall_x1, wall_y1),
                             (wall_x2, wall_y2)):
                    return True
            if cell.walls['right']:
                wall_x1 = (cell.x + 1) * cell_dimension
                wall_x2 = (cell.x + 1) * cell_dimension
                wall_y1 = cell.y * cell_dimension
                wall_y2 = (cell.y + 1) * cell_dimension
                if intersect((node.x, node.y), (other_node.x, other_node.y), (wall_x1, wall_y1),
                             (wall_x2, wall_y2)):
                    return True
            if cell.y > 0:
                cell_above = self.runner.cells[self.runner.get_cell_index(cell.x, cell.y - 1)]
                if cell_above.walls['bottom']:
                    wall_x1 = cell_above.x * cell_dimension
                    wall_x2 = (cell_above.x + 1) * cell_dimension
                    wall_y1 = (cell_above.y + 1) * cell_dimension
                    wall_y2 = (cell_above.y + 1) * cell_dimension
                    if intersect((node.x, node.y), (other_node.x, other_node.y), (wall_x1, wall_y1),
                                 (wall_x2, wall_y2)):
                        return True
            if cell.x > 0:
                cell_to_left = self.runner.cells[self.runner.get_cell_index(cell.x - 1, cell.y)]
                if cell_to_left.walls['right']:
                    wall_x1 = (cell_to_left.x + 1) * cell_dimension
                    wall_x2 = (cell_to_left.x + 1) * cell_dimension
                    wall_y1 = cell_to_left.y * cell_dimension
                    wall_y2 = (cell_to_left.y + 1) * cell_dimension
                    if intersect((node.x, node.y), (other_node.x, other_node.y), (wall_x1, wall_y1),
                                 (wall_x2, wall_y2)):
                        return True
        return False

    def get_cells_to_check(self, node, other_node):
        """ Returns a list of cells to check for collisions.

        Consider a path from cell (0,0) to (2, 3), the list of cells returned will those in the range (0-2, 0-3). The
        same list of cells would also be returned for a path from (2, 3) to (0, 0)"""
        cell_dimension = self.runner.display.cell_dimension
        path_x1 = int(floor(node.x / cell_dimension))
        path_y1 = int(floor(node.y / cell_dimension))
        path_x2 = int(floor(other_node.x / cell_dimension))
        path_y2 = int(floor(other_node.y / cell_dimension))
        x_range = path_x2 - path_x1
        y_range = path_y2 - path_y1
        start_x = path_x1 if x_range >= 0 else path_x2
        start_y = path_y1 if y_range >= 0 else path_y2

        cells = []
        for x_offset in range(abs(x_range) + 1):
            for y_offset in range(abs(y_range) + 1):
                cells.append(self.runner.cells[self.runner.get_cell_index(start_x + x_offset, start_y + y_offset)])
        return cells

    def dijkstras_search(self):
        """ Performs dijkstra's algorithm on the graph to find an optimal path. """
        self.queue.put(self.current_node)
        while not self.queue.empty():
            self.current_node = self.queue.get()
            self.current_node.distance = 0
            for node in self.adjacency_list[self.current_node.id]:
                distance = self.current_node.distance + self.current_node.distance_to(node)
                if distance < node.distance:
                    node.distance = distance
                    node.parent = self.current_node
                    if self.queue.contains(node):
                        self.queue.delete(node)
                    self.queue.put(node)
        self.construct_path()

    def recommence(self):
        """ Recommences the solver. """
        self.run()

    def construct_path(self):
        """ Constructs a path from the results of the search. """
        path = []
        try:
            node = self.goal_node
            path.append(node)
            while node != self.start_node:
                path.append(node.parent)
                node = node.parent
            path.reverse()
            print(path)
        except Exception:
            print("Path not found")
            return
        for node, node2 in zip(path[:-1], path[1:]):
            # Add half ellipse_size to hit node center
            self.line_items.append(
                self.runner.display.addLine(node.x + self.ellipse_size / 2, node.y + self.ellipse_size / 2,
                                            node2.x + self.ellipse_size / 2, node2.y + self.ellipse_size / 2,
                                            Config.CELL_PATH_PEN))
        self.runner.display.update()
        QCoreApplication.processEvents()

    def clear_display_items(self):
        """ Removes the sample node ellipses and the path lines from the display. """
        for ellipse in self.ellipse_items:
            self.runner.display.removeItem(ellipse)
        del self.ellipse_items[:]
        for line in self.line_items:
            self.runner.display.removeItem(line)
        del self.line_items[:]


def intersect(a1, a2, b1, b2):
    """ Returns true if the two line segments with end-points a1, a2 and b1, b2 instersect. Each end-point is a tuple
    (int, int) representing the (x, y) coordinates of the point. This is an implementation of a post by Bryce Boe
    available here https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/ """
    return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)


def ccw(a, b, c):
    """ Returns true if points a, b and c are in counterclockwise order. """
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
