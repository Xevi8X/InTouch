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

def get_icon_url(marker: Marker) -> str:
    path = get_icon_path(marker)
    if not path:
        return ""
    return _load_icon_url(path)


def get_icon_path(marker: Marker) -> str:
    icon_paths = {
        Marker.AMBULANCE:   "ambulance.png",
        Marker.DOG:         "dog.png",
        Marker.FIRETRUCK:   "firetruck.png",
        Marker.FIREFIGHTER: "fireman.png",
        Marker.PARAMEDIC:   "paramedic.png",
        Marker.UAV:         "uav.png",
    }
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", icon_paths.get(marker, ""))
    if not os.path.exists(path):
        return ""
    return path

def _load_icon_url(image_path: str) -> str:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", image_path)
    try:
        with open(full_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        print(f"Icon file {image_path} not found at {full_path}.")
        return ""
    