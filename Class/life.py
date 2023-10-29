import sys
import os

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import OCR 

tentativas_falhas = 0

def getLife():
    global tentativas_falhas
    ocr_processor = OCR()

    coords_life = ocr_processor.data['coordinates']['coords_life']
    if coords_life is None:
        print("Barra de vida não encontrada. (NAO MONITORANDO)")
        return None
    percent = ocr_processor.ocr_from_coords(coords_life)
    if percent is None or not isinstance(percent, (int, float)):
        tentativas_falhas += 1
        if tentativas_falhas >= 10:
            print("Recalculando VIDA.")
            from Config.coords import ImageFinder 
            finder = ImageFinder()
            finder.main()
            tentativas_falhas = 0 
        return 100
    tentativas_falhas = 0
    return percent
