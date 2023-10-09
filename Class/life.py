import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import ocr

def getLife():
    ocr_processor = ocr()

    coords_life = ocr_processor.data['coordinates']['coords_life']
    percent = ocr_processor.ocr_from_coords(coords_life)
    return percent

while True:
    
    print(getLife())
