import sys
from PyQt5.QtWidgets import QApplication
from gui import ShellCommanderApp
from controller import Controller

def main():
    # Initialisiere COntroller und Datenbank
    db_file = "scripts.db"
    controller = Controller(db_file)
    controller.initialize_database()
    
    #    Startet die ShellCommander-Anwendung.
    app = QApplication(sys.argv)
    main_window = ShellCommanderApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
