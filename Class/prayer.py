import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import ocr

def getPrayer():
    ocr_processor = ocr()

    coords_prayer = ocr_processor.data['coordinates']['coords_pray']
    percent = ocr_processor.ocr_from_coords(coords_prayer)
    return percent

while True:
    
    print(getPrayer())
