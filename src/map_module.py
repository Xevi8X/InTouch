import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView

from src.static_data import people_points, fire_coords, ActorType, additional_actors


class MapHandler:
    """
    Klasa odpowiedzialna za inicjalizację i zarządzanie mapą Folium
    wyświetlaną w QWebEngineView.
    """

    def __init__(self, web_view: QWebEngineView):
        self.web_view = web_view
        self.m = None
        self.init_map()

    def init_map(self):
        """
        Inicjalizuje mapę Folium z obszarem pożaru i znacznikami osób,
        a następnie ładuje ją do QWebEngineView.
        """
        # Ustawienie centrum mapy na współrzędne pożaru dla lepszej widoczności
        self.m = folium.Map(location=fire_coords, zoom_start=16, tiles="Cartodb dark_matter")

        # Rysowanie obszaru pożaru (okręgu)
        folium.Circle(
            location=fire_coords,
            radius=20,  # Promień pożaru w metrach (20 m)
            color='darkred',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup="<b>Obszar Pożaru</b><br>Wykryto pożar!"
        ).add_to(self.m)

        # Dodawanie znaczników dla osób
        for person in people_points:
            folium.Marker(
                location=[person["lat"], person["lon"]],
                popup=folium.Popup(f"<b>{person['name']}</b><br>{person['info']}", max_width=200),
                tooltip=person['name'],
                icon=folium.Icon(color="green", icon="user")
            ).add_to(self.m)

        # Dodawanie znaczników dla dodatkowych aktorów
        for actor in additional_actors:
            folium.Marker(
                location=[actor["lat"], actor["lon"]],
                popup=folium.Popup(f"<b>{actor['name']}</b><br>{actor['info']}", max_width=200),
                tooltip=actor['name'],
                icon=folium.Icon(color=actor["color"], icon=actor["icon"])
            ).add_to(self.m)

        data = self.m._repr_html_()
        self.web_view.setHtml(data)