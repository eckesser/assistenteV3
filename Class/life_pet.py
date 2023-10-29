import sys
import os

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import OCR

tentativas_falhas = 0

def getPet_life():
    global tentativas_falhas
    ocr_processor = OCR()
    
    coords_pet_life = ocr_processor.data['coordinates']['coords_pet_life']
    if coords_pet_life is None:
        print("Barra de vida do pet não encontrada. (NAO MONITORANDO)")
        return None
    percent = ocr_processor.ocr_from_coords(coords_pet_life)
    if percent is None or not isinstance(percent, (int, float)):
        tentativas_falhas += 1
        if tentativas_falhas >= 10:
            print("Recalculando PET.")
            from Config.coords import ImageFinder 
            finder = ImageFinder()
            finder.main()
            tentativas_falhas = 0
        return 100 
    tentativas_falhas = 0
    return percent
