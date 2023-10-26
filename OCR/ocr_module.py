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

class OCR:
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
        screenshot_np = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
        
        # Verificando se a captura da tela foi bem-sucedida
        if screenshot_np.size == 0:
            print("Erro na captura da tela.")
            return 100  # Retornando um valor padrão
        
        screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        results = self.reader.readtext(screenshot)
        texts = [result[1] for result in results]
        result = ' '.join(texts)

        try:
            if result:
                valores_separados = str(result).split("/")
                num1 = int(valores_separados[0])
                num2 = int(valores_separados[1])
                
                # Se num1 for maior que num2, definimos num1 como igual a num2
                if num1 >= num2:
                    num1 = num2
                
                percent = round((num1 / num2) * 100)
                
                print(f"{num1} / {num2}")
                # Se percent for maior que 100, definimos como 100
                return min(100, percent)
        except ValueError as e:
            # Você pode adicionar um log aqui se necessário
            return 100
