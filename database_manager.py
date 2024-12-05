import sqlite3

class DatabaseManager:
    def __init__(self, db_name="shellcommander.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()

    def add_script(self, name, path, script_type):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO scripts (name, path, type) VALUES (?, ?, ?)', (name, path, script_type))
        connection.commit()
        connection.close()

    def remove_script(self, name):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM scripts WHERE name = ?', (name,))
        connection.commit()
        connection.close()

    def get_all_scripts(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('SELECT name, path, type FROM scripts')
        scripts = cursor.fetchall()
        connection.close()
        return scripts
