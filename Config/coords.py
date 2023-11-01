import pyautogui
import json
import os
from PIL import Image
import pytesseract

class ImageFinder:
    
    def __init__(self):
        self.tesseract_cmd = '/usr/bin/tesseract'  # Ajuste o caminho para o Tesseract se necessário

    def capture_image_from_coords(self, coords, file_name):
        if coords:
            left, top, right, bottom = map(int, coords.split(","))
            image = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
            image_path = os.path.join("img_return", file_name)
            image.save(image_path)

    def get_reference_characters_from_image(self, path):
        image = Image.open(path)
        text = pytesseract.image_to_string(image, lang='eng')
        chars = ''.join(text)
        return set(chars)

    def find_text_coords(self, region):
        reference_chars = self.get_reference_characters_from_image("Imagem/fonte_ocr.png")
        expanded_region = (
            region[0],
            region[1],
            region[2],
            region[3],
        )
        screenshot = pyautogui.screenshot(region=expanded_region)
        text = pytesseract.image_to_string(screenshot, lang='eng')
        if all(char in reference_chars for char in text):
            text_location = pyautogui.locateOnScreen(screenshot, region=expanded_region)
            if text_location:
                return text, f"{int(text_location.left)}, {int(text_location.top)}, {int(text_location.left + text_location.width)}, {int(text_location.top + text_location.height)}"
        return None, None

    def find_image_hp_coords(self, image_path):
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location:
            adjusted_coords = (
                location.left + 0,
                location.top + 0,
                location.left + 0,
                location.top + 0
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
