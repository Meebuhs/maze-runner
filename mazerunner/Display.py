import mazerunner.Config as Config
import os
import sys
from PyQt5.Qt import QIntValidator, QEasingCurve
from PyQt5.QtCore import QRect, QTimer, pyqtSlot, QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, \
    QGraphicsView, QLineEdit, QComboBox, QLabel, QGraphicsOpacityEffect
from mazerunner.MazeGeneratorScene import MazeGeneratorScene
from mazerunner.MazeRunnerScene import MazeRunnerScene


class App(QMainWindow):
    """ Defines the main application window. """

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
        self.setWindowIcon(QIcon(resource_path('resources\\icon-512.png')))

        # Set up tabs
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Display
        self.show()

    def resizeEvent(self, event):
        """ On resize, set the window dimension constants. """
        Config.set_window_dimensions(event.size().width(), event.size().height())


class TabWidget(QWidget):
    """ Defines the tab view. """

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
        self.runner_scene = MazeRunnerScene()
        self.runner_tab = QGraphicsView()
        self.runner_tab.setViewportUpdateMode(QGraphicsView.NoViewportUpdate)
        self.runner_tab.setScene(self.runner_scene)

        self.runner_load_maze_button = QPushButton(self.runner_tab)
        self.runner_load_maze_button.setGeometry(QRect(10, 10, 90, 30))
        self.runner_load_maze_button.setText("Load Maze")
        self.runner_load_maze_button.clicked.connect(self.load_maze_on_click)

        self.runner_search_combobox = QComboBox(self.runner_tab)
        self.runner_search_combobox.setGeometry(110, 11, 200, 28)
        # New solvers need to be added to this list and added to start_search in maze-runner/MazeRunner.py
        search_options = ['Breadth First Search', 'Bidirectional BFS', 'Depth First Search', 'Bidirectional DFS',
                          'Greedy Best First', 'A*']
        self.runner_search_combobox.addItems(search_options)

        self.runner_start_button = QPushButton(self.runner_tab)
        self.runner_start_button.setGeometry(QRect(320, 10, 90, 30))
        self.runner_start_button.setText("Start")
        self.runner_start_button.clicked.connect(self.start_search_on_click)

        self.runner_pause_button = QPushButton(self.runner_tab)
        self.runner_pause_button.setGeometry(QRect(420, 10, 90, 30))
        self.runner_pause_button.setText("Pause")
        self.runner_pause_button.setCheckable(True)
        self.runner_pause_button.clicked.connect(self.toggle_pause_runner)

        self.runner_render_progress_button = QPushButton(self.runner_tab)
        self.runner_render_progress_button.setGeometry(QRect(520, 10, 150, 30))
        self.runner_render_progress_button.setText("Show Progress")
        self.runner_render_progress_button.setCheckable(True)
        self.runner_render_progress_button.setChecked(True)
        self.runner_render_progress_button.clicked.connect(self.toggle_render_runner)

        self.runner_console_label = QLabel(self.runner_tab)
        self.runner_console_label.setGeometry(680, 10, 1000, 30)
        self.runner_console_label.setText('')

        # Initialise the maze generator
        self.generator_scene = MazeGeneratorScene()
        self.generator_tab = QGraphicsView()
        self.generator_tab.setViewportUpdateMode(QGraphicsView.NoViewportUpdate)
        self.generator_tab.setScene(self.generator_scene)

        self.generator_columns_label = QLabel(self.generator_tab)
        self.generator_columns_label.setText('Columns:')
        self.generator_columns_label.setGeometry(10, 10, 45, 30)
        self.generator_columns_line_edit = QLineEdit(self.generator_tab)
        self.generator_columns_line_edit.setGeometry(QRect(65, 10, 90, 30))
        self.generator_columns_line_edit.setValidator(QIntValidator(1, 99))
        self.generator_columns_line_edit.setText(str(Config.DEFAULT_MAZE_COLUMNS))

        self.generator_rows_label = QLabel(self.generator_tab)
        self.generator_rows_label.setText('Rows:')
        self.generator_rows_label.setGeometry(165, 10, 30, 30)
        self.generator_rows_line_edit = QLineEdit(self.generator_tab)
        self.generator_rows_line_edit.setGeometry(QRect(205, 10, 90, 30))
        self.generator_rows_line_edit.setValidator(QIntValidator(1, 99))
        self.generator_rows_line_edit.setText(str(Config.DEFAULT_MAZE_ROWS))

        self.generator_start_button = QPushButton(self.generator_tab)
        self.generator_start_button.setGeometry(QRect(305, 10, 90, 30))
        self.generator_start_button.setText("Generate")
        self.generator_start_button.clicked.connect(self.start_generation_on_click)

        self.generator_save_button = QPushButton(self.generator_tab)
        self.generator_save_button.setGeometry(QRect(405, 10, 90, 30))
        self.generator_save_button.setText("Save Maze")
        self.generator_save_button.clicked.connect(self.save_maze_on_click)

        self.generator_pause_button = QPushButton(self.generator_tab)
        self.generator_pause_button.setGeometry(QRect(505, 10, 90, 30))
        self.generator_pause_button.setText("Pause")
        self.generator_pause_button.setCheckable(True)
        self.generator_pause_button.clicked.connect(self.toggle_pause_generator)

        self.generator_render_progress_button = QPushButton(self.generator_tab)
        self.generator_render_progress_button.setGeometry(QRect(605, 10, 150, 30))
        self.generator_render_progress_button.setText("Show Progress")
        self.generator_render_progress_button.setCheckable(True)
        self.generator_render_progress_button.setChecked(True)
        self.generator_render_progress_button.clicked.connect(self.toggle_render_generator)

        self.generator_console_label = QLabel(self.generator_tab)
        self.generator_console_label.setGeometry(765, 10, 1000, 30)
        self.generator_console_label.setText('')

        # Add tabs to layout
        self.tabs.addTab(self.runner_tab, "Maze Runner")
        self.tabs.addTab(self.generator_tab, "Maze Generator")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def fade_label(self, label):
        """ Fades a label out over a 3 second duration. """
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
        """ Resets the text in the console labels. """
        self.runner_console_label.setText('')
        self.generator_console_label.setText('')

    @pyqtSlot(name="runner_load_maze")
    def load_maze_on_click(self):
        """ Attempts to load a maze from file. """
        if not self.runner_scene.load_maze_on_click():
            self.runner_console_label.setText('Maze not loaded.')
            self.fade_label(self.runner_console_label)
        else:
            self.maze_loaded = True

    @pyqtSlot(name="runner_start_search")
    def start_search_on_click(self):
        """ If a maze is loaded, the selected search method will be used to find a solution to the maze. """
        if self.maze_loaded:
            self.runner_scene.start_search_on_click(self.runner_search_combobox.currentText())
        else:
            self.runner_console_label.setText('Load a maze first')
            self.fade_label(self.runner_console_label)

    @pyqtSlot(name="runner_pause")
    def toggle_pause_runner(self):
        """ Toggles the paused state of the runner. """
        if self.runner_pause_button.isChecked():
            self.runner_scene.runner.set_paused(True)
        else:
            self.runner_scene.runner.set_paused(False)
            if not self.runner_scene.runner.get_solved() and self.runner_scene.runner.solver is not None:
                self.runner_scene.runner.recommence()

    @pyqtSlot(name="runner_render_progress")
    def toggle_render_runner(self):
        """ Toggles the render state of the runner. """
        self.runner_scene.set_render_progress(self.runner_render_progress_button.isChecked())

    @pyqtSlot(name="generator_start")
    def start_generation_on_click(self):
        """ Starts the generation of a maze of the size defined by the user. """
        self.generator_scene.set_maze_dimensions(int(self.generator_columns_line_edit.text()),
                                                 int(self.generator_rows_line_edit.text()))
        self.generator_scene.start_generation_on_click()

    @pyqtSlot(name="generator_save_maze")
    def save_maze_on_click(self):
        """ Saves the generated maze. """
        if self.generator_scene.generator.get_finished():
            self.generator_scene.save_maze_on_click()
            self.generator_console_label.setText('Maze saved')
            self.fade_label(self.generator_console_label)
        else:
            self.generator_console_label.setText('Generate a maze first')
            self.fade_label(self.generator_console_label)

    @pyqtSlot(name="generator_pause")
    def toggle_pause_generator(self):
        """ Toggles the paused state of the generator. """
        if self.generator_pause_button.isChecked():
            self.generator_scene.generator.set_paused(True)
        else:
            self.generator_scene.generator.set_paused(False)
            if not self.generator_scene.generator.get_finished():
                self.generator_scene.generator.recommence()

    @pyqtSlot(name="generator_render_progress")
    def toggle_render_generator(self):
        """ Toggles the render state of the generator. """
        self.generator_scene.set_render_progress(self.generator_render_progress_button.isChecked())


def except_hook(cls, exception, traceback):
    """ Ensure pyqt doesn't eat exception tracebacks. """
    sys.__excepthook__(cls, exception, traceback)


def resource_path(relative_path):
    """ Returns the absolute path to a resource, works for dev and PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = App()
    sys.exit(app.exec_())
