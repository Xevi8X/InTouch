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

        self.map_container_widget = QWidget()
        self.map_container_layout = QGridLayout(self.map_container_widget)
        self.map_container_layout.setContentsMargins(0, 0, 0, 0)

        # --- Lewa strona: Mapa ---
        self.map_container = QVBoxLayout()

        # Controls container
        self.controls_layout = QHBoxLayout()
        self.heatmap_toggle = QPushButton("Toggle Heatmap")
        self.heatmap_toggle.setCheckable(True)
        self.heatmap_toggle.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #FF5722;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:checked:hover {
                background-color: #E64A19;
            }
        """)
        self.controls_layout.addWidget(self.heatmap_toggle)
        self.controls_layout.addStretch()

        self.map_container.addLayout(self.controls_layout)

        self.web_view = QWebEngineView()
        self.map_container_layout.addWidget(self.web_view, 0, 0, 1, 1)

        self.button_panel_widget = ButtonPanelWidget(self.map_container_widget)
        self.map_container_layout.addWidget(self.button_panel_widget, 0, 0, 1, 1, Qt.AlignTop)

        self.main_layout.addWidget(self.map_container_widget, 3)

        self.map_handler = MapHandler(self.web_view)

        # Connect heatmap toggle
        self.heatmap_toggle.clicked.connect(self.toggle_heatmap)

        self.button_panel_widget.button_clicked.connect(self.map_handler.update_map_style)

        self.info_panel = QVBoxLayout()
        self.info_panel_widget = QWidget()
        self.info_panel_widget.setLayout(self.info_panel)
        self.info_panel_widget.setStyleSheet(
            "background-color: #f0f8ff; border-left: 2px solid #a0a0a0; padding: 10px; border-radius: 5px;")

        self.main_layout.addWidget(self.info_panel_widget, 1)

    def toggle_heatmap(self):
        """Toggle heatmap visualization on the map"""
        is_heatmap_enabled = self.heatmap_toggle.isChecked()
        self.map_handler.toggle_heatmap(is_heatmap_enabled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec_())

