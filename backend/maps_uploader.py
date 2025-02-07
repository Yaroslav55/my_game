import math

import requests
import os

from backend.debug_logger import Logger


class OsmLoader:
    url = "https://a.tile.openstreetmap.org"
    headers = {
        "User-Agent": "Mozilla"
    }
    def __init__(self):
        pass

    @staticmethod
    def lat_lon_to_tile(lat_deg, lon_deg, zoom):
        # Convert latitude and longitude to tile coordinates
        lat_rad = math.radians(lat_deg)
        n = 1 << zoom
        x_tile = int((lon_deg + 180.0) / 360.0 * n)
        y_tile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)

        return x_tile, y_tile

    @classmethod
    def get_tile(cls, lat: float, lon: float, zoom: int):
        x, y, = cls.lat_lon_to_tile(lat, lon, zoom)
        return cls.download_osm_tile(cls, x, y, zoom)

    def download_osm_tile(self, x: int, y: int, zoom: int, tile_folder: str = "tiles"):
        # Create the folder if it doesn't exist
        if not os.path.exists(tile_folder):
            os.makedirs(tile_folder)


        # URL for OSM tile server
        tile_url = f"{self.url}/{zoom}/{x}/{y}.png"
        Logger.info(tile_url)

        # Send the GET request to download the tile
        response = requests.get(tile_url, headers=self.headers)
        if response.status_code == 200:
            # Save the tile image as a PNG file
            tile_path = os.path.join(tile_folder, "test_tail.png")
            with open(tile_path, "wb") as tile_file:
                tile_file.write(response.content)
            Logger.info(f"Tile saved as {tile_path}")
            return 1

        Logger.warn(f"Error downloading tile: {response.status_code}")
        return -1


_lat = 50.485845
_lon = 30.464745
_zoom = 17

OsmLoader.get_tile(_lat, _lon, _zoom)
