import sys

from PyQt5.Qt import QIntValidator, QEasingCurve
from PyQt5.QtCore import QRect, QTimer, pyqtSlot, QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, \
    QGraphicsView, QLineEdit, QComboBox, QLabel, QGraphicsOpacityEffect

import mazerunner.Config as Config
from mazerunner.MazeGeneratorScene import MazeGeneratorScene
from mazerunner.MazeRunnerScene import MazeRunnerScene


class App(QMainWindow):
    """ Defines the main application window """

    def __init__(self):
        super().__init__()
        # Set main window properties
        self.title = 'Maze Runner'
        self.left = 300
        self.top = 300
        self.width = Config.WINDOW_WIDTH
        self.height = Config.WINDOW_HEIGHT
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('..\\resources\\icon-512.png'))

        # Set up tabs
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Display
        self.show()

    def resizeEvent(self, event):
        """ On resize, set the window dimension constants. """
        Config.set_window_dimensions(event.size().width(), event.size().height())


class TabWidget(QWidget):
    """ Defines the tab view """

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        # Set up process flow logic
        self.maze_loaded = False
        self.maze_generated = False

        # Instantiate a reference to an animation
        self.animation = None

        # Initialise tab screen
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        # Initialise the maze runner
        self.runnerScene = MazeRunnerScene()
        self.runnerTab = QGraphicsView()
        self.runnerTab.setViewportUpdateMode(QGraphicsView.NoViewportUpdate)
        self.runnerTab.setScene(self.runnerScene)

        self.loadMazeButton = QPushButton(self.runnerTab)
        self.loadMazeButton.setGeometry(QRect(10, 10, 90, 30))
        self.loadMazeButton.setText("Load Maze")
        self.loadMazeButton.clicked.connect(self.load_maze_on_click)

        self.searchMethodComboBox = QComboBox(self.runnerTab)
        self.searchMethodComboBox.setGeometry(110, 11, 150, 28)
        search_options = ['Breadth First Search', 'Bidirectional BFS', 'Depth First Search', 'Bidirectional DFS',
                          'Greedy Best First', 'A*']
        self.searchMethodComboBox.addItems(search_options)

        self.startSearchButton = QPushButton(self.runnerTab)
        self.startSearchButton.setGeometry(QRect(270, 10, 90, 30))
        self.startSearchButton.setText("Start")
        self.startSearchButton.clicked.connect(self.start_search_on_click)

        self.runnerConsoleLabel = QLabel(self.runnerTab)
        self.runnerConsoleLabel.setGeometry(370, 10, 1000, 30)
        self.runnerConsoleLabel.setText('')

        # Initialise the maze generator
        self.generatorScene = MazeGeneratorScene()
        self.generatorTab = QGraphicsView()
        self.generatorTab.setViewportUpdateMode(QGraphicsView.NoViewportUpdate)
        self.generatorTab.setScene(self.generatorScene)

        self.columnsLabel = QLabel(self.generatorTab)
        self.columnsLabel.setText('Columns:')
        self.columnsLabel.setGeometry(10, 10, 45, 30)
        self.columnsText = QLineEdit(self.generatorTab)
        self.columnsText.setGeometry(QRect(65, 10, 90, 30))
        self.columnsText.setValidator(QIntValidator(1, 99))
        self.columnsText.setText(str(Config.GENERATOR_MAZE_COLUMNS))

        self.rowsLabel = QLabel(self.generatorTab)
        self.rowsLabel.setText('Rows:')
        self.rowsLabel.setGeometry(165, 10, 30, 30)
        self.rowsText = QLineEdit(self.generatorTab)
        self.rowsText.setGeometry(QRect(205, 10, 90, 30))
        self.rowsText.setValidator(QIntValidator(1, 99))
        self.rowsText.setText(str(Config.GENERATOR_MAZE_ROWS))

        self.startGenerationButton = QPushButton(self.generatorTab)
        self.startGenerationButton.setGeometry(QRect(305, 10, 90, 30))
        self.startGenerationButton.setText("Generate")
        self.startGenerationButton.clicked.connect(self.start_generation_on_click)

        self.saveMazeButton = QPushButton(self.generatorTab)
        self.saveMazeButton.setGeometry(QRect(405, 10, 90, 30))
        self.saveMazeButton.setText("Save Maze")
        self.saveMazeButton.clicked.connect(self.save_maze_on_click)

        self.generatorConsoleLabel = QLabel(self.generatorTab)
        self.generatorConsoleLabel.setGeometry(505, 10, 1000, 30)
        self.generatorConsoleLabel.setText('')

        # Add tabs to layout
        self.tabs.addTab(self.runnerTab, "Maze Runner")
        self.tabs.addTab(self.generatorTab, "Maze Generator")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def fade_label(self, label):
        """ Fades a label out over a 3 second duration """
        fade = QGraphicsOpacityEffect()
        label.setGraphicsEffect(fade)
        animation = QPropertyAnimation(fade, b"opacity")
        # Fade opacity from 1 to 0 over 3 seconds
        animation.setDuration(3000)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InQuad)
        animation.start()
        # Have to keep a reference to the animation or else it doesn't work
        self.animation = animation
        QTimer.singleShot(4000, self.clear_consoles)

    def clear_consoles(self):
        """ Resets the text in the console labels """
        self.runnerConsoleLabel.setText('')
        self.generatorConsoleLabel.setText('')

    @pyqtSlot()
    def load_maze_on_click(self):
        """ Attempts to load a maze from file """
        if not self.runnerScene.load_maze_on_click():
            self.runnerConsoleLabel.setText('Maze not loaded.')
            self.fade_label(self.runnerConsoleLabel)
        else:
            self.maze_loaded = True

    @pyqtSlot()
    def start_search_on_click(self):
        """ If a maze is loaded, the selected search method will be used to find a solution to the maze """
        if self.maze_loaded:
            self.runnerScene.start_search_on_click(self.searchMethodComboBox.currentText())
        else:
            self.runnerConsoleLabel.setText('Load a maze first')
            self.fade_label(self.runnerConsoleLabel)

    @pyqtSlot()
    def start_generation_on_click(self):
        """ Starts the generation of a maze of the size defined by the user """
        Config.set_maze_dimensions(int(self.columnsText.text()), int(self.rowsText.text()), 'generator')
        self.generatorScene.start_generation_on_click()
        self.maze_generated = True

    @pyqtSlot()
    def save_maze_on_click(self):
        """ Saves the generated maze """
        if self.maze_generated:
            self.generatorScene.save_maze_on_click()
            self.generatorConsoleLabel.setText('Maze saved')
            self.fade_label(self.generatorConsoleLabel)
        else:
            self.generatorConsoleLabel.setText('Generate a maze first')
            self.fade_label(self.generatorConsoleLabel)


def except_hook(cls, exception, traceback):
    """ Ensure pyqt doesn't eat exception tracebacks. """
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = App()
    sys.exit(app.exec_())
