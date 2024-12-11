from database_manager import DatabaseManager

class Controller:
    def __init__(self, db_file):
        """
        Initialisiert den Controller mit der Datenbank.
        :param db_file: Pfad zur SQLite-Datenbankdatei.
        """
        self.db_manager = DatabaseManager(db_file)

    def initialize_database(self):
        """
        Initialisiert die Datenbank (z. B. erstellt Tabellen).
        """
        self.db_manager.create_table()

    def add_script(self, name, path):
        """
        Fügt ein neues Skript hinzu.
        :param name: Name des Skripts.
        :param path: Pfad zum Skript.
        """
        self.db_manager.add_script(name, path)

    def get_all_scripts(self):
        """
        Ruft alle Skripte aus der Datenbank ab.
        :return: Liste von Skriptdaten.
        """
        return self.db_manager.get_all_scripts()

    def delete_script(self, script_id):
        """
        Löscht ein Skript anhand der ID.
        :param script_id: ID des Skripts.
        """
        self.db_manager.delete_script(script_id)

    def close(self):
        """
        Schließt die Datenbankverbindung.
        """
        self.db_manager.close_connection()
