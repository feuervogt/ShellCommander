import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QPushButton, QDialog, QLabel, QHBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

class ShellCommanderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShellCommander")
        self.setGeometry(100, 100, 800, 400)
        self.initUI()

    def initUI(self):
        # Central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Table for scripts
        self.table = QTableWidget(0, 2)  # 0 rows, 2 columns
        self.table.setHorizontalHeaderLabels(["Name", "Pfad"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Hinzufügen")
        self.add_button.clicked.connect(self.add_script)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Entfernen")
        self.remove_button.clicked.connect(self.remove_script)
        button_layout.addWidget(self.remove_button)

        self.run_button = QPushButton("Ausführen")
        self.run_button.clicked.connect(self.run_script)
        button_layout.addWidget(self.run_button)

        self.about_button = QPushButton("Über")
        self.about_button.clicked.connect(self.show_about_dialog)
        button_layout.addWidget(self.about_button)

        layout.addLayout(button_layout)

        # Set layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_script(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Skript hinzufügen", "", "PowerShell Skripte (*.ps1);;Alle Dateien (*)", options=options
        )
        if file_path:
            script_name = file_path.split("/")[-1]
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 0, QTableWidgetItem(script_name))
            self.table.setItem(row_count, 1, QTableWidgetItem(file_path))

    def remove_script(self):
        selected_rows = self.table.selectionModel().selectedRows()
        for index in sorted(selected_rows, reverse=True):
            self.table.removeRow(index.row())

    def run_script(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte wählen Sie ein Skript aus, das ausgeführt werden soll.")
            return

        for row in selected_rows:
            script_path = self.table.item(row.row(), 1).text()
            QMessageBox.information(self, "Ausführen", f"Skript wird ausgeführt: {script_path}")
            # Hier kann die eigentliche Logik zum Ausführen des Skripts ergänzt werden.

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("Über ShellCommander")
        about_dialog.setFixedSize(300, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ShellCommander\nVersion 1.0\n\nEin Tool zur Verwaltung und Ausführung von Skripten."))
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(about_dialog.accept)
        layout.addWidget(ok_button)
        about_dialog.setLayout(layout)
        about_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ShellCommanderGUI()
    main_window.show()
    sys.exit(app.exec_())
