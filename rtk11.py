import math
from operator import iand, ior
import os
import shutil
import signal
import sys
import tempfile
from functools import reduce
from pprint import pprint
from sqlite3 import connect

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
                             QDialog, QFileDialog, QInputDialog, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QScrollArea,
                             QTableWidget, QTableWidgetItem, QTabWidget,
                             QToolBar, QVBoxLayout, QWidget)

from binary_parser.binary_parser import BinaryParser
from constants import *


class Unimplemented(Exception):
    pass


class ROTKXIGUI(QMainWindow):
    def init_menubar(self):
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("&File")

        # Add "Open Database" action
        self.open_file_action = QAction("&Open Database", self)
        self.open_file_action.setShortcut("Ctrl+O")
        self.open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_file_action)

        # Add "Save Database" action
        self.save_file_action = QAction("&Save Database", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.triggered.connect(self.save_file)
        self.save_file_action.setEnabled(False)
        self.file_menu.addAction(self.save_file_action)

        # Add "Save As Database" action
        self.save_as_file_action = QAction("Save &As Database", self)
        self.save_as_file_action.setShortcut("Ctrl+Shift+S")
        self.save_as_file_action.triggered.connect(self.save_as_file)
        self.save_as_file_action.setEnabled(False)
        self.file_menu.addAction(self.save_as_file_action)

        # Add "Exit" action
        self.exit_action = QAction("&Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

    def init_functions(self):
        self.filter_toolbar = QToolBar(self)
        self.filter_toolbar.setWindowTitle("Filter")
        self.addToolBar(self.filter_toolbar)

        self.search_box = QLineEdit()
        self.search_box.returnPressed.connect(self.filter_table)
        self.filter_toolbar.addWidget(self.search_box)

        self.filter_action = QAction("Filter", self)
        self.filter_action.triggered.connect(self.filter_table)
        self.filter_toolbar.addAction(self.filter_action)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROTK XI Editor")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(800, 600)

        self.init_functions()
        self.init_menubar()

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.table_widgets: list[QTableWidget] = []
        self.table_datas = {}
        self.sorting_order = Qt.AscendingOrder

        self.new_scen_path = None
        self.is_initialized = False

        self.open_file()

    def init_cell(self, cell_data, table_name, col_name):
        cell_item = QTableWidgetItem()
        if col_name == "specialty":
            specialty_idx = specialty_hex.index(cell_data)
            cell_text = specialty_options[specialty_idx]
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif col_name == "alliance":
            cell_text = "Edit"
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif col_name == "force":
            if cell_data == 0xFF:
                cell_text = "None"
            else:
                ruler_id = self.get_values_by_enum(Force.RULER)[cell_data]
                cell_text = self.get_officer_name(ruler_id)
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif col_name in officer_columns:

            cell_text = self.get_officer_name(cell_data)
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif col_name in col_map:
            cell_text = col_map[col_name][cell_data]
            cell_item.setFlags(cell_item.flags() & ~Qt.ItemIsEditable)
        elif self.datatypes[table_name][col_name] == 'int':
            cell_text = int(cell_data)
        elif self.datatypes[table_name][col_name] == 'str':
            cell_text = str(cell_data)
            cell_item.setTextAlignment(
                QTextOption.WrapAtWordBoundaryOrAnywhere)
            cell_item.setTextAlignment(Qt.AlignVCenter)
        cell_item.setData(Qt.DisplayRole, cell_text)
        return cell_item

    def init_table_widget(self, table_name, col_names, table_data):
        table_widget = QTableWidget(self)
        table_widget.setObjectName(table_name)
        table_widget.setColumnCount(len(col_names))
        table_widget.setHorizontalHeaderLabels(col_names)
        table_widget.setRowCount(len(table_data))
        table_widget.setSortingEnabled(True)
        table_widget.cellDoubleClicked.connect(self.on_cell_doubleclick)
        table_widget.itemChanged.connect(self.on_cell_update)
        table_widget.keyPressEvent = self.on_key_pressed

        header = table_widget.horizontalHeader()
        header.sectionClicked.connect(self.sort_table)
        header.setSectionsClickable(True)

        for row_idx in range(len(table_data)):
            for col_idx, col_name in enumerate(col_names):
                cell_data = table_data[row_idx][col_idx]
                if self.datatypes[table_name][col_name] == 'int':
                    cell_data = int(cell_data)
                elif self.datatypes[table_name][col_name] == 'str':
                    # Replace null bytes
                    cell_data = cell_data.replace('\x00', '')
                cell_item = self.init_cell(cell_data, table_name, col_name)
                table_widget.setItem(row_idx, col_idx, cell_item)

        self.tab_widget.addTab(table_widget, table_name)
        self.table_widgets.append(table_widget)

    def officer_names(self):
        return [
            self.get_officer_name(officer_id)
            for officer_id in range(NUM_OFFICERS)]

    def get_officer_name(self, officer_id):
        if officer_id == 0xFFFF:
            return "None"
        elif officer_id >= 850:  # TODO Shared parent
            return "Parent"
        officer_data = self.table_datas['officer']['data'][officer_id]
        return (officer_data[Officer.FAMILYNAME] + ' ' + officer_data[Officer.GIVENNAME]).replace('\x00', '').strip()

    def on_key_pressed(self, event):
        table_widget = self.tab_widget.currentWidget()
        item = table_widget.currentItem()
        if not item:
            return

        row = item.row()
        col = item.column()
        key = event.key()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            if not item.flags() & Qt.ItemIsEditable:
                self.on_cell_doubleclick(row, col)
            else:
                table_widget.editItem(item)
        elif key == Qt.Key_Left and col > 0:
            table_widget.setCurrentCell(row, col - 1)
        elif key == Qt.Key_Right and col < table_widget.columnCount() - 1:
            table_widget.setCurrentCell(row, col + 1)
        elif key == Qt.Key_Up and row > 0:
            table_widget.setCurrentCell(row - 1, col)
        elif key == Qt.Key_Down and row < table_widget.rowCount() - 1:
            table_widget.setCurrentCell(row + 1, col)

    def on_cell_update(self, item):
        if not self.is_initialized:
            return
        row_idx = item.row()
        col_idx = item.column()
        table_widget = item.tableWidget()
        table_name = table_widget.objectName()
        col_name = self.table_datas[table_name]['col_names'][col_idx]
        cell_text = item.text()
        # print(
        # f"Cell ({row_idx}, {col_idx}) in {table_name} with column name {col_name} was modified with new value {cell_text}")

        def reverse(d): return {v: k for k, v in d.items()}
        if col_name == 'id':
            return
        elif col_name == 'specialty':
            cell_data = reverse(specialty_options)[cell_text]
        elif col_name == 'alliance':
            return
        elif col_name == "force":
            if cell_text == "None":
                cell_data = 0xFF
            else:
                officer_id = self.officer_names().index(cell_text)
                cell_data = self.get_values_by_enum(
                    Force.RULER).index(officer_id)
        elif col_name in officer_columns:
            if cell_text == "None":
                cell_data = 0xFFFF
            else:
                cell_data = self.officer_names().index(cell_text)
        elif col_name in col_map:
            cell_data = reverse(col_map[col_name])[cell_text]
        elif self.datatypes[table_name][col_name] == 'int':
            cell_data = int(cell_text)
        elif self.datatypes[table_name][col_name] == 'str':
            cell_data = cell_text

        self.table_datas[table_name]['data'][row_idx][col_idx] = cell_data

    def on_cell_doubleclick(self, row_idx, col_idx):
        current_tab = self.tab_widget.currentIndex()
        current_table = self.table_widgets[current_tab]
        cell_item = current_table.item(row_idx, col_idx)
        table_name = current_table.objectName()
        col_name = self.table_datas[table_name]['col_names'][col_idx]
        if col_name == 'specialty':
            options = specialty_options.values()
            self.choose_option(cell_item, options)
        elif col_name == 'alliance':
            self.alliance(row_idx)
        elif col_name == "force":
            ruler_ids = self.get_values_by_enum(Force.RULER)
            officer_names = self.officer_names()
            options = sorted([officer for officer in officer_names if officer_names.index(
                officer) in ruler_ids]) + ["None"]
            self.choose_option(cell_item, options)
        elif col_name in officer_columns:
            options = sorted(self.officer_names()) + ["None"]
            self.choose_option(cell_item, options)
        elif col_name in col_map:
            options = col_map[col_name].values()
            self.choose_option(cell_item, options)
        else:
            return

    def choose_option(self, cell_item, options):
        combo_box = QComboBox()
        combo_box.addItems(options)
        combo_box.setEditText(cell_item.text())
        combo_box.setInsertPolicy(QComboBox.NoInsert)

        item, ok = QInputDialog.getItem(
            self, "Choose option", "Select an option:", options)

        if ok and item and item in options:
            cell_item.setText(item)

    def create_alliance_value(self, force_numbers):
        return reduce(lambda x, y: x | (1 << y), force_numbers, 0)

    def parse_alliance_value(self, alliance_value):
        return [alliance_value for i in range(NUM_FORCES) if alliance_value & (1 << i)]

    def get_values_by_enum(self, enum_value):
        return [x[enum_value] for x in self.table_datas[enum_value.__class__.__name__.lower()]['data']]

    def alliance(self, row_idx):
        dialog = QDialog()
        dialog.setWindowTitle('Alliances')

        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(scroll_area)

        checkboxes_widget = QWidget()
        checkboxes_layout = QVBoxLayout(checkboxes_widget)

        alliance_value = self.table_datas['force'][row_idx][Force.ALLIANCE]

        force_numbers = self.parse_alliance_value(alliance_value)
        alliance_values = self.get_values_by_enum(Force.ALLIANCE)
        force_rulers = self.get_values_by_enum(Force.RULER)
        allegiance_values = self.get_values_by_enum(Officer.ALLEGIANCE)
        # ruler_allegiances = [allegiance_values[x]
        #                      if x != 0xFFFF else 0xFF for x in force_rulers]

        checkboxes: list[QCheckBox] = []

        for i, ruler in enumerate(force_rulers):
            ruler_name = officer_map[ruler]
            checkbox = QCheckBox(f'{ruler_name}')

            if i in force_numbers:
                checkbox.setChecked(True)

            checkboxes.append(checkbox)

            if ruler_name != 'Unknown':
                checkboxes_layout.addWidget(checkbox)

        checkboxes_widget.setLayout(checkboxes_layout)
        scroll_area.setWidget(checkboxes_widget)

        button = QPushButton('OK')
        button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(button)

        if dialog.exec_() != QDialog.Accepted:
            return

        checked = [
            i for i, checkbox in enumerate(checkboxes)
            if checkbox.isChecked()]

        new_alliance_value = self.create_alliance_value(checked)

        for i, alliance_value in enumerate(alliance_values):
            if i in checked:
                self.table_datas['force'][i][Force.ALLIANCE] = new_alliance_value
            else:
                self.table_datas['force'][i][Force.ALLIANCE] &= ~new_alliance_value
            print(self.parse_alliance_value(
                self.table_datas['force'][i][Force.ALLIANCE]))
        print()

    def sort_table(self, col_idx):
        table_widget = self.table_widgets[-1]
        self.sorting_order = Qt.DescendingOrder if self.sorting_order == Qt.AscendingOrder else Qt.AscendingOrder
        table_widget.sortItems(col_idx, self.sorting_order)

        # Update sorting_order attribute
        self.sorting_order = table_widget.horizontalHeader().sortIndicatorOrder()

    def filter_table(self):
        search_text = self.search_box.text().lower()

        for table in self.table_widgets:
            table.setSortingEnabled(False)

            for row_idx in range(table.rowCount()):
                match_found = False

                for col_idx in range(table.columnCount()):
                    cell_text = table.item(row_idx, col_idx).text().lower()

                    if search_text in cell_text:
                        match_found = True
                        break

                table.setRowHidden(row_idx, not match_found)

            table.setSortingEnabled(True)
            table.sortByColumn(0, self.sorting_order)

    def open_file(self):
        """Opens a scenario file and parses the data into a database file for editing.
        """
        self.is_initialized = False
        self.old_scen_path, _ = QFileDialog.getOpenFileName(
            self, "Open Scenario File", "", "Scenario Files (*.s11 SAN11RES.BIN)")

        if not self.old_scen_path:
            return

        if self.old_scen_path.endswith("SAN11RES.BIN"):
            self.version = Version.PS2EN
            # List of scenario names
            item, ok = QInputDialog.getItem(
                self, "Select Scenario", "Select a scenario:", ps2_scenarios, 0, False)
            if ok:
                # Get the index of the selected item
                self.file_offset = ps2_scenarios[item]
            else:
                return

        else:
            self.version = Version.PCEN
            self.file_offset = 0

        self.tab_widget.clear()

        self.db_path = os.path.join(tempfile.gettempdir(), 'rtk11.db')

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        # This reads the data from the scenario file into the database
        with BinaryParser('rtk11.lyt', encoding='shift-jis', file_offset=self.file_offset) as bp:
            bp.parse_file(self.old_scen_path, self.db_path)
            self.datatypes = {
                tablename: {
                    col_idx[0]: col_idx[1]
                    for section in tabledata['sections']
                    for col_idx in section['data']
                }
                for tablename, tabledata in bp.data.items()
            }
            for table in self.datatypes.values():
                table['id'] = 'int'

        with connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            table_names = [x[0] for x in cursor.fetchall()]

            # Retrieve the tables in the database
            for table_name in table_names:
                # Retrieve the column names and data from the table
                cursor.execute(f"SELECT * FROM {table_name}")
                col_names = [x[0] for x in cursor.description]
                table_data = [list(x) for x in cursor.fetchall()]
                self.table_datas[table_name] = {}
                self.table_datas[table_name]['data'] = table_data
                self.table_datas[table_name]['col_names'] = col_names

            # Initialise table widgets
            for table_name in table_names:
                if table_name == 'sqlite_sequence':
                    continue
                self.init_table_widget(
                    table_name,
                    self.table_datas[table_name]['col_names'],
                    self.table_datas[table_name]['data'])

        self.save_file_action.setEnabled(True)
        self.save_as_file_action.setEnabled(True)
        self.is_initialized = True

    def save_file(self):
        """
        Saves the current state of the database to the scenario file.
        Will first prompt for the path to save to if it doesn't exist yet
        """

        if not self.new_scen_path:
            self.save_as_file()
            return

        with connect(self.db_path, isolation_level=None) as conn:
            for table_widget in self.table_widgets:
                table_name = table_widget.objectName()
                table_data = self.table_datas[table_name]['data']
                col_names = self.table_datas[table_name]['col_names']
                placeholders = ','.join(['?'] * len(col_names))
                for row_idx in table_data:
                    conn.execute(
                        f"REPLACE INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})", row_idx)

        # This writes the data from the database back to the scenario file
        with BinaryParser('rtk11.lyt', encoding='shift-jis', file_offset=self.file_offset) as bp:
            bp.write_back(self.new_scen_path, self.db_path)

    def save_as_file(self):
        """
        Prompts the user for a scenario file before calling the regular save function.
        """
        self.new_scen_path, _ = QFileDialog.getSaveFileName(
            self, "Save Scenario File", "", "Scenario Files (*.s11)")

        if not self.new_scen_path:
            return

        if self.old_scen_path != self.new_scen_path:
            shutil.copyfile(self.old_scen_path, self.new_scen_path)

        self.save_file()


def main():
    app = QApplication(sys.argv)
    gui = ROTKXIGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
