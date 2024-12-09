import os
import json
import subprocess
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QPlainTextEdit,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QGridLayout, QFrame, QVBoxLayout, QMenu, QAction
)
from PyQt5.QtCore import Qt
#from database_manager import DatabaseManager #Import der Datenbanklogik
from datetime import datetime


APP_NAME = "ShellCommander © 2024 feuervogt"
VERSION = "0.2.7"

class ShellCommanderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_list = []  # Liste der geladenen Skripte
        self.script_file = "scripts.json"  # Datei für persistente Speicherung
        self.load_scripts()  # Skripte beim Start laden
        self.init_ui()  # Benutzeroberfläche initialisieren

    def init_ui(self):
        """
        Initialisiert die Hauptbenutzeroberfläche.
        """
        # Hauptfenster konfigurierengit 
        self.setGeometry(100, 100, 1024, 768)

        # Zentrales Widget und Hauptlayout erstellen
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 5, 15, 15)  # Margins angepasst
        main_layout.setSpacing(5)  # Geringere Abstände zwischen Elementen

        # Farbverlauf für den Hintergrund
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5c5c5c, /* Orange am Startpunkt */
                    stop: 0.6 #c4c4c4, /* Übergang beginnt bei 60% Höhe */
                    stop: 1 #d7d7d7  /* Blaugrün endet unten */
                );
            }
        """)

        # Begrüßungstext (kompakter Bereich)
        welcome_label = QLabel(f"Willkommen bei {APP_NAME}!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        main_layout.addWidget(welcome_label)  # Label oben hinzufügen
        welcome_label.setMaximumHeight(40)  # Höhe des Labels begrenzen

        # Tabelle für Skripte erstellen
        self.script_table = QTableWidget()  # Tabelle mit Skripten
        self.script_table.setColumnCount(2)  # Zwei Spalten: Name und Pfad
        self.script_table.setHorizontalHeaderLabels(["Script-Name", "Pfad"])  # Kopfzeilen
        self.script_table.horizontalHeader().setStretchLastSection(True)  # Pfad-Spalte füllt Platz aus
        self.script_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Tabelle nicht bearbeitbar
        self.script_table.setMaximumHeight(250)  # Höhe begrenzen
        self.script_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.script_table.customContextMenuRequested.connect(self.context_menu)
        main_layout.addWidget(self.script_table)  # Tabelle zum Layout hinzufügen

        # Log-Bereich 
        log_layout = QHBoxLayout()
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)

        clear_log_button = QPushButton("Clear Log", self)
        clear_log_button.clicked.connect(self.clear_log)
        clear_log_button.setFixedWidth(100)  # Fixiere die Breite des Buttons
        clear_log_button.setMaximumHeight(150)  # Gleiche Höhe wie das Logfenster
        
        clear_log_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #d7d7d7, /* Helles Silber */
                    stop: 0.5 #c4c4c4, /* Mittelgrau */
                    stop: 1 #a6a6a6  /* Dunkleres Silber */
                );
                color: black; /* Schwarzer Text */
                border: 1px solid #6e6e6e; /* Dunkler Rand */
                border-radius: 5px; /* Abgerundete Ecken */
                padding: 5px; /* Innenabstand */
                font-size: 14px; /* Schriftgröße */
                font-weight: bold; /* Fettere Schrift */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); /* Leichter 3D-Schatten */
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e6e6e6, /* Heller bei Hover */
                    stop: 0.5 #dcdcdc,
                    stop: 1 #c8c8c8
                );
            }
            QPushButton:pressed {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #c4c4c4, /* Dunkler bei Klick */
                    stop: 0.5 #a6a6a6,
                    stop: 1 #8a8a8a
                );
                border: 1px solid #4a4a4a; /* Dunklerer Rand */
            }
        """)
        
        log_layout.addWidget(clear_log_button)
        

        main_layout.addLayout(log_layout)
        
        # Bereich für Kacheln
        tile_layout = QGridLayout()  # Rasterlayout für die Kacheln
        for i in range(20):  # 20 Kacheln erzeugen
            tile = QFrame()  # Einzelne Kachel als Rahmen
            tile.setFrameShape(QFrame.Box)  # Rahmenform als Box
            tile.setStyleSheet("""
                QFrame {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #d7d7d7, /* Helles Silber */
                        stop: 0.5 #c4c4c4, /* Mittelgrau */
                        stop: 1 #a6a6a6  /* Dunkleres Silber */
                    );
                    border: 1px solid #6e6e6e; /* Dunkler Rand */
                    border-radius: 5px; /* Abgerundete Ecken */
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); /* Leichter 3D-Schatten */
                }
                QFrame:hover {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #e6e6e6, /* Heller bei Hover */
                        stop: 0.5 #dcdcdc,
                        stop: 1 #c8c8c8
                    );
                }
                QFrame:pressed {
                    background-color: qlineargradient(
                        x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #c4c4c4, /* Dunkler bei Klick */
                        stop: 0.5 #a6a6a6,
                        stop: 1 #8a8a8a
                    );
                    border: 1px solid #4a4a4a; /* Dunklerer Rand */
                }
            """)
            #tile.setStyleSheet("background-color: lightgray; border: 1px solid black;")  # Stil setzen

            # Beschriftung für die Kachel
            tile_layout_inner = QVBoxLayout()  # Inneres Layout für die Kachel
            tile_label = QLabel(f"Kachel {i + 1}")  # Nummerierung der Kachel
            tile_label.setAlignment(Qt.AlignCenter)  # Text zentrieren
            tile_layout_inner.addWidget(tile_label)  # Label ins Layout einfügen
            tile.setLayout(tile_layout_inner)  # Inneres Layout der Kachel zuweisen

            # Kachel im Rasterlayout platzieren
            tile_layout.addWidget(tile, i // 5, i % 5)  # 4 Zeilen, 5 Spalten
        main_layout.addLayout(tile_layout)  # Kachelbereich ins Hauptlayout einfügen

        # Buttons erstellen
        button_layout = QHBoxLayout()  # Horizontaler Bereich für Buttons

        # Stil für die Buttons festlegen
        button_style = """
            QPushButton {
                background-color: #004d40; /* Dunkles Blaugrün */
                color: white; /* Weißer Text */
                border: none;
                border-radius: 5px; /* Abgerundete Ecken */
                padding: 8px 15px; /* Innenabstand für bessere Lesbarkeit */
                font-size: 14px; /* Größere, moderne Schrift */
            }
            QPushButton:hover {
                background-color: #00695c; /* Etwas helleres Blaugrün beim Hover */
            }
            QPushButton:pressed {
                background-color: #003d33; /* Dunklerer Ton beim Drücken */
            }
        """

        load_script_button = QPushButton("Script hinzufügen", self)
        load_script_button.setStyleSheet(button_style)
        load_script_button.clicked.connect(self.add_script)
        button_layout.addWidget(load_script_button)

        run_script_button = QPushButton("Ausgewähltes Script ausführen", self)
        run_script_button.setStyleSheet(button_style)
        run_script_button.clicked.connect(self.run_selected_script)
        button_layout.addWidget(run_script_button)

        delete_script_button = QPushButton("Script entfernen", self)
        delete_script_button.setStyleSheet(button_style)
        delete_script_button.clicked.connect(self.remove_selected_script)
        button_layout.addWidget(delete_script_button)

        about_button = QPushButton("Über", self)
        about_button.setStyleSheet(button_style)
        about_button.clicked.connect(self.show_about)
        button_layout.addWidget(about_button)

        exit_button = QPushButton("Beenden", self)
        exit_button.setStyleSheet(button_style)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)  # Buttonbereich ins Hauptlayout einfügen

        # Layout dem zentralen Widget zuweisen und im Hauptfenster setzen
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Tabelle initial füllen
        self.update_script_table()

    # --- Kontextmenü-Logik ---
    def context_menu(self, position):
        """
        Kontextmenü für die Tabelle.
        """
        menu = QMenu()
        run_action = QAction("Ausführen", self)
        delete_action = QAction("Entfernen", self)
        run_action.triggered.connect(self.run_selected_script)
        delete_action.triggered.connect(self.remove_selected_script)
        menu.addAction(run_action)
        menu.addAction(delete_action)
        menu.exec_(self.script_table.viewport().mapToGlobal(position))

    # --- Logik für Skript-Verwaltung ---
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
            self.script_table.setItem(row, 0, QTableWidgetItem(name))  # Name einfügen
            self.script_table.setItem(row, 1, QTableWidgetItem(path))  # Pfad einfügen

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
            if result.returncode == 0:
                self.log_message(f"Skript '{script_name}' erfolgreich ausgeführt.")
            else:
                self.log_message(f"Skript '{script_name}' fehlgeschlagen. Fehler: {result.stderr.strip()}")
        except Exception as e:
            self.log_message(f"Fehler beim Ausführen von '{script_name}': {e}")

    def log_message(self, message):
        """
        Fügt eine neue Nachricht ins Log hinzu.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.appendPlainText(f"[{timestamp}] {message}")

    def clear_log(self):
        """
        Löscht das Log.
        """
        self.log_text.clear()    
    
    def show_about(self):
        """
        Zeigt Informationen über die Anwendung an.
        """
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("Über")
        about_dialog.setText(f"{APP_NAME} v{VERSION}\n\n"
                             "Ein Tool für IT-Administratoren, um Skripte und Automatisierungen zu verwalten.\n\n"
                             "© 2024 ShellCommander Team.")
        about_dialog.setIcon(QMessageBox.Information)
        about_dialog.setStandardButtons(QMessageBox.Ok)
        about_dialog.exec_()