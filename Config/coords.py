import pyautogui
import json
import os
from PIL import Image
import pytesseract
from Config.rscheck import is_runescape_running
#from rscheck import is_runescape_running


class ImageFinder:
    
    def __init__(self):
        pass

    def capture_image_from_coords(self, coords, file_name):
        if coords:
            left, top, right, bottom = map(int, coords.split(","))
            image = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
            image_path = os.path.join("img_return", file_name)
            image.save(image_path)

    def find_text_coords(self, region):
        expanded_region = (
            region[0],
            region[1],
            region[2],
            region[3],
        )
        screenshot = pyautogui.screenshot(region=expanded_region)
        text = pytesseract.image_to_string(screenshot, config='--psm 6').strip()
        if all(char in "0123456789/" for char in text):
            text_location = pyautogui.locateOnScreen(screenshot, region=expanded_region)
            if text_location:
                return text, f"{int(text_location.left)}, {int(text_location.top)}, {int(text_location.left + text_location.width)}, {int(text_location.top + text_location.height)}"
        return None, None

    def find_image_hp_coords(self, image_path):
        location = pyautogui.locateOnScreen(image_path, confidence=0.7)
        if location:
            adjusted_coords = (
                location.left + 23,
                location.top + 0,
                location.left + 114,
                location.top + 16
            )
            return f"{adjusted_coords[0]}, {adjusted_coords[1]}, {adjusted_coords[2]}, {adjusted_coords[3]}"
        else:
            return None
        
    def find_image_prayer_coords(self, image_path):
        location = pyautogui.locateOnScreen(image_path, confidence=0.9)
        if location:
            adjusted_coords = (
                location.left + 22,
                location.top + -2,
                location.left + 80,
                location.top + 14
            )
            return f"{adjusted_coords[0]}, {adjusted_coords[1]}, {adjusted_coords[2]}, {adjusted_coords[3]}"
        else:
            return None

    def find_image_pet_coords(self, image_path):
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location:
            adjusted_coords = (
                location.left + 18,
                location.top + 0,
                location.left + 155,
                location.top + 20
            )
            return f"{adjusted_coords[0]}, {adjusted_coords[1]}, {adjusted_coords[2]}, {adjusted_coords[3]}"
        else:
            return None

    def main(self):
        if is_runescape_running():
            coords_life = self.find_image_hp_coords('Imagem/cropped_hp.png')
            coords_pray = self.find_image_prayer_coords('Imagem/cropped_prayer.png')
            coords_pet_life = self.find_image_pet_coords('Imagem/cropped_summon_life.png')

            data = {
                "coordinates": {
                    "coords_life": coords_life,
                    "coords_pray": coords_pray,
                    "coords_pet_life": coords_pet_life
                }
            }

            if not os.path.exists('img_return'):
                os.makedirs('img_return')
            
            self.capture_image_from_coords(coords_life, "life_image.png")
            self.capture_image_from_coords(coords_pray, "pray_image.png")
            self.capture_image_from_coords(coords_pet_life, "pet_life_image.png")

            if not os.path.exists('Json'):
                os.makedirs('Json')

            with open('Json/coords.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            print("RuneScape is not running.")

finder = ImageFinder()
finder.main()
