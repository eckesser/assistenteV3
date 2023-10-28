import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from OCR.ocr_module import OCR

# Contador global de tentativas falhas
tentativas_falhas = 0

def getPet_life():
    global tentativas_falhas  # Usar a variável global
    ocr_processor = OCR()
    
    coords_pet_life = ocr_processor.data['coordinates']['coords_pet_life']

    # Verifica se coords_pet_life é None e retorna None se for o caso
    if coords_pet_life is None:
        print("Barra de vida do pet não encontrada. (NAO MONITORANDO)")
        return None

    percent = ocr_processor.ocr_from_coords(coords_pet_life)

    # Verifica se percent é None ou não numérico e trata a situação
    if percent is None or not isinstance(percent, (int, float)):
        tentativas_falhas += 1
        #print(f"Barra de vida do pet nao encontrada. (Tentativa {tentativas_falhas})")
        if tentativas_falhas >= 10:
            print("Recalculando.")
            from Config.coords import ImageFinder 
            finder = ImageFinder()
            finder.main()
            tentativas_falhas = 0  # Resetar contador de tentativas
        return 100  # Retorne um valor padrão (por exemplo, 100)

    # Se percentual válido for encontrado, resetar o contador de tentativas falhas
    tentativas_falhas = 0

    return percent
