import os
import json

class JsonViewerUpdated:
    def __init__(self, directory):
        self.directory = directory
        self.file_display_names = {
            "percent_key.json": "Porcentagens",
            "teclas.json": "Teclas",
            "ulti.json": "Teclas para Porcoes e Magias"
        }
        self.mapping = {
            "percent_key.json": {
                "life_percent": "Life",
                "prayer_percent": "Prayer",
                "pet_life_percent": "Pet Life"
            },
            "teclas.json": {
                "life_key": "Life",
                "prayer_key": "Prayer",
                "pet_life_key": "Pet Life"
            },
            "ulti.json": {
                "ovl_key": "Overload potion",
                "anti_fire_key": "Antifire potion",
                "anti_poison_key": "Antipoison",
                "weapon_poison_key": "Weapon poison potion",
                "necro_mage_key": "Darkness ou Animate Dead"
            }
        }

    def display_content(self):
        # Lista dos arquivos a serem excluídos
        exclude_files = ["coords.json"]

        # Obtendo todos os arquivos JSON no diretório
        all_files = [f for f in os.listdir(self.directory) if f.endswith('.json') and f not in exclude_files]

        for file in all_files:
            with open(os.path.join(self.directory, file), 'r') as f:
                data = json.load(f)
                # Use o nome exibido do arquivo aqui
                print(f"\nConteúdo do arquivo {self.file_display_names.get(file, file)}:")
                print("\n")
                
                for original_key, values in data.items():
                    display_key = self.mapping[file].get(original_key, original_key)
                    
                    if isinstance(values, list):
                        values = ' + '.join(values)
                    elif isinstance(values, int):
                        values = f"{values}%"
                        
                    print(f"{display_key}: {values}")
                
                print("\n--------------------------")