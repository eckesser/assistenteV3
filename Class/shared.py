import psutil
import threading

running = True
paused = False
restart = False
threads_paused = False
pause_condition = threading.Condition()


press300sec_running = True   
press360sec_running = True
press720sec_running = True
life_thread_running = True
prayer_thread_running = True
pet_thread_running = True

def clear_console():
    print('\033c')

def kill_processes():
    for process in psutil.process_iter():
        try:
            process_name = process.name().lower()
            if process_name == "conhost.exe" or process_name == "cmd.exe":
                process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
