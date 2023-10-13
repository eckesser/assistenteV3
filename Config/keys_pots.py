import os
import json

class KeyManagerPot:
    
    def __init__(self):
        self.label_mapping = {
            'ovl_key': 'Overload',
            'anti_fire_key': 'Anti-fire',
            'anti_poison_key': 'Anti-Poison',
            'weapon_poison_key': 'Weapon poison',
            'necro_mage_key': 'Darkness ou Animate Dead'
        }

    def parse_key_combination(self, input_string):
        keys = input_string.lower().split('+')
        return [key.strip() for key in keys]

    def get_label(self, key):
        """Return the user-friendly label for the key."""
        return self.label_mapping.get(key, key)

    def get_key_for(self, label):
        """Get key combination from user for a specific label."""
        key_input = input(f"Digite a de tecla para {self.get_label(label)} (Caso use exemplo: alt+2, coloque o + para combinacao) (pressione Enter para pular): ")
        if not key_input.strip():
            return None
        return self.parse_key_combination(key_input)

    def save_to_json(self, data, path):
        """Save data to a JSON file."""
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def run(self):
        if not os.path.exists("Json"):
            os.mkdir("Json")
        
        data = {}
        
        for key, label in self.label_mapping.items():
            data[key] = self.get_key_for(key)
        
        self.save_to_json(data, os.path.join("Json", "ulti.json"))

manager = KeyManagerPot()
manager.run()
