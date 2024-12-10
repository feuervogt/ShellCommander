import sys
from PyQt5.QtWidgets import QApplication
from gui import ShellCommanderApp

def main():
    """
    Startet die ShellCommander-Anwendung.
    """
    app = QApplication(sys.argv)
    main_window = ShellCommanderApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
