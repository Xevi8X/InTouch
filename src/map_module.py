import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView

from src.static_data import people_points, fire_coords, additional_actors


class MapHandler:
    """
    Klasa odpowiedzialna za inicjalizację i zarządzanie mapą Folium
    wyświetlaną w QWebEngineView.
    """

    def __init__(self, web_view: QWebEngineView):
        self.web_view = web_view
        self.m = None
        # Definicja dostępnych stylów map z ich kafelkami i atrybucją
        self.map_styles = {
            "Strona Główna": {"tiles": "Cartodb dark_matter", "attr": "CartoDB"},
            "Filtry": {"tiles": "Cartodb Positron", "attr": "CartoDB"},  # Styl "fossil map" - używamy Cartodb Positron
            "Ostrzeżenia": {"tiles": "OpenStreetMap", "attr": "OpenStreetMap contributors"},
            "Aktorzy": {"tiles": "Cartodb Positron", "attr": "CartoDB"},
            "Zdarzenia": {"tiles": "Stamen Toner", "attr": "Stamen Toner"},
            "Kanał": {"tiles": "Esri.WorldImagery",
                      "attr": "Esri, DigitalGlobe, GeoEye, i-cubed, USDA FSA, USGS, AEX, Getmapping, Aerogrid, IGN, IGP, swisstopo, and the GIS User Community"}
        }
        self.current_style_name = "Strona Główna"  # Domyślny styl
        self.init_map()

    def init_map(self):
        """
        Inicjalizuje mapę Folium z obszarem pożaru i znacznikami osób,
        a następnie ładuje ją do QWebEngineView.
        """
        self._render_map_with_current_style()

    def _render_map_with_current_style(self):
        """
        Renderuje mapę Folium z aktualnie wybranym stylem.
        """
        style_config = self.map_styles[self.current_style_name]
        self.m = folium.Map(
            location=fire_coords,
            zoom_start=16,  # Poziom przybliżenia jest stały
            tiles=style_config["tiles"],
            attr=style_config["attr"]
        )

        folium.Circle(
            location=fire_coords,
            radius=20,
            color='darkred',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup="<b>Obszar Pożaru</b><br>Wykryto pożar!"
        ).add_to(self.m)

        for person in people_points:
            folium.Marker(
                location=[person["lat"], person["lon"]],
                popup=folium.Popup(f"<b>{person['name']}</b><br>{person['info']}", max_width=200),
                tooltip=person['name'],
                icon=folium.Icon(color="green", icon="user")
            ).add_to(self.m)

        for actor in additional_actors:
            folium.Marker(
                location=[actor["lat"], actor["lon"]],
                popup=folium.Popup(f"<b>{actor['name']}</b><br>{actor['info']}", max_width=200),
                tooltip=actor['name'],
                icon=folium.Icon(color=actor["color"], icon=actor["icon"])
            ).add_to(self.m)

        data = self.m._repr_html_()
        self.web_view.setHtml(data)

    def update_map_style(self, style_name: str):
        """
        Zmienia styl mapy i ponownie ją renderuje.
        """
        if style_name in self.map_styles:
            self.current_style_name = style_name
            self._render_map_with_current_style()
        else:
            print(f"Nieznany styl mapy: {style_name}")

