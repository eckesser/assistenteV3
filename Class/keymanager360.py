import json
import time
import random

from .keypresser import KeyPresser

class KeyManager360:
    def __init__(self, json_path):
        self.json_path = json_path
        self.key_data = self.load_json()
    
    def load_json(self):
        with open(self.json_path, 'r') as f:
            return json.load(f)

    def press_keys(self):
        for key, value in self.key_data.items():
            if value:  # Check if the value is not null
                key_presser_instance = KeyPresser(key, self.key_data)
                key_presser_instance.press()
                time.sleep(0.5)  # Delay between variable executions
                if key in ['ovl_key', 'anti_fire_key', 'anti_poison_key', 'aggression_key']:
                    self.wait_random_time(360)

    def wait_random_time(self, base_time):
        random_delay = base_time * 0.1
        wait_time = base_time + random.uniform(-random_delay, random_delay)
        time.sleep(wait_time)

    def run(self):
        self.press_keys()
        while True:
            self.press_keys()

manager = KeyManager360('Json/ulti.json')  # Caminho atualizado para o arquivo JSON
manager.run()
