import json
import time
import cv2
import numpy as np
from PIL import ImageGrab
import easyocr

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        
        # Loading the coordinates
        with open("Json/coords.json", "r") as file:
            self.data = json.load(file)
            self.coords_list = list(self.data['coordinates'].values())
        
    def ocr_from_coords(self, coords):
        """
        Captura a região da tela especificada pelas coordenadas e realiza o OCR usando easyocr.
        """
        x1, y1, x2, y2 = map(int, coords.split(", "))
        screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_RGB2BGR)
        results = self.reader.readtext(screenshot)
        texts = [result[1] for result in results]
        return ' '.join(texts)

    @staticmethod
    def div(x):
        try:
            if x:
                valores_separados = str(x).split("/")
                return round((int(valores_separados[0]) / int(valores_separados[1])) * 100)
        except ValueError as e:
            # Você pode adicionar um log aqui se necessário
            pass

    def process_ocr(self):
        prayer_x = 0
        hp_x = 0
        pet_x = 0
        
        while True:
            for coords_key, coords_value in self.data['coordinates'].items():
                text = self.ocr_from_coords(coords_value)
                if(coords_key == "coords_life" ):
                    hp_x = text
                if(coords_key == "coords_pray"):
                    prayer_x = text
                if(coords_key == "coords_pet_life"):
                    pet_x = text

                print(self.div(hp_x))
                print(self.div(prayer_x))
                print(self.div(pet_x))

            time.sleep(1)

# Use example:
ocr_processor = OCR()
ocr_processor.process_ocr()
