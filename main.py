# main_app.py
# To jest główny plik aplikacji, który łączy wszystkie moduły.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Importowanie modułów
from src.map_module import MapHandler


class MapApp(QMainWindow):
    """
    Główna klasa aplikacji, która tworzy okno, układy
    i integruje moduły mapy oraz panelu informacyjnego.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interaktywna Mapa PyQt5 z Folium - Pożar w Warszawie")
        self.setGeometry(100, 100, 1200, 800)  # Początkowy rozmiar okna

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

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
        self.map_container.addWidget(self.web_view)
        self.main_layout.addLayout(self.map_container, 3)  # Proporcje 3:1 dla mapy

        # Inicjalizacja obsługi mapy
        self.map_handler = MapHandler(self.web_view)
        
        # Connect heatmap toggle
        self.heatmap_toggle.clicked.connect(self.toggle_heatmap)

        # --- Prawa strona: Panel informacyjny ---
        self.info_panel = QVBoxLayout()  # Układ pionowy dla panelu
        self.info_panel_widget = QWidget()  # Widget-kontener dla panelu
        self.info_panel_widget.setLayout(self.info_panel)
        # Stylizacja kontenera panelu, aby był wyraźnie widoczny
        self.info_panel_widget.setStyleSheet(
            "background-color: #f0f8ff; border-left: 2px solid #a0a0a0; padding: 10px; border-radius: 5px;")

        # Inicjalizacja obsługi panelu informacyjnego
        self.main_layout.addLayout(self.info_panel, 1)  # Proporcje 1:3 dla panelu

    def toggle_heatmap(self):
        """Toggle heatmap visualization on the map"""
        is_heatmap_enabled = self.heatmap_toggle.isChecked()
        self.map_handler.toggle_heatmap(is_heatmap_enabled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec_()) # Zmiana z app.exec() na app.exec_() dla PyQt5