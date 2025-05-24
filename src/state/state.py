from ..markers.markers import Marker

class Node:
    def __init__(self, name: str, marker: Marker, location: tuple[float, float]):
        self.name = name
        self.marker = marker
        self.location = location

class State:
    def __init__(self):
        self.nodes : list[Node] = []
        self.map_zoom = 1.0
        self.map_center = (0.0, 0.0)

def create_fake_state() -> State:
    state = State()
    state.nodes.append(Node("Node 1", Marker.AMBULANCE, (10.0, 20.0)))
    state.nodes.append(Node("Node 2", Marker.FIRETRUCK, (30.0, 40.0)))
    state.nodes.append(Node("Node 3", Marker.DOG, (50.0, 60.0)))
    state.map_zoom = 1.5
    state.map_center = (25.0, 30.0)
    return state