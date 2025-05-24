# main_app.py
# To jest główny plik aplikacji, który łączy wszystkie moduły.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
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
        self.web_view = QWebEngineView()
        self.map_container.addWidget(self.web_view)
        self.main_layout.addLayout(self.map_container, 3)  # Proporcje 3:1 dla mapy

        # Inicjalizacja obsługi mapy
        self.map_handler = MapHandler(self.web_view)

        # --- Prawa strona: Panel informacyjny ---
        self.info_panel = QVBoxLayout()  # Układ pionowy dla panelu
        self.info_panel_widget = QWidget()  # Widget-kontener dla panelu
        self.info_panel_widget.setLayout(self.info_panel)
        # Stylizacja kontenera panelu, aby był wyraźnie widoczny
        self.info_panel_widget.setStyleSheet(
            "background-color: #f0f8ff; border-left: 2px solid #a0a0a0; padding: 10px; border-radius: 5px;")

        # Inicjalizacja obsługi panelu informacyjnego
        self.main_layout.addLayout(self.info_panel, 1)  # Proporcje 1:3 dla panelu


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec_()) # Zmiana z app.exec() na app.exec_() dla PyQt5