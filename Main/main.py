import sys
import os
import time
import json
from threading import Thread
import random
from time import sleep
from pyautogui import press

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from Config.rscheck import is_runescape_running
from Config.coords import ImageFinder
from Config.perct_key import JsonSaver
from Config.keys import KeyManager
from Class.life import getLife
from Class.prayer import getPrayer
from Class.life_pet import getPet_life

life_key = ['f5', 'f6', 'f7']
life_percent = 98
prayer_key = ['tab']
prayer_percent = 95
pet_life_key = ['3', '4']
pet_life_percent = 30

class Life:
    def execute(self):
        while True:
            life_value = getLife()
            if life_percent != life_value:
                for key in life_key:
                    press(key)
                    sleep(random.uniform(0, 0.7))
            sleep(random.uniform(0.5, 1))

class Prayer:
    def execute(self):
        while True:
            prayer_value = getPrayer()
            if prayer_percent != prayer_value:
                press(prayer_key[0])
            sleep(random.uniform(0.5, 1))

class LifePet:
    def execute(self):
        while True:
            pet_life_value = getPet_life()
            if pet_life_percent != pet_life_value:
                for key in pet_life_key:
                    press(key)
                    sleep(random.uniform(0, 0.7))
            sleep(random.uniform(0.5, 1))

def load_config_from_json():
    # Carregando configurações das teclas
    with open(os.path.join(root_directory, 'Json', 'teclas.json'), 'r') as file:
        teclas_config = json.load(file)

    global life_key, prayer_key, pet_life_key
    
    life_key = teclas_config.get('life_key', life_key)
    prayer_key = teclas_config.get('prayer_key', prayer_key)
    pet_life_key = teclas_config.get('pet_life_key', pet_life_key)

    # Carregando configurações das porcentagens
    with open(os.path.join(root_directory, 'Json', 'percent_key.json'), 'r') as file:
        percent_config = json.load(file)

    global life_percent, prayer_percent, pet_life_percent
    
    life_percent = percent_config.get('life_percent', life_percent)
    prayer_percent = percent_config.get('prayer_percent', prayer_percent)
    pet_life_percent = percent_config.get('pet_life_percent', pet_life_percent)

def execute_classes_in_sequence():
    while True:
        try:
            if is_runescape_running():
                ImageFinder()
                JsonSaver()
                KeyManager()
                break
            else:
                print("Please open the RuneScape program.")
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}. Restarting the sequence.")

def main_threading():
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
    load_config_from_json()  # Carrega as configurações dos arquivos JSON
    execute_classes_in_sequence()
    main_threading()
