import sys
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

        self.main_layout.addWidget(self.map_container_widget, 3)

        self.map_handler = MapHandler(self.web_view)

        # Connect button panel signals
        self.button_panel_widget.button_clicked.connect(self.map_handler.update_map_style)
        self.button_panel_widget.heatmap_toggled.connect(self.map_handler.toggle_heatmap)

        self.info_panel = QVBoxLayout()
        self.info_panel_widget = QWidget()
        self.info_panel_widget.setLayout(self.info_panel)
        self.info_panel_widget.setStyleSheet(
            "background-color: #f0f8ff; border-left: 2px solid #a0a0a0; padding: 10px; border-radius: 5px;")

        self.main_layout.addWidget(self.info_panel_widget, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec_())

