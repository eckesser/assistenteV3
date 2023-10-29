import json
import os

from Class.shared import clear_console
from Main.main_menu import main_menu

class KeyManager:
    
    def __init__(self):
        self.label_mapping = {
            'life_key': 'Life',
            'prayer_key': 'Prayer',
            'pet_life_key': 'Pet Life'
        }

    def get_label(self, key):
        return self.label_mapping.get(key, key)

    def get_keys_for(self, label, max_keys):
        keys = []
        while len(keys) < max_keys:
            key = input(f"Digite uma tecla para {self.get_label(label)} ({len(keys)+1}/{max_keys}): ")
            if key:
                keys.append(key)
            else:
                break
        return keys

    def get_number_of_keys(self, label, max_keys):
        while True:
            try:
                print(f"\nCaso nao deseje mapear a {self.get_label(label)}, aperte ENTER!")
                print("-------------------------")
                print("\n")
                num = input(f"Quantas teclas você deseja designar para {self.get_label(label)} (máximo {max_keys}): ")
                if not num:
                    return None
                num = int(num)
                if 0 < num <= max_keys:
                    return num
                else:
                    print(f"Por favor, insira um número entre 1 e {max_keys}.")
            except ValueError:
                print("Por favor, insira um número válido.")

    def choose_label_to_edit(self):
        while True:
            print("\nEscolha qual configuracao você deseja editar:")
            print("-------------------------")
            print("\n")
            print("1. Life")
            print("2. Prayer")
            print("3. Pet Life")
            print("4. Voltar")
            print("\n")
            choice = input("Digite a opção desejada: ")
            if choice == "1":
                clear_console() 
                return 'life_key', 3
            elif choice == "2":
                clear_console() 
                return 'prayer_key', 1
            elif choice == "3":
                clear_console() 
                return 'pet_life_key', 2
            elif choice == "4":
                clear_console() 
                return main_menu()
            else:
                print("Opção inválida. Tente novamente.")

    def load_existing_data(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def save_to_json(self, data, path):
        existing_data = self.load_existing_data(path)
        existing_data.update(data)
        with open(path, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def run(self):
        if not os.path.exists("Json"):
            os.mkdir("Json")
        label, max_keys = self.choose_label_to_edit()
        num_keys = self.get_number_of_keys(label, max_keys)
        data_to_save = {label: self.get_keys_for(label, num_keys) if num_keys else None}
        self.save_to_json(data_to_save, os.path.join("Json", "teclas.json"))

manager = KeyManager()
manager.run()
