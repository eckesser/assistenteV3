import sys
import os
import time
import json
from threading import Thread
import random
from time import sleep
from pyautogui import press
import keyboard
import pygetwindow as gw
from pystray import Icon as TrayIcon, MenuItem
from PIL import Image

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from Config.rscheck import is_runescape_running
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
restart = False

def minimize_window():
    window = gw.getWindowsWithTitle('RuneScape Assistente do Tio Erick')[0]
    window.minimize()

def tray_icon_manager():
    global paused
    icon_path_green = os.path.join(root_directory, 'Icon', 'green.png')
    icon_path_red = os.path.join(root_directory, 'Icon', 'red.png')

    icon_image_green = Image.open(icon_path_green)
    icon_image_red = Image.open(icon_path_red)

    menu = (
        MenuItem('Pause/Resume', lambda icon, item: toggle_pause(icon)),
        MenuItem('Exit', lambda icon, item: exit_program(icon))
    )

    tray_icon = TrayIcon("RuneScape Assistente", icon_image_green, "RuneScape Assistente", menu)

    def toggle_pause(icon):
        paused = not paused
        if paused:
            icon.icon = icon_image_red
        else:
            icon.icon = icon_image_green
        icon.update_menu()

    def exit_program(icon):
        running = False
        icon.stop()

    tray_icon.run()

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
                            sleep(random.uniform(0.2, 0.7))
                    sleep(random.uniform(0.5, 1))
                except Exception:
                    #print(f"Error in Life. Restarting...")
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
                except Exception:
                    #print(f"Error in Prayer. Restarting...")
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
                            sleep(random.uniform(3, 0.7))
                    sleep(random.uniform(0.5, 1))
                except Exception:
                    #print(f"Error in Life Pet. Restarting...")
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
    global running, paused, restart
    
    def on_key_event(e):
        global running, paused, restart

        if e.name == 'insert' and e.event_type == 'down':
            paused = not paused
            print("Pausado" if paused else "Resumido")
        elif e.name == 'home' and e.event_type == 'down':
            restart = True

    keyboard.hook(on_key_event)
    while running:
        time.sleep(0.1)

def execute_classes_in_sequence():

    from Config.coords import ImageFinder
    from Config.perct_key import JsonSaver
    from Config.keys import KeyManager

    while True:
        try:
            if is_runescape_running():
                ImageFinder()
                KeyManager()
                JsonSaver()
                break
            else:
                print("Please open the RuneScape program.")
                time.sleep(5)
        except Exception:
            print(f"An error occurred. Restarting the sequence.")

def periodic_clear_console():
    while running:
        time.sleep(5)
        clear_console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_threading():
    global restart
    exit_thread = Thread(target=check_for_exit_or_pause_key, args=())
    exit_thread.start()

    # Iniciar a thread de limpeza periódica
    clear_thread = Thread(target=periodic_clear_console, args=())
    clear_thread.start()

    life_thread = Thread(target=Life().execute, args=())
    prayer_thread = Thread(target=Prayer().execute, args=())
    pet_thread = Thread(target=LifePet().execute, args=())
    
    life_thread.start()
    prayer_thread.start()
    pet_thread.start()

    time.sleep(10)  # Aguarde 10 segundos
    minimize_window()  # Minimize a janela
    tray_icon_manager()  # Inicie o ícone da bandeja

    life_thread.join()
    prayer_thread.join()
    pet_thread.join()

    if is_runescape_running():
    # Verifica periodicamente se o RuneScape ainda está rodando
        while is_runescape_running():
            time.sleep(5)  # Verifica a cada segundo (pode ajustar esse valor conforme necessário)

        # Se sair do loop, significa que o RuneScape foi fechado
        print("Jogo Fechado, fechando assistente...")
        time.sleep(6)
        exit()

    if restart:
        restart = False
        main_menu()

def main_menu():
    while True:
        clear_console()
        print("\nRuneScape Assistente do Tio Erick")
        print("-------------------------")
        print("1. Configurar teclas")
        print("2. Configurar porcentagem")
        print("3. Start")
        print("4. Exit")
        print("-------------------------")
        print("Comandos:")
        print("Botao INSERT para Pause e Resume do programa.")
        print("Botao HOME, para PARAR o programa")
        print("-------------------------")
        choice = input("Digite a opcao desejada: ")

        if choice == "1":
            from Config.keys import KeyManager
            KeyManager()

        elif choice == "2":
            from Config.perct_key import JsonSaver
            JsonSaver()

        elif choice == "3":
            print("Verificando configuracoes:")
            time.sleep(0.4)
            print("Dados de teclas carregados... Ok!")
            time.sleep(0.4)
            print("Dados de porcentagem carregado... Ok!")
            time.sleep(0.4)
            print("Verificando se Runescape...")
            time.sleep(0.4)
            if is_runescape_running():
                print("Runescape aberto.")
                from Config.coords import ImageFinder
                ImageFinder()
                main_threading()

            else:
                print("Abra o runescape")
                main_threading
                break

                    
        elif choice == "4":
            global running
            running = False
            print("Fechando programa.")
            break

        else:
            print("Opcao invalida, escolha uma das opcoes acima.")

if __name__ == "__main__":
    main_menu()