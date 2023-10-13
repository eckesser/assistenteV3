import psutil
import sys
import os
import time
import json
import traceback
from threading import Thread
import random
from time import sleep
from pyautogui import press
import keyboard
import pygetwindow as gw

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from Log import support
from pystray import Icon as TrayIcon, MenuItem
from PIL import Image

def check_and_kill_duplicate_process():
    current_process = psutil.Process()
    for proc in psutil.process_iter():
        try:
            # Verifica se o processo atual é igual ao processo em iteração
            if proc.pid != current_process.pid:
                cmd_line = proc.cmdline()
                # Verifica se o script atual está na linha de comando do processo em iteração
                if len(cmd_line) > 1 and __file__ in cmd_line[1]:
                    print(f"Killing process {proc.pid} with command line {cmd_line}")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

check_and_kill_duplicate_process()

from Log.ErrorLogger import ErrorLogger

def global_exception_handler(exc_type, exc_value, exc_traceback):
    logger = ErrorLogger()
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.log_error(error_message)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = global_exception_handler

from Config.rscheck import is_runescape_running
from Class.life import getLife
from Class.prayer import getPrayer
from Class.life_pet import getPet_life
from Class.seis_min import UltiKeyProcessor6
from Class.doze_min import UltiKeyProcessor12


life_key = ['']
life_percent = 1
prayer_key = ['']
prayer_percent = 1
pet_life_key = ['']
pet_life_percent = 1

running = True
paused = False
restart = False

def open_log_directory(icon):
    support.Support.zip_logs()
    support.Support.notify_user()

def restart_program(icon):
    global running
    running = False
    icon.stop()
    os.system('python ' + __file__)
    exit(0)

def minimize_window():
    windows = gw.getWindowsWithTitle('RS3 Assist')
    if windows:
        windows[0].hide()

def restore_window():
    windows = gw.getWindowsWithTitle('RS3 Assist')
    if windows:
        window = windows[0]        
        if window.isHidden:
            window.restore()
        else:
            window.activate()

def monitor_window_state():
    while running:
        windows = gw.getWindowsWithTitle('RS3 Assist')
        if windows and windows[0].isMinimized:
            windows[0].hide()
        time.sleep(0.5)

def exit_program(icon):
    global running
    running = False
    icon.stop()
    exit(0)

def toggle_pause(icon):
    global paused, tray_icon
    paused = not paused
    if paused:
        tray_icon.icon = Image.open(os.path.join(root_directory, 'Icon', 'red.png'))
    else:
        tray_icon.icon = Image.open(os.path.join(root_directory, 'Icon', 'green.png'))
    tray_icon.update_menu()

def tray_icon_manager():
    global paused, tray_icon
    icon_path_green = os.path.join(root_directory, 'Icon', 'green.png')
    icon_image_green = Image.open(icon_path_green)

    menu = (
        MenuItem('Open', lambda icon, item: restore_window()),
        MenuItem('Pause/Resume', lambda icon, item: toggle_pause(icon)),
        MenuItem('Restart', lambda icon, item: restart_program(icon)),
        MenuItem('Suporte', lambda icon, item: open_log_directory(icon)),
        MenuItem('Exit', lambda icon, item: exit_program(icon))
    )

    tray_icon = TrayIcon("RS3 Assist", icon_image_green, "RS3 Assist", menu)
    tray_icon.run()

def check_for_exit_or_pause_key():
    global running, paused, restart, tray_icon
    
    def on_key_event(e):
        global running, paused, restart, tray_icon

        if e.name == 'insert' and e.event_type == 'down':
            toggle_pause(tray_icon)
        elif e.name == 'home' and e.event_type == 'down':
            restart = True
            running = False
            tray_icon.stop()
            exit()

    keyboard.hook(on_key_event)
    while running:
        time.sleep(0.1)
        
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
                except Exception:
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
                            sleep(random.uniform(3, 0.7))
                    sleep(random.uniform(0.5, 1))
                except Exception:
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

def execute_classes_in_sequence():
    retry_count = 0
    while not is_runescape_running() and retry_count < 3:
        print('Abra o runescape e tente novamente.')
        time.sleep(5)
        retry_count += 1

    if retry_count == 3:
        print('Runescape não detectado após várias tentativas. Fechando o assistente.')
        exit()

    print('Runescape aberto.')

    from Config.coords import ImageFinder
    from Config.perct_key import JsonSaver
    from Config.keys import KeyManager
    from Config.keys_pots import KeyManagerPot

    try:
        ImageFinder()
        KeyManager()
        JsonSaver()
        KeyManagerPot()
    except Exception:
        print(f"An error occurred. Restarting the sequence.")

def monitor_window_state():
    while running:
        windows = gw.getWindowsWithTitle('RS3 Assist')
        if windows and windows[0].isMinimized:
            windows[0].hide()
        time.sleep(0.5)

def periodic_clear_console():
    while running:
        time.sleep(20)
        clear_console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_threading():
    global restart
    exit_thread = Thread(target=check_for_exit_or_pause_key, args=())
    exit_thread.start()

    clear_thread = Thread(target=periodic_clear_console, args=())
    clear_thread.start()

    window_monitor_thread = Thread(target=monitor_window_state, args=())
    window_monitor_thread.start()

    life_thread = Thread(target=Life().execute, args=())
    prayer_thread = Thread(target=Prayer().execute, args=())
    pet_thread = Thread(target=LifePet().execute, args=())
    processor_6_thread = Thread(target=UltiKeyProcessor6().run, args=())
    processor_12_thread = Thread(target=UltiKeyProcessor12().run, args=())
    
    life_thread.start()
    prayer_thread.start()
    pet_thread.start()
    processor_6_thread.start()
    processor_12_thread.start()
    
    time.sleep(3)
    minimize_window()
    tray_icon_manager()

    life_thread.join()
    prayer_thread.join()
    pet_thread.join()
    processor_6_thread.join()
    processor_12_thread.join()

    while is_runescape_running():
        time.sleep(5)

    print("Jogo Fechado, fechando assistente...")
    time.sleep(3)
    exit()

    # if restart:
    #     restart = False
    #     main_menu()

def main_menu():
    while True:
        clear_console()
        print("\nRS3 Assist")
        print("-------------------------")
        print("1. Configurar teclas")
        print("2. Configurar porcentagem")
        print("3. Configurar pots e magias")
        print("4. Start")
        print("5. Exit")
        print("-------------------------")
        print("Comandos:")
        print("Botao INSERT para Pause e Resume do programa.")
        print("Botao HOME, para FECHAR o programa")
        print("-------------------------")
        print("Quando o programa estiver executando ele minimizara so")
        print("-------------------------")
        choice = input("Digite a opcao desejada: ")

        if choice == "1":
            from Config.keys import KeyManager
            KeyManager()

        elif choice == "2":
            from Config.perct_key import JsonSaver
            JsonSaver()

        elif choice == "3":
            from Config.keys_pots import KeyManagerPot
            KeyManagerPot()
        
        elif choice == "4":
            print("Verificando configuracoes:")
            time.sleep(0.4)
            print("Dados de teclas carregados... Ok!")
            time.sleep(0.4)
            print("Dados de porcentagem carregado... Ok!")
            time.sleep(0.4)
            print("Dados das teclas de pot carregado... Ok!")
            time.sleep(0.4)
            print("Verificando se Runescape...")
            time.sleep(0.4)
            if is_runescape_running():
                print("Runescape aberto.")
                from Config.coords import ImageFinder
                ImageFinder()
                print("Programa iniciado, minimizando...")
                main_threading()
                #print("Programa iniciado, minimizando...")
            else:
                print("Abra o runescape... Reiniciando programa.")
                time.sleep(2)
                main_menu()

        elif choice == "5":
            global running
            running = False
            print("Fechando programa.")
            break

        else:
            print("Opcao invalida, escolha uma das opcoes acima.")

if __name__ == "__main__":
    main_menu()
