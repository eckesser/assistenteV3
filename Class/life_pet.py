import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import OCR

def getPet_life():
    ocr_processor = OCR()
    
    coords_pet_life = ocr_processor.data['coordinates']['coords_pet_life']
    percent = ocr_processor.ocr_from_coords(coords_pet_life)

    # Verifica se percent é None ou não numérico e trata a situação
    if percent is None or not isinstance(percent, (int, float)):
        # Aqui você pode adicionar um log para registrar quando isso acontece
        print(f"Barra de vida do pet nao encontrada.")
        return 100  # Retorne um valor padrão (por exemplo, 100) ou qualquer valor que faça sentido para sua aplicação

    return percent
