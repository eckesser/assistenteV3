import psutil
import time
import json
import os

def is_runescape_running():
    for process in psutil.process_iter(attrs=["name"]):
        if "runescape" in process.info["name"].lower():
            return True
    return False

def save_to_json(status):
    # Verifique se a pasta 'json' existe, se não, crie-a
    if not os.path.exists('json'):
        os.mkdir('json')
        
    with open(os.path.join('json', 'checkrs.json'), "w") as json_file:
        json.dump({"runescape_running": status}, json_file)

def check_and_save_runescape_status():
    while True:
        if is_runescape_running():
            save_to_json(True)
            return "Runescape detectado e informação salva no JSON."
        time.sleep(2)

# Para usar o código, basta chamar a função check_and_save_runescape_status()
check_and_save_runescape_status()
