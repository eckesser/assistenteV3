import sys
import os
import time
import json
from threading import Thread
import random
from time import sleep
from pyautogui import press
import keyboard

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from Config.rscheck import is_runescape_running
from Config.coords import ImageFinder
from Config.perct_key import JsonSaver
from Config.keys import KeyManager
from Class.life import getLife
from Class.prayer import getPrayer
from Class.life_pet import getPet_life

life_key = ['']
life_percent = 1
prayer_key = ['']
prayer_percent = 1
pet_life_key = ['']
pet_life_percent = 1

running = True
paused = False

class Life:
    def execute(self):
        while running:
            if not paused:
                try:
                    load_config_from_json()
                    life_value = getLife()
                    if life_value < life_percent:
                        for key in life_key:
                            press(key)
                            sleep(random.uniform(0, 0.7))
                    sleep(random.uniform(0.5, 1))
                except Exception as e:
                    print(f"Error in Life. Restarting...")
                    continue

class Prayer:
    def execute(self):
        while running:
            if not paused:
                try:
                    load_config_from_json()
                    prayer_value = getPrayer()
                    if prayer_value < prayer_percent:
                        press(prayer_key[0])
                    sleep(random.uniform(0.5, 1))
                except Exception as e:
                    print(f"Error in Prayer. Restarting...")
                    continue

class LifePet:
    def execute(self):
        while running:
            if not paused:
                try:
                    load_config_from_json()
                    pet_life_value = getPet_life()
                    if pet_life_value < pet_life_percent:
                        for key in pet_life_key:
                            press(key)
                            sleep(random.uniform(0, 0.7))
                    sleep(random.uniform(0.5, 1))
                except Exception as e:
                    print(f"Error in Life Pet. Restarting...")
                    continue

def load_config_from_json():
    with open(os.path.join(root_directory, 'Json', 'teclas.json'), 'r') as file:
        teclas_config = json.load(file)

    global life_key, prayer_key, pet_life_key
    life_key = teclas_config.get('life_key', life_key)
    prayer_key = teclas_config.get('prayer_key', prayer_key)
    pet_life_key = teclas_config.get('pet_life_key', pet_life_key)

    with open(os.path.join(root_directory, 'Json', 'percent_key.json'), 'r') as file:
        percent_config = json.load(file)

    global life_percent, prayer_percent, pet_life_percent
    life_percent = percent_config.get('life_percent', life_percent)
    prayer_percent = percent_config.get('prayer_percent', prayer_percent)
    pet_life_percent = percent_config.get('pet_life_percent', pet_life_percent)

def check_for_exit_or_pause_key():
    global running, paused
    while running:
        if keyboard.is_pressed('insert'):
            paused = not paused
            print("Paused" if paused else "Resumed")
            sleep(1)
        sleep(0.1)

def execute_classes_in_sequence():
    while True:
        try:
            if is_runescape_running():
                ImageFinder()

                # Perguntar ao usuário se deseja alterar as teclas definidas anteriormente
                response = input("Você deseja alterar as teclas definidas anteriormente? (s/n): ").strip().lower()
                if response == "s":
                    KeyManager().run()

                # Perguntar ao usuário se deseja alterar as porcentagens definidas anteriormente
                response = input("Você deseja alterar as porcentagens definidas anteriormente? (s/n): ").strip().lower()
                if response == "s":
                    JsonSaver().run()

                break
            else:
                print("Please open the RuneScape program.")
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred. Restarting the sequence.")

def main_threading():
    exit_thread = Thread(target=check_for_exit_or_pause_key, args=())
    exit_thread.start()

    life_thread = Thread(target=Life().execute, args=())
    prayer_thread = Thread(target=Prayer().execute, args=())
    pet_thread = Thread(target=LifePet().execute, args=())
    
    life_thread.start()
    prayer_thread.start()
    pet_thread.start()

    life_thread.join()
    prayer_thread.join()
    pet_thread.join()

if __name__ == "__main__":
    execute_classes_in_sequence()
    main_threading()
