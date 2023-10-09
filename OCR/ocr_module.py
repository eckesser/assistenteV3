import json
import cv2
import numpy as np
from PIL import ImageGrab
import easyocr

# Inicializando o easyocr.Reader globalmente
READER = None

def get_reader():
    global READER
    if READER is None:
        READER = easyocr.Reader(['en'])
    return READER

class ocr:
    def __init__(self):
        self.reader = get_reader()
        
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
        result = ' '.join(texts)

        try:
            if result:
                valores_separados = str(result).split("/")
                return round((int(valores_separados[0]) / int(valores_separados[1])) * 100)
        except ValueError as e:
            # Você pode adicionar um log aqui se necessário
            pass
