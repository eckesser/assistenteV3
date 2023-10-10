import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import ocr

def getPet_life():
    ocr_processor = ocr()

    coords_pet_life = ocr_processor.data['coordinates']['coords_pet_life']
    percent = ocr_processor.ocr_from_coords(coords_pet_life)
    print(percent)
    #return percent