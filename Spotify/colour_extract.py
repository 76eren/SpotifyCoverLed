from colorthief import ColorThief
import requests
import os
class ColourExtract:

    @staticmethod
    def get_colour(image_url):
        # TODO: Update some of this logic
        ColourExtract.download_image(image_url)
        color_thief = ColorThief(os.path.join(os.path.dirname(__file__), "images", "image.jpg"))
        dominant_colour = color_thief.get_color(quality=1)
        ColourExtract.remove_image()
        return dominant_colour

    @staticmethod
    def download_image(url):
        response = requests.get(url)
        with open(os.path.join(os.path.dirname(__file__), "images", "image.jpg"), "wb") as file:
            # Save image as image.jpg
            file.write(response.content)


    @staticmethod
    def remove_image():
        os.remove(os.path.join(os.path.dirname(__file__), "images", "image.jpg"))
