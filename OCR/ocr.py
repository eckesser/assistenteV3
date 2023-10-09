import json
import time
import cv2
import numpy as np
from PIL import ImageGrab
import easyocr

def ocr_from_coords(coords, reader):
    """
    Captura a região da tela especificada pelas coordenadas e realiza o OCR usando easyocr.
    """
    x1, y1, x2, y2 = map(int, coords.split(", "))
    screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_RGB2BGR)
    results = reader.readtext(screenshot)
    texts = [result[1] for result in results]
    return ' '.join(texts)

def main():
    # Inicialização do reader do easyocr
    reader = easyocr.Reader(['en'])

    # Carregando as coordenadas
    with open("Json/coords.json", "r") as file:
        data = json.load(file)
        coords_list = list(data['coordinates'].values())

    while True:
        for coords_key, coords_value in data['coordinates'].items():
            text = ocr_from_coords(coords_value, reader)
            print(f"Texto reconhecido nas coordenadas {coords_key}: {text}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
