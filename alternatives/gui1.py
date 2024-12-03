import os
import json
import subprocess
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt

APP_NAME = "ShellCommander"
VERSION = "0.2.0"

class ShellCommanderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_list = []  # Liste der geladenen Skripte
        self.script_file = "scripts.json"  # Datei für persistente Speicherung
        self.load_scripts()  # Skripte beim Start laden
        self.init_ui()

    def init_ui(self):
        """
        Initialisiert die Hauptbenutzeroberfläche.
        """
        self.setWindowTitle(f"{APP_NAME} v{VERSION}")
        self.setGeometry(100, 100, 1024, 768)

        # Layout und Widgets
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Label
        welcome_label = QLabel(f"Willkommen bei {APP_NAME}!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(welcome_label)

        # Skript-Tabelle
        self.script_table = QTableWidget()
        self.script_table.setColumnCount(2)
        self.script_table.setHorizontalHeaderLabels(["Script-Name", "Pfad"])
        self.script_table.horizontalHeader().setStretchLastSection(True)
        self.script_table.setEditTriggers(QTableWidget.NoEditTriggers)
        main_layout.addWidget(self.script_table)

        # Buttons
        button_layout = QHBoxLayout()

        load_script_button = QPushButton("Script hinzufügen", self)
        load_script_button.clicked.connect(self.add_script)
        button_layout.addWidget(load_script_button)

        run_script_button = QPushButton("Ausgewähltes Script ausführen", self)
        run_script_button.clicked.connect(self.run_selected_script)
        button_layout.addWidget(run_script_button)

        delete_script_button = QPushButton("Script entfernen", self)
        delete_script_button.clicked.connect(self.remove_selected_script)
        button_layout.addWidget(delete_script_button)

        about_button = QPushButton("Über", self)
        about_button.clicked.connect(self.show_about)
        button_layout.addWidget(about_button)

        exit_button = QPushButton("Beenden", self)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)

        # Layout zuweisen
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.update_script_table()  # Tabelle initial füllen

    def load_scripts(self):
        """
        Lädt die Skripte aus der JSON-Datei.
        """
        if os.path.exists(self.script_file):
            with open(self.script_file, "r") as file:
                self.script_list = json.load(file)

    def save_scripts(self):
        """
        Speichert die Skripte in die JSON-Datei.
        """
        with open(self.script_file, "w") as file:
            json.dump(self.script_list, file)

    def update_script_table(self):
        """
        Aktualisiert die Tabelle mit den geladenen Skripten.
        """
        self.script_table.setRowCount(len(self.script_list))
        for row, (name, path) in enumerate(self.script_list):
            self.script_table.setItem(row, 0, QTableWidgetItem(name))
            self.script_table.setItem(row, 1, QTableWidgetItem(path))

    def add_script(self):
        """
        Fügt ein neues Skript zur Liste hinzu und speichert es.
        """
        options = QFileDialog.Options()
        script_file, _ = QFileDialog.getOpenFileName(self, "Script auswählen", "", "PowerShell Scripts (*.ps1);;Alle Dateien (*)", options=options)
        if script_file:
            script_name = os.path.basename(script_file)
            self.script_list.append((script_name, script_file))
            self.save_scripts()  # Speichern der aktualisierten Liste
            self.update_script_table()
            QMessageBox.information(self, "Script hinzugefügt", f"Das Script wurde hinzugefügt:\n{script_name}")

    def remove_selected_script(self):
        """
        Entfernt das ausgewählte Skript und speichert die Änderungen.
        """
        selected_row = self.script_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte wählen Sie ein Skript aus!")
            return

        self.script_list.pop(selected_row)
        self.save_scripts()  # Speichern der aktualisierten Liste
        self.update_script_table()
        QMessageBox.information(self, "Script entfernt", "Das ausgewählte Script wurde entfernt.")

    def run_selected_script(self):
        """
        Führt das ausgewählte Skript aus.
        """
        selected_row = self.script_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte wählen Sie ein Skript aus!")
            return
        
        script_name, script_path = self.script_list[selected_row]
        try:
            result = subprocess.run(["powershell", "-File", script_path], capture_output=True, text=True)
            output = result.stdout
            error = result.stderr

            if result.returncode == 0:
                QMessageBox.information(self, "Script erfolgreich", f"Das Script wurde ausgeführt:\n\n{output}")
            else:
                QMessageBox.critical(self, "Fehler beim Ausführen", f"Das Script konnte nicht ausgeführt werden:\n\n{error}")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    def show_about(self):
        """
        Zeigt Informationen über die Anwendung an.
        """
        QMessageBox.about(self, "Über", f"{APP_NAME} v{VERSION}\n\nEin Tool für IT-Administratoren, um Skripte und Automatisierungen zu verwalten.\n\n© 2024 ShellCommander Team.")
