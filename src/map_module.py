import folium
from folium.plugins import HeatMap
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np

from src.static_data import people_points, fire_coords, ActorType, additional_actors


class MapHandler:
    """
    Klasa odpowiedzialna za inicjalizację i zarządzanie mapą Folium
    wyświetlaną w QWebEngineView.
    """

    def __init__(self, web_view: QWebEngineView):
        self.web_view = web_view
        self.m = None
        self.heatmap_enabled = False
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
        
        self._add_base_layers()
        
        # Add heatmap if enabled
        if self.heatmap_enabled:
            self._add_heatmap()
            
        self._update_map_display()

    def _add_base_layers(self):
        """Add base map layers (fire area, markers)"""

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
                icon=folium.CustomIcon(actor["icon"])
            ).add_to(self.m)

    def _add_heatmap(self):
        """Add heatmap layer to the current map"""
        heatmap_data = self._create_grid_heatmap_data()
        HeatMap(
            heatmap_data,
            min_opacity=0.3,  # Higher minimum opacity
            max_zoom=20,
            radius=35,  # Larger radius for smoother coverage
            blur=20,    # More blur for gradient effect
            gradient={
                0.0: 'rgba(0, 255, 0, 0.0)',      # Transparent (no blue)
                0.2: 'rgba(100, 255, 100, 0.4)',  # Light green
                0.4: 'rgba(200, 255, 0, 0.6)',    # Yellow-green
                0.6: 'rgba(255, 255, 0, 0.8)',    # Yellow
                0.7: 'rgba(255, 200, 0, 0.85)',   # Orange
                0.8: 'rgba(255, 100, 0, 0.9)',    # Red-orange
                1.0: 'rgba(255, 0, 0, 0.95)'      # Red
            }
        ).add_to(self.m)

    def _create_grid_heatmap_data(self):
        """Create a grid-based heatmap covering the entire area with heat concentrated around points"""
        # Define the area bounds
        center_lat, center_lon = fire_coords
        lat_range = 0.002  # ~200m coverage
        lon_range = 0.003  # ~300m coverage

        # Create grid
        grid_size = 20  # 20x20 grid
        lat_step = lat_range / grid_size
        lon_step = lon_range / grid_size

        heatmap_data = []

        # Generate grid points
        for i in range(grid_size + 1):
            for j in range(grid_size + 1):
                grid_lat = center_lat - lat_range/2 + i * lat_step
                grid_lon = center_lon - lon_range/2 + j * lon_step

                # No base temperature - only heat around actual points
                base_temp = 0.0

                # Calculate distance-based heat from fire center
                fire_distance = np.sqrt((grid_lat - center_lat)**2 + (grid_lon - center_lon)**2)
                fire_heat = max(0, 0.8 * np.exp(-fire_distance * 8000))  # Exponential decay

                # Calculate heat from people points
                people_heat = 0
                for person in people_points:
                    person_distance = np.sqrt((grid_lat - person["lat"])**2 + (grid_lon - person["lon"])**2)
                    people_heat += max(0, 0.6 * np.exp(-person_distance * 12000))

                # Calculate heat from emergency actors
                actor_heat = 0
                for actor in additional_actors:
                    actor_distance = np.sqrt((grid_lat - actor["lat"])**2 + (grid_lon - actor["lon"])**2)
                    if actor["type"] in [ActorType.FIREFIGHTER, ActorType.DOCTOR]:
                        actor_heat += max(0, 0.4 * np.exp(-actor_distance * 10000))
                    else:
                        actor_heat += max(0, 0.2 * np.exp(-actor_distance * 15000))

                # Combine all heat sources
                total_heat = min(1.0, base_temp + fire_heat + people_heat + actor_heat)

                # Only add points with meaningful heat (higher threshold)
                if total_heat > 0.15:
                    heatmap_data.append([grid_lat, grid_lon, total_heat])

        # Add concentrated points around key locations for better visualization
        self._add_concentrated_points(heatmap_data)

        return heatmap_data

    def _add_concentrated_points(self, heatmap_data):
        """Add additional concentrated points around key locations for smoother gradients"""
        # Fire center concentration
        fire_lat, fire_lon = fire_coords
        for radius_factor in [0.5, 1.0, 1.5, 2.0]:
            for angle in range(0, 360, 30):  # Every 30 degrees
                radius = 0.0001 * radius_factor
                lat_offset = radius * np.cos(np.radians(angle))
                lon_offset = radius * np.sin(np.radians(angle))
                heat_intensity = max(0.2, 0.9 - radius_factor * 0.2)  # Higher minimum
                heatmap_data.append([
                    fire_lat + lat_offset,
                    fire_lon + lon_offset,
                    heat_intensity
                ])

        # People concentration
        for person in people_points:
            for radius_factor in [0.3, 0.6, 0.9]:
                for angle in range(0, 360, 45):  # Every 45 degrees
                    radius = 0.00008 * radius_factor
                    lat_offset = radius * np.cos(np.radians(angle))
                    lon_offset = radius * np.sin(np.radians(angle))
                    heat_intensity = max(0.2, 0.7 - radius_factor * 0.15)  # Higher minimum
                    heatmap_data.append([
                        person["lat"] + lat_offset,
                        person["lon"] + lon_offset,
                        heat_intensity
                    ])

    def toggle_heatmap(self, enabled):
        """Toggle heatmap visualization"""
        self.heatmap_enabled = enabled
        # Re-render the map with current style and heatmap state
        self._render_map_with_current_style()

    def _update_map_display(self):
        """Update the web view with current map state"""
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

