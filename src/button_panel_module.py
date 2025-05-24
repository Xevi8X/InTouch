from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class ButtonPanelWidget(QWidget):
    """
    Widget zawierający zestaw przycisków filtrujących dla mapy.
    """
    button_clicked = pyqtSignal(str)
    heatmap_toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_layout = QHBoxLayout(self)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            "background-color: #f0f0f0; border-bottom: 1px solid #ccc; padding: 5px; border-radius: 5px;")

        self._create_buttons()

    def _create_buttons(self):
        """
        Tworzy i stylizuje przyciski filtrujące.
        """
        # Add heatmap toggle button first
        self.heatmap_toggle = QPushButton("Toggle Heatmap")
        self.heatmap_toggle.setCheckable(True)
        self.heatmap_toggle.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:checked {
                background-color: #FF5722;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:checked:hover {
                background-color: #E64A19;
            }
        """)
        self.heatmap_toggle.clicked.connect(lambda checked: self.heatmap_toggled.emit(checked))
        self.button_layout.addWidget(self.heatmap_toggle)

        # Add map style buttons
        button_names = ["Strona Główna", "Filtry", "Ostrzeżenia", "Aktorzy", "Zdarzenia", "Kanał"]
        self.filter_buttons = []
        for name in button_names:
            button = QPushButton(name)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; /* Zielony */
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #367c39;
                }
            """)
            button.clicked.connect(lambda checked, name=name: self.button_clicked.emit(name))
            self.button_layout.addWidget(button)
            self.filter_buttons.append(button)

