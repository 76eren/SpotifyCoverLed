import os
from colorsys import rgb_to_hsv
import requests
from colorthief import ColorThief

class ColourExtract:

    @staticmethod
    def is_vibrant(color):
        r, g, b = color
        h, s, v = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        return s > 0.2 and v > 0.3  # Thresholds to avoid grayscale tones

    @staticmethod
    def get_colour(image_url):
        ColourExtract.download_image(image_url)
        image_path = os.path.join(os.path.dirname(__file__), "images", "image.jpg")
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=5, quality=1)
        ColourExtract.remove_image()

        # Prioritize vibrant colors
        vibrant_colors = [color for color in palette if ColourExtract.is_vibrant(color)]

        return vibrant_colors[0] if vibrant_colors else palette[0]  # Prefer vibrant color if available

    @staticmethod
    def download_image(url):
        response = requests.get(url)
        with open(os.path.join(os.path.dirname(__file__), "images", "image.jpg"), "wb") as file:
            # Save image as image.jpg
            file.write(response.content)


    @staticmethod
    def remove_image():
        os.remove(os.path.join(os.path.dirname(__file__), "images", "image.jpg"))
