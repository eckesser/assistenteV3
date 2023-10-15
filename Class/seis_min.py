import json
import time
import random
import pyautogui
from threading import Thread

class UltiKeyProcessor6:

    def __init__(self, ovl=None, anti_fire=None, anti_poison=None, aggression=None):
        self.key_data = {
            'ovl': ovl,
            'anti_fire': anti_fire,
            'anti_poison': anti_poison,
            'aggression': aggression
        }

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

    def process_key_6(self, key):
        """Continuously process a key with a delay."""
        while True:
            key_combination = self.key_data.get(key)
            if key_combination:
                self.press_key(key_combination)
                # Calculate random time in the last 10% of 360 seconds
                wait_time = random.uniform(0.9 * 360, 360)
                time.sleep(wait_time)
            else:
                time.sleep(random.uniform(0.4, 1))  # intervalo entre as verificações

    def run(self):
        keys_to_process_6 = ['ovl', 'anti_fire', 'anti_poison', 'aggression']
        for key in keys_to_process_6:
            thread = Thread(target=self.process_key_6, args=(key,))
            thread.start()
            time.sleep(0.5)  # Aguarda um tempo antes de iniciar a próxima thread
