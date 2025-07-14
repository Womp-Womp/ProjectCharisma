# This will be the main entry point for the Charisma Editor
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar, QMdiArea, QWidget,
                             QVBoxLayout, QTreeView, QFormLayout, QLineEdit, QSpinBox,
                             QPushButton, QSplitter, QMdiSubWindow)
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
import json
import os

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from charisma_common.models import Unit


class UnitEditor(QWidget):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.project_data = project_data
        self.units = self.project_data.get('units', [])

        self.setWindowTitle("Unit Editor")

        # Main layout
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # Left side: Tree view of units
        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Units'])
        self.tree_view.setModel(self.model)
        self.tree_view.selectionModel().selectionChanged.connect(self.on_unit_selected)
        splitter.addWidget(self.tree_view)

        # Right side: Form to edit unit properties
        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.hp_input = QSpinBox()
        self.hp_input.setRange(0, 9999)
        self.movement_input = QSpinBox()
        self.movement_input.setRange(0, 100)
        self.faction_id_input = QLineEdit()

        self.form_layout.addRow("ID:", self.id_input)
        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("HP:", self.hp_input)
        self.form_layout.addRow("Movement:", self.movement_input)
        self.form_layout.addRow("Faction ID:", self.faction_id_input)

        splitter.addWidget(self.form_widget)

        # Buttons
        button_layout = QVBoxLayout()
        self.add_button = QPushButton("Add Unit")
        self.add_button.clicked.connect(self.add_unit)
        self.remove_button = QPushButton("Remove Unit")
        self.remove_button.clicked.connect(self.remove_unit)
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_units)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        self.load_units()

    def load_units(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Units'])
        for unit_data in self.units:
            item = QStandardItem(unit_data.get('name', 'Unknown'))
            item.setData(unit_data, Qt.ItemDataRole.UserRole)
            self.model.appendRow(item)

    def on_unit_selected(self, selected, deselected):
        if not selected.indexes():
            return
        index = selected.indexes()[0]
        unit_data = self.model.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)

        self.id_input.setText(unit_data.get('id', ''))
        self.name_input.setText(unit_data.get('name', ''))
        self.hp_input.setValue(unit_data.get('hp', 0))
        self.movement_input.setValue(unit_data.get('movement', 0))
        self.faction_id_input.setText(unit_data.get('faction_id', ''))

    def add_unit(self):
        new_unit = {
            "id": f"unit_{len(self.units)}",
            "name": "New Unit",
            "hp": 100,
            "movement": 5,
            "faction_id": "",
            "abilities": []
        }
        self.units.append(new_unit)
        self.load_units()

    def remove_unit(self):
        if not self.tree_view.selectionModel().hasSelection():
            return
        index = self.tree_view.selectionModel().selectedIndexes()[0]
        unit_data = self.model.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)
        self.units.remove(unit_data)
        self.load_units()

    def save_units(self):
        # In a real app, this would be handled by a project manager class
        with open('data/units.json', 'w') as f:
            json.dump(self.units, f, indent=4)


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

        edit_menu = menu_bar.addMenu("&Edit")
        unit_editor_action = QAction("&Unit Editor", self)
        unit_editor_action.triggered.connect(self.open_unit_editor)
        edit_menu.addAction(unit_editor_action)

    def open_unit_editor(self):
        units = self.load_data("data/units.json")
        project_data = {"units": units}

        editor_widget = UnitEditor(project_data)
        sub_window = QMdiSubWindow()
        sub_window.setWidget(editor_widget)
        sub_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def load_data(self, file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            return json.load(f)

    def save_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
