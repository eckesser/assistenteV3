import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import OCR

def getPrayer():
    ocr_processor = OCR()  # Alterando 'ocr' para 'OCR'

    coords_pray = ocr_processor.data['coordinates']['coords_pray']

    # Verifica se coords_pet_life é None e retorna None se for o caso
    if coords_pray is None:
        print("Barra de Prayer não encontrada.(NAO MONITORANDO)")
        return None

    percent = ocr_processor.ocr_from_coords(coords_pray)

    # Verifica se percent é None ou não numérico e trata a situação
    if percent is None or not isinstance(percent, (int, float)):
        # Aqui você pode adicionar um log para registrar quando isso acontece
        print(f"Barra de prayer do nao encontrada.")
        return 100  # Retorne um valor padrão (por exemplo, 100) ou qualquer valor que faça sentido para sua aplicação

    return percent