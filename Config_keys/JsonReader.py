import json
from time360 import Time360
from time720 import Time720

class JsonReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_and_execute(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                if value:  # Checagem modificada para valores "falsy"
                    if key in ["ovl_key", "anti_fire_key", "Anti-fire", "anti_poison_key", "Anti-Poison", "aggression_key", "Aggression potion"]:
                        Time360().run(key)
                    elif key in ["weapon_poison_key", "necro_mage_key"]:
                        Time720().run(key)

# Usando a classe
reader = JsonReader("Json/ulti.json")
reader.read_and_execute()
