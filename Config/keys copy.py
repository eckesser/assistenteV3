import json
import os

class KeyManager:
    
    def __init__(self):
        self.label_mapping = {
            'life_key': 'Life',
            'prayer_key': 'Prayer',
            'pet_life_key': 'Pet Life'
        }

    def get_label(self, key):
        """Return the user-friendly label for the key."""
        return self.label_mapping.get(key, key)

    def get_keys_for(self, label, max_keys):
        """Get keys from user for a specific label."""
        keys = []
        while len(keys) < max_keys:
            key = input(f"Digite uma tecla para {self.get_label(label)} ({len(keys)+1}/{max_keys}): ")
            if key:
                keys.append(key)
            else:
                break
        return keys

    def get_number_of_keys(self, label, max_keys):
        """Get the number of keys the user wants to assign."""
        while True:
            try:
                print(f"\nCaso nao deseje mapear a {self.get_label(label)}, aperte ENTER!")
                print("\n")
                num = input(f"Quantas teclas você deseja designar para {self.get_label(label)} (máximo {max_keys}): ")
                if not num:  # If user input is empty
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
            print("\nEscolha qual item você deseja editar:")
            print("1. Life")
            print("2. Prayer")
            print("3. Pet Life")
            choice = input("Digite a opção desejada: ")
            if choice == "1":
                return 'life_key', 3
            elif choice == "2":
                return 'prayer_key', 1
            elif choice == "3":
                return 'pet_life_key', 2
            else:
                print("Opção inválida. Tente novamente.")

    def save_to_json(self, data, path):
        """Save data to a JSON file."""
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def run(self):
        if not os.path.exists("Json"):
            os.mkdir("Json")

        data = {}
        label, max_keys = self.choose_label_to_edit()
        num_keys = self.get_number_of_keys(label, max_keys)
        data[label] = self.get_keys_for(label, num_keys) if num_keys else None
        self.save_to_json(data, os.path.join("Json", "teclas.json"))

manager = KeyManager()
manager.run()
