import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("InTouch")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())