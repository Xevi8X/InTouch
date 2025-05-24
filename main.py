import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from src.nodelist.nodelist import NodeList
from src.state.state import State, create_fake_state

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dark_stylesheet = """
    QWidget {
        background-color: #121212;
        color: #ffffff;
    }
    QPushButton {
        background-color: #1f1f1f;
        border: 1px solid #333;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #323232;
    }
    """

    app.setStyleSheet(dark_stylesheet)

    window = QWidget()
    window.setWindowTitle("InTouch")
    window.resize(400, 300)

    state = create_fake_state()
    node_list = NodeList(state)
    layout = QHBoxLayout()

    layout.addWidget(node_list)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())