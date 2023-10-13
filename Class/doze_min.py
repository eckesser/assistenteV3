import json
import time
import random
import pyautogui
from threading import Thread

class UltiKeyProcessor12:

    def __init__(self, json_path="Json/ulti.json"):
        with open(json_path, 'r') as f:
            self.key_data = json.load(f)

    def press_key(self, key_combination):
        """Simulate simultaneous key press using pyautogui."""
        try:
            for key in key_combination:
                pyautogui.keyDown(key)
            for key in reversed(key_combination):
                pyautogui.keyUp(key)
            print(f"Keys {key_combination} pressed simultaneously.")
        except Exception as e:
            print(f"Error pressing keys {key_combination}: {e}")

    def process_key_12(self, key):
        """Continuously process a key with a delay."""
        while True:
            key_combination = self.key_data.get(key)
            if key_combination:
                self.press_key(key_combination)
                # Calculate random time in the last 10% of 720 seconds
                wait_time = random.uniform(0.9 * 720, 720)
                time.sleep(wait_time)
            else:
                time.sleep(random.uniform(0.4, 1))  # intervalo entre as verificações

    def run(self):
        keys_to_process_12 = ['necro_mage_key', 'weapon_poison_key']
        for key in keys_to_process_12:
            thread = Thread(target=self.process_key_12, args=(key,))
            thread.start()
            #time.sleep(random.uniform(0.5, 1)) # Aguarda um random antes de iniciar a próxima thread
            time.sleep(0.5)
