from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from ..markers.markers import get_icon_path
from ..state.state import Node, State

class NodeListItem(QWidget):
    def __init__(self, node: Node, center_callback=None):
        super().__init__()
        self.node = node

        main_layout = QHBoxLayout()

        icon = QIcon(get_icon_path(node.marker))
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(32, 32))
        icon_label.setFixedSize(32, 32)
        main_layout.addWidget(icon_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        center_button = QPushButton("Center", self)
        if center_callback:
            center_button.clicked.connect(lambda: center_callback(self.node.location))
        button_layout.addWidget(center_button)


        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(QLabel(f"{node.name}"))
        vertical_layout.addStretch()
        vertical_layout.addLayout(button_layout)

        main_layout.addLayout(vertical_layout)

        self.setLayout(main_layout)

class NodeList(QWidget):
    def __init__(self, state: State):
        super().__init__()
        self.state = state
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        self.refresh()

    def refresh(self):
        self.list_widget.clear()
        for node in self.state.nodes:
            item = QListWidgetItem()
            widget = NodeListItem(node)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
        self.list_widget.selectedItems().clear()
        