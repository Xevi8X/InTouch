import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from src.nodelist.nodelist import NodeList
from src.state.state import State, create_fake_state
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt

# Importowanie modułów
from src.map_module import MapHandler
from src.button_panel_module import ButtonPanelWidget


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interaktywna Mapa PyQt5 z Folium - Pożar w Warszawie")
        self.setGeometry(100, 100, 1200, 800)  # Początkowy rozmiar okna

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        # --- Lewa strona: Mapa ---
        self.map_container_widget = QWidget()
        self.map_container_layout = QVBoxLayout(self.map_container_widget)
        self.map_container_layout.setContentsMargins(0, 0, 0, 0)

        # Create a widget to hold both the web view and button panel
        self.map_and_buttons_widget = QWidget()
        self.map_and_buttons_layout = QGridLayout(self.map_and_buttons_widget)
        self.map_and_buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.web_view = QWebEngineView()
        self.map_and_buttons_layout.addWidget(self.web_view, 0, 0, 1, 1)

        self.button_panel_widget = ButtonPanelWidget(self.map_and_buttons_widget)
        self.map_and_buttons_layout.addWidget(self.button_panel_widget, 0, 0, 1, 1, Qt.AlignTop)

        # Add the map and buttons widget to the main container
        self.map_container_layout.addWidget(self.map_and_buttons_widget)

        self.main_layout.addWidget(self.map_container_widget, 5)

        self.map_handler = MapHandler(self.web_view)

        # Connect button panel signals
        self.button_panel_widget.button_clicked.connect(self.map_handler.update_map_style)
        self.button_panel_widget.heatmap_toggled.connect(self.map_handler.toggle_heatmap)

        self.info_panel = QVBoxLayout()
        self.info_panel_widget = NodeList(create_fake_state())
        self.info_panel_widget.setLayout(self.info_panel)
        self.main_layout.addWidget(self.info_panel_widget, 1)


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

    window = MapApp()
    window.show()
    sys.exit(app.exec_())

