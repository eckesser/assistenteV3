import json
import os
import sys

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from Config_keys.time360 import Time360
from Config_keys.time720 import Time720
from Config_keys.first_press import FirstPress

class JsonReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_and_execute(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            
            # Primeira ativação das teclas com FirstPress
            first_press = FirstPress(data)
            first_press.run()

            # Iniciar a contagem com Time360 ou Time720
            for key, value in data.items():
                if value:  # Checagem modificada para valores "falsy"
                    if key in ["ovl_key", "anti_fire_key", "Anti-fire", "anti_poison_key", "Anti-Poison", "aggression_key", "Aggression potion"]:
                        Time360().run(key)
                    elif key in ["weapon_poison_key", "necro_mage_key"]:
                        Time720().run(key)

# Usando a classe
reader = JsonReader("Json/ulti.json")
reader.read_and_execute()
