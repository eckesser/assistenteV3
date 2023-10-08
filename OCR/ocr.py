import json
import time
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os  # Importe a biblioteca os para trabalhar com caminhos de arquivo

# Configurando o pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Caminho para o Tesseract no seu sistema

def capture_and_ocr(coords, key):
    # Convertendo a string de coordenadas para uma tupla de inteiros
    x, y, width, height = map(int, coords.split(', '))

    # Capturando a região da tela
    screenshot = pyautogui.screenshot(region=(x, y, width-x, height-y))

    # Salvando a imagem temporariamente para inspeção
    image_path = os.path.join('Ocr_img', f"{key}_capture.png")  # Caminho para a pasta Ocr_img
    screenshot.save(image_path)

    # Processamento da imagem para melhorar a precisão do OCR
    img = screenshot.convert('L')  # Convertendo para escala de cinza
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Convertendo para preto e branco (binário)
    img = img.filter(ImageFilter.SHARPEN)  # Aplicando um filtro de nitidez

    # OCR com psm 6
    text = pytesseract.image_to_string(img, config='--psm 6')

    # Filtrando a saída
    filtered_text = ''.join(filter(lambda x: x in '0123456789/', text))
    
    return filtered_text

def main():
    # Crie a pasta Ocr_img se ela não existir
    if not os.path.exists('Ocr_img'):
        os.makedirs('Ocr_img')

    # Carregando as coordenadas do arquivo
    with open('Json/coords.json', 'r') as f:
        data = json.load(f)

    while True:
        for key, coords in data['coordinates'].items():
            print(f"{key}: {capture_and_ocr(coords, key)}")  # Passando 'key' como argumento adicional
        time.sleep(1)

if __name__ == "__main__":
    main()
