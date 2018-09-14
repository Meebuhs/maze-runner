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
        self.max_distance = 1000
        # Current and goal cells, the cells assigned here are discarded once search is commenced
        self.id_counter = 0
        self.start_node = self.create_node(
            (self.runner.start_cell.x + 0.5) * self.runner.display.cell_dimension,
            (self.runner.start_cell.y + 0.5) * self.runner.display.cell_dimension)
        self.current_node = self.start_node
        self.goal_node = self.create_node(
            (self.runner.goal_cell.x + 0.5) * self.runner.display.cell_dimension,
            (self.runner.goal_cell.y + 0.5) * self.runner.display.cell_dimension)
        self.runner.display.addEllipse(self.start_node.x - 5, self.start_node.y - 5, 5, 5, Config.CELL_QUEUE_PEN,
                                       Config.CELL_QUEUE_BRUSH)
        self.runner.display.addEllipse(self.goal_node.x - 5, self.goal_node.y - 5, 5, 5, Config.CELL_QUEUE_PEN,
                                       Config.CELL_QUEUE_BRUSH)
        self.nodes = []
        self.adjacency_list = []
        self.queue = PriorityQueue()

    def test_points(self):
        first_x = 100
        first_y = 100
        second_x = 300
        second_y = 100
        node_1 = SampleGraphNode(first_x, first_y, 0)
        node_2 = SampleGraphNode(second_x, second_y, 1)
        self.runner.display.addEllipse(node_1.x, node_1.y, 5, 5, Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
        self.runner.display.addEllipse(node_2.x, node_2.y, 5, 5, Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
        if not self.has_path_collision(node_1, node_2):
            self.runner.display.addLine(node_1.x, node_1.y, node_2.x, node_2.y, Config.CELL_QUEUE_PEN)
        self.runner.display.update()

    def create_node(self, x, y):
        """ Creates a new sample node. """
        node = SampleGraphNode(x, y, self.id_counter)
        self.id_counter += 1
        return node

    def start(self):
        """ Starts the solver. """
        # self.test_points()
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
        cell_dimension = self.runner.display.cell_dimension
        while len(self.nodes) < self.max_nodes:
            x = randint(0, self.runner.display.columns * cell_dimension - 5)
            y = randint(0, self.runner.display.rows * cell_dimension - 5)
            if not abs(x % cell_dimension) < 2 or not abs(y % cell_dimension) < 2:
                self.nodes.append(self.create_node(x, y))
                self.runner.display.addEllipse(x, y, 5, 5, Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
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
        same list of cells would be returned for a path from (2, 3) to (0, 0)"""
        cell_dimension = self.runner.display.cell_dimension
        path_x1 = int(floor(node.x / cell_dimension))
        path_y1 = int(floor(node.y / cell_dimension))
        path_x2 = int(floor(other_node.x / cell_dimension))
        path_y2 = int(floor(other_node.y / cell_dimension))
        x_range = path_x2 - path_x1
        y_range = path_y2 - path_y1
        start_x = path_x1 if x_range >= 0 else path_x2
        start_y = path_y1 if y_range >= 0 else path_y2

        # print(path_x1, path_y1, path_x2, path_y2, x_range, y_range)
        cells = []
        for x_offset in range(abs(x_range) + 1):
            for y_offset in range(abs(y_range) + 1):
                # print(start_x, x_offset, start_y, y_offset)
                cells.append(self.runner.cells[self.runner.get_cell_index(start_x + x_offset, start_y + y_offset)])

        # print(cells)
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
            self.runner.display.addLine(node.x, node.y, node2.x, node2.y, Config.CELL_QUEUE_PEN)
        self.runner.display.update()
        QCoreApplication.processEvents()

    def test_collisions(self):
        """ Tests a range of line segment intersections to determine if the collision detection is working as intended.
        """
        p1, p2, p3, p4, p5, p6, p7 = (1, 1), (1, 3), (2, 2), (2, 4), (3, 1), (3, 3), (4, 3)
        print("should intersect")
        print("2,6 and 3,4", intersect(p2, p6, p3, p4))
        print("2,6 and 1,4", intersect(p2, p6, p1, p4))
        print("2,3 and 1,4", intersect(p2, p3, p1, p4))
        print("3,7 and 5,6", intersect(p3, p7, p5, p6))
        print("shouldn't")
        print("2,3 and 5,6", intersect(p2, p3, p5, p6))
        print("2,6 and 3,7", intersect(p2, p6, p3, p7))
        print("1,4 and 3,7", intersect(p1, p4, p3, p7))
        print("1,4 and 5,6", intersect(p1, p4, p5, p6))


def intersect(a1, a2, b1, b2):
    return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)


def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
