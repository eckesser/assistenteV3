import json
import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract

class OCR:
    def __init__(self):
        with open("Json/coords.json", "r") as file:
            self.data = json.load(file)
            self.coords_list = list(self.data['coordinates'].values())

    def ocr_from_coords(self, coords):
        x1, y1, x2, y2 = map(int, coords.split(", "))
        screenshot_np = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
        if screenshot_np.size == 0:
            print("Erro na captura da tela.")
            return 100 
        screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        result = pytesseract.image_to_string(screenshot)
        try:
            if result:
                valores_separados = str(result).split("/")
                num1 = int(valores_separados[0])
                num2 = int(valores_separados[1])
                if num1 >= num2:
                    num1 = num2
                percent = round((num1 / num2) * 100)
                return min(100, percent)
        except ValueError as e:
            return 100
