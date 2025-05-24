import base64
from enum import Enum, auto
import os

def get_file_path() -> str:
    return os.path.abspath(__file__)

class Marker(Enum):
    AMBULANCE = auto()
    DOG = auto()
    FIRETRUCK = auto()
    FIREFIGHTER = auto()
    PARAMEDIC = auto()
    UAV = auto()

def get_icon(marker: Marker) -> str:
    """Returns the icon associated with the given marker."""
    icons = {
        Marker.AMBULANCE:   _load_icon("ambulance.png"),
        Marker.DOG:         _load_icon("dog.png"),
        Marker.FIRETRUCK:   _load_icon("firetruck.png"),
        Marker.FIREFIGHTER: _load_icon("firefighter.png"),
        Marker.PARAMEDIC:   _load_icon("paramedic.png"),
        Marker.UAV:         _load_icon("uav.png"),
    }
    return icons.get(marker, "")

def _load_icon(image_path: str) -> str:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", image_path)
    try:
        with open(full_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        print(f"Icon file {image_path} not found at {full_path}.")
        return ""
    