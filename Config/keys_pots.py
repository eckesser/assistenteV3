import os
import json
import sys

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from Class.shared import clear_console
from Main.main_menu import main_menu

class KeyManagerPot:
    
    def __init__(self):
        self.label_mapping = {
            'ovl_key': 'Overload',
            'anti_fire_key': 'Anti-fire',
            'anti_poison_key': 'Anti-Poison',
            'aggression_key': 'Aggression potion',
            'weapon_poison_key': 'Weapon poison',
            'necro_mage_key': 'Darkness ou Animate Dead',
            'elven_shard_key': 'Anciente elven ritual shard'
        }
        self.reset_json()

    def reset_json(self):
        """Reset the JSON file to its default structure."""
        json_path = os.path.join("Json", "ulti.json")
        
        if os.path.exists(json_path):
            os.remove(json_path)
        
        default_structure = {
            "ovl_key": None,
            "anti_fire_key":  None,
            "anti_poison_key": None,
            "aggression_key": None,
            "weapon_poison_key": None,
            "necro_mage_key": None,
            "elven_shard_key": None
        }
        self.save_to_json(default_structure, json_path)
    def parse_key_combination(self, input_string):
        keys = input_string.lower().split('+')
        return [key.strip() for key in keys]

    def get_label(self, key):
        return self.label_mapping.get(key, key)

    def get_key_for(self, label):
        key_input = input(f"Defina a combinação de teclas para {self.get_label(label)} (Exemplo: alt+2, coloque o +) (pressione Enter para pular): ")
        if not key_input.strip():
            return None
        return self.parse_key_combination(key_input)

    def choose_label_to_edit(self):
        while True:
            print("\nEscolha qual configuração você deseja editar:")
            for idx, key in enumerate(self.label_mapping, start=1):
                print(f"{idx}. {self.get_label(key)}")
            print(f"{len(self.label_mapping) + 1}. Salvar e sair")

            choice = input("\nDigite a opção desejada: ")
            clear_console()
            try:
                choice = int(choice)
                if 1 <= choice <= len(self.label_mapping):
                    return list(self.label_mapping.keys())[choice - 1]
                elif choice == len(self.label_mapping) + 1:
                    return None
            except ValueError:
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

        data = self.load_existing_data(os.path.join("Json", "ulti.json"))
        while True:
            selected_key = self.choose_label_to_edit()
            if selected_key is None:
                break
            user_input = self.get_key_for(selected_key)
            data[selected_key] = user_input
        for key, value in data.items():
            if value is None:
                data[key] = None

        self.save_to_json(data, os.path.join("Json", "ulti.json"))
        main_menu()

def execute_manager():
    manager = KeyManagerPot()
    manager.run()
