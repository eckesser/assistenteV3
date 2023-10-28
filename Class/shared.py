import psutil

running = True
paused = False
restart = False
threads_paused = False

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