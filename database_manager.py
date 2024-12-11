import sqlite3
from sqlite3 import Error


class DatabaseManager:
    def __init__(self, db_file):
        """
        Initialisiert die Verbindung zur SQLite-Datenbank.
        :param db_file: Pfad zur SQLite-Datenbankdatei.
        """
        self.db_file = db_file
        self.connection = None
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.row_factory = sqlite3.Row  # Erlaubt Zugriff auf Spaltennamen
            print(f"Verbindung zur Datenbank '{db_file}' erfolgreich hergestellt.")
        except Error as e:
            print(f"Fehler beim Verbinden mit der Datenbank: {e}")

    def create_table(self):
        """
        Erstellt die Tabelle für Skriptdaten, falls sie noch nicht existiert.
        """
        query = """
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL
        );
        """
        self.execute_query(query)

    def execute_query(self, query, parameters=()):
        """
        Führt eine SQL-Abfrage aus (INSERT, UPDATE, DELETE).
        :param query: Die SQL-Abfrage.
        :param parameters: Parameter für die Abfrage.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
            self.connection.commit()
            print("Abfrage erfolgreich ausgeführt.")
        except Error as e:
            print(f"Fehler beim Ausführen der Abfrage: {e}")

    def fetch_all(self, query, parameters=()):
        """
        Führt eine SELECT-Abfrage aus und gibt alle Ergebnisse zurück.
        :param query: Die SELECT-Abfrage.
        :param parameters: Parameter für die Abfrage.
        :return: Liste von Ergebnissen.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
        except Error as e:
            print(f"Fehler beim Abrufen von Daten: {e}")
            return []

    def add_script(self, name, path):
        """
        Fügt ein neues Skript zur Datenbank hinzu.
        :param name: Name des Skripts.
        :param path: Pfad zum Skript.
        """
        query = "INSERT INTO scripts (name, path) VALUES (?, ?)"
        self.execute_query(query, (name, path))

    def delete_script(self, script_id):
        """
        Löscht ein Skript aus der Datenbank anhand der ID.
        :param script_id: ID des Skripts.
        """
        query = "DELETE FROM scripts WHERE id = ?"
        self.execute_query(query, (script_id,))

    def get_all_scripts(self):
        """
        Ruft alle Skriptdaten aus der Datenbank ab.
        :return: Liste von Skriptdaten (id, name, path).
        """
        query = "SELECT * FROM scripts"
        return self.fetch_all(query)

    def close_connection(self):
        """
        Schließt die Verbindung zur Datenbank.
        """
        if self.connection:
            self.connection.close()
            print("Datenbankverbindung geschlossen.")
