from src.markers.markers import Marker, get_icons

detailed_events = [
    {
        "type": "Ranny człowiek",
        "name": "Ranny człowiek 1",
        "coords": "52.2501, 21.1000", # Współrzędne w obrębie pożaru
        "threat_level": "Wysoki",
        "time_found": "12:35",
        "block_index": 0 # Indeks bloku, który ma być zaktualizowany
    },
    {
        "type": "Ranny człowiek",
        "name": "Ranny człowiek 2",
        "coords": "52.2500, 21.1001", # Współrzędne w obręgu pożaru
        "threat_level": "Średni",
        "time_found": "12:40",
        "block_index": 1
    },
    {
        "type": "Ranny człowiek",
        "name": "Ranny człowiek 3",
        "coords": "52.2499, 21.0999", # Współrzędne w obrębie pożaru
        "threat_level": "Niski",
        "time_found": "12:45",
        "block_index": 2
    },
    {
        "type": "Pożar",
        "name": "Pożar w Pradze-Południe",
        "scale": "Duża",
        "time_detected": "12:30",
        "status": "Aktywny", # Dodana informacja o statusie
        "details": "Służby ratunkowe w drodze.", # Dodana trzecia linia szczegółów dla pożaru
        "block_index": 3
    }
]

people_points = [
    {"lat": 52.2501, "lon": 21.1000, "name": "Osoba A", "info": "W pobliżu pożaru"}, # ok. 11m na N
    {"lat": 52.2500, "lon": 21.1001, "name": "Osoba B", "info": "Zgłosiła dym"}, # ok. 7m na E
    {"lat": 52.2499, "lon": 21.0999, "name": "Osoba C", "info": "Ewakuowana"} # ok. 11m na S, 7m na W
]

# Współrzędne pożaru (centrum okręgu)
fire_coords = [52.250, 21.100]

import enum

class ActorType(enum.Enum):
    DOCTOR = "Lekarz"
    DRONE = "Dron"
    VEHICLE = "Pojazd"
    FIREFIGHTER = "Strażak"
    DOG = "Pies"

additional_actors = [
    # {"type": ActorType.DOCTOR, "lat": 52.2505, "lon": 21.1010, "name": "Lekarz A", "info": "Przybył na miejsce", "icon": get_icons(Marker.PARAMEDIC)}, # Outside
    {"type": ActorType.VEHICLE, "lat": 52.2499, "lon": 21.0987, "name": "Wóz strażacki 1", "info": "Na stanowisku", "icon": get_icons(Marker.FIRETRUCK)}, # Moved further outside - southwest
    {"type": ActorType.VEHICLE, "lat": 52.2510, "lon": 21.0997, "name": "Wóz strażacki 2", "info": "Na stanowisku", "icon": get_icons(Marker.FIRETRUCK)}, # Added second fire truck - northeast
    {"type": ActorType.VEHICLE, "lat": 52.2492, "lon": 21.1009, "name": "Wóz strażacki 3", "info": "Na stanowisku", "icon": get_icons(Marker.FIRETRUCK)}, # Added third fire truck - southeast
    {"type": ActorType.DRONE, "lat": 52.2500, "lon": 21.1000, "name": "Dron 1", "info": "Monitoruje teren", "icon": get_icons(Marker.UAV)}, # Inside (at fire center)
    {"type": ActorType.FIREFIGHTER, "lat": 52.2498, "lon": 21.1002, "name": "Strażak Kowalski", "info": "Akcja gaśnicza", "icon": get_icons(Marker.FIREFIGHTER)}, # Inside
    {"type": ActorType.DOG, "lat": 52.2501, "lon": 21.0998, "name": "Pies ratowniczy Burek", "info": "Szuka poszkodowanych", "icon": get_icons(Marker.DOG)}
]