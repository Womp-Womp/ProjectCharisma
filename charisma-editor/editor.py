# This will be the main entry point for the Charisma Editor
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QMdiArea
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Charisma Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        self._create_menus()

    def _create_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")

        new_action = QAction("&New Project", self)
        open_action = QAction("&Open Project", self)
        save_action = QAction("Save &Project", self)
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
