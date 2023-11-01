import json
import keyboard
import os
import pygetwindow as gw
import sys
import time
import traceback
import random
import warnings
import subprocess
import win32gui
import win32con

warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.modules.rnn")

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    logger = ErrorLogger()  
    error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.log_error(error_message)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
sys.excepthook = global_exception_handler

from Class.base import Base
from Class.life import getLife
from Class.life_pet import getPet_life
from Class.prayer import getPrayer
from Log import support
from Log.ErrorLogger import ErrorLogger
from PIL import Image
from pyautogui import press
from pystray import Icon as TrayIcon, MenuItem
from threading import Thread
from Main.main_menu import main_menu
from Class.shared import running, paused, restart, kill_processes
from Class.shared import press300sec_running, press360sec_running, press720sec_running, life_thread_running, prayer_thread_running, pet_thread_running, pause_condition

life_key = ['']
life_percent = 1
prayer_key = ['']
prayer_percent = 1
pet_life_key = ['']
pet_life_percent = 1

def open_log_directory(icon):
    support.Support.zip_logs()
    support.Support.notify_user()


def restart_program(icon):
    global running, press300sec_running, press360sec_running, press720sec_running, life_thread_running, prayer_thread_running, pet_thread_running
    running = False
    press300sec_running = False
    press360sec_running = False
    press720sec_running = False
    life_thread_running = False
    prayer_thread_running = False
    pet_thread_running = False
    icon.stop()
    time.sleep(2)  
    
    script_file = os.path.abspath(__file__)
    python_executable = sys.executable

    batch_commands = f"""@echo off
timeout /t 5
"{python_executable}" "{script_file}"
del "%~f0"
"""
    batch_file_path = os.path.join(os.path.dirname(script_file), "restart.bat")
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_commands)

    subprocess.Popen(batch_file_path, shell=True)
    sys.exit(0)

def minimize_window():
    windows = gw.getWindowsWithTitle('RS Assist')
    if windows:
        windows[0].hide()


def restore_window():
    def window_enum_handler(hwnd, extra):
        if 'RS Assist' in win32gui.GetWindowText(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return extra.append(True)  # Adiciona um indicador de sucesso à lista

    found = []
    win32gui.EnumWindows(window_enum_handler, found)
    
    if not found:  # Se a lista está vazia, a janela não foi encontrada
        print("A janela 'RS Assist' não foi encontrada.")
    else:
        print("A janela 'RS Assist' foi restaurada.")

def monitor_window_state():
    while running:
        if not paused:
            windows = gw.getWindowsWithTitle('RS Assist')
            if windows and windows[0].isMinimized:
                windows[0].hide()
            time.sleep(0.5)
        else:
            time.sleep(1)

def exit_program(icon):
    global running
    running = False
    icon.stop()
    kill_processes()
    sys.exit(0)

def tray_icon_manager():
    global paused, tray_icon
    icon_path_green = os.path.join(root_directory, 'Icon', 'green.png')
    icon_image_green = Image.open(icon_path_green)
    menu = (
        MenuItem('Open', lambda icon, item: restore_window()),
        # MenuItem('Pause/Resume', lambda icon, item: toggle_pause(icon)),
        MenuItem('Restart', lambda icon, item: restart_program(icon)),
        MenuItem('Suporte', lambda icon, item: open_log_directory(icon)),
        MenuItem('Exit', lambda icon, item: exit_program(icon))
    )
    tray_icon = TrayIcon("RS Assist", icon_image_green, "RS Assist", menu)
    tray_icon.run()

def toggle_pause(Icon):
    global paused, tray_icon, pause_condition
    with pause_condition:
        paused = not paused
        pause_condition.notify_all()
        if paused:
            tray_icon.icon = Image.open(os.path.join(root_directory, 'Icon', 'red.png'))
        else:
            tray_icon.icon = Image.open(os.path.join(root_directory, 'Icon', 'green.png'))
        tray_icon.update_menu()

def check_for_exit_or_pause_key():
    global running, paused, restart, tray_icon
    def on_key_event(e):
        global running, paused, restart, tray_icon
        if e.name == 'f11' and e.event_type == 'down':
            toggle_pause(tray_icon)
            paused = not paused
        elif e.name == 'f10' and e.event_type == 'down':                                    
            restart_program(tray_icon)
        elif e.name == 'f12' and e.event_type == 'down':            
            restart = True
            running = False 
            tray_icon.stop()
            kill_processes()
            exit()
    keyboard.hook(on_key_event)
    while running:
        time.sleep(0.1)

def life_action():
    for key in life_key:
        delay_ms = random.randint(300, 758)
        time.sleep(delay_ms / 1000)
        press(key)
        print("Restaurando vida.")

def prayer_action():
    for key in prayer_key:
        delay_ms = random.randint(300, 758)
        time.sleep(delay_ms / 1000)
        press(key)  
        print("Restaurando prayer.")

def life_pet_action():
    for key in pet_life_key:
        delay_ms = random.randint(300, 758)
        time.sleep(delay_ms / 1000)
        press(key)
        print("Restaurando vida do pet.")
        time.sleep(1)

from Class.KeyPresser import KeyPresser

def should_start_300sec_thread():
    with open('Json/ulti.json', 'r') as f:
        data = json.load(f)
    
    keys_to_check = ['elven_shard_key']
    
    for key in keys_to_check:
        if data.get(key) is not None:
            return True
    return False

def press300sec():
    global press300sec_running
    while running and press300sec_running: 
        if not paused:
            with open('Json/ulti.json', 'r') as f:
                data = json.load(f)
            keys_to_check = ['elven_shard_key']
            for key in keys_to_check:
                value = data.get(key)
                if value:
                    keypress = KeyPresser(key, data)
                    keypress.press()
                    time.sleep(1)    
            time_to_wait = random.randint(301, 310)
            time.sleep(time_to_wait)
        else:
            time.sleep(1)

def should_start_360sec_thread():
    with open('Json/ulti.json', 'r') as f:
        data = json.load(f)
    
    keys_to_check = ['ovl_key', 'anti_fire_key', 'anti_poison_key', 'aggression_key']
    
    for key in keys_to_check:
        if data.get(key) is not None:
            return True
    return False

def press360sec():
    global press360sec_running
    while running and press360sec_running: 
        if not paused:
            with open('Json/ulti.json', 'r') as f:
                data = json.load(f)
            keys_to_check = ['ovl_key', 'anti_fire_key', 'anti_poison_key', 'aggression_key']
            for key in keys_to_check:
                value = data.get(key)
                if value:
                    keypress = KeyPresser(key, data)
                    keypress.press()
                    time.sleep(1)    
            time_to_wait = random.randint(345, 360)
            time.sleep(time_to_wait)
        else:
            time.sleep(1)

def should_start_720sec_thread():
    with open('Json/ulti.json', 'r') as f:
        data = json.load(f)
    
    keys_to_check = ['weapon_poison_key', 'necro_mage_key']
    
    for key in keys_to_check:
        if data.get(key) is not None:
            return True
    return False

def press720sec():
    global press720sec_running
    while running and press720sec_running:
        if not paused:
            with open('Json/ulti.json', 'r') as f:
                data = json.load(f)
            keys_to_check = ['weapon_poison_key', 'necro_mage_key']
            for key in keys_to_check:
                value = data.get(key)
                if value:
                    keypress = KeyPresser(key, data)
                    keypress.press()
                    time.sleep(1)
            time_to_wait = random.randint(690, 720)
            time.sleep(time_to_wait)
        else:
            time.sleep(1)

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

def main_threading():
    load_config_from_json()

    exit_thread = Thread(target=check_for_exit_or_pause_key)
    exit_thread.start()
    
    window_monitor_thread = Thread(target=monitor_window_state)
    window_monitor_thread.start()

    global press300sec_running, press360sec_running, press720sec_running, life_thread_running, prayer_thread_running, pet_thread_running
    press300sec_running = True
    press360sec_running = True
    press720sec_running = True
    life_thread_running = True
    prayer_thread_running = True
    pet_thread_running = True

    if should_start_300sec_thread():
        pressionar_thread0 = Thread(target=press300sec)
        time.sleep(0.5)
        pressionar_thread0.start()
        print("Iniciando monitoramento de 300 segundos")

    if should_start_360sec_thread():
        pressionar_thread = Thread(target=press360sec)
        time.sleep(0.5)
        pressionar_thread.start()
        print("Iniciando monitoramento de 360 segundos")

    if should_start_720sec_thread():
        pressionar_thread2 = Thread(target=press720sec)
        time.sleep(0.5) 
        pressionar_thread2.start()
        print("Iniciando monitoramento de 720 segundos")

    if life_key:
        life_value = getLife()
        if life_value is not None:
            life = Base(getLife, life_percent, life_action)
            life_thread = Thread(target=life.execute)
            life_thread.start()
            print("iniciando monitoramento da Vida")
        else:
            print("Monitoramento da vida nao iniciada")

    if prayer_key:
        prayer_value = getPrayer()
        if prayer_value is not None:
            prayer = Base(getPrayer, prayer_percent, prayer_action)
            prayer_thread = Thread(target=prayer.execute)
            prayer_thread.start()
            print("iniciando monitoramento do Prayer")
        else:
            print("Monitoramento da oracao nao iniciada")

    if pet_life_key:
        pet_life_value = getPet_life()
        if pet_life_value is not None:
            pet_life = Base(getPet_life, pet_life_percent, life_pet_action)
            pet_thread = Thread(target=pet_life.execute)
            pet_thread.start()
            print("iniciando monitoramento do Pet")
        else:
            print("Monitoramento do pet nao iniciado")

    exit()

if __name__ == "__main__":
    main_menu(main_threading, tray_icon_manager)