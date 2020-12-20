#!/usr/bin/python
from PyQt5.QtWidgets import QApplication
from SqliteQt import Fenetre
import sys

# ===================================================================
#                         Programme principal
# ===================================================================

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
