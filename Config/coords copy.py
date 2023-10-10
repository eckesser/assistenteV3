import pyautogui
import json
import os
from PIL import Image
import pytesseract
from rscheck import is_runescape_running  # Importe a função

class ImageFinder:
    
    def __init__(self):
        pass

    def find_text_coords(self, region):
        expanded_region = (
            region[0] - 5,
            region[1] - 5,
            region[2] + 10,
            region[3] + 10
        )
        screenshot = pyautogui.screenshot(region=expanded_region)
        text = pytesseract.image_to_string(screenshot, config='--psm 6').strip()
        if all(char in "0123456789%/,." for char in text):
            text_location = pyautogui.locateOnScreen(screenshot, region=expanded_region)
            if text_location:
                return text, f"{int(text_location.left)}, {int(text_location.top)}, {int(text_location.left + text_location.width)}, {int(text_location.top + text_location.height)}"
        return None, None

    def find_image_coords(self, image_path, save_name):
        location = pyautogui.locateOnScreen(image_path, confidence=0.5)
        if location:
            text, text_coords = self.find_text_coords(location)
            if text and text_coords:
                x1, y1, x2, y2 = map(int, text_coords.split(','))
                x1 -= 5
                y1 -= 5
                x2 += 5
                y2 += 5
            
            coords_str = f"{int(location.left) - 5}, {int(location.top) - 5}, {int(location.left + location.width) + 5}, {int(location.top + location.height) + 5}"
            if text_coords:
                coords_str += f""
            return coords_str
        else:
            return None

    def main(self):
        if is_runescape_running():  # Verifique se o RuneScape está em execução
            coords_life = self.find_image_coords('Imagem/hp.png', 'hp')
            coords_pray = self.find_image_coords('Imagem/prayer.png', 'prayer')
            coords_pet_life = self.find_image_coords('Imagem/summon_life.png', 'pet_life')

            data = {
                "coordinates": {
                    "coords_life": coords_life,
                    "coords_pray": coords_pray,
                    "coords_pet_life": coords_pet_life
                }
            }

            if not os.path.exists('json'):
                os.makedirs('json')

            with open('Json/coords.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print("RuneScape não está em execução.")

finder = ImageFinder()
finder.main()
